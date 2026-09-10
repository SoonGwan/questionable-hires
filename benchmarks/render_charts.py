#!/usr/bin/env python3
"""Render local SVGs with optional Playwright Chromium for visual inspection."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chromium", args=["--disable-gpu"])
        page = browser.new_page(viewport={'width': 1200, 'height': 760}, device_scale_factor=1)
        page.route('http://**/*', lambda route: route.abort())
        page.route('https://**/*', lambda route: route.abort())
        for svg in args.files:
            page.set_content('<html><body style="margin:0">' + svg.read_text() + '</body></html>')
            page.screenshot(path=str(args.output / (svg.stem + '.png')), animations="disabled", timeout=15000)
        browser.close()


if __name__ == '__main__':
    main()
