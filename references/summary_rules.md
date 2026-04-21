# Summary 작성 규칙

> 이 파일은 Phase 2 (raw.md → `summary.md` + `abstract.md` 작성) 시 LLM 이 따라야 할 규칙. SKILL.md 에서 시작 시 load 한다.

## 0. 폴더명 · venue 결정 ★

### 0.1 폴더명 규칙

`<N>_<firstauthor><year><METHOD>(<venue><year>)`

- `<N>`: 프로젝트 `papers/` 아래에서의 추가 순서 인덱스 (1 부터). `PAPERS.md` 인덱스와 동일.
- `<firstauthor>`: 제1저자 성 (소문자). 예: `zhu`, `kim`, `qi`.
- `<year>`: 논문 연도 (4자리).
- `<METHOD>`: 논문의 핵심 알고리즘·method 이름 (대문자 acronym 우선). 예: `MELON`, `KLASS`, `PAPL`. Method 이름이 긴 경우 acronym 만 / 핵심 키워드만 (2-3 단어 camelCase).
- `<venue><year>`: 학회 약어 + 연도. 예: `ICML2025`, `NeurIPS2025`, `ICLR2026`. Oral/Spotlight 가 명시돼 있으면 `(ICLR2026-Spotlight)` 식으로 suffix.

예: `1_zhu2025MELON(ICML2025)`, `2_kim2025KLASS(NeurIPS2025)`.

### 0.2 venue 결정 — preprint 인 경우 web search 필수 ★

- arXiv PDF 에는 학회 정보가 없거나 오래된 버전일 수 있음.
- 논문이 arXiv 만으로 보이면 **Google 에서 정확한 제목 검색** 해서 ICML/NeurIPS/ICLR/ACL 등에 accept 됐는지 확인.
- 확인되면 해당 venue 사용. 확인 안 되면 `preprint`.

### 0.3 PDF 파일명

폴더 안의 PDF 는 `<firstauthor><year><METHOD>.pdf` 또는 원 arXiv ID 유지 (`2502.05174v4.pdf`) 중 프로젝트 convention 을 따른다. 폴더가 이미 식별자 역할을 하므로 PDF 명 자체는 덜 중요.

## 0.4 Phase 2 출력물 두 개

- **`abstract.md`**: 메타데이터 + Abstract 원문 + 한글 번역. 짧다. 급히 논문 서치 시 관련성만 판단하는 용도.
- **`summary.md`**: 전체 사실 요약 (수식 / figure / Table / Glossary / Section 상세 포함). 앞으로 대화의 1차 소스.

`abstract.md` 는 `summary.md` 의 메타데이터 + Abstract 섹션을 추출·복제한 짧은 파일. 두 파일 간 메타·번역은 반드시 **동일 문구** — 한 쪽 수정하면 다른 쪽도 동기화.

## 1. 내용 원칙

### 1.1 사실만 쓴다 (hallucination 금지) ★★

- **수치 / 인용 / 수식 / 저자명 / 연도는 raw.md 원문 그대로.** 기억·감으로 변형 금지.
- 확신 없으면 "raw.md 에 명시 없음" 이라고 쓰고 넘어간다. **짐작·지어내기 금지.**
- 주장·해석할 때 **출처 명시**: "raw.md p. 5", "Eq. 7", "Fig 3 caption" 식으로.

### 1.2 개인 idea / 우리 연구 연결 금지

- summary.md 는 논문 **내부 사실** 만. "이걸 우리 연구에 어떻게 쓸까" 류 금지 (별도 skill 이 담당).
- 예외: figure 의 "직관적 해석" — **논문 주장에 기반한** "왜 이 배치인지" 해설은 허용. 새 아이디어 X.

### 1.3 Claude 조어 금지 ★

- 논문에 없는 **새 용어를 만들어 쓰지 않는다**. 따옴표/볼드로 새 명사처럼 보이게 하는 것도 금지.
- 대신:
  - 논문 용어 (Glossary) 를 그대로 쓴다
  - 확립된 일반 ML 용어 (probing, ablation, embedding 등) 단독 사용
  - 기능적 평서문으로 푼다 ("X 는 Y 를 Z 한다" 식)

## 2. 수식 포맷

### 2.1 Display vs Inline

- **짧은 기호·변수** ($x$, $\alpha_t$, $|M|$) 만 인라인 허용.
- **한 줄 이상**, 분자/분모/적분/합/기댓값 포함이면 **무조건 display math** (`$$...$$`).
- 각 display 수식 아래에 **한국어 한 줄 주석**.

### 2.2 본문 수식은 빠짐없이 포함

논문 본문(main sections)의 수식은 **누락 없이** summary.md 에 옮긴다. Appendix-only 수식은 선택.

포맷 (시각 위계 강제):

```
#### (수식 제목, h4)

$$\text{수식}$$

> 한 줄 한국어 주석.

> **Notation**
> - 기호: 정의
>
> **Per-term**
> - factor: 역할
```

Proposition / Theorem / Lemma 은 동일 구조이되, Notation/Per-term 뒤에 추가:

```
> **무엇을 증명하려는가 (직관)**: 한 줄.
>
> **증거 / 핵심 아이디어**: 한두 줄 (full proof: Appendix X.X).
```

## 3. Figure 규칙

### 3.1 Embed 위치

- 본문에 등장하는 figure 는 **해당 Section 안에 embed**.
- 경로: `![Fig N — 한 줄 제목](figures/figN.png)` (main) / `figures/figAN.png` (appendix).
- Main / Appendix 모두 embed. figure 를 "Figure 인덱스" 표에만 넣고 본문에서 누락 금지.

### 3.2 Figure 주석 (3줄)

각 figure embed 바로 밑에:

- **저자 주장**: 저자가 이 figure 로 보이려는 본문 § X.X 의 주장 (사실 기반).
- **직관적 해석**: 왜 이 figure 가 여기 있어야 하는지 — 짧게, **논문 주장 범위 내에서만** (새 아이디어 금지).
- **본문 언급**: 본문에서 이 figure 를 인용한 모든 위치 + 그때 저자가 한 주장. raw.md 에서 "Fig N" / "Figure N" 으로 grep. `- § X.X: "원문 인용" — 주장 요약` 포맷.

## 4. Glossary 운용

- 이 논문이 **새로 정의하거나 특별한 의미로 사용하는** 용어·기호만. 일반 ML 용어 제외.
- 각 항목: **용어 → 한 줄 정의 → 출처 (§ / Eq. / Fig.) → (필요시) 기호**.
- 본문 곳곳에서 그 용어가 나올 때마다 정의 반복 금지 — 첫 등장 또는 glossary 참조.

## 5. 금지 표현

- "통찰", "영감", "시사점", "가능성 있는", "의미 있는", "흥미로운", "중요한" 등 평가·수사.
- "우리는", "본 연구는" — 논문 화자인지 독자인지 헷갈리게 함. "저자는", "논문은" 으로.
- 볼드·따옴표로 새 용어 꾸미기.

## 6. 체크리스트 (작성 종료 시)

- [ ] 메타데이터 + BibTeX 모두 채움
- [ ] Abstract 원문 + 한글 번역
- [ ] TL;DR 3줄
- [ ] Glossary 에 이 논문 고유 용어 전부
- [ ] 본문 수식 누락 없이 모두 포함 (h4 + display + Notation/Per-term)
- [ ] 모든 figure 가 Section 내부에 embed + 3줄 주석
- [ ] 모든 figure 가 Figure 인덱스 표에 등재
- [ ] idea / 우리 연구 연결 / Claude 조어 0건
- [ ] "raw.md 에 없음" 대신 지어낸 수치 0건
