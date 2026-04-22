# Examples

`paper-summary` skill 을 실제 논문 두 편에 적용한 결과물입니다.

| 폴더 | 논문 | 학회 | 핵심 |
|------|------|-----|------|
| [`1_zhu2025MELON(ICML2025)`](1_zhu2025MELON%28ICML2025%29/) | MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents | ICML 2025 | Masked re-execution + tool call comparison 으로 IPI 공격 탐지 |
| [`2_chang2026ChatInject(ICLR2026)`](2_chang2026ChatInject%28ICLR2026%29/) | ChatInject | ICLR 2026 | Chat format 기반 prompt injection 공격 |

각 폴더에 들어있는 것:

- `abstract.md` — 메타데이터 + Abstract 원문 + 한글 번역 (phase C 산출물, 짧음)
- `summary.md` — Section 상세 + 수식 + Table + figure embed (phase C 산출물, 1차 소스)
- `raw.md` — PDF 전문 + figure embed + figure index (phase B 산출물, 재독용)
- `figures/figN.png`, `figures/figAN.png` — 크롭된 main / appendix figure

> 참고: `figures/_pages/` (200dpi 페이지 원본) 과 PDF 파일은 용량 / 저작권 관계로 이 public examples 에 포함하지 않았습니다. 실제 skill 을 돌리면 로컬 산출물에는 같이 생성됩니다.

## 저작권 / Fair use

Figure 이미지와 abstract 원문은 각 논문 저자의 저작권이며, 이 repo 에는 skill 사용 예시를 보여주기 위한 교육적 목적으로 일부 포함했습니다. 논문 인용 및 원본 링크는 각 폴더의 `abstract.md` 상단 메타데이터를 참고하세요.
