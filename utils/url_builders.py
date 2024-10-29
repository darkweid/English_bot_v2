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