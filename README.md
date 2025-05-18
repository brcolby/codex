# Research Tracking Agent

This project provides a simple autonomous agent that tracks research papers from arXiv based on user defined topics. The agent stores results in JSON files under `data/` and can be run on a schedule using external tools like `cron`.

## Features

- Manage topics with natural language queries
- Query arXiv for recent papers
- Store paper metadata and summaries generated with the Mistral API
- Interactive browsing and PDF download
- Command line interface

## Setup

Run the setup script to install dependencies and initialize submodules:

```bash
./setup_macos.sh
```

Optionally, run `./setup_mistral.sh` to store your API key in a `.env` file.
The agent automatically loads variables from `.env` if present, so after
running the setup script you can simply keep the file in the project
directory. Alternatively you can set the `MISTRAL_API_KEY` environment
variable manually. Optional variables `MISTRAL_MODEL` and
`MISTRAL_RATE_LIMIT` can be used to configure the model name and rate limit.


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
