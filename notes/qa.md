# Questions and Answers 

- These are the questions about agentic coding I asked LLM models.

----

Q: "For my project, I need to repeatedly generate some QA figures with a specific format. For these figures and all figures, I have specific requirements for their format and style. I want to remind the agent to remember these and follow my instructions every time. What's the best way to achieve this? For example, for using CLAUDE Code, should I put them in CLAUDE.md? Or develop a subagent just for making these QA figures? Or should I develop a SKILL.md file to record all my rules for making QA figures? 

A from GPT 5.2 (summary): 

- Rules need to be (a) discoverable, (b) executable, and (c) testable.
	- The agent then only has one correct path: use the standardized code and pass the checks.
- The core principle: “policy in docs, enforcement in code.”
    - Create `docs/qa/QA_FIGURE_SPEC.md` Expliciti and searchable name.
    	- Agents handle “a small authoritative spec + pointers” better than large scattered rules, especially under context-window pressure.
    - Create `isoster/qa/figstyle.py` and/or `isoster/qa/qa_figures.py`.
        - The agent can’t “forget” the style if the code applies it.
	- Add automated checks so violations are caught immediately.

 - Where to put the Agent Reminder:
 	- Use CLAUDE.md (or equivalent) as the entry point and pointer: right place for "project operating rules.
    	- "Where the specs live", "what files to read", "what API to use", "what tests must pass".
    - Use SKILL.md only if you actually have a “skills framework” you are consistently using.
    	- SKILL fails for one mundane reason: agents and humans won’t know it exists unless the entry point points to it.
    - Build a subagent only if the figure task is large, diverse, and ongoing.
    	- A dedicated “QA Figure Agent” (subagent) makes sense when 1. you are generating many figure variants, 2. the logic is nontrivial (many conditionals, instrument modes, survey versions), 3. you want a “specialist workflow” (validate inputs → render → annotate → export → register artifacts), 4. ou foresee iterative prompting cycles specifically for figure QA.
     	- A subagent improves task focus, not policy adherence; adherence is better achieved by code + tests + a clear entrypoint. 	      	
