#!/usr/bin/env python3
"""Print the fields, buttons and links of a public page. Read-only: it never types or clicks.

Run from the automation/ folder:
    python3 ui/tools/dump_form.py /create-academy
Then paste the output into the chat so the page object can use the real labels and ids.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))

from playwright.sync_api import sync_playwright  # noqa: E402

from common.guardrails import parse_hosts, require_host_allowed  # noqa: E402

JS = """
() => [...document.querySelectorAll('input, select, textarea, button, a[href]')].map(el => {
  const id = el.id || '';
  let label = '';
  if (id) { const l = document.querySelector('label[for="' + CSS.escape(id) + '"]'); if (l) label = l.innerText.trim(); }
  if (!label) { const w = el.closest('label'); if (w) label = w.innerText.trim(); }
  const tag = el.tagName.toLowerCase();
  return {
    tag, type: el.getAttribute('type') || '', id, name: el.getAttribute('name') || '',
    label: label.slice(0, 60), placeholder: el.getAttribute('placeholder') || '',
    aria: el.getAttribute('aria-label') || '', required: !!el.required,
    maxlength: el.getAttribute('maxlength') || '', pattern: el.getAttribute('pattern') || '',
    text: (tag === 'button' || tag === 'a') ? el.innerText.trim().slice(0, 40) : '',
    href: el.getAttribute('href') || ''
  };
})
"""


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "/create-academy"
    base = os.environ.get("EVA_BASE_URL", "https://evalytics.in")
    url = base.rstrip("/") + path
    require_host_allowed(url, parse_hosts(os.environ.get("EVA_ALLOWED_HOSTS")))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        print(f"URL: {page.url}\nTitle: {page.title()}\n")
        for item in page.evaluate(JS):
            shown = {k: v for k, v in item.items() if v not in ("", False)}
            print(shown)
        browser.close()


if __name__ == "__main__":
    main()
