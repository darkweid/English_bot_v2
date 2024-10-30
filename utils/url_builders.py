import re


def youglish_url_builder(word: str) -> str:
    # Убираем слова в скобках
    word = re.sub(r'\(.*?\)', '', word)
    # Убираем "somebody", "something", "smb", "smth"
    word = re.sub(r'\b(somebody|something|smb|smth)\b', '', word, flags=re.IGNORECASE)
    word = word.replace('/', ' ')
    # Убираем лишние пробелы и кодируем пробелы для URL
    word = ' '.join(word.split()).replace(' ', '%20')

    return f'https://www.youglish.com/pronounce/{word}/english'


def word_with_youglish_link(word_english: str) -> str:
    """
    Creates an HTML hyperlink to YouGlish pronunciation for the given word.

    The hyperlink uses YouGlish's URL structure for English pronunciation.

    Args:
        word_english (str): The word to link to YouGlish.

    Returns:
        str: An HTML anchor element as a string.
    """
    return f'<a href="{youglish_url_builder(word_english)}">{word_english.capitalize()}</a>'
