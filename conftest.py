import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Generator


@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    """Fixture dla przeglądarki - jedna instancja na sesję testową"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Ustaw na True dla CI/CD
            slow_mo=1000     # Spowolnienie dla lepszej obserwacji
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Fixture dla kontekstu przeglądarki - nowy na każdy test"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    )
    yield context
    context.close()


@pytest.fixture(scope="function") 
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Fixture dla strony - nowa na każdy test"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def base_url() -> str:
    """URL strony do testowania"""
    return "https://vod.film"