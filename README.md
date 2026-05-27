# ProjectX

ProjectX is a proactive AI system built around 5 core primitives: **Engine**, **Agents**, **Skills**, **Memory**, and **Learning**. Eight built-in agents ship in three execution modes — on-demand, scheduled, and continuous.

---

## The 5 Primitives

### 1. Engine — LLM Backend Abstraction

The Engine is the single interface through which every agent talks to a model. Backends are swappable without touching agent code.

**Supported backends**

| Type | Backends |
|------|----------|
| Local | Ollama, vLLM, SGLang, llama.cpp |
| Cloud | OpenAI, Anthropic, Google Gemini, OpenRouter, MiniMax |

**ProjectX starting point:** Anthropic behind an `Engine` class. One interface, swappable backends — `anthropic.client` is never called directly from agent code.

```
engine/
  base.py          # Engine abstract base class
  anthropic.py     # Anthropic implementation
```

---

### 2. Agents — Eight Built-in Agents, Three Execution Modes

Agents are the workers. Each agent has a role, a set of tools it can call, and an execution mode.

**Execution modes**

| Mode | Description |
|------|-------------|
| On-demand | Triggered by a user request, runs once, returns a result |
| Scheduled | Runs at a fixed interval (cron-style) |
| Continuous | Runs indefinitely, monitors state, acts proactively |

**Built-in agents**

| Agent | Role |
|-------|------|
| Chat | Single-turn baseline — question in, answer out |
| Researcher | Deep research with inline citations |
| Coder | CodeAct-style — writes, runs, and debugs code in a loop |
| Monitor | Continuous background agent with memory compression for long-horizon workflows |
| Planner | Breaks a goal into an ordered task graph |
| Critic | Evaluates another agent's output and returns structured feedback |
| Summarizer | Compresses long contexts into structured memory entries |
| Orchestrator | Routes subtasks to the right specialist agent |

**ProjectX starting point:** the **Monitor** agent. It's the proactive background one — the core of the system's vision. Build this first.

```
agents/
  base.py          # Agent abstract base class
  monitor.py       # Continuous monitor (start here)
  chat.py
  researcher.py
  coder.py
```

---

### 3. Skills — The Plugin/Tool System

Skills are the tools agents can call. Each skill is a self-contained folder: a `SKILL.md` spec (YAML frontmatter + description) and a Python implementation file. Adding a skill never touches core code.

**Trust tiers**

| Tier | Description |
|------|-------------|
| Bundled | Ships with ProjectX, fully audited |
| Indexed | Listed in the skill registry, reviewed |
| Unreviewed | Installed by the user, runs with a warning |
| Workspace | Local to the current project, highest trust |

**Key components**

- `SkillExecutor` — sequential pipeline execution
- Dependency graph with cycle detection
- File-based discovery — drop a folder in `skills/` and it's available

**ProjectX starting point:** `tools/registry.py` is the seed. The next step is evolving it toward the file-based skill format so the registry is auto-populated from the `skills/` directory.

```
skills/
  web_search/
    SKILL.md
    skill.py
  code_runner/
    SKILL.md
    skill.py
tools/
  registry.py      # Skill discovery and loading
  executor.py      # SkillExecutor
```

---

### 4. Memory — Conversation History and Semantic Search

Memory is what separates a stateless chatbot from a system that can operate over days and weeks.

**Layers**

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Conversation history | SQLite | Stores every message and agent trace |
| Semantic search | ChromaDB + embeddings | Retrieves relevant past context by meaning |
| Compressed memory | Summarizer agent | Long-horizon context without token overflow |

The continuous Monitor agent uses memory compression: when the context window fills, the Summarizer agent compresses old turns into a structured memory entry and clears the raw history. The summary re-enters context as a system message.

**ProjectX starting point:** SQLite for conversation history (already in scope). Add ChromaDB when retrieval gets painful — it's the lowest-friction path to semantic search.

```
memory/
  db.py            # SQLite conversation history
  store.py         # ChromaDB semantic store (add when needed)
  compression.py   # Memory compression via Summarizer agent
```

---

### 5. Learning — Trace Logging and Optimization

The learning loop is what turns a working system into an improving one. It's the hardest primitive — save it for last, but instrument for it from day one.

**Components**

| Component | Role |
|-----------|------|
| Trace logger | Records every agent run: input, plan, tools called, outcome |
| Pattern discovery | Finds recurring failure modes and successful strategies |
| DSPy/GEPA optimization | Rewrites prompts and tool calls based on trace patterns |
| SkillBenchmarkRunner | 4-condition evaluation across seeds and tasks |

**ProjectX starting point:** log every agent trace from day one. You won't use the optimization pipeline yet — but when you do, the data will be there. This is what separates a toy from a real system.

```
learning/
  tracer.py        # Trace logging (instrument from day one)
  patterns.py      # Pattern discovery (add later)
  optimizer.py     # DSPy/GEPA prompt optimization (add later)
  benchmark.py     # SkillBenchmarkRunner (add later)
```

---

## Build Order

The right order to build ProjectX, from foundation to frontier:

1. **Engine** — `Anthropic` behind `Engine` base class
2. **Monitor agent** — the continuous background worker
3. **Skills** — file-based registry, start with `web_search` and `code_runner`
4. **Memory** — SQLite first, ChromaDB when retrieval gets painful
5. **Learning** — trace logging on day one; optimization pipeline when you have enough traces

---

## Project Structure

```
projectx/
  engine/          # LLM backend abstraction
  agents/          # Eight built-in agents
  skills/          # File-based skill plugins
  tools/           # Skill registry and executor
  memory/          # SQLite + semantic store + compression
  learning/        # Trace logging and optimization pipeline
  main.py
```
