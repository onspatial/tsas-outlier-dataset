def append(text, file):
    with open(file, 'a') as f:
        f.write(text)
        f.write('\n')