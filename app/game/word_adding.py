def find_known_char(x):
    word_len = x
    if word_len <= 4:
        known_char = 0
    elif word_len <= 8:
        known_char = 1
    elif word_len <= 13:
        known_char = 2
    else:
        known_char = 3

    return known_char