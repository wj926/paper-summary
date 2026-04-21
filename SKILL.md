---
name: paper-summary
description: PDF 논문을 raw.md(전문 + figures) / summary.md(사실 기반 상세 요약 + figure embed) / abstract.md(메타 + 원문 + 한글번역) 세 파일로 나눠 정리한다. Phase 1 은 Python(PyMuPDF) 기반이라 토큰 0, Phase 2 만 LLM 사용. 새 논문 PDF 를 받아 프로젝트에 편입시킬 때 / arXiv PDF 를 다시 이 규칙대로 정리할 때 호출.
---

# paper-summary

논문 PDF 를 **검색·재독에 최적화된 세 파일** 로 나눠 저장하는 skill.

## 언제 사용

- 새 논문 PDF 를 받아 프로젝트 `papers/` 폴더에 편입시킬 때.
- 이미 받은 PDF 를 이 규칙대로 재정리할 때.

## 철학 — 왜 3 파일인가

| 파일 | 언제 열어봄 | 생성 주체 |
|------|------------|---------|
| `abstract.md` | 서치할 때 관련성만 빠르게 판단 (수십 초) | LLM (phase 2) |
| `summary.md` | Q&A / 논의의 1차 소스. 수식 · Table · Glossary · figure 포함 | LLM (phase 2) |
| `raw.md` | summary 에 빠진 게 있을 때만 참조 (PDF 재독 대체) | Python (phase 1, 토큰 0) |

`idea.md` (우리 연구 관점 / 활용 전략 / 심층 분석) 는 **이 skill 밖**. 향후 `paper-analyze` skill 로 분리 예정.

## 절차 (3 phase)

### Phase 1 — Python 추출 (토큰 0)

```bash
python3 ~/.claude/skills/paper-summary/scripts/extract.py <pdf_path> <out_dir>
```

의존성: `pymupdf` (miniconda python 에 이미 있으면 `/home/dami/miniconda3/bin/python3` 사용, 없으면 `pip install pymupdf`).

산출물 (`<out_dir>/` 아래):

- `raw.md` — 페이지별 전문 + figure embed + figure index + boundary 정보.
- `figures/figN.png`, `figures/figAN.png` — main / appendix figure 크롭.
- `figures/_pages/p-NN.png` — 200dpi 페이지 원본. figure 크롭이 이상할 때 수동 재크롭용.

경고: 크롭이 비정상으로 작거나 vector graphic 감지 실패 시 stderr + raw.md `Figure index` 에 ⚠ 로 표시됨. 해당 figure 는 `_pages/` 에서 수동 재크롭.

### Phase 2 — LLM 요약

1. `<out_dir>/raw.md` 를 Read.
2. `references/summary_rules.md` 를 Read — 폴더명 규칙 / 수식 포맷 / figure 주석 / hallucination 금지 / Claude 조어 금지.
3. `templates/summary.md` 를 기준으로 `<out_dir>/summary.md` 작성.
4. `templates/abstract.md` 를 기준으로 `<out_dir>/abstract.md` 작성.
5. 두 파일의 메타/원문/번역 섹션은 **문구 동일** 로 유지 (한쪽 수정 시 다른 쪽 동기화).

### Phase 3 — 폴더명 확정 + PAPERS.md 업데이트

1. **venue 확인**:
   - arXiv PDF metadata 에 학회 표기 없으면 Google 에서 "<정확한 논문 제목>" 검색해 ICML / NeurIPS / ICLR / ACL 등 accept 됐는지 확인.
   - 확인되면 해당 venue, 아니면 `preprint`.
2. **폴더명**: `<N>_<firstauthor><year><METHOD>(<venue><year>)`.
   - `<N>`: 프로젝트 `papers/` 내 추가 순서 (1부터).
   - `<firstauthor>`: 제1저자 성 (소문자).
   - `<METHOD>`: 핵심 알고리즘·method 이름 (acronym 이면 대문자).
   - `<venue><year>`: `ICML2025`, `NeurIPS2025`, `ICLR2026`, `preprint` 등.
   - 예: `1_zhu2025MELON(ICML2025)`.
3. PDF + output 을 최종 폴더로 이동/rename.
4. 프로젝트 `PAPERS.md` 인덱스 표에 행 추가: 카테고리 + 한 줄 핵심 연결점.

## 제약

- 논문 본문에 없는 새 용어를 만들지 않는다 (Claude 조어 금지).
- 수치 / 수식 / 저자명 / 연도는 raw.md 원문 그대로 — 기억·감으로 변형 금지.
- 확신 없으면 "raw.md 에 명시 없음" 이라고 쓰고 넘어간다.

## 파일 구조

```
~/.claude/skills/paper-summary/
├── SKILL.md                          (이 파일)
├── scripts/
│   └── extract.py                    (phase 1: PDF -> raw.md + figures/)
├── templates/
│   ├── summary.md                    (phase 2 placeholder)
│   └── abstract.md                   (phase 2 short view)
└── references/
    └── summary_rules.md              (phase 2 작성 규칙 세부)
```
