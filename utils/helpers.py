import re
from typing import Optional, Any


def safe_get_text(soup_element: Optional[Any], default: str = "") -> str:
    """
    Safely retrieves text from a BeautifulSoup element.
    Returns the default value if the element is missing to prevent NoneType errors.
    """
    if soup_element:
        return soup_element.get_text(strip=True)
    return default


def clean_numeric(text: Optional[str]) -> Optional[int]:
    """
    Uses Regular Expressions to extract only digits from a string.
    Useful for cleaning strings like '1.250 €' or '150 m²' into integers (1250, 150).
    """
    if not text:
        return None
    # r"\d+" finds all sequences of numbers in the text
    numbers = "".join(re.findall(r"\d+", text))
    return int(numbers) if numbers else None
