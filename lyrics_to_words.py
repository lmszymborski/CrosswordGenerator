words = []
f = open('melodrama.txt', 'r')
for line in f:
    line_split = line.split(' ')
    for word in line_split:
        if word.strip() not in words:
            words.append(word.strip())

with open('melodrama_words.txt', 'w') as new_f:
    for word in words:
        new_f.write(word + '\n')
