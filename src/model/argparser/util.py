def tokenize(string, token=' '):
    index = 0
    word = ''
    tokenized = []
    is_quoted = False

    def add_word():
        nonlocal index, tokenized, word
        index += 1
        tokenized.append(word)
        word = ''

    while index < len(string):
        char = string[index]

        if char == '"':
            index += 1
            if is_quoted:
                add_word()
                is_quoted = False
            else:
                is_quoted = True
            continue

        if char == token and not is_quoted:
            add_word()
            continue

        index += 1
        word += char
    else:
        tokenized.append(word)

    return tokenized
