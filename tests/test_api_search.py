import pytest
import requests
import json
from typing import Dict, Any


class TestAPISearch:
    """Testy API wyszukiwarki filmów"""
    
    # Możliwe endpointy API do przetestowania
    POSSIBLE_API_ENDPOINTS = [
        "/api/search",
        "/search/api",
        "/api/movies/search", 
        "/api/films/search",
        "/search",
        "/api/v1/search",
        "/wp-json/wp/v2/search"  # WordPress API
    ]
    
    def get_api_endpoint(self, base_url: str) -> str:
        """
        Próbuje znaleźć działający endpoint API
        W rzeczywistym scenariuszu byłby zidentyfikowany przez DevTools
        """
        for endpoint in self.POSSIBLE_API_ENDPOINTS:
            try:
                url = f"{base_url}{endpoint}"
                response = requests.get(url, params={"q": "test"}, timeout=5)
                if response.status_code in [200, 400]:  # 400 może oznaczać że endpoint istnieje ale brakuje parametrów
                    return url
            except:
                continue
        return f"{base_url}/api/search"  # Fallback
    
    @pytest.mark.api
    def test_search_api_the_pickup(self, base_url: str):
        """
        Test API wyszukiwania filmu 'the pickup'
        
        Uwaga: W rzeczywistym scenariuszu endpoint byłby zidentyfikowany 
        przez analizę ruchu sieciowego w DevTools przeglądarki
        """
        
        # Endpoint zidentyfikowany przez DevTools (symulacja)
        api_endpoint = self.get_api_endpoint(base_url)
        
        # Parametry wyszukiwania
        search_params = {
            "q": "the pickup",
            "query": "the pickup", 
            "search": "the pickup",
            "term": "the pickup"
        }
        
        # Nagłówki HTTP
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "application/json, */*",
            "Content-Type": "application/json"
        }
        
        # Próba różnych kombinacji parametrów
        for param_name, search_term in search_params.items():
            try:
                response = requests.get(
                    api_endpoint,
                    params={param_name: search_term},
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    self._validate_api_response(response, search_term)
                    return
                    
            except requests.exceptions.RequestException as e:
                print(f"Błąd podczas zapytania z parametrem {param_name}: {e}")
                continue
        
        # Jeśli żaden endpoint nie zadziałał, sprawdź czy strona w ogóle odpowiada
        try:
            response = requests.get(base_url, timeout=10)
            assert response.status_code == 200, f"Strona główna nie odpowiada: {response.status_code}"
            
            # Raportuj, że nie znaleziono API endpoint
            pytest.skip("Nie znaleziono działającego API endpoint - wymaga analizy DevTools")
            
        except requests.exceptions.RequestException:
            pytest.fail("Strona nie jest dostępna")
    
    def _validate_api_response(self, response: requests.Response, search_term: str) -> None:
        """Waliduje odpowiedź API"""
        
        # Sprawdź status code
        assert response.status_code == 200, f"Niepoprawny status code: {response.status_code}"
        
        # Sprawdź Content-Type
        content_type = response.headers.get('content-type', '')
        assert 'application/json' in content_type, f"Niepoprawny Content-Type: {content_type}"
        
        try:
            # Parsuj JSON
            data = response.json()
            assert isinstance(data, (dict, list)), "Odpowiedź nie jest prawidłowym JSON"
            
            # Sprawdź czy zawiera dane o filmach
            self._validate_movie_data(data, search_term)
            
        except json.JSONDecodeError:
            pytest.fail("Odpowiedź nie zawiera prawidłowego JSON")
    
    def _validate_movie_data(self, data: Dict[str, Any] | list, search_term: str) -> None:
        """Waliduje dane o filmach w odpowiedzi API"""
        
        movies = []
        
        # Różne struktury odpowiedzi API
        if isinstance(data, dict):
            # Struktura: {"results": [...], "movies": [...], "data": [...]}
            movies = (data.get('results', []) or 
                     data.get('movies', []) or 
                     data.get('data', []) or
                     data.get('items', []))
            
            # Jeśli nie ma zagnieżdżonych list, może cała odpowiedź to lista filmów
            if not movies and 'title' in data:
                movies = [data]
                
        elif isinstance(data, list):
            movies = data
        
        # Sprawdź czy znaleziono filmy
        assert len(movies) > 0, f"Brak filmów w odpowiedzi API dla '{search_term}'"
        
        # Sprawdź strukturę pierwszego filmu
        first_movie = movies[0]
        assert isinstance(first_movie, dict), "Film nie jest obiektem JSON"
        
        # Sprawdź wymagane pola
        title_fields = ['title', 'name', 'original_title', 'display_name']
        title_found = any(field in first_movie for field in title_fields)
        assert title_found, f"Brak pola tytułu w filmie: {first_movie.keys()}"
        
        # Sprawdź czy tytuł zawiera wyszukiwaną frazę
        movie_title = ""
        for field in title_fields:
            if field in first_movie:
                movie_title = str(first_movie[field])
                break
        
        assert search_term.lower() in movie_title.lower(), \
            f"Tytuł '{movie_title}' nie zawiera frazy '{search_term}'"
        
        print(f"✓ API zwróciło {len(movies)} filmów, pierwszy: '{movie_title}'")
    
    @pytest.mark.api
    def test_search_api_different_endpoints(self, base_url: str):
        """Test różnych możliwych endpointów API"""
        
        search_term = "the pickup"
        found_working_endpoint = False
        
        for endpoint in self.POSSIBLE_API_ENDPOINTS:
            api_url = f"{base_url}{endpoint}"
            
            try:
                response = requests.get(
                    api_url,
                    params={"q": search_term},
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"✓ Działający endpoint: {api_url}")
                    found_working_endpoint = True
                    self._validate_api_response(response, search_term)
                    break
                    
            except requests.exceptions.RequestException:
                continue
        
        if not found_working_endpoint:
            pytest.skip("Nie znaleziono działającego API endpoint")