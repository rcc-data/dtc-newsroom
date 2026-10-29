# DTC Newsroom

A market-pulse dashboard for DTC performance marketers: Northbeam's weekly Media Buyer Index and benchmarks, Motion (Runneth) creative research, Meta's quarterly ad pricing, and a live BFCM desk. Haus and Triple Whale desks are scouted and next.

- `template.html` — page markup, styles and chart code (Chart.js 4.4.1)
- `data/` — every dataset as CSV; comment lines (`#`) describe the source
- `library.py` — source library: every post/report with stats, quotes and links
- `build.py` — embeds data + library into the template → `dtc-newsroom.html`
- `tests/shot.js` — Playwright render check across all views
- `UPDATING.md` — the weekly / daily / quarterly update procedure

Build: `python3 build.py`
