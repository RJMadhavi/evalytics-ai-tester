---
id: ADR-0001
title: Use Python with pytest-playwright for UI automation
status: Proposed
date: 2026-11-16
---

# ADR-0001: Use Python with pytest-playwright for UI automation

## Context

The first draft of the test plan proposed Playwright with TypeScript. The project also needs Python for AI evaluation scorers (G6) and for AI agents (G9), and an earlier Python test suite already exists on a parked branch.

## Decision

Write UI tests, API tests (httpx), AI evaluation and agent code in **Python**, using `pytest` and `pytest-playwright`. Put shared safety rules in `automation/common/` so UI tests, API tests and agents all use the same guardrails.

## Reasons

- One language across UI, API, AI evaluation and agents, which means one set of tools to learn and one set of guardrails.
- `pytest-playwright` gives browser fixtures, traces and screenshots on failure.
- The agent layer will likely call an LLM API from Python.
- Unit tests of the guardrails (goal G2) run without a browser.

## Consequences

- The test plan's tooling table should say Python and pytest-playwright instead of TypeScript.
- Accessibility checks will use `axe-playwright-python` or inject axe-core.
- Existing Python work on the parked branch can be reused rather than rewritten.

## Alternatives considered

- Playwright with TypeScript: strong tooling, but would add a second language.
- Selenium: slower and less convenient than Playwright for this work.
