import re # regex
import unicodedata 
from bs4 import BeautifulSoup # html parsing


class TextCleaner:

    def remove_html_tags(self, text: str) -> str:
        return BeautifulSoup(text, "html.parser").get_text()

    def normalize_unicode(self, text: str) -> str:
        return unicodedata.normalize("NFKC", text)

    def remove_extra_whitespace(self, text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    def remove_control_chars(self, text: str) -> str:
        return re.sub(r"[\x00-\x1F\x7F]", "", text)

    def basic_filter(self, text: str, min_length: int = 10) -> str:
        if len(text) < min_length:
            return ""
        return text

    def clean(self, text: str) -> str:
        text = self.remove_html(text)
        text = self.normalize_unicode(text)
        text = self.remove_control_chars(text)
        text = self.remove_extra_whitespace(text)
        text = self.basic_filter(text)
        return text