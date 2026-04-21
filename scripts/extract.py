#!/usr/bin/env python3
"""
PDF -> raw.md + figures/ extractor (phase 1 of paper-summary skill).

Usage:
    python extract.py <pdf_path> <out_dir>

Outputs under <out_dir>:
    raw.md                         full text per page + figure embeds
    figures/figN.png               main figures (renumbered 1..)
    figures/figAN.png              appendix figures (renumbered A1..)
    figures/_pages/p-NN.png        full-page renders (200dpi), kept as
                                   source for manual re-cropping
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

CAPTION_RE = re.compile(r"^\s*(?:Figure|Fig\.?)\s*(\d+)\s*[:.\-]", re.IGNORECASE)
# Boundary headings: whole line must BE the heading (optionally with section id)
REFERENCES_RE = re.compile(r"^\s*references\s*$", re.IGNORECASE)
APPENDIX_RE = re.compile(
    r"^\s*(appendix(\s*[A-Z0-9]{1,3})?|supplementary\s+material)\s*[:.]?\s*$",
    re.IGNORECASE,
)


def dump_pages(doc: fitz.Document, pages_dir: Path, dpi: int = 200) -> None:
    pages_dir.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    for idx, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat)
        pix.save(str(pages_dir / f"p-{idx:02d}.png"))


def find_boundary_page(doc: fitz.Document) -> int:
    """Return 0-based page index where references/appendix starts (== main end)."""
    for i, page in enumerate(doc):
        for line in page.get_text("text").splitlines():
            if REFERENCES_RE.match(line) or APPENDIX_RE.match(line):
                return i
    return doc.page_count


def caption_blocks(page: fitz.Page):
    """Yield (fig_num, caption_bbox, caption_text) for each figure caption on page."""
    for b in page.get_text("blocks"):
        # block = (x0, y0, x1, y1, text, block_no, block_type)
        text = (b[4] or "").strip()
        if not text:
            continue
        first_line = text.splitlines()[0]
        m = CAPTION_RE.match(first_line)
        if not m:
            continue
        fig_num = int(m.group(1))
        bbox = fitz.Rect(b[0], b[1], b[2], b[3])
        yield fig_num, bbox, " ".join(text.splitlines())


def image_bboxes_on_page(page: fitz.Page):
    """Return list of Rects covering embedded raster images on the page."""
    rects = []
    for img in page.get_images(full=True):
        xref = img[0]
        try:
            for r in page.get_image_rects(xref):
                rects.append(r)
        except Exception:
            continue
    return rects


def drawing_bboxes_on_page(page: fitz.Page):
    """Return Rects for vector drawings on the page. Filters out degenerate
    rects (lines, tiny marks) and rects that cover most of the page (likely
    crop boxes or rule lines spanning the margin)."""
    page_rect = page.rect
    rects = []
    for d in page.get_drawings():
        r = d.get("rect")
        if r is None:
            continue
        # skip tiny (strokes, lines)
        if r.width < 5 or r.height < 5:
            continue
        # skip near-page-spanning (likely page border or full-width rule)
        if r.width > page_rect.width * 0.95 and r.height > page_rect.height * 0.9:
            continue
        rects.append(fitz.Rect(r))
    return rects


def _text_block_bottom_above(page: fitz.Page, caption_bbox: fitz.Rect) -> float:
    """Bottom y of the lowest text block above caption that overlaps its
    x-range. Returns a small top margin if none found. This becomes the
    hard upper bound on the figure crop, so we never bleed into title or
    body text above the figure."""
    best_y = page.rect.y0 + 18
    cx0, cx1 = caption_bbox.x0, caption_bbox.x1
    caption_w = max(1.0, cx1 - cx0)
    for b in page.get_text("blocks"):
        x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
        text = (b[4] or "").strip()
        if not text:
            continue
        if y1 > caption_bbox.y0 - 1:
            continue
        if x1 < cx0 or x0 > cx1:
            continue
        # filter short text (likely figure-internal annotations/axis labels)
        if len(text.replace("\n", " ")) < 40:
            continue
        # filter narrow text blocks (also figure-internal)
        if (x1 - x0) < caption_w * 0.4:
            continue
        if y1 > best_y:
            best_y = y1
    return best_y


def figure_region_above_caption(
    page: fitz.Page, caption_bbox: fitz.Rect, image_rects, drawing_rects
):
    """Return (rect, source_tag).
    source_tag in {'image', 'drawing', 'mixed', 'text-bound', 'page-top'}.

    Strategy:
      1. Collect image + drawing rects above caption and x-overlapping it.
      2. Union them; clamp top with text-block bottom to avoid bleeding.
      3. If the text-bound top sits too close to caption (< 60pt of space),
         relax to page-top fallback — a figure clearly exists, better to
         over-crop slightly than to miss it.
      4. If no graphic rects, use text-bounded slab.
    """
    page_rect = page.rect
    text_floor = _text_block_bottom_above(page, caption_bbox) + 2
    # relax floor when it sits suspiciously close to caption (figure is likely
    # a vector graphic that we could not detect via get_drawings)
    if caption_bbox.y0 - text_floor < 60:
        text_floor = page_rect.y0 + 36

    cx0, cx1 = caption_bbox.x0, caption_bbox.x1
    def _above_and_overlapping(rects):
        out = []
        for r in rects:
            if r.y1 > caption_bbox.y0 + 2:
                continue
            if r.y1 < caption_bbox.y0 - 600:
                continue
            if r.x1 < cx0 - 10 or r.x0 > cx1 + 10:
                continue
            out.append(r)
        return out

    img_cands = _above_and_overlapping(image_rects)
    drw_cands = _above_and_overlapping(drawing_rects)

    if img_cands or drw_cands:
        all_cands = img_cands + drw_cands
        rect = fitz.Rect(all_cands[0])
        for r in all_cands[1:]:
            rect |= r
        rect.x0 = min(rect.x0, caption_bbox.x0) - 4
        rect.x1 = max(rect.x1, caption_bbox.x1) + 4
        rect.y0 = max(rect.y0, text_floor)
        rect.y1 = caption_bbox.y0 - 2
        rect &= page_rect
        if rect.height >= 40 and rect.width >= 40:
            if img_cands and drw_cands:
                tag = "mixed"
            elif img_cands:
                tag = "image"
            else:
                tag = "drawing"
            return rect, tag

    # text-bound or page-top slab
    slab = fitz.Rect(
        max(page_rect.x0, caption_bbox.x0 - 6),
        text_floor,
        min(page_rect.x1, caption_bbox.x1 + 6),
        caption_bbox.y0 - 2,
    )
    tag = "text-bound" if text_floor > page_rect.y0 + 40 else "page-top"
    if slab.height >= 40 and slab.width >= 40:
        return slab, tag
    return None, "none"


def render_crop(page: fitz.Page, rect: fitz.Rect, dpi: int = 200) -> fitz.Pixmap:
    zoom = dpi / 72.0
    return page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=rect)


def extract(pdf_path: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_dir = out_dir / "figures"
    pages_dir = fig_dir / "_pages"
    fig_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    print(f"[info] pages: {doc.page_count}")
    dump_pages(doc, pages_dir)

    boundary = find_boundary_page(doc)
    print(f"[info] main/appendix boundary page: {boundary + 1}")

    main_n = 0
    appx_n = 0
    figures = []  # list of dicts

    for i, page in enumerate(doc):
        is_appx = i >= boundary
        img_rects = image_bboxes_on_page(page)
        drw_rects = drawing_bboxes_on_page(page)
        for fig_num, cap_bbox, cap_text in caption_blocks(page):
            rect, source = figure_region_above_caption(
                page, cap_bbox, img_rects, drw_rects
            )
            if rect is None:
                print(f"[warn] could not crop Fig {fig_num} on p{i+1}")
                continue
            if is_appx:
                appx_n += 1
                fname = f"figA{appx_n}.png"
            else:
                main_n += 1
                fname = f"fig{main_n}.png"
            render_crop(page, rect).save(str(fig_dir / fname))
            # flag suspicious crops: unusually small or text-bound fallback
            warn = None
            if rect.height < 80 or rect.width < 80:
                warn = f"small crop ({int(rect.width)}x{int(rect.height)}pt)"
            elif source in ("text-bound", "page-top"):
                warn = f"no graphic rects detected (source={source})"
            if warn:
                print(f"[warn] Fig {fig_num} p{i+1} ({fname}): {warn} -> check _pages/p-{i+1:02d}.png")
            figures.append(
                {
                    "page": i + 1,
                    "is_appx": is_appx,
                    "fname": fname,
                    "orig_num": fig_num,
                    "caption": cap_text,
                    "source": source,
                    "warn": warn,
                }
            )

    raw_md = out_dir / "raw.md"
    with raw_md.open("w", encoding="utf-8") as f:
        f.write(f"# raw: {pdf_path.name}\n\n")
        meta = doc.metadata or {}
        if meta.get("title"):
            f.write(f"- title: {meta['title']}\n")
        if meta.get("author"):
            f.write(f"- author: {meta['author']}\n")
        f.write(f"- pages: {doc.page_count}\n")
        f.write(f"- main/appendix boundary page: {boundary + 1}\n")
        f.write(f"- figures: {main_n} main + {appx_n} appendix\n\n")

        f.write("## Figure index\n\n")
        for rec in figures:
            tag = "A" if rec["is_appx"] else "M"
            warn_str = f"  ⚠ {rec['warn']}" if rec.get("warn") else ""
            f.write(
                f"- [{tag}] p.{rec['page']} orig Fig {rec['orig_num']} -> "
                f"`figures/{rec['fname']}` (src: {rec['source']}){warn_str}\n"
            )
            f.write(f"  > {rec['caption'][:240]}\n")
        f.write("\n> Note: for figures flagged with ⚠, re-crop manually from "
                "`figures/_pages/p-NN.png`.\n\n---\n\n")

        figs_by_page: dict[int, list] = {}
        for rec in figures:
            figs_by_page.setdefault(rec["page"], []).append(rec)

        for i, page in enumerate(doc):
            f.write(f"\n## p. {i+1}\n\n")
            f.write(page.get_text("text").strip() + "\n\n")
            for rec in figs_by_page.get(i + 1, []):
                f.write(f"![{rec['fname']}](figures/{rec['fname']})\n\n")
                f.write(f"_caption_: {rec['caption']}\n\n")

    print(f"[done] raw.md -> {raw_md}")
    print(f"[done] figures -> {fig_dir} ({main_n} main, {appx_n} appendix)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("out_dir")
    args = ap.parse_args()
    extract(Path(args.pdf), Path(args.out_dir))


if __name__ == "__main__":
    main()
