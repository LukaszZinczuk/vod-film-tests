import pytest
import time
from playwright.sync_api import Page
from pages import HomePage, MoviePage


class TestE2ESearch:
    """Testy End-to-End wyszukiwarki filmów"""
    
    @pytest.mark.e2e
    @pytest.mark.parametrize("search_term,expected_result", [
        ("the pickup", "positive"),
        ("abcxyz123", "negative")
    ])
    def test_movie_search_and_playback(self, page: Page, base_url: str, search_term: str, expected_result: str):
        """
        Test wyszukiwania i odtwarzania filmu
        
        Workflow:
        1. Wejście na stronę główną
        2. Kliknięcie w ikonę lupki 
        3. Wyszukanie frazy
        4. Sprawdzenie wyników
        5. Wejście na stronę filmu (tylko pozytywny przypadek)
        6. Weryfikacja H1, odtwarzacza i popupa
        """
        home_page = HomePage(page)
        movie_page = MoviePage(page)
        
        # Krok 1: Wejście na stronę główną
        home_page.open_homepage()
        
        # Krok 2: Kliknięcie w ikonę lupki
        home_page.click_search_icon()
        
        # Krok 3: Wyszukanie frazy
        home_page.search_for_movie(search_term)
        
        # Krok 4: Sprawdzenie wyników
        search_results = home_page.get_search_results()
        
        if expected_result == "positive":
            # Przypadek pozytywny - oczekujemy wyników
            assert len(search_results) > 0, f"Brak wyników wyszukiwania dla '{search_term}'"
            
            # Krok 5: Wejście na stronę szczegółów filmu
            movie_url = home_page.click_first_movie_result()
            assert movie_url, "Nie znaleziono linku do filmu"
            
            # Poczekaj na załadowanie strony filmu
            time.sleep(2)
            
            # Krok 6: Sprawdzenie nagłówka H1
            movie_title = movie_page.get_movie_title()
            assert movie_title, "Brak tytułu filmu (H1)"
            assert search_term.lower() in movie_title.lower(), f"Tytuł '{movie_title}' nie zawiera frazy '{search_term}'"
            
            # Krok 7: Sprawdzenie odtwarzacza wideo
            assert movie_page.is_video_player_visible(), "Odtwarzacz wideo nie jest widoczny"
            
            # Krok 8: Uruchomienie odtwarzania
            movie_page.play_video()
            
            # Krok 9: Weryfikacja popupa (1-60 sekund)
            popup_appeared = movie_page.wait_for_popup(timeout=60)
            assert popup_appeared, "Popup nie pojawił się w ciągu 60 sekund"
            
            # Krok 10: Sprawdzenie URL przekierowania z popupa
            redirect_url = movie_page.get_popup_redirect_url()
            assert redirect_url, "Nie znaleziono URL przekierowania w popupie"
            
            print(f"URL przekierowania z popupa: {redirect_url}")
            
        else:
            # Przypadek negatywny - brak wyników
            assert len(search_results) == 0, f"Znaleziono nieoczekiwane wyniki dla '{search_term}'"
            
    @pytest.mark.e2e
    def test_search_positive_the_pickup(self, page: Page, base_url: str):
        """Test pozytywny wyszukiwania 'the pickup'"""
        self.test_movie_search_and_playback(page, base_url, "the pickup", "positive")
        
    @pytest.mark.e2e  
    def test_search_negative_nonexistent(self, page: Page, base_url: str):
        """Test negatywny wyszukiwania nieistniejącego filmu"""
        self.test_movie_search_and_playback(page, base_url, "abcxyz123", "negative")