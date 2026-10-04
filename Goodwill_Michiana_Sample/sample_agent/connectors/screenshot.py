"""Reusable screenshot helpers."""

from __future__ import annotations

from typing import Any


async def capture_page_screenshot(
    url: str,
    headers: dict[str, str] | None = None,
    viewport: dict[str, int] | None = None,
    wait_until: str = "networkidle",
) -> bytes:
    """Capture a full-page screenshot with Playwright Chromium."""
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(
            extra_http_headers=headers or {},
            viewport=viewport or {"width": 1440, "height": 1000},
        )
        page = await context.new_page()
        await page.goto(url, wait_until=wait_until, timeout=60_000)
        image = await page.screenshot(full_page=True, type="png")
        await browser.close()
        return image


def placeholder_png_bytes() -> bytes:
    """Return a tiny PNG used when no screenshot provider is configured."""
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
        b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff"
        b"\xff?\x00\x05\xfe\x02\xfeA\xe2q\xb5\x00\x00\x00\x00IEND\xaeB`\x82"
    )


def normalize_filter_params(filters: dict[str, str] | None) -> dict[str, Any]:
    """Convert display filters into generic URL query params."""
    return {f"filter_{key}": value for key, value in (filters or {}).items()}

