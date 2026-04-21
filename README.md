# paper-summary

> 논문 PDF 한 편을 **검색·재독·인용에 최적화된 세 파일**로 나눠 정리하는 Claude Code skill.
>
> Phase B 는 Python (PyMuPDF) 로 LLM 토큰 **0**. Phase A 에서 폴더명을 먼저 확정하고 Phase C 에서 요약을 쓴다 — 임시 이름 (`_tmp`) 을 거치지 않아 rename 을 까먹을 일이 없다.

## 산출물

하나의 PDF 에 대해 `<out_dir>/` 아래에 다음을 만든다.

| 파일 | 언제 열어봄 | 생성 주체 |
|------|------------|---------|
| `abstract.md` | 서치할 때 관련성만 수십 초에 판단 | LLM (phase C) |
| `summary.md` | 앞으로의 Q&A / 논의의 1차 소스 — 메타, TL;DR, Glossary, Section 상세 (수식 · Table · Figure embed 포함) | LLM (phase C) |
| `raw.md` | summary 에 빠진 게 있을 때만 참조 (PDF 재독 대체) | Python (phase B) |
| `figures/figN.png`, `figures/figAN.png` | main / appendix figure 크롭 | Python (phase B) |
| `figures/_pages/p-NN.png` | 200dpi 페이지 원본, figure 크롭이 이상할 때 수동 재크롭용 | Python (phase B) |

## 왜 이렇게 쪼갰나

- 논문이 쌓일수록 "이 논문이 관련 있나?" 를 빨리 판단하고 싶다 → `abstract.md` 만 열면 됨.
- 본격 논의 / 질문에는 수식·수치·figure 가 필요한데 매번 PDF 를 다시 읽기 싫다 → `summary.md` 하나를 primary source 로.
- 요약이 놓친 디테일은 원문 재확인이 필요 → `raw.md` + `figures/_pages/` 를 재독 대체물로.
- 본문 추출은 Python 이면 충분 → LLM 비용 줄이려고 phase 1/2 분리.

## 의존성

- Python 3.10+ with [PyMuPDF](https://pymupdf.readthedocs.io/) (`pip install pymupdf`)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (phase 2, 3 를 orchestrate)

## 설치

이 repo 를 clone 해서 `~/.claude/skills/paper-summary/` 에 놓거나 symlink.

```bash
git clone https://github.com/<you>/paper-summary.git ~/.claude/skills/paper-summary
```

새 Claude Code 세션을 열면 `paper-summary` 가 skill 목록에 자동 등록된다.

## 사용

Claude Code 세션에서 자연어로 호출.

```
이 PDF paper-summary 로 정리해줘: /path/to/paper.pdf
```

또는 Python 으로 phase B 만 직접 실행 (raw.md + figures 만 필요할 때):

```bash
python3 ~/.claude/skills/paper-summary/scripts/extract.py <pdf_path> <out_dir>
```

PDF metadata 만 빠르게 확인하려면:

```bash
python3 ~/.claude/skills/paper-summary/scripts/extract.py --metadata-only <pdf_path>
```

## 흐름 (4 phase, 순서 중요)

1. **Phase A — metadata 확인 + 폴더명 확정 (LLM)**. `extract.py --metadata-only` 로 title / author / pages / arxiv id / 첫 페이지 머리글을 뽑는다. 여기서 venue 를 판별하고 (PDF 에 없으면 Google 검색), 폴더명 `<N>_<firstauthor><year><METHOD>(<venue><year>)` 을 확정해 해당 폴더를 만든다.
2. **Phase B — Python 추출 (토큰 0)**. Phase A 에서 만든 폴더를 `out_dir` 로 넘겨 `extract.py` 실행. PDF 를 200dpi 로 덤프하고 본문 텍스트 + figure caption 을 분석, embedded image + vector drawing bbox 를 합쳐 figure 를 크롭한다. main / appendix 경계는 독립 heading (`References`, `Appendix <id>`) 만 인식해 문장 내부 언급에 오탐하지 않는다.
3. **Phase C — LLM 요약**. `raw.md` 를 읽고 `references/summary_rules.md` 의 규칙을 따라 `summary.md` 와 `abstract.md` 를 작성한다. 두 파일의 메타·원문·번역은 동일 문구로 유지.
4. **Phase D — PAPERS.md 업데이트**. 프로젝트 `PAPERS.md` 인덱스 표에 행을 추가 (폴더 링크 + 카테고리 + 한 줄 핵심 연결점).

왜 Phase A 가 맨 앞? — 폴더명을 **Phase B 시작 전에** 결정해두면 `_tmp1` 같은 임시 이름을 쓰고 나중에 rename 하다가 까먹는 사고가 원천 차단된다.

## 폴더명 규칙

```
<N>_<firstauthor><year><METHOD>(<venue><year>)
```

| field | 규칙 | 예시 |
|-------|------|------|
| `<N>` | 프로젝트 `papers/` 내 추가 순서 (1 부터) | `1` |
| `<firstauthor>` | 제1저자 성, 소문자 | `zhu` |
| `<year>` | 논문 연도 | `2025` |
| `<METHOD>` | 핵심 알고리즘 / method 이름 (acronym 은 대문자) | `MELON`, `KLASS` |
| `<venue><year>` | 학회 약어 + 연도, preprint 는 `preprint` | `ICML2025`, `NeurIPS2025`, `ICLR2026-Spotlight` |

예: `1_zhu2025MELON(ICML2025)`

## Phase 2 가 따르는 원칙 (요약)

자세한 건 `references/summary_rules.md`.

- 수치·수식·저자명·연도는 `raw.md` 원문 그대로. 기억·감으로 변형하지 않는다.
- 논문에 없는 새 용어를 만들어 쓰지 않는다 (Claude 조어 금지).
- 수식은 display math (`$$...$$`) + Notation / Per-term blockquote 위계.
- Figure 는 해당 Section 안에 embed + 3줄 주석 (저자 주장 / 직관적 해석 / 본문 언급).
- `summary.md` 는 사실 기반만. "우리 연구와의 연결 / 활용 전략 / 심층 분석" 은 이 skill 범위 밖이다 (향후 `paper-analyze` skill 로 분리 예정).

## 파일 구조

```
paper-summary/
├── SKILL.md                # Claude agent 가 따르는 오케스트레이션
├── README.md               # 이 문서
├── scripts/
│   └── extract.py          # Phase 1: PDF -> raw.md + figures/
├── templates/
│   ├── summary.md          # Phase 2 long-form placeholder
│   └── abstract.md         # Phase 2 short-view placeholder
└── references/
    └── summary_rules.md    # Phase 2 작성 규칙 세부
```

## 한계

- **OCR 불가**: PDF 에 text layer 가 있어야 한다. 스캔본·이미지 PDF 는 별도 OCR 선행 필요.
- **Figure 크롭 휴리스틱**: caption 위의 embedded image + vector drawing bbox 를 union 한 뒤 텍스트 블록으로 top clamp 하는 방식. 대부분 잘 동작하지만 실패할 수 있고, 그 경우 `_pages/p-NN.png` 에서 수동 크롭. raw.md 의 Figure index 에 ⚠ 로 표시된다.
- **Non-English 논문**: 추출 자체는 되지만 summary 작성 시 Glossary 와 번역 품질이 떨어질 수 있다.

## 검증

Prototype 단계에서 두 논문 (ICML 2025 / arXiv preprint, 각 20p / 28p) 에 적용해 figure 12 개 전부 깨끗하게 크롭됨을 확인했다.

| | paper1 (20p) | paper2 (28p) |
|---|---|---|
| 감지 | 4 / 4 | 8 / 8 |
| 크롭 품질 | 전부 깨끗 (제목/저자 번짐 0) | 전부 깨끗 |
| 경고 | 0 | 0 |

## License

MIT (또는 사용자가 원하는 license 로 변경)
