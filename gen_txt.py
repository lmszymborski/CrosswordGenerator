
words = []
f = open('4000_common_words.txt', 'r')
for line in f:
    line_split = line.split('\t')
    for word in line_split:
        words.append(word.strip())

with open('4000_common_words_new.txt', 'w') as new_f:
    for word in words:
        new_f.write(word + '\n')