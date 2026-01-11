# Personal Notes from My Own Learning Experience

- Important to remember the "lost in the middle" effect. 
  - When designing a prompt, keep the critical information in the beginning and the end. 

## Principles 

- [如何做 AI Agent 喜欢的基础软件](https://mp.weixin.qq.com/s/BZcRwgGZNinBK9K2L38LYg)
  - "心智模型": 好的心智模型的特征是它一定是可扩展的
  - 接口设计：可以被自然语言描述；可以被符号逻辑固化；并且能够交付确定性的结果。
    - 2025年底最好的逻辑符号描述，就是代码，即使对于非编程Agent 来说也是。

## Tools 

- [The complete Claude code tutorial](https://x.com/eyad_khrais/status/2010076957938188661?s=20)
  - Build a system where Claude Code is a component.
    - "Think about where in your workflow Claude could run without you watching."
  - Plan first: "Architecture, especially in software engineering, is a little bit like giving a person the output and nothing more."
  - CLAUDE.md: keep it short; specific to your project; update it constantly.
    - Explain "Why": provide the context, the motivation of a certain choice.
    - Anything that needs to be explained or corrected twice should go into CLAUDE.md.
    - "Good CLAUDE.md looks like notes you'd leave yourself if you knew you'd have amnesia tomorrow."
  - Context Window:
    - At around 20-40% context usage, the quality of the output starts to chip away.
    - Scope your conversations: one conversation per feature or task.
    - Use external memory: write plans and progress to actual files.
    - "Copy-paste reset":
      - Copy everything important from the terminal.
      - Run `/compact` to get a summary.
      - Run `/clear` the context entirely.
      - Paste back in only what matters.
  - Prompts are everything:
    - "Like any communication, being clear gets you better results than being vague."
    - Be specific about what you want.
    - Tell it what NOT to do.
      - Claude Opus 4.5 likes to overengineer: "Keep this simple. Don't add abstractions I didn't ask for. One file if possible."
    - Give it context about why.
    - Example is better than description.
  - A workflow that works:
    - Use Opus to plan and make architectural decisions, then switch to Sonnet (Shift+Tab in Claude Code) for implementation.
  - Tools and configurations:
    - MCP:
      - "If you find yourself constantly copying information from one place into Claude, there's probably an MCP server that can do it automatically."
    - Hook:
      - "Hooks let you run code automatically before or after Claude makes changes."
    - Slash Commands:
      - "Custom slash commands are just prompts you use repeatedly, packaged as commands."     
  - When Claude Gets Stuck:
    - Clear the conversation; Simplify the task, break it into smaller pieces.
    - "Show instead of tell."
    - Be creative, try a different angle, reframing.
  

## Skills

- Planning with Files
  - 3-File pattern: `task_plan` after each phase; `notes` during research; `deliverable` at completion.
  - `plan` structure: goal, phases, key questions, decision made, error encountered, and status.
  - `notes` structure: itemized sources and findings. 
  - Critical rules: 
    - 1. Always create a plan first
    - 2. Read before decide
    - 3. Update after the act
    - 4. Store, don't stuff: large output goes to files, not context
    - 5. Log ALL errors
