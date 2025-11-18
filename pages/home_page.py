from .base_page import BasePage
from playwright.sync_api import Page
import time


class HomePage(BasePage):
    """Strona główna VOD.Film"""
    
    # Selektory elementów
    SEARCH_ICON = "button[title='Szukaj']"
    SEARCH_INPUT = "input[placeholder*='Szukaj']"
    SEARCH_BUTTON = "button[type='submit']"
    SEARCH_RESULTS = ".search-results"
    MOVIE_LINK = "a[href*='/film/']"
    LOGO = ".logo"
    MENU_FILMY = "a[href='/filmy']"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.base_url = "https://vod.film"
        
    def open_homepage(self) -> None:
        """Otwiera stronę główną"""
        self.navigate_to(self.base_url)
        
    def click_search_icon(self) -> None:
        """Klika w ikonę wyszukiwania (lupkę)"""
        # Próba różnych selektorów dla ikony wyszukiwania
        possible_selectors = [
            "button[title='Szukaj']",
            ".search-icon",
            "[data-testid='search-button']",
            "button[aria-label*='search']",
            "button[aria-label*='szukaj']",
            ".fa-search",
            "[class*='search-btn']",
            "button:has(.fa-search)",
            "a[href*='search']"
        ]
        
        for selector in possible_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                return
                
        # Jeśli nie znajdzie ikony, spróbuje bezpośrednio pola wyszukiwania
        self.click_search_input()
        
    def click_search_input(self) -> None:
        """Klika w pole wyszukiwania"""
        possible_selectors = [
            "input[placeholder*='Szukaj']",
            "input[placeholder*='szukaj']",
            "input[name='search']",
            "input[type='search']",
            ".search-input",
            "#search",
            "[data-testid='search-input']"
        ]
        
        for selector in possible_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                return
                
    def search_for_movie(self, query: str) -> None:
        """Wyszukuje film po frazie"""
        # Znajdź pole wyszukiwania
        search_selectors = [
            "input[placeholder*='Szukaj']",
            "input[placeholder*='szukaj']", 
            "input[name='search']",
            "input[type='search']",
            ".search-input",
            "#search",
            "[data-testid='search-input']",
            "input"  # ostateczność
        ]
        
        for selector in search_selectors:
            if self.is_element_visible(selector):
                self.type_text(selector, query)
                break
                
        # Poczekaj chwilę na live search
        time.sleep(1)
        
        # Spróbuj różnych sposobów zatwierdzenia wyszukiwania
        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Szukaj')",
            ".search-button",
            "[data-testid='search-submit']"
        ]
        
        for selector in submit_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                return
                
        # Jeśli nie ma przycisku, naciśnij Enter
        for selector in search_selectors:
            if self.is_element_visible(selector):
                self.page.keyboard.press("Enter")
                return
                
    def get_search_results(self) -> list:
        """Pobiera wyniki wyszukiwania"""
        # Czekaj na wyniki
        time.sleep(2)
        
        result_selectors = [
            ".search-results a",
            ".movie-item a",
            "[data-testid='movie-link']",
            "a[href*='/film/']",
            ".film-link",
            ".movie-link"
        ]
        
        for selector in result_selectors:
            elements = self.page.query_selector_all(selector)
            if elements:
                return [elem.get_attribute('href') for elem in elements]
                
        return []
        
    def click_first_movie_result(self) -> str:
        """Klika w pierwszy wynik wyszukiwania i zwraca URL"""
        movie_selectors = [
            ".search-results a:first-child",
            ".movie-item:first-child a",
            "a[href*='/film/']:first-child",
            ".film-link:first-child"
        ]
        
        for selector in movie_selectors:
            if self.is_element_visible(selector):
                href = self.get_attribute(selector, 'href')
                self.click_element(selector)
                return href or ""
                
        return ""
        
    def go_to_movies_page(self) -> None:
        """Przechodzi do strony Filmy"""
        if self.is_element_visible(self.MENU_FILMY):
            self.click_element(self.MENU_FILMY)
        else:
            self.navigate_to(f"{self.base_url}/filmy")