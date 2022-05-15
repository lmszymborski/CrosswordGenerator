import random
import numpy as np

class Placement:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

def load_file():
    words = []
    with open("example_1.txt", "r") as file:
        for line in file:
            word = line.strip()
            words.append(word)
    return words

def gen_empty_row(length):
    row = []
    for i in range(length):
        row.append('▀')
    return row

def place(word, crossword, x, y, horizontal):
    print('NEW WORD:', word, x, y, horizontal)
    is1d = False


    if (crossword is None):
        crossword = list(word)
    else:
        if len(crossword[0]) == 1:
            is1d = True

        if (x < 0):
            rows = len(crossword)
            cols = len(crossword[0])
            if is1d:
                rows = len(crossword[0])
                cols = len(crossword)
            new_col = np.array([gen_empty_row(rows)]).T
            while(x < 0):
                crossword = np.append(new_col, crossword, axis = 1)
                x += 1
        if (y < 0):
            rows = len(crossword)
            cols = len(crossword[0])
            if is1d:
                rows = len(crossword[0])
                cols = len(crossword)
            while (y < 0):
                print('y is', y)
                if is1d:
                    crossword = np.vstack([gen_empty_row(len(crossword)), crossword])
                    is1d = False
                else:
                    crossword = np.vstack([gen_empty_row(len(crossword[0])), crossword])
                y += 1

        word_lst = list(word)
        for i in range(len(word)):
            if horizontal:
                rows = len(crossword)
                cols = len(crossword[0])
                if is1d:
                    rows = len(crossword[0])
                    cols = len(crossword)
                if (cols <= x + i):
                    if is1d:
                        #crossword = np.hstack([crossword, '▀'])
                        crossword.append('▀')
                    else:
                        new_col = np.array([gen_empty_row(rows)]).T
                        crossword = np.append(crossword, new_col, axis = 1)
                if (is1d):
                    crossword[x + i] = word_lst[i]

                else:
                    crossword[y][x + i] = word_lst[i]

            else:
                rows = len(crossword)
                if is1d:
                    rows = len(crossword[0])
                    
                if (rows <= y + i):
                    if is1d:
                        crossword = np.vstack([crossword, gen_empty_row(len(crossword))])
                    else:
                        crossword = np.vstack([crossword, gen_empty_row(len(crossword[0]))])
                    is1d = False
                #print('changing letter at', x, y + i, crossword[x][y + i])
                if is1d:
                    crossword[x] = word_lst[i]
                else:

                    #crossword[x][y + i] = word_lst[i]
                    crossword[y + i][x] = word_lst[i]

    return crossword

def canPlace(word, crossword, x, y):
    if len(crossword[0]) == 1: # 1d
        # check vertical alignment
        matched_letter = crossword[x][y]

        slides = 0 # number of times we had to slide the word
        for letter in word:
            if letter == matched_letter:
                placement = Placement(x, y - slides, False)
                return placement, True
            slides += 1

        print('hm')
        return None, False

    else: #2d
        matched_letter = crossword[x][y]
        
        # check vertical alignment
        print('checking vertial alignment...')
        slides = 0
        for letter in word:
            valid = True
            if valid and letter == matched_letter:
                for i in range(len(word)):
                    x_pos = x - slides + i
                    if (x_pos > 0 and letter != crossword[x_pos][y] and crossword[x_pos][y] != '▀'):
                        valid = False
                        break

                    # check for other interferences

                    # check side to side
                    print('checking side to side', y, crossword[x_pos])
                    if (y + 1 < len(crossword[0])):
                        print(crossword[x_pos][y + 1])
                    if (y - 1 > 0):
                        print(crossword[x_pos][y - 1])
                    print(x_pos < len(crossword), x_pos >= 0, x_pos, y - 1 >= 0, y + 1 < len(crossword[0]))
                    if not (x_pos == x):
                        if (x_pos < len(crossword) and x_pos > 0):
                            if (y - 1 >= 0 and crossword[x_pos][y - 1]):
                                valid = False
                                break
                            if (y + 1 < len(crossword[0]) and crossword[x_pos][y + 1]):
                                valid = False
                                break

                    # check up
                    if i == len(word) - 1 and x_pos - 1 >= 0 and crossword[x_pos - 1][y] != '▀':
                        valid = False
                        break
                    # check down
                    if i == 0 and x_pos + 1 <= len(crossword) and crossword[x_pos + 1][y] != '▀':
                        print('this should exit')
                        valid = False
                        break

                # found valid spot
                if (valid):
                    placement = Placement(y, x - slides, False)
                    return placement, True
            slides += 1

        # check horizontal alignment

        print('checking horizontal alignment...')
        slides = 0
        for letter in word:
            valid = True
            if valid and letter == matched_letter:
                for i in range(len(word)):
                    #x_pos = x - slides + i
                    y_pos = y - slides + i
                    if (y_pos < len(crossword[0]) and letter != crossword[x][y_pos] and crossword[x][y_pos] != '▀'):
                        valid = False
                        print('check empty space failed')
                        break

                    # check for other interferences

                    # check up and down
                    if not (y_pos == y):
                        if (y_pos < len(crossword[0]) and y_pos >= 0):
                            if (x >= 0 and crossword[x - 1][y_pos] != '▀'):
                                valid = False
                                break
                            if (x < len(crossword[0]) and crossword[x + 1][y_pos]):
                                valid = False
                                break

                    # check right
                    if i == 0 and y_pos - 1 >= 0 and crossword[x][y_pos - 1] != '▀':
                        print('checking right failed')
                        valid = False
                        break
                    # check left
                    if i == len(crossword[0]) and y_pos + 1 < len(crossword[0]) and crossword[x][y_pos + 1] != '▀':
                        print('checking left failed')
                        valid = False
                        break

                # found valid spot
                if (valid):
                    placement = Placement(y - slides, x, True)
                    return placement, True
            slides += 1

        # check vertical alignment
    return None, False

def updateRows(crossword):
    if len(crossword[0]) == 1:
        is1d = True
    else:
        is1d = False
    rows = len(crossword)
    cols = len(crossword[0])
    if is1d:
        rows = 1
        cols = len(crossword)
    return rows, cols

def place_word(words, maxWords):
    
    random.shuffle(words)
    ''
    words = ['april', 'leather', 'cloud', 'dui']
    #words = ['are','lxx','leather']
    #words = ['xxxdax', 'april']
    #words = ['april', 'leather', 'cloud']
    words = ['cloud', 'tinkerbell', 'april', 'cap', 'puma', 'traderjoes', 'leather']
   # words = ['visualstudiocode', 'cloud', 'tinkerbell', 'april', 'cap', 'puma', 'traderjoes', 'leather']

    ''

    word = words.pop()
    horizontal = True
    crossword = place(word, None, 0, 0, horizontal)
    count = 1
    while count < maxWords and len(words) > 0:
        word = words.pop()
        if len(crossword[0]) == 1:
            is1d = True
        else:
            is1d = False
        rows = len(crossword)
        cols = len(crossword[0])
        if is1d:
            print('is1d')
            rows = 1
            cols = len(crossword)
        #rows = len(crossword[0])
        #cols = len(crossword)
        print('crossword num rows', rows)
        print('crossword num cols', cols)
        #crossword = place(word, crossword, random.randint(0, cols - 1), random.randint(0, rows - 1), random.choice([True, False]))
        #count += 1
        spotFound = False
        for letter in word:
            for y in range(rows):
                for x in range(cols):
                    if len(crossword[0]) == 1:
                        is1d = True
                    else:
                        is1d = False
                    new_x = x
                    new_y = y
                    
                    if (not is1d):
                        tmpx = x
                        new_x = y
                        new_y = tmpx
                    
                    if crossword[new_x][new_y] == letter:
                        print('matched letter', crossword[new_x][new_y], new_x, new_y, word)
                        placement, ok = canPlace(word, crossword, new_x, new_y)
                        if ok:
                            crossword = place(word, crossword, placement.x, placement.y, placement.direction)
                            count = count + 1
                            spotFound = True
                            print(crossword)
                            break
                if spotFound:
                    break
            if spotFound:
                break
                    
                

                        
    print(word)


def main():
    words = load_file()
    place_word(words, len(words))

if __name__ == '__main__':
    main()