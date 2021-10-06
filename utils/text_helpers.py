from transliterate import translit


def make_slug(string):
    return translit(string, 'ru', reversed=True).lower().replace(' ', '_')
