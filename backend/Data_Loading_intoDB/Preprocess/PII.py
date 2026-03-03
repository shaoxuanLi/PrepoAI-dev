import re

class PIIRemover:

    def remove_email(self, text: str) -> str:
        # More precise email pattern
        return re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[EMAIL]", text)

    def remove_phone(self, text: str) -> str:
        # 10–11 digit phone numbers
        return re.sub(r"\b\d{10,11}\b", "[PHONE]", text)

    def remove_id_card(self, text: str) -> str:
        # Chinese ID card (15–18 digits, optional X)
        return re.sub(r"\b\d{15,18}[Xx]?\b", "[ID]", text)

    def remove_ip(self, text: str) -> str:
        return re.sub(r"\b\d{1,3}(\.\d{1,3}){3}\b", "[IP]", text)

    def remove_credit_card(self, text: str) -> str:
        return re.sub(r"\b\d{13,16}\b", "[CARD]", text)

    def remove(self, text: str) -> str:
        text = self.remove_email(text)
        text = self.remove_phone(text)
        text = self.remove_id_card(text)
        text = self.remove_ip(text)
        text = self.remove_credit_card(text)
        return text