# chang2026ChatInject — Abstract

> 이 파일은 "급히 논문 검색 · 관련성만 판단" 용 short view.
> 수식·figure·본문 상세는 `summary.md`, 원본 전문은 `raw.md`.

## 메타데이터

- **제목**: ChatInject: Abusing Chat Templates for Prompt Injection in LLM Agents
- **저자**: Hwan Chang*, Yonghyun Jun*, Hwanhee Lee† (*Equal, †Corresponding; Chung-Ang University)
- **학회/저널**: ICLR 2026
- **연도**: 2026
- **arXiv/DOI**: arXiv:2509.22830v3
- **BibTeX key**: `chang2026chatinject`
- **폴더**: `2_chang2026ChatInject(ICLR2026)`

## 원문 (영어)

> The growing deployment of large language model (LLM) based agents that interact with external environments has created new attack surfaces for adversarial manipulation. One major threat is indirect prompt injection, where attackers embed malicious instructions in external environment output, causing agents to interpret and execute them as if they were legitimate prompts. While previous research has focused primarily on plain-text injection attacks, we find a significant yet underexplored vulnerability: LLMs' dependence on structured chat templates and their susceptibility to contextual manipulation through persuasive multi-turn dialogues. To this end, we introduce ChatInject, an attack that formats malicious payloads to mimic native chat templates, thereby exploiting the model's inherent instruction-following tendencies. Building on this foundation, we develop a template-based Multi-turn variant that primes the agent across conversational turns to accept and execute otherwise suspicious actions. Through comprehensive experiments across frontier LLMs, we demonstrate three critical findings: (1) ChatInject achieves significantly higher average attack success rates than traditional prompt injection methods, improving from 5.18% to 32.05% on AgentDojo and from 15.13% to 45.90% on InjecAgent, with multi-turn dialogues showing particularly strong performance at average 52.33% success rate on InjecAgent, (2) chat-template-based payloads demonstrate strong transferability across models and remain effective even against closed-source LLMs, despite their unknown template structures, and (3) existing prompt-based defenses are largely ineffective against this attack approach, especially against Multi-turn variants. These findings highlight vulnerabilities in current agent systems. The code is available at https://hwanchang00.github.io/chatinject_project_page.

## 한글 번역

> 외부 환경과 상호작용하는 LLM 기반 에이전트가 확산되면서 새로운 공격 표면이 열렸다. 대표적 위협이 indirect prompt injection으로, 공격자가 외부 환경 출력에 악성 지시를 심어 에이전트가 이를 정상 프롬프트처럼 해석·실행하게 만드는 공격이다. 기존 연구는 대부분 plain-text 주입에 집중했으나, 본 논문은 중요하지만 충분히 탐구되지 않은 취약점을 발견했다. LLM이 구조화된 chat template에 의존한다는 점과 설득력 있는 multi-turn 대화를 통한 문맥 조작에 취약하다는 점이다. 이를 이용해, 악성 payload를 대상 모델의 native chat template처럼 포맷하는 공격 ChatInject를 제안한다. 여기에 template 기반 Multi-turn 변형을 덧붙여, 의심스러운 행동도 여러 턴에 걸쳐 수용·실행하도록 agent를 길들인다. frontier LLM들에서 대규모 실험을 수행해 세 가지 결과를 얻었다. (1) ChatInject는 기존 prompt injection 대비 평균 ASR을 크게 올린다 — AgentDojo에서 5.18% → 32.05%, InjecAgent에서 15.13% → 45.90%, Multi-turn은 InjecAgent에서 평균 52.33%에 달한다. (2) chat-template 기반 payload는 모델 간 강한 전이성을 보이며, template 구조가 알려지지 않은 closed-source LLM에도 여전히 유효하다. (3) 기존 prompt 기반 방어는 특히 Multi-turn 변형에 대해 거의 무력하다. 이는 현재 에이전트 시스템의 취약성을 드러낸다. 코드: https://hwanchang00.github.io/chatinject_project_page.
