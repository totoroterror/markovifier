import re


def min_indent(text: str) -> int:
    lines = [line for line in text.split('\n') if line.strip()]

    return min(len(line) - len(line.lstrip()) for line in lines)


def strip_indent(text: str) -> str:
    indent = min_indent(text)

    while text.startswith('\n'):
        text = text.strip('\n')

    while text.endswith('\n'):
        text = text.rstrip('\n')

    if indent == 0:
        return text

    regex = f'^[ \\t]{{{indent}}}'

    return re.sub(regex, '', text, flags=re.MULTILINE)


def strip_indents(text: str) -> str:
    while text.startswith('\n'):
        text = text.strip('\n')

    while text.endswith('\n'):
        text = text.rstrip('\n')

    return re.sub('^[ \\t]+', '', text, flags=re.MULTILINE)
