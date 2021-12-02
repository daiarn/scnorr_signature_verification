import hashlib


def h28(text):
    if not type(text) == str:
        text = str(text)
    encoded = text.encode()
    result = hashlib.sha256(encoded).hexdigest()
    return result[-7:].upper()


def hd28(text):
    hex_value = h28(text)
    dec = int(hex_value, 16)
    return dec