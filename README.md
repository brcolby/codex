# Research Tracking Agent

This project provides a simple autonomous agent that tracks research papers from arXiv based on user defined topics. The agent stores results in JSON files under `data/` and can be run on a schedule using external tools like `cron`.

## Features

- Manage topics with natural language queries
- Query arXiv for recent papers
- Store paper metadata and summaries generated with ChatGPT
- Interactive browsing and PDF download
- Command line interface

## Usage

Add a topic:

```bash
python -m research_agent.main add "FPGA Neuromorphic" "neuromorphic computing FPGA"
```

List topics:

```bash
python -m research_agent.main list
```

Run the agent once (for example weekly via cron):

```bash
python -m research_agent.main run
```

Results are stored in `data/<topic>.json`.

Browse and download papers interactively:

```bash
python -m research_agent.main browse
```
