import pytest
from playwright.sync_api import Page
from pages import MoviesPage


class TestManualBugVerification:
    """Testy weryfikujące błędy znalezione podczas analizy manualnej"""
    
    @pytest.mark.regression
    def test_clear_button_bug_verification(self, page: Page):
        """
        Test weryfikujący błąd przycisku 'Wyczyść' na stronie Filmy
        
        Ten test dokumentuje istniejący błąd i służy jako test regresyjny
        po jego naprawie.
        """
        movies_page = MoviesPage(page)
        
        # Krok 1: Wejdź na stronę filmów
        movies_page.open_movies_page()
        
        # Krok 2: Sprawdź czy elementy sortowania są dostępne
        assert movies_page.is_sort_dropdown_visible(), "Lista rozwijana sortowania nie jest widoczna"
        assert movies_page.is_clear_button_visible(), "Przycisk 'Wyczyść' nie jest widoczny"
        
        # Krok 3: Zapisz aktualny stan sortowania
        initial_sort_value = movies_page.get_current_sort_value()
        
        # Krok 4: Zmień sortowanie na inne niż domyślne
        movies_page.select_sort_option("Data dodania")  # lub inna dostępna opcja
        
        # Poczekaj na przeładowanie
        page.wait_for_timeout(2000)
        
        # Krok 5: Sprawdź czy sortowanie się zmieniło
        new_sort_value = movies_page.get_current_sort_value()
        assert new_sort_value != initial_sort_value, "Sortowanie nie zmieniło się po wybraniu opcji"
        
        # Krok 6: Kliknij przycisk 'Wyczyść' 
        movies_page.click_clear_button()
        
        # Poczekaj na ewentualną reakcję
        page.wait_for_timeout(2000)
        
        # Krok 7: Sprawdź czy sortowanie zostało zresetowane
        final_sort_value = movies_page.get_current_sort_value()
        
        # UWAGA: Ten test POWINIEN OBECNIE FAILOWAĆ z powodu błędu
        # Po naprawie błędu, ten assert powinien przechodzić
        try:
            assert final_sort_value == initial_sort_value, \
                f"BŁĄD POTWIERDZONY: Przycisk 'Wyczyść' nie resetuje sortowania. " \
                f"Oczekiwano: {initial_sort_value}, Aktualne: {final_sort_value}"
        except AssertionError as e:
            # Dokumentujemy błąd w logach
            print(f"🐛 BŁĄD POTWIERDZONY: {str(e)}")
            # Przekazujemy błąd dalej aby test był oznaczony jako failed
            pytest.fail(str(e))
            
    @pytest.mark.smoke
    def test_empty_search_validation(self, page: Page, base_url: str):
        """
        Test weryfikujący walidację pustych wyszukiwań
        """
        from pages import HomePage
        
        home_page = HomePage(page)
        
        # Wejdź na stronę główną  
        home_page.open_homepage()
        
        # Kliknij w wyszukiwarkę
        home_page.click_search_icon()
        
        # Spróbuj wyszukać pustą frazę
        home_page.search_for_movie("")
        
        # Sprawdź URL - czy zawiera pusty parametr wyszukiwania
        current_url = page.url
        
        # Ten test dokumentuje drugi znaleziony błąd
        if "search" in current_url and ("q=" in current_url or "query=" in current_url):
            pytest.fail("🐛 BŁĄD POTWIERDZONY: System akceptuje puste wyszukiwania bez walidacji")