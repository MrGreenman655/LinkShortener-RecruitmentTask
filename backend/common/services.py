from django.conf import settings

DEFAULT_ALPHABET = settings.BASE_62_ALPHABET


class Base62:

    @staticmethod
    def encode(number, alphabet=DEFAULT_ALPHABET):
        if number == 0:
            return alphabet[0]
        encoded = ""
        while number > 0:
            number, rem = divmod(number, len(alphabet))
            encoded = alphabet[rem] + encoded
        return encoded

    @staticmethod
    def decode(text, alphabet):
        num = 0
        for char in text:
            num = num * 62 + alphabet.index(char)
        return num
