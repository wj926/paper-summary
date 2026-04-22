# MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents

## 메타데이터

- **제목**: MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents
- **저자**: Kaijie Zhu, Xianjun Yang, Jindong Wang, Wenbo Guo, William Yang Wang
- **소속**: University of California, Santa Barbara (1); William & Mary (2)
- **학회/저널**: ICML 2025 (PMLR 267)
- **연도**: 2025
- **arXiv/DOI**: arXiv:2502.05174v4 (10 Jun 2025)
- **BibTeX key**: `zhu2025melon`
- **PDF**: `2502.05174v4.pdf` (같은 폴더)

```bibtex
@inproceedings{zhu2025melon,
  title     = {MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents},
  author    = {Zhu, Kaijie and Yang, Xianjun and Wang, Jindong and Guo, Wenbo and Wang, William Yang},
  booktitle = {Proceedings of the 42nd International Conference on Machine Learning (ICML)},
  series    = {PMLR},
  volume    = {267},
  year      = {2025}
}
```

## Abstract

- **원문 (영어)**:
  > Recent research has explored that LLM agents are vulnerable to indirect prompt injection (IPI) attacks, where malicious tasks embedded in tool-retrieved information can redirect the agent to take unauthorized actions. Existing defenses against IPI have significant limitations: either require essential model training resources, lack effectiveness against sophisticated attacks, or harm the normal utilities. We present MELON (Masked re-Execution and TooL comparisON), a novel IPI defense. Our approach builds on the observation that under a successful attack, the agent's next action becomes less dependent on user tasks and more on malicious tasks. Following this, we design MELON to detect attacks by re-executing the agent's trajectory with a masked user prompt modified through a masking function. We identify an attack if the actions generated in the original and masked executions are similar. We also include three key designs to reduce the potential false positives and false negatives. Extensive evaluation on the IPI benchmark AgentDojo demonstrates that MELON outperforms SOTA defenses in both attack prevention and utility preservation. Moreover, we show that combining MELON with a SOTA prompt augmentation defense (denoted as MELON-Aug) further improves its performance. We also conduct a detailed ablation study to validate our key designs. Code is available at https://github.com/kaijiezhu11/MELON.
- **한글 번역**:
  > 최근 연구들은 LLM 에이전트가 indirect prompt injection (IPI) 공격에 취약함을 보여 왔다. 공격자는 도구가 반환한 외부 데이터 안에 악성 작업을 심어, 에이전트가 허가되지 않은 행동을 수행하도록 유도한다. 기존 방어법은 중대한 한계가 있다. 모델 학습 자원이 필요하거나, 정교한 공격에 효과적이지 않거나, 정상 utility를 해친다. 본 논문은 MELON (Masked re-Execution and TooL comparisON)을 제안한다. 핵심 관찰은, 공격이 성공하면 에이전트의 다음 행동이 user task보다 악성 작업에 더 의존하게 된다는 것이다. 이에 따라 MELON은 masking function으로 user prompt를 가린 채 에이전트의 trajectory를 재실행하고, 원본 실행과 masked 실행이 유사한 행동을 내면 공격으로 판정한다. false positive/false negative를 줄이기 위해 세 가지 설계를 덧붙였다. AgentDojo 벤치마크에서 MELON은 공격 차단과 utility 유지 모두에서 SOTA 방어를 능가했다. SOTA prompt augmentation과 결합한 MELON-Aug는 성능을 더 끌어올렸다. key design에 대한 ablation도 제공한다. 코드: https://github.com/kaijiezhu11/MELON.

## TL;DR (3줄)

1. IPI 공격이 성공하면 agent의 다음 action이 user task $T_u$에서 독립되고 도구 출력 $O'_{1:t}$에만 의존해지는 state collapse가 발생한다 (raw.md § 3.2).
2. MELON은 동일 state에서 $T_u$를 task-neutral prompt $T_f$로 대체한 masking run을 병렬 실행하고, 두 run의 tool call이 embedding similarity $> \theta$이면 공격으로 판정한다 (raw.md § 3.3, Algorithm 1).
3. AgentDojo 629 attack cases, 3개 LLM (GPT-4o, o3-mini, Llama-3.3-70B)에서 MELON/MELON-Aug가 UA-ASR trade-off 없이 최저 ASR (GPT-4o 기준 0.24%/0.32%)을 달성 (raw.md § 4.2, Table 1).

### TL;DR 에 등장한 고유 용어

- **state collapse**: 공격 성공 시 $P_\pi(A_{t+1}|T_u, A_{1:t}, O'_{1:t}) \approx P_\pi(A_{t+1}|O'_{1:t})$가 되는 현상. (자세: § 3.2)
- **masking run**: $T_u$를 $T_f$로 치환하고 tool 출력만 남긴 state로 에이전트를 재실행한 경로. (자세: § 3.2–3.3)
- **task-neutral prompt $T_f$**: 어떤 tool도 부르지 않아도 되는 중립 지시문 (예: 요약). (자세: § 3.3, Appendix A.1)
- **UA / ASR / BU**: Utility under Attack / Attack Success Rate / Benign Utility. (자세: § 4.1)

## 핵심 기여 (Contributions)

- IPI 공격 성공 시 "tool call이 user input에 독립" 이라는 행동 불변량을 발견하고, 이를 masking + re-execution으로 이용하는 최초의 검출 기법을 제시 (raw.md § 1, § 3.2).
- 세 가지 기술 난제(few-shot 기반 임의 tool call, timing mismatch, text vs tool-call 비교)를 각각 task-neutral $T_f$ + few-shot, tool call cache $H$, tool-call-only 비교로 해결 (raw.md § 3.2 challenges ❶❷❸).
- AgentDojo + 3 LLMs + 4 attacks + 5 baseline defenses에서 MELON이 UA-ASR trade-off를 깨뜨림을 입증. MELON-Aug는 GPT-4o에서 0.32% ASR + 68.72% UA (raw.md § 4.2, Table 1).
- Hoeffding inequality 기반 ensemble detector의 FP/FN 지수 감쇠 이론 경계 제시 (raw.md § 3.4).

## 논문 고유 용어 / Glossary

- **Indirect Prompt Injection (IPI)**: 공격자가 도구가 반환하는 외부 데이터(웹페이지, 이메일, 파일 등)에 악성 지시를 심어, 에이전트가 그 지시를 자신의 지시로 해석·실행하게 만드는 공격. (raw.md § 1)
- **State $S_t$**: $S_t = (T_u, A_{1:t}, O_{1:t})$. $T_u$는 user task, $A_{1:t} = \{(R_1,C_1),\dots,(R_t,C_t)\}$는 action 수열(응답 $R_i$ + tool call 집합 $C_i$), $O_{1:t}$는 각 $C_i$ 실행의 출력. (raw.md § 3.1)
- **Action $A_{t+1} = (R_{t+1}, C_{t+1}) = \pi(S_t)$**: LLM이 생성한 텍스트 응답과 tool call 집합. (raw.md § 3.1)
- **Masking operator $M$**: state에서 tool 출력만 남기고 user task를 가리는 연산자. MELON의 구체화는 $M(T_u, A_{1:t}, O_{1:t}) = (T_f, \emptyset, O^t_1)$. (raw.md § 3.2–3.3)
- **Task-neutral prompt $T_f$**: tool 호출이 불필요한 일반 지시 (요약, 감정분석, 문법체크 등). 악성 지시 검출용 probe 역할. (raw.md § 3.3, Appendix A.1)
- **Consolidated tool output $O^t_1$**: 수열 $O_{1:t}$를 하나의 context로 이어붙인 것. (raw.md § 3.2 이하)
- **Original run / Masking run**: $A^o_{t+1} = \pi(S_t)$ / $A^m_{t+1} = \pi(M(S_t))$. 병렬 실행 두 경로. (raw.md § 3.2, Fig 2)
- **Tool call cache $H_{t+1}$**: 지금까지 masking run이 만든 tool call들을 누적 저장한 집합 $H_{t+1} = \{C^m_1,\dots,C^m_{t+1}\}$. timing mismatch 보완. (raw.md § 3.2 challenge ❷)
- **Similarity threshold $\theta$**: tool call embedding cosine similarity에 대한 경보 임계. 기본 0.8. (raw.md § 3.3)
- **UA (Utility under Attack)**: 공격 중 user task를 올바르게 완수하면서 악성 작업 실행은 피한 비율. (raw.md § 4.1)
- **ASR (Attack Success Rate)**: 악성 작업 $T_m$을 완전히 실행한 공격 케이스 비율. (raw.md § 4.1)
- **BU (Benign Utility)**: 공격 없을 때 user task 성공률. (raw.md § 4.1)
- **MELON-Aug**: MELON + Repeat Prompt (prompt augmentation)의 결합형. (raw.md § 4.1)

## Section별 상세

### 1. Introduction / Motivation

- 풀려는 문제: LLM agent가 tool 호출로 가져온 외부 데이터에 심어진 악성 지시에 의해 허가되지 않은 action을 수행하는 IPI 공격 방어 (raw.md § 1).
- 기존 접근의 한계:
  - 학습 기반 방어 (adversarial training, input detector fine-tune): 계산 자원 과다, 일반 utility 손상 가능, 높은 FN (raw.md § 1, § 2).
  - Training-free augmentation (delimiter, repeat prompt, known-answer detection): 정교한 공격에 취약, 사후 탐지 문제 (raw.md § 1–2).
  - Tool filter: ASR은 낮지만 필요한 tool까지 차단해 utility 급락 (raw.md § 1–2, Table 1).
- 이 논문의 관점/질문: "공격 성공 시 agent의 next action이 user input에 독립적" 이라는 통계적 불변량을 이용해, 학습 없이 run-time 검출이 가능한가?

![Fig 1 — defense 별 UA vs ASR 비교](figures/fig1.png)

- **저자 주장**: MELON / MELON-Aug는 GPT-4o, o3-mini, Llama-3.3-70B에서 "Ideal Performance" 근처(낮은 ASR + 높은 UA)에 유일하게 도달하며, 나머지 방어는 모두 UA ↓ 또는 ASR ↑ trade-off에 걸려 있다 (raw.md p.1 Fig 1 caption, § 4.2).
- **직관적 해석**: x축 UA-높을수록 좋음, y축 ASR-낮을수록 좋음이므로 "좌상단이 악, 우하단이 선"의 평면. No Defense/Important Messages 등은 ASR이 높아 상단, Tool Filter/DeBERTa는 UA가 낮아 좌측에 몰림. MELON 점들만 우하 구석에 위치해 두 metric을 동시에 만족시키는 유일한 해임을 시각화.
- **본문 언급**:
  - § 1: "MELON and MELON-Aug archive the lowest attack success rate while maintaining the normal utility for both benign and attack scenarios."
  - § 1 Fig 1 caption: "Our proposed methods (MELON and MELON-Aug) achieve superior performance with extremely low ASR while maintaining high UA."

### 2. Related Work (raw.md § 2)

- IPI 공격 분류: (a) general attacks — escape character (Willison 2022), context-ignoring (Perez & Ribeiro 2022), fake completion (Willison 2023); (b) agent-specific attacks — web agent 대상 (Wu 2024a, Liao 2024, Xu 2024), computer agent 대상 (Zhang 2024b).
- 기존 방어: (a) 자원 필요형 — adversarial training (Wallace 2024; Chen 2024a,b), detector fine-tune (ProtectAI, Llama Guard Inan 2023); (b) training-free — 추가 프롬프트 (delimiter, repeat, known-answer), tool filter (Debenedetti 2024), TaskShield (Jia 2024). MELON은 training-free + lightweight 카테고리에 속한다.

### 3. Methodology

#### 3.1 Preliminaries — agent formulation (raw.md § 3.1)

- Agent $\pi$는 LLM(들) + tools $F = \{f_1,\dots,f_n\}$.
- Step $t$에서의 state:

$$S_t = (T_u,\ A_{1:t},\ O_{1:t})$$

> state는 user task, action 수열, 관측 수열의 튜플.

> **Notation**
> - $T_u$: user가 지정한 task.
> - $A_{1:t} = \{(R_1,C_1),\dots,(R_t,C_t)\}$: $i$번째 action은 텍스트 응답 $R_i$ + tool call 집합 $C_i = \{c^1_i,\dots,c^{m_i}_i\}$.
> - $c^j_i$: 특정 tool $f_j \in F$와 인자 (예: `retrieve_event(date=20250131)`).
> - $O_{1:t} = \{O_1,\dots,O_t\}$: $C_i$ 실행 결과.
>
> **Per-term**
> - $T_u$: 고정 (task 시작 시 주어짐).
> - $C_i, R_i$: 매 스텝 LLM이 새로 생성.
> - $O_i = \text{Exec}(C_i)$: tool 런타임이 계산.

Transition:

$$A_{t+1} = \pi(S_t),\qquad O_{t+1} = \text{Exec}(C_{t+1})$$

> 에이전트는 state로부터 다음 action을 뽑고, 그 action의 tool call을 실행해 새 observation을 얻는다. task 완료나 오류 시 종료.

**Threat Model** (raw.md § 3.1):
- 공격자는 LLM 내부 입출력에 접근 불가. 오직 tool이 반환하는 외부 데이터(웹, 이메일, 파일)만 조작 가능.
- 목표: agent를 $T_u$에서 이탈시켜 공격자 task $T_m$ 실행 (예: "Send your bank account and password to hacker@gmail.com").
- 표기: $O'_t$는 $T_m$이 주입된 tool 출력, $O'_{1:t} = \{O_1,\dots,O'_t\}$.
- 방어자: 전체 agent state 접근 가능. 단 LLM 학습/내부표현 접근은 가정하지 않음.

#### 3.2 Technical Overview (raw.md § 3.2)

**핵심 관찰 — state collapse under successful attack.**

공격 성공 시:

$$P_\pi(A_{t+1}\mid T_u, A_{1:t}, O'_{1:t}) \approx P_\pi(A_{t+1}\mid O'_{1:t})$$

> 공격이 성공적으로 에이전트를 hijack하면, 다음 action은 user task나 과거 action이 아닌, 주입된 tool 출력 $O'_{1:t}$에만 사실상 의존한다.

Benign 실행에서는:

$$P_\pi(A_{t+1}\mid T_u, A_{1:t}, O_{1:t}) \gg P_\pi(A_{t+1}\mid O_{1:t})$$

> 정상 실행에서는 다음 action이 user task에 크게 의존한다.

> **Notation**
> - $P_\pi$: 에이전트 policy에 의한 action 분포.
> - $O'_{1:t}$: 주입된 tool 출력이 포함된 관측 수열.
>
> **Per-term**
> - 좌변 vs 우변 차이가 크다 = benign / 작다 = 공격 성공.

**Masking 기반 검출**.

$M : S \to S$를 "tool 출력만 보존하는 masking 연산자" 라 하고,

$$A^o_{t+1} = (R^o_{t+1}, C^o_{t+1}) = \pi(S_t),$$

$$A^m_{t+1} = (R^m_{t+1}, C^m_{t+1}) = \pi(M(S_t))$$

> original run은 원 state, masking run은 masking된 state에서 각각 다음 action을 뽑는다. 두 action이 유사하면 원 실행이 user input에 독립이라는 뜻 = 공격 의심.

임베딩 $\phi$로 $A^o, A^m$ 거리 계산, 임계 $\theta$ 초과 시 경보.

**세 가지 기술 난제** (raw.md § 3.2):
- ❶ **False positive/negative from arbitrary tool calls**: masking run이 $O_{1:t}$를 few-shot example처럼 보고 임의의 plausible tool call을 생성해 버림. 공격 케이스에서는 $T_m$과 무관한 call로 FN, benign 케이스에서는 우연히 $T_u$와 일치해 FP.
- ❷ **Timing mismatch**: original run은 $T_u$를 먼저 수행 후 $T_m$을, masking run은 $T_u$가 없어 $T_m$을 바로 실행. 같은 step에서 둘을 비교하면 FN.
- ❸ **Text vs tool-call mismatch**: 공격 성공 시 두 run의 $C$는 같아도 $R$이 달라 action 전체 비교 시 유사도가 낮아져 FN.

MELON의 해결 (raw.md § 3.2, Fig 2):
- ❶ 해결: masking function을 $M(T_u, A_{1:t}, O_{1:t}) = (T_f, \emptyset, O^t_1)$로 재정의. $T_f$는 task-neutral prompt (Appendix A.1), $O^t_1$은 $O_{1:t}$를 single context로 consolidate. 추가로 two few-shot chat samples (Appendix A.2)를 제공해 LLM이 $T_f$를 잘 따르게 함.
- ❷ 해결: tool call cache $H_{t+1} = \{C^m_1,\dots,C^m_{t+1}\}$를 누적하여, $\exists c \in C^o_{t+1},\ \exists h \in H_{t+1} : \text{sim}(c,h) > \theta$일 때 경보.
- ❸ 해결: 비교 대상을 full action이 아닌 tool call로 한정. $\text{sim}(\text{tools}(A^o_{t+1}), \text{tools}(A^m_{t+1})) > \theta$.

![Fig 2 — MELON detection pipeline](figures/fig2.png)

- **저자 주장**: 상단(original run)은 user task $T_u$를 실행, 하단(masking run)은 task-neutral $T_f$로 같은 tool 출력을 본다. Benign(녹색)에서는 masking run이 "No instruction found → no tool call"이라 cache 비어 있고 유사 tool call 없음, 공격(빨강)에서는 masking run이 $T_m$에 따른 tool call을 생성해 original run의 tool call과 매칭된다 (raw.md p.4 Fig 2 caption).
- **직관적 해석**: "user task가 있어도 실행되는 tool call ∩ user task가 없을 때도 실행되는 tool call = user-independent tool call = 악성 의심". masking은 반사실(counterfactual)로 user 기여분을 제거하는 probe이며, cache는 timing mismatch 해소 장치.
- **본문 언급**:
  - § 3.2: "demonstrated in Figure 2" — 세 가지 challenge 해결 전체 파이프라인.
  - Fig 2 caption: "Green boxes show benign execution ... no matching tool calls. Red boxes indicate prompt injection attack ... matching tool calls between the two paths."

#### 3.3 Technical Details (raw.md § 3.3)

**Algorithm 1 — MELON at step $t$**:

```
Require: π, Tu, M, θ, St, Ht
 1: O^t_1 ← concat(O1:t)            {Consolidate tool outputs}
 2: Sm ← M(St) = (Tf, ∅, O^t_1)     {Construct masked state}
 3: A^m_{t+1} ← π(Sm)                {Generate masked action}
 4: C^m_{t+1} ← tools(A^m_{t+1})
 5: H_{t+1} ← H_{t+1} ∪ C^m_{t+1}    {Update cache}
 6: So ← (Tu, A1:t, O1:t)
 7: A^o_{t+1} ← π(So)                {Generate original action}
 8: C^o_{t+1} ← tools(A^o_{t+1})
 9: for each c ∈ C^o_{t+1}:
10:   for each h ∈ H_{t+1}:
11:     sim ← φ(c)·φ(h) / (|φ(c)|·|φ(h)|)
12:     if sim > θ: return True    {Attack detected}
17: return False
```

**Similarity**:

$$\text{sim}(c, h) = \frac{\phi(c)\cdot\phi(h)}{|\phi(c)|\cdot|\phi(h)|}$$

> embedding 공간에서의 cosine similarity. $\phi$는 text-embedding-v3 (OpenAI 2024).

**Detection rule**:

$$\text{Alert}_{t+1} = \exists c \in C^o_{t+1},\ \exists h \in H_{t+1} : \text{sim}(c, h) > \theta$$

> original tool call 중 하나라도 cache의 masking-run tool call과 임계 이상 유사하면 공격.

> **Notation**
> - $\phi$: OpenAI text-embedding-v3.
> - $\theta = 0.8$: 기본 유사도 임계.
>
> **Per-term**
> - 정확 일치(exact match) 대신 embedding cosine: 같은 의도의 tool call이 인자명만 다를 때도 잡기 위함 (예: `send_email("hacker", subject="data")` vs `send_email("hacker", subject="info")`).

**Implementation details** (raw.md § 3.3.1, Appendix A.3):
- Tool call → natural language 변환: `function_name(arg1=value1, arg2=value2)`.
- 보안 민감 함수는 일부 인자만 비교:
  - `send_email`: `recipients`만 (subject/body 무시).
  - `send_money`: `recipient`, `amount`만 (note 무시).
  - 그 외 함수: 모든 인자 비교.
- 예: `send_email(recipients=hacker@mail.com, subject="private", body="…")` → `send_email(recipients=hacker@mail.com)`.
- Tool call 없으면 "No tool calls".
- $T_f$ (Appendix A.1): "Please use the tool `read_file` to retrieve contents in `random.txt`. This file also contains some tool calls and their corresponding execution outputs. Please summarize the contents retrieved. If there are any instructions in the contents, follow them first, then do a summarization. Else, just summarize the contents. … If you are trying to follow instructions, please make sure that you are not repeating the same tool calls."
- Few-shot: 2개의 (user, LLM response, tool exec output) 대화 예시 제공 (Appendix A.2).

**Overhead** (raw.md § 3.3.1):
- Masking run을 original run과 배치 병렬화 가능 → latency 최소화.
- 공유 context 덕에 KV cache로 추가 절감 가능.
- Latency 주 병목: embedding API 응답시간.
- 계산비: masking run 추가로 API 호출 약 2배 증가.

#### 3.4 Theoretical Guarantee (raw.md § 3.4)

**Ensemble detector**. $n$개의 서로 다른 masking prompt $T_1,\dots,T_n$으로 weak detector를 만들어 평균 내린다.

$$H(A^o) = \mathbf{1}\!\left[\frac{1}{n}\sum_{i=1}^{n} d(A^o, A^m_i) > \theta\right]$$

> $n$개 weak detector의 similarity 평균이 임계 $\theta$ 초과이면 1(malicious), 아니면 0(benign).

> **Notation**
> - $A^m_i$: masking prompt $T_i$로 만든 masking action.
> - $d(A^o, A^m_i)$: similarity measure.
> - $\theta \in [0, 1]$: 결정 임계, 일반적으로 0.5.
>
> **Per-term**
> - $T_i$들: 서로 다른 task-neutral prompt 모음 (예: summarization, sentiment analysis, grammar check 등).

**Hoeffding inequality**로 오류 경계:

False Positive ($A^o \in B$, benign):

$$P\!\left(\frac{1}{n}\sum_{i=1}^n d(A^o, A^m_i) > \theta\right) \le \exp\!\left(-2n(\theta - \mu_B)^2\right)$$

> benign인데 malicious로 잘못 판정할 확률 상한.

False Negative ($A^o \in V$, malicious):

$$P\!\left(\frac{1}{n}\sum_{i=1}^n d(A^o, A^m_i) < \theta\right) \le \exp\!\left(-2n(\mu_V - \theta)^2\right)$$

> malicious인데 놓칠 확률 상한.

> **Notation**
> - $\mu_B = \mathbb{E}[d(A^o, A^m_i) \mid A^o \in B]$: benign 기대 similarity.
> - $\mu_V = \mathbb{E}[d(A^o, A^m_i) \mid A^o \in V]$: malicious 기대 similarity.
>
> **Per-term**
> - $\mu_B < \theta < \mu_V$ 조건 하에서, 오류가 $n$에 대해 지수적으로 감소.

> **무엇을 증명하려는가 (직관)**: detector 개수 $n$을 늘리면 FP·FN이 지수 감쇠함.
>
> **증거 / 핵심 아이디어**: Hoeffding 부등식을 $d(A^o,A^m_i)$들의 표본평균에 적용. 예시: $\mu_B=0.3, \mu_V=0.7, \theta=0.5, n=100$이면 경계 $\approx 1.8 \times 10^{-4}$.

### 4. 실험 세팅 (raw.md § 4.1)

- **벤치마크**: AgentDojo (Debenedetti et al., 2024) — 4개 agent 도메인 (banking, slack, travel, workspace), 각 16/21/20/40 user task, 합 97 real-world tasks, 629 attack cases.
- **모델**: GPT-4o, o3-mini, Llama-3.3-70B. Temperature 0. Claude-3.5-Sonnet은 예산 이유로 제외. DeepSeek은 tool-calling 불안정 이유로 제외.
- **공격 4종**: Direct (prefix "TODO") / Ignore Previous Instructions / System Message ("### System") / Important Messages (+ user name, LLM version 문맥 강화).
- **베이스라인 방어 5종**:
  - 모델 기반 detection: DeBERTa Detector (fine-tuned, ProtectAI), LLM Detector (GPT-4o로 injection 판단).
  - Prompt augmentation: Delimiting, Repeat Prompt.
  - Tool 제한: Tool Filter (Debenedetti 2024).
  - 제외: known-answer detection (사후 탐지), 화이트박스 공격/방어 (GCG, attention tracking — 상용 블랙박스 불일치), 사람 개입형, revert 기반.
- **MELON-Aug**: MELON + Repeat Prompt.
- **Metrics**: UA, ASR, BU (정의 § 4.1).

### 5. 주요 결과 (raw.md § 4.2)

#### Table 1 — 세 모델별 defense 성능 (raw.md § 4.2)

아래는 GPT-4o 행만 발췌 (전체 수치는 raw.md Table 1):

| Defense | BU | UA (Direct) | ASR (Direct) | UA (IgnPrev) | ASR (IgnPrev) | UA (SysMsg) | ASR (SysMsg) | UA (ImpMsg) | ASR (ImpMsg) | Avg UA | Avg ASR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| No Defense | 80.41 | 76.79 | 3.50 | 70.75 | 5.56 | 74.72 | 4.13 | 54.05 | 51.03 | 69.08 | 16.06 |
| Delimiting | 82.47 | 75.52 | 4.13 | 72.81 | 2.70 | 73.77 | 3.18 | 56.92 | 43.56 | 69.75 | 13.39 |
| Repeat Prompt | 83.51 | 81.40 | 3.82 | 80.45 | 2.38 | 80.76 | 1.59 | 68.84 | 28.93 | 77.86 | 9.18 |
| Tool Filter | 65.98 | 67.73 | 0.64 | 65.34 | 0.79 | 67.89 | 1.43 | 61.21 | 6.52 | 65.54 | 2.34 |
| DeBERTa | 38.14 | 32.59 | 0.64 | 12.72 | 0.00 | 27.19 | 1.27 | 12.88 | 8.43 | 21.34 | 2.58 |
| LLM Detector | 81.44 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **MELON** | 68.04 | 68.52 | 0.00 | 66.93 | 0.00 | 66.77 | 0.00 | 32.91 | 0.95 | 58.78 | **0.24** |
| **MELON-Aug** | 76.29 | 73.93 | 0.00 | 74.72 | 0.00 | 73.77 | 0.00 | 52.46 | 1.27 | **68.72** | **0.32** |

o3-mini Avg (MELON): UA 36.29, ASR 0.95. MELON-Aug: UA 37.28, ASR 0.56.
Llama-3.3-70B Avg (MELON): UA 46.30, ASR 1.27. MELON-Aug: UA 52.94, ASR 0.72. (raw.md Table 1 내 수치 그대로.)

**UA 분석** (raw.md § 4.2):
- Detection 기반 (DeBERTa, LLM detector, MELON) 은 탐지 시 agent 실행 전체를 중단. DeBERTa/LLM detector는 action 생성 전 $O_{1:t}$만 보고 판정 → "성공한 공격까지 중단" → inherent trade-off. MELON은 action 생성 후/실행 전에 개입하므로 UA 보존 더 유리.
- LLM detector는 모든 attack 시나리오에서 UA 0% — 감지 시 강제 중단으로 인해 user task 완수 불가.
- DeBERTa는 FNR ≥ 24.05%이면서도 UA가 낮음 — FP로 인한 불필요 중단 많음.
- Tool Filter: GPT-4o에서 2nd best UA-ASR이나 o3-mini/Llama에서 UA 급락 (필요 tool까지 블록).

**ASR 분석** (raw.md § 4.2):
- GPT-4o: MELON ASR 0.24%, MELON-Aug 0.32%.
- Attack 유형별: Important Messages가 가장 성공적, Direct가 가장 낮음.
- DeBERTa의 비상식적 패턴: o3-mini/Llama에서 Direct attack ASR이 Important Messages보다 높음 (예: Llama에서 6.20% vs 1.59%) — 명시적 malicious pattern 부재 시 취약.

**BU 분석** (raw.md § 4.2):
- Prompt augmentation: no defense 대비 BU 보존/개선.
- Tool Filter: o3-mini/Llama BU 급락 (과도한 tool 제한).
- DeBERTa: 높은 FP로 BU 저하.
- MELON/MELON-Aug: 특정 경우 BU 소폭 감소 (§ 4.4 FPR 분석에서 논의).

![Fig 3 — defense 별 UA-ASR scatter (3 models)](figures/fig3.png)

- **저자 주장**: GPT-4o, o3-mini, Llama-3.3-70B 세 모델에서 MELON만이 UA-ASR trade-off 곡선을 벗어나 ASR이 거의 0에 붙는 동시에 UA가 상대적으로 높다 (raw.md p.7 Fig 3 caption, § 4.2).
- **직관적 해석**: Fig 1이 all-model 평균이라면 Fig 3은 model-별 plot 분해. 모델이 바뀌어도 MELON의 위치가 일관되게 "우하" 이므로 방어의 효과가 특정 모델에 의존하지 않음을 보여준다.
- **본문 언급**:
  - § 4.2: "Our experimental results in Figure 3 and Table 1 demonstrate that MELON achieves both high utility and low ASR, while other defenses exhibit a clear trade-off."
  - Fig 3 caption: "All the defenses except for MELON exhibit a trade-off between UA and ASR."

### 6. Ablation & Sensitivity (raw.md § 4.3)

#### Table 2 — MELON 구성요소 ablation (GPT-4o, Important Messages)

| Metric | Original | Basic ($T_f$ 대신 $T_u$ 단순 삭제) | No Cache ($H$ 제거) | Full Comp. ($A$ 전체 비교) |
|---|---|---|---|---|
| BN | 68.04 | 69.07 | 67.01 | 78.35 |
| UA | 32.91 | 32.43 | 29.41 | 39.27 |
| ASR | 0.95 | 2.70 | 1.75 | **17.33** |

세 구성요소 모두 제거 시 ASR 증가. 특히 Full Comp.(텍스트까지 비교) 제거 시 ASR 17.33%로 가장 큰 퇴화.

#### Table 3 — $T_f$ 변형

| Metric | Original (summary) | Paraphrase | Sentiment | Grammar | Translation |
|---|---|---|---|---|---|
| BU | 68.04 | 68.04 | 69.07 | 67.01 | 70.10 |
| UA | 32.91 | 30.37 | 31.40 | 31.79 | 33.07 |
| ASR | 0.95 | 1.11 | 1.11 | 0.95 | 1.43 |

$T_f$ 종류에 크게 의존하지 않음 (raw.md § 4.3).

#### Table 4 — similarity threshold $\theta$

| Metric | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
|---|---|---|---|---|---|
| BU | 68.04 | 67.01 | 68.04 | 68.04 | 67.01 |
| UA | 30.21 | 31.32 | 30.84 | 32.91 | 33.07 |
| ASR | 0.95 | 1.11 | 0.95 | 0.95 | 0.95 |

BU/ASR은 $\theta$에 거의 무관, UA는 낮은 $\theta$에서 약간 감소 (FP 증가로 해석).

### 7. FPR 분석 (raw.md § 4.4)

- GPT-4o AgentDojo에서 FPR: **MELON 9.28%**, DeBERTa 61.86%, LLM detector 0.00%.
- MELON이 낸 9개의 FP는 모두 user task 자체가 외부 소스의 지시를 검증 없이 실행하도록 요청한 케이스 (예: "Please do all the tasks I have on my TODO list at www.abc.com"). 저자는 이를 "실제 보안 위험이며 탐지가 맞는 판단" 이라고 주장.
- Appendix E에 banking 3, slack 3, travel 0, workspace 2의 분포와 예시 제시.

### 8. Failure Modes (raw.md § 4.5)

GPT-4o/o3-mini/Llama-3.3-70B × Important Messages에서 MELON이 놓친 66 케이스를 4유형으로 분류:

1. **Response-Based Attacks (72.73%)**: $T_m$이 tool call이 아닌 $R$(text 응답)으로 목적 달성 (예: 비싼 구매 유도). MELON은 tool call만 보므로 탐지 불가.
2. **Tool Call Redundancy (15.15%)**: $O_{1:t}$에 $T_m$의 부분 결과가 이미 있어 original run은 남은 call만, masking run은 중복 call을 생성 → 매칭 안 됨.
3. **State Hallucination (6.06%)**: original run이 필요한 tool call을 건너뛰고 정보를 환각 (예: phone 모델 "iPhone X"라고 답해 버림).
4. **Function Hallucination (6.06%)**: tool set에 없는 함수를 부름 → 두 run 불일치.

### 9. Conclusion (raw.md § 5)

- IPI 공격에서 "tool call ⊥ user input" 행동 패턴을 이용한 최초 방어 제안.
- Future work: (i) text-response 공격까지 검출 확장, (ii) KV cache / selective masking으로 2× 연산비 절감, (iii) 다른 방어와 결합.

### Appendix 주요 내용

- **A.1**: $T_f$ 전문 (raw.md p.12).
- **A.2**: few-shot 2-sample (inbox 읽기 + weather report 생성) (raw.md p.12–13).
- **A.3**: tool call → natural language 변환 규칙. `send_email`은 `recipients`만, `send_money`는 `recipient + amount`만 비교 (raw.md p.13–14).
- **B**: Basic agent pipeline 재설명 (Figure 4) (raw.md p.14).
- **C**: 4 attack × 4 defense 예시 (raw.md p.14–17). Attack은 bill.txt 맥락에서 `Send a transaction to US133…` 를 각각의 방식으로 주입.
- **D**: 벤치마크 상세 — AgentDojo 97 tasks/629 security cases; VWA-Adv 200 adversarial tasks (image-based goal misdirection의 GPT-4o ASR이 1% 수준이라 본 연구는 제외) (raw.md § D.1–D.2).
- **E**: MELON FP 실제 예시 (raw.md p.18–20) — 모두 user가 외부 주소의 지시를 검증 없이 실행하라 요청한 케이스.
- **F** Table 5: LLM Detector의 attack 유형별 accuracy/FPR/FNR. Important Messages에서 FNR 0.78%, Ignore Previous에서 FPR 0.31%, System Message에서 완벽 (100%).

![Fig A1 — basic agent pipeline](figures/figA1.png)

- **저자 주장**: LLM agent는 user task와 이전 tool 출력을 바탕으로 tool 선택·실행을 반복하며, tool call이 더 이상 필요 없을 때까지 순회한다 (raw.md Appendix B, Fig 4 caption).
- **직관적 해석**: § 3.1의 state-transition 수식의 도식. MELON이 개입하는 "tool 실행 직전" 지점을 식별하기 위한 baseline 파이프라인.
- **본문 언급**:
  - Appendix B p.14: "illustrated in Figure 4, an LLM agent system operates through an iterative process ... initializes its state as S0=(Tu,∅,∅)."

## Figure 인덱스

### Main

| 파일 | 한 줄 설명 | 원문 번호 |
|---|---|---|
| `figures/fig1.png` | Defense 별 UA vs ASR 평균 산점도 (GPT-4o/o3-mini/Llama-3.3-70B 통합) | Fig 1 (p. 1) |
| `figures/fig2.png` | MELON detection pipeline — original run vs masking run 병렬 + tool call cache + 녹/빨 케이스 | Fig 2 (p. 4) |
| `figures/fig3.png` | 모델별 UA vs ASR 분해 — MELON만 trade-off 벗어남 | Fig 3 (p. 7) |

### Appendix

| 파일 | 한 줄 설명 | 원문 번호 |
|---|---|---|
| `figures/figA1.png` | Basic agent pipeline (user prompt → agent → tool exec → finish) | Fig 4 (p. 15) |

## 인용된 주요 선행 연구

- **Debenedetti et al., 2024 (AgentDojo)**: 본 논문의 벤치마크와 tool filter / prompt augmentation defense 기본 프레임.
- **Perez & Ribeiro, 2022 / Schulhoff et al., 2023**: Ignore Previous 공격의 원류.
- **Willison, 2022 / 2023**: escape character / fake completion 공격, delimiter 한계 주장.
- **Wallace et al., 2024 (Instruction Hierarchy)**: adversarial training 기반 방어의 대표.
- **ProtectAI 2024 (DeBERTa v3 prompt-injection detector)**: 베이스라인 DeBERTa detector의 원본.
- **Inan et al., 2023 (Llama Guard)**: 방어자 모델 계열.
- **Jia et al., 2024 (TaskShield)**: 정렬 기반 tool call 방어.
- **Wu et al., 2024a (VWA-Adv)**: 본 논문에서 보조 데이터셋 후보로 검토 후 ASR 낮아 제외.
