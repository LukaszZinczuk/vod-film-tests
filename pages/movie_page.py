from .base_page import BasePage
from playwright.sync_api import Page
import time


class MoviePage(BasePage):
    """Strona szczegółów filmu"""
    
    # Selektory elementów
    MOVIE_TITLE_H1 = "h1"
    VIDEO_PLAYER = "video, iframe, .video-player, [class*='player']"
    PLAY_BUTTON = "button[aria-label*='play'], .play-button, button:has-text('Play'), [class*='play-btn']"
    POPUP_MODAL = ".modal, .popup, [role='dialog'], .overlay"
    POPUP_LINK = ".modal a, .popup a, [role='dialog'] a"
    CLOSE_BUTTON = "button[aria-label*='close'], .close, .modal-close"
    
    def __init__(self, page: Page):
        super().__init__(page)
        
    def get_movie_title(self) -> str:
        """Pobiera tytuł filmu z H1"""
        if self.is_element_visible(self.MOVIE_TITLE_H1):
            return self.get_text(self.MOVIE_TITLE_H1)
        return ""
        
    def is_video_player_visible(self) -> bool:
        """Sprawdza czy odtwarzacz wideo jest widoczny"""
        player_selectors = [
            "video",
            "iframe[src*='player']", 
            ".video-player",
            "[class*='player']",
            "[id*='player']",
            "iframe[src*='youtube']",
            "iframe[src*='vimeo']",
            ".embed-container"
        ]
        
        for selector in player_selectors:
            if self.is_element_visible(selector):
                return True
        return False
        
    def play_video(self) -> None:
        """Uruchamia odtwarzanie wideo"""
        play_selectors = [
            "button[aria-label*='play']",
            "button[title*='play']", 
            ".play-button",
            "button:has-text('Play')",
            "[class*='play-btn']",
            ".vjs-play-control",  # Video.js
            "button[data-testid='play-button']"
        ]
        
        for selector in play_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                return
                
        # Jeśli nie ma przycisku play, spróbuj kliknąć w sam player
        player_selectors = ["video", ".video-player", "[class*='player']"]
        for selector in player_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                return
                
    def wait_for_popup(self, timeout: int = 60) -> bool:
        """Czeka na pojawienie się popupa (1-60 sekund)"""
        popup_selectors = [
            ".modal",
            ".popup", 
            "[role='dialog']",
            ".overlay",
            ".ad-overlay",
            ".advertisement",
            "[class*='modal']",
            "[class*='popup']",
            "[id*='modal']",
            "[id*='popup']"
        ]
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            for selector in popup_selectors:
                if self.is_element_visible(selector):
                    return True
            time.sleep(1)
            
        return False
        
    def get_popup_redirect_url(self) -> str:
        """Pobiera URL przekierowania z popupa"""
        if not self.is_popup_visible():
            return ""
            
        link_selectors = [
            ".modal a",
            ".popup a",
            "[role='dialog'] a",
            ".overlay a",
            ".ad-overlay a", 
            ".advertisement a",
            "[class*='modal'] a",
            "[class*='popup'] a"
        ]
        
        for selector in link_selectors:
            if self.is_element_visible(selector):
                href = self.get_attribute(selector, 'href')
                if href:
                    return href
                    
        return ""
        
    def is_popup_visible(self) -> bool:
        """Sprawdza czy popup jest widoczny"""
        popup_selectors = [
            ".modal",
            ".popup",
            "[role='dialog']", 
            ".overlay",
            ".ad-overlay",
            "[class*='modal']",
            "[class*='popup']"
        ]
        
        for selector in popup_selectors:
            if self.is_element_visible(selector):
                return True
        return False
        
    def click_popup_link(self) -> str:
        """Klika w link w popupie i zwraca URL docelowy"""
        url_before = self.get_current_url()
        
        link_selectors = [
            ".modal a",
            ".popup a", 
            "[role='dialog'] a",
            ".overlay a",
            ".ad-overlay a"
        ]
        
        for selector in link_selectors:
            if self.is_element_visible(selector):
                # Pobierz href przed kliknięciem
                href = self.get_attribute(selector, 'href')
                self.click_element(selector)
                
                # Poczekaj na ewentualną zmianę URL
                time.sleep(2)
                url_after = self.get_current_url()
                
                # Zwróć href lub nowy URL
                return href or url_after
                
        return ""
        
    def close_popup(self) -> None:
        """Zamyka popup"""
        close_selectors = [
            "button[aria-label*='close']",
            ".close",
            ".modal-close",
            ".popup-close",
            "[data-dismiss='modal']"
        ]
        
        for selector in close_selectors:
            if self.is_element_visible(selector):
                self.click_element(selector)
                return