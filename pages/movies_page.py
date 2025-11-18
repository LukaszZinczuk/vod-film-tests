from .base_page import BasePage
from playwright.sync_api import Page


class MoviesPage(BasePage):
    """Strona z listą filmów"""
    
    # Selektory elementów
    SORT_DROPDOWN = "select[name*='sort'], .sort-select, [class*='sort-dropdown']"
    CLEAR_BUTTON = "button:has-text('Wyczyść'), .clear-button, [data-action='clear']"
    MOVIE_ITEMS = ".movie-item, .film-card, [class*='movie-card']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.movies_url = "https://vod.film/filmy"
        
    def open_movies_page(self) -> None:
        """Otwiera stronę filmów"""
        self.navigate_to(self.movies_url)
        
    def is_sort_dropdown_visible(self) -> bool:
        """Sprawdza czy lista rozwijana sortowania jest widoczna"""
        sort_selectors = [
            "select[name*='sort']",
            ".sort-select",
            "[class*='sort-dropdown']",
            "select:has-text('Sortuj')",
            "[id*='sort']"
        ]
        
        for selector in sort_selectors:
            if self.is_element_visible(selector):
                return True
        return False
        
    def select_sort_option(self, option_text: str) -> None:
        """Wybiera opcję sortowania"""
        sort_selectors = [
            "select[name*='sort']", 
            ".sort-select",
            "[class*='sort-dropdown']"
        ]
        
        for selector in sort_selectors:
            if self.is_element_visible(selector):
                self.page.select_option(selector, label=option_text)
                return
                
    def click_clear_button(self) -> None:
        """Klika przycisk Wyczyść"""
        clear_selectors = [
            "button:has-text('Wyczyść')",
            ".clear-button",
            "[data-action='clear']",
            "button[title*='wyczyść']",
            "button[aria-label*='clear']",
            ".reset-button"
        ]
        
        for selector in clear_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                return
                
    def is_clear_button_visible(self) -> bool:
        """Sprawdza czy przycisk Wyczyść jest widoczny"""
        clear_selectors = [
            "button:has-text('Wyczyść')",
            ".clear-button", 
            "[data-action='clear']",
            "button[title*='wyczyść']"
        ]
        
        for selector in clear_selectors:
            if self.is_element_visible(selector):
                return True
        return False
        
    def get_current_sort_value(self) -> str:
        """Pobiera aktualną wartość sortowania"""
        sort_selectors = [
            "select[name*='sort']",
            ".sort-select", 
            "[class*='sort-dropdown']"
        ]
        
        for selector in sort_selectors:
            if self.is_element_visible(selector):
                element = self.page.query_selector(selector)
                if element:
                    return element.input_value() or ""
        return ""
        
    def get_movies_count(self) -> int:
        """Zwraca liczbę filmów na stronie"""
        movie_selectors = [
            ".movie-item",
            ".film-card", 
            "[class*='movie-card']",
            ".movie"
        ]
        
        for selector in movie_selectors:
            elements = self.page.query_selector_all(selector)
            if elements:
                return len(elements)
        return 0