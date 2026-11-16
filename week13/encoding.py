def count_freq(message:str):
    frequency = dict()
    for char in message:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency