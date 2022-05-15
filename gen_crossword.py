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
        print(crossword)
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
                print('x is', x)
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

        print(crossword)
        word_lst = list(word)
        for i in range(len(word)):
            if horizontal:
                rows = len(crossword)
                cols = len(crossword[0])
                if is1d:
                    rows = len(crossword[0])
                    cols = len(crossword)
                print('cols, x + i:', cols, x + i)
                if (cols <= x + i):
                    if is1d:
                        #crossword = np.hstack([crossword, '▀'])
                        crossword.append('▀')
                        print('is1d')
                    else:
                        new_col = np.array([gen_empty_row(rows)]).T
                        print(new_col)
                        crossword = np.append(crossword, new_col, axis = 1)
                    print(crossword)
                if (is1d):
                    crossword[x + i] = word_lst[i]
                    print(crossword)

                else:
                    print('y, x + i:', y, x + i, crossword[y][x + i])
                    crossword[y][x + i] = word_lst[i]
                    print(crossword)

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
                    print(crossword)
                #print('changing letter at', x, y + i, crossword[x][y + i])
                if is1d:
                    crossword[x] = word_lst[i]
                    print(crossword)
                else:

                    #crossword[x][y + i] = word_lst[i]
                    crossword[y + i][x] = word_lst[i]
                    print(crossword)

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
        # check horizontal alignment
        horizontal = True
        i = 0
        for letter in word:
            if (crossword[x][y + i] != letter and crossword[x][y + i] != '▀'):
                horizontal = False
                break
            i += 1

        if horizontal:
            placement = Placement(x, y, True)
            return placement, True

        # check vertical alignment
        vertical = True
        i = 0
        for letter in word:
            if (crossword[x + i][y] != letter and crossword[x + i][y] != '▀'):
                vertical = False
                break
            i += 1

        if vertical:
            placement = Placement(x, y, False)
            return placement, True  
    

    return None, False

def place_word(words, maxWords):
    random.shuffle(words)
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

        for letter in word:
            for y in range(rows):
                for x in range(cols):
                    #crossword = place(word, crossword, random.randint(0, cols - 1), random.randint(0, rows - 1), random.choice([True, False]))
                    #continue
                    #crossword = place(word, crossword, random.randint(0, cols - 1), random.randint(0, rows - 1), False)
                   
                    #count += 1
                    if len(crossword[0]) == 1:
                        is1d = True
                    else:
                        is1d = False
                    if (not is1d):
                        tmpx = x
                        x = y
                        y = tmpx
                    if crossword[x][y] == letter:
                        print('matched letter', crossword[x][y], x, y, word)
                        placement, ok = canPlace(word, crossword, x, y)
                        if ok:
                            crossword = place(word, crossword, placement.x, placement.y, placement.direction)
                            count = count + 1
                            continue
                    
                

                        
    print(word)


def main():
    words = load_file()
    place_word(words, len(words))

if __name__ == '__main__':
    main()