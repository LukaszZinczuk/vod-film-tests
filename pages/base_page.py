from playwright.sync_api import Page, expect
from typing import Optional
import time


class BasePage:
    """Bazowa klasa dla wszystkich stron - zawiera wspólne metody"""
    
    def __init__(self, page: Page):
        self.page = page
        
    def navigate_to(self, url: str) -> None:
        """Nawiguje do podanego URL"""
        self.page.goto(url)
        
    def wait_for_element(self, selector: str, timeout: int = 10000) -> None:
        """Czeka na pojawienie się elementu"""
        self.page.wait_for_selector(selector, timeout=timeout)
        
    def click_element(self, selector: str) -> None:
        """Klika w element"""
        self.page.click(selector)
        
    def type_text(self, selector: str, text: str) -> None:
        """Wpisuje tekst w pole"""
        self.page.fill(selector, text)
        
    def get_text(self, selector: str) -> str:
        """Pobiera tekst z elementu"""
        return self.page.text_content(selector) or ""
        
    def is_element_visible(self, selector: str) -> bool:
        """Sprawdza czy element jest widoczny"""
        try:
            return self.page.is_visible(selector)
        except:
            return False
            
    def get_current_url(self) -> str:
        """Zwraca aktualny URL"""
        return self.page.url
        
    def wait_for_url_change(self, timeout: int = 10000) -> str:
        """Czeka na zmianę URL i zwraca nowy URL"""
        current_url = self.get_current_url()
        start_time = time.time()
        
        while time.time() - start_time < timeout/1000:
            new_url = self.get_current_url()
            if new_url != current_url:
                return new_url
            time.sleep(0.1)
            
        return self.get_current_url()
        
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Pobiera wartość atrybutu elementu"""
        return self.page.get_attribute(selector, attribute)