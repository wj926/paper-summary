# zhu2025MELON — Abstract

> 이 파일은 "급히 논문 검색 · 관련성만 판단" 용 short view.
> 수식·figure·본문 상세는 `summary.md`, 원본 전문은 `raw.md`.

## 메타데이터

- **제목**: MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents
- **저자**: Kaijie Zhu, Xianjun Yang, Jindong Wang, Wenbo Guo, William Yang Wang
- **학회/저널**: ICML 2025 (PMLR 267)
- **연도**: 2025
- **arXiv/DOI**: arXiv:2502.05174v4
- **BibTeX key**: `zhu2025melon`
- **폴더**: `1_zhu2025MELON(ICML2025)`

## 원문 (영어)

> Recent research has explored that LLM agents are vulnerable to indirect prompt injection (IPI) attacks, where malicious tasks embedded in tool-retrieved information can redirect the agent to take unauthorized actions. Existing defenses against IPI have significant limitations: either require essential model training resources, lack effectiveness against sophisticated attacks, or harm the normal utilities. We present MELON (Masked re-Execution and TooL comparisON), a novel IPI defense. Our approach builds on the observation that under a successful attack, the agent's next action becomes less dependent on user tasks and more on malicious tasks. Following this, we design MELON to detect attacks by re-executing the agent's trajectory with a masked user prompt modified through a masking function. We identify an attack if the actions generated in the original and masked executions are similar. We also include three key designs to reduce the potential false positives and false negatives. Extensive evaluation on the IPI benchmark AgentDojo demonstrates that MELON outperforms SOTA defenses in both attack prevention and utility preservation. Moreover, we show that combining MELON with a SOTA prompt augmentation defense (denoted as MELON-Aug) further improves its performance. We also conduct a detailed ablation study to validate our key designs. Code is available at https://github.com/kaijiezhu11/MELON.

## 한글 번역

> 최근 연구들은 LLM 에이전트가 indirect prompt injection (IPI) 공격에 취약함을 보여 왔다. 공격자는 도구가 반환한 외부 데이터 안에 악성 작업을 심어, 에이전트가 허가되지 않은 행동을 수행하도록 유도한다. 기존 방어법은 중대한 한계가 있다. 모델 학습 자원이 필요하거나, 정교한 공격에 효과적이지 않거나, 정상 utility를 해친다. 본 논문은 MELON (Masked re-Execution and TooL comparisON)을 제안한다. 핵심 관찰은, 공격이 성공하면 에이전트의 다음 행동이 user task보다 악성 작업에 더 의존하게 된다는 것이다. 이에 따라 MELON은 masking function으로 user prompt를 가린 채 에이전트의 trajectory를 재실행하고, 원본 실행과 masked 실행이 유사한 행동을 내면 공격으로 판정한다. false positive/false negative를 줄이기 위해 세 가지 설계를 덧붙였다. AgentDojo 벤치마크에서 MELON은 공격 차단과 utility 유지 모두에서 SOTA 방어를 능가했다. SOTA prompt augmentation과 결합한 MELON-Aug는 성능을 더 끌어올렸다. key design에 대한 ablation도 제공한다. 코드: https://github.com/kaijiezhu11/MELON.
