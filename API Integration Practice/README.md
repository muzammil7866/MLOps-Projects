
# API Integration Practice

## Overview

This project shows a clean API-integration pattern using `requests`. It builds a JSON payload, sends it to a configurable endpoint, and extracts the primary response item.

## Business Goal

The purpose is to demonstrate reliable third-party API integration, which is useful for product prototypes, service orchestration, and AI-enabled applications that depend on external endpoints.

## Structure

- `api_client.py` - request builder, API caller, and response parser
- `requirements.txt` - minimal runtime dependency list

## Setup

Set these environment variables before running:

- `API_URL`
- `API_KEY`
- `API_MODEL`
- `API_PROMPT`

## Run

```bash
python api_client.py
```

## Notes

If `API_URL` is missing, the script prints the payload instead of making a request. That makes it safe to inspect before connecting to a live service.
