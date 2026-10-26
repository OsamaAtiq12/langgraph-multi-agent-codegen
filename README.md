# LangGraph Multi-Agent Code Generation with Guardrails, HITL and MLflow

A multi-agent system that plans, writes, runs and grades code.

- Agent nodes: Director, Architect, Engineer, QA and Scorer wired as a LangGraph state graph
- PII redaction guardrail at the director (sample report in `pa5_guardrail_report.json`)
- Summarisation middleware, sandboxed code-interpreter tool, ReAct engineer and QA agents
- Groundedness scoring and one MLflow run per iteration (screenshots: `iteration-*.PNG`)
- Human-in-the-loop approval gates between phases, MemorySaver checkpoint-and-resume
- `generated_game_example.py` is an example of code produced by the agents

Files: `langgraph_multi_agent_codegen.ipynb` (core graph), `extension_agent_experiments.ipynb`, `guardrails_hitl_mlflow_agent.ipynb` (guardrails, HITL, MLflow).
Built on Databricks as part of the MLOps course in my MS in AI at LUMS.
