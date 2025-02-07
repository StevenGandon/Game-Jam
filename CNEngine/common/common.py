def byte_value_size(size: int):
    value = 0
    while (size / 1000 > 1):
        size /= 1000
        value += 1
    return (str(round(size, 2)) + ("o", "Ko", "Mo", "Go", "To", "Po")[value])
