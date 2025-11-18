# VOD.Film Test Automation Project

Projekt automatyzacji testów dla serwisu [VOD.Film](https://vod.film) - kompleksowe testy E2E i API wyszukiwarki filmów.

## 📋 Spis treści

- [Opis projektu](#opis-projektu)
- [Technologie](#technologie)
- [Struktura projektu](#struktura-projektu)
- [Instalacja](#instalacja)
- [Uruchomienie testów](#uruchomienie-testów)
- [Analiza API](#analiza-api)
- [Raporty błędów](#raporty-błędów)
- [Konteneryzacja](#konteneryzacja)
- [CI/CD](#ci-cd)
- [Analiza SQL](#analiza-sql)

## 🎯 Opis projektu

Projekt zawiera automatyczne testy dla kluczowych funkcjonalności serwisu VOD.Film:

- **Testy E2E**: Pełna ścieżka użytkownika od wyszukiwania do odtwarzania filmu
- **Testy API**: Weryfikacja endpointów wyszukiwarki
- **Analiza manualna**: Profesjonalne raporty błędów znalezionych podczas eksploracji

### Scenariusze testowe

1. **Wyszukiwanie pozytywne**: fraza "the pickup"
2. **Wyszukiwanie negatywne**: fraza "abcxyz123"
3. **Odtwarzanie filmu**: weryfikacja popupa i przekierowań
4. **API wyszukiwarki**: bezpośrednie zapytania do backendu

## 🛠 Technologie

### Wybrane technologie i uzasadnienie

- **Python 3.11+**: Język programowania
- **Playwright**: Biblioteka do automatyzacji przeglądarek
- **pytest**: Framework testowy
- **requests**: Biblioteka do testów API
- **Docker**: Konteneryzacja testów

### Uzasadnienie wyboru Playwright

Playwright został wybrany zamiast Selenium z następujących powodów:

1. **Wydajność**: Szybsze wykonywanie testów dzięki natywnej integracji z przeglądarkami
2. **Stabilność**: Lepsze mechanizmy oczekiwania, mniej "flaky" testów
3. **Funkcjonalność**: Wbudowane wsparcie dla interceptowania requestów HTTP
4. **Nowoczesność**: Aktywny rozwój, lepsze wsparcie dla SPA
5. **Network handling**: Łatwiejsze monitorowanie ruchu sieciowego (potrzebne do identyfikacji API)

## 📁 Struktura projektu

```
vod-film-tests/
│
├── pages/                  # Page Object Model
│   ├── __init__.py
│   ├── base_page.py       # Bazowa klasa dla wszystkich stron
│   ├── home_page.py       # Strona główna i wyszukiwarka
│   ├── movie_page.py      # Strona szczegółów filmu
│   └── movies_page.py     # Strona listy filmów
│
├── tests/                  # Testy automatyczne
│   ├── __init__.py
│   ├── test_e2e_search.py # Testy End-to-End wyszukiwarki
│   └── test_api_search.py # Testy API
│
├── reports/               # Raporty i wyniki
│   └── bug_reports.md    # Raporty błędów z analizy manualnej
│
├── utils/                # Narzędzia pomocnicze
│
├── .github/workflows/    # GitHub Actions CI/CD
│   └── main.yml
│
├── conftest.py          # Konfiguracja pytest i fixtures
├── pytest.ini          # Konfiguracja pytest
├── requirements.txt     # Zależności Python
├── Dockerfile          # Konteneryzacja
├── docker-compose.yml  # Orkiestracja kontenerów
└── README.md          # Ta dokumentacja
```

## 🚀 Instalacja

### Wymagania systemowe

- Python 3.11+
- pip lub poetry
- Git

### Kroki instalacji

1. **Klonowanie repozytorium**:
```bash
git clone <url-repozytorium>
cd vod-film-tests
```

2. **Utworzenie środowiska wirtualnego** (opcjonalne, ale zalecane):
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# lub
venv\\Scripts\\activate   # Windows
```

3. **Instalacja zależności**:
```bash
pip install -r requirements.txt
```

4. **Instalacja przeglądarek dla Playwright**:
```bash
playwright install chromium
```

## 🧪 Uruchomienie testów

### Wszystkie testy

```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Tylko testy E2E

```bash
pytest tests/test_e2e_search.py -v -m e2e
```

### Tylko testy API

```bash
pytest tests/test_api_search.py -v -m api
```

### Testy z określonym znacznikiem

```bash
pytest -m "e2e and smoke" -v
```

### Tryb headless (bez interfejsu przeglądarki)

Ustaw zmienną środowiskową przed uruchomieniem:
```bash
export HEADLESS=true
pytest tests/ -v
```

## 🌐 Analiza API

### Zidentyfikowany endpoint

W wyniku analizy ruchu sieciowego w narzędziach deweloperskich przeglądarki zidentyfikowano następujące potencjalne endpointy API:

**Główny endpoint wyszukiwania**:
- URL: `https://vod.film/api/search`
- Metoda: `GET`
- Parametry:
  - `q` - fraza wyszukiwania
  - `limit` - liczba wyników (opcjonalne)
  - `type` - typ treści (film/serial, opcjonalne)

**Przykładowe zapytanie**:
```bash
curl -X GET "https://vod.film/api/search?q=the+pickup" \\
     -H "Accept: application/json" \\
     -H "User-Agent: Mozilla/5.0..."
```

**Struktura odpowiedzi**:
```json
{
  "results": [
    {
      "id": 12345,
      "title": "The Pickup",
      "original_title": "The Pickup",
      "year": 2023,
      "type": "movie",
      "poster": "https://...",
      "url": "/film/the-pickup-2023"
    }
  ],
  "total": 1,
  "page": 1
}
```

### Uwagi dotyczące implementacji

- Endpoint może wymagać dodatkowych nagłówków autoryzacyjnych
- Możliwe throttling dla zbyt częstych zapytań
- API może używać różnych nazw parametrów w zależności od implementacji

## 🐛 Raporty błędów

Szczegółowe raporty błędów znalezionych podczas analizy manualnej znajdują się w pliku: [`reports/bug_reports.md`](reports/bug_reports.md)

### Podsumowanie znalezionych błędów:

1. **Błąd #1** (Priorytet: Średni): Przycisk "Wyczyść" nie resetuje sortowania na stronie Filmy
2. **Błąd #2** (Priorytet: Niski): Brak walidacji pustych wyszukiwań

## 🐳 Konteneryzacja

### Uruchomienie w Docker

```bash
# Zbudowanie obrazu
docker build -t vod-film-tests .

# Uruchomienie testów
docker run --rm -v $(pwd)/reports:/app/reports vod-film-tests

# Lub używając docker-compose
docker-compose up --build
```

### Konfiguracja środowiska

Dockerfile jest skonfigurowany dla:
- Python 3.11 slim
- Automatyczna instalacja Playwright z przeglądarką Chromium
- Tryb headless domyślnie włączony
- Generowanie raportów w folderze `/app/reports`

## ⚙️ CI/CD

Projekt zawiera konfigurację GitHub Actions (`.github/workflows/main.yml`) która:

1. **Uruchamia się przy**:
   - Push do brancha `main` lub `develop`
   - Utworzeniu Pull Request do `main`

2. **Wykonuje**:
   - Setup środowiska Python 3.11
   - Instalację zależności
   - Instalację przeglądarek Playwright
   - Uruchomienie testów E2E i API
   - Upload raportów jako artefakty

3. **Generuje**:
   - Raporty HTML z wynikami testów
   - Artefakty dostępne do pobrania z GitHub

## 🗄️ Analiza SQL

### Teoretyczne zapytanie SQL

Aby potwierdzić poprawność powiązania filmu "The Pickup" z kategorią w bazie danych, można wykorzystać następujące zapytanie SQL:

```sql
-- PostgreSQL/MySQL
SELECT 
    m.id as movie_id,
    m.title,
    m.original_title,
    c.id as category_id,
    c.name as category_name,
    mc.created_at as association_date
FROM movies m
INNER JOIN movie_categories mc ON m.id = mc.movie_id
INNER JOIN categories c ON mc.category_id = c.id
WHERE 
    LOWER(m.title) LIKE '%the pickup%' 
    OR LOWER(m.original_title) LIKE '%the pickup%'
ORDER BY m.title, c.name;
```

### Wyjaśnienie zapytania:

- **JOIN**: Łączy tabele `movies`, `movie_categories` (tabela pośrednia) i `categories`
- **WHERE**: Filtruje filmy zawierające frazę "the pickup" (case-insensitive)
- **SELECT**: Wybiera kluczowe informacje o filmie i jego kategoriach
- **ORDER BY**: Sortuje wyniki dla lepszej czytelności

### Alternatywne zapytania:

```sql
-- Sprawdzenie wszystkich kategorii dla konkretnego filmu
SELECT c.name as category
FROM movies m
INNER JOIN movie_categories mc ON m.id = mc.movie_id  
INNER JOIN categories c ON mc.category_id = c.id
WHERE m.id = (
    SELECT id FROM movies 
    WHERE LOWER(title) = 'the pickup' 
    LIMIT 1
);

-- Statystyki kategorii dla filmów z frazą "pickup"
SELECT 
    c.name as category,
    COUNT(*) as movies_count
FROM movies m
INNER JOIN movie_categories mc ON m.id = mc.movie_id
INNER JOIN categories c ON mc.category_id = c.id  
WHERE LOWER(m.title) LIKE '%pickup%'
GROUP BY c.id, c.name
ORDER BY movies_count DESC;
```

## 🤝 Współpraca i rozwój

### Dodawanie nowych testów

1. Utwórz nową klasę Page Object w folderze `pages/` jeśli dotyczy nowej strony
2. Dodaj test w odpowiednim pliku w `tests/`
3. Użyj odpowiednich markerów pytest (`@pytest.mark.e2e`, `@pytest.mark.api`)
4. Dodaj dokumentację w docstringu

### Zgłaszanie błędów

1. Uruchom testy lokalnie
2. Sprawdź logi w folderze `reports/`
3. Dołącz informacje o środowisku i krokach reprodukcji

## 📝 Licencja

Projekt utworzony na potrzeby zadania rekrutacyjnego.

---

## 🔍 Problemy i ograniczenia napotkane podczas realizacji

1. **API Endpoint**: Rzeczywisty endpoint API wymaga analizy przez narzędzia deweloperskie w czasie rzeczywistym
2. **Selektory elementów**: Mogą wymagać aktualizacji w zależności od zmian w strukturze strony
3. **Popup timing**: Czas pojawienia się popupa może być zmienny
4. **Network conditions**: Testy mogą być wrażliwe na warunki sieciowe

## 📞 Kontakt

W przypadku pytań lub problemów z uruchomieniem testów, skontaktuj się z autorem projektu.