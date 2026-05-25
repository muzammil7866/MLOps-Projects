"""Reusable API client example for notebook-to-script conversion."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class ApiConfig:
    api_url: str
    api_key: str
    model: str
    prompt: str


def load_config() -> ApiConfig:
    return ApiConfig(
        api_url=os.getenv("API_URL", "").strip(),
        api_key=os.getenv("API_KEY", "").strip(),
        model=os.getenv("API_MODEL", "gpt-4o-mini").strip(),
        prompt=os.getenv("API_PROMPT", "What is AI?").strip(),
    )


def build_headers(api_key: str) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def build_payload(config: ApiConfig) -> dict[str, Any]:
    return {
        "model": config.model,
        "messages": [{"role": "user", "content": config.prompt}],
    }


def call_api(config: ApiConfig) -> dict[str, Any]:
    if not config.api_url:
        raise ValueError("Set API_URL before running the script.")

    response = requests.post(
        config.api_url,
        headers=build_headers(config.api_key),
        json=build_payload(config),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def extract_primary_result(payload: dict[str, Any]) -> Any:
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        return choices[0]
    return payload


def main() -> None:
    config = load_config()
    if not config.api_url:
        print("API_URL is missing. Set API_URL and API_KEY to run a live request.")
        print(build_payload(config))
        return

    payload = call_api(config)
    print(extract_primary_result(payload))


if __name__ == "__main__":
    main()