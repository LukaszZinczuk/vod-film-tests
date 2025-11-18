import logging
import os
from datetime import datetime


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Konfiguruje logger dla testów
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Format logów
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler konsoli
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pliku (opcjonalny)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_screenshot_path(test_name: str) -> str:
    """
    Generuje ścieżkę dla screenshota
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    
    # Utwórz folder screenshots jeśli nie istnieje
    screenshots_dir = "reports/screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    
    return os.path.join(screenshots_dir, filename)


def is_headless_mode() -> bool:
    """
    Sprawdza czy testy mają być uruchomione w trybie headless
    """
    return os.getenv('HEADLESS', 'false').lower() == 'true'