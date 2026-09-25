#!/usr/bin/env python3
"""Fetch the provider's available model list for the agent to tier itself.

Runs at session start from the plugin's SessionStart hook. Prints the raw
model ids; the agent maps them onto the orchestration tiers from its own
knowledge of the model families (no name-regex heuristics live here).
A session hook never crashes: every error path exits 0 with an empty list.

Sources, first configured wins:
  ORCHESTRATION_MODELS_FIXTURE_FILE  JSON fixture {"data": [{"id": ...}]} (tests)
  ANTHROPIC_API_KEY                  GET api.anthropic.com/v1/models
  OPENAI_API_KEY                     GET api.openai.com/v1/models
  opencode registry                  `opencode models` output lines provider/model
Results cache at ~/.cache/orchestration/models.txt (24h TTL).
Subscription-auth Claude Code carries no API key: expect an empty list there.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

CACHE = Path.home() / ".cache" / "orchestration" / "models.txt"
TTL = 24 * 3600


def anthropic_models():
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/models",
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return [m["id"] for m in json.load(r)["data"]]


def openai_models():
    req = urllib.request.Request(
        "https://api.openai.com/v1/models",
        headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return [m["id"] for m in json.load(r)["data"]]


def opencode_models():
    out = subprocess.run(["opencode", "models"], capture_output=True, text=True, timeout=10)
    return [line.split()[0] for line in out.stdout.splitlines() if "/" in line]


def discover():
    fixture = os.environ.get("ORCHESTRATION_MODELS_FIXTURE_FILE")
    if fixture:
        return [m["id"] for m in json.loads(Path(fixture).read_text())["data"]]
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return anthropic_models()
        except Exception as e:
            print(f"models: anthropic query failed: {e}", file=sys.stderr)
    if os.environ.get("OPENAI_API_KEY"):
        try:
            return openai_models()
        except Exception as e:
            print(f"models: openai query failed: {e}", file=sys.stderr)
    try:
        models = opencode_models()
        if models:
            return models
    except Exception:
        pass
    return []


def render(models):
    lines = ["Provider models discovered at session start "
             "(map tiers yourself; empty = harness defaults):"]
    lines += models or ["(none discovered)"]
    return "\n".join(lines)


def main():
    if "--selftest" in sys.argv:
        import tempfile
        cases = [  # (fixture payload, must appear in output)
            ('{"data": [{"id": "anthropic/claude-haiku-4-5"}, {"id": "openai/gpt-5"}]}',
             "anthropic/claude-haiku-4-5"),
            ('{"data": []}', "(none discovered)"),
            ("not json", "(none discovered)"),
        ]
        for payload, want in cases:
            f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
            f.write(payload)
            f.close()
            os.environ["ORCHESTRATION_MODELS_FIXTURE_FILE"] = f.name
            try:
                models = discover()
            except Exception:
                models = []
            out = render(models)
            assert want in out, (payload, out)
        print("models selftest: 3/3 PASS")
        return 0
    if CACHE.exists() and time.time() - CACHE.stat().st_mtime < TTL:
        print(CACHE.read_text())
        return 0
    try:
        models = discover()
    except Exception as e:
        print(f"models: discover failed: {e}", file=sys.stderr)
        models = []
    out = render(models)
    if models:  # cache only real discoveries, never failures
        try:
            CACHE.parent.mkdir(parents=True, exist_ok=True)
            CACHE.write_text(out + "\n")
        except OSError:
            pass
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
