import re

from rich.prompt import FloatPrompt, PromptType, InvalidResponse, Prompt
from unidecode import unidecode


class TolerancePrompt(FloatPrompt):
    validate_error_message = "[prompt.invalid]Veuillez rentrer une valeur positive supérieure à 0.01. " \
                             "Pour un score de 17.50, cela correspond à un espace de recherche [17.49, 17.51]"

    def process_response(self, value: str) -> PromptType:
        value = value.strip()
        try:
            return_value = self.response_type(value)
            if return_value < 0.01:
                raise InvalidResponse(self.validate_error_message)
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        return return_value


class ScorePrompt(FloatPrompt):
    validate_error_message = "[prompt.invalid]Veuillez rentrer un nombre compris entre -100.0 et 100.0"

    def process_response(self, value: str) -> PromptType:
        value = value.strip()
        try:
            return_value = self.response_type(value)
            if abs(return_value) > 100.:
                raise InvalidResponse(self.validate_error_message)
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        return return_value


class WordPrompt(Prompt):
    validate_error_message = "[prompt.invalid]Veuillez rentrer un seul mot en minuscules"

    def process_response(self, value: str) -> PromptType:
        value = value.strip()
        try:
            return_value = self.response_type(value)
            if not re.fullmatch(r"[a-z\-']+", unidecode(return_value)):
                raise InvalidResponse(self.validate_error_message)
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        return return_value
