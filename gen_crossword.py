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
        matched_letter = crossword[x][y]
        xtmp = x
        x = y
        y = xtmp
        # check vertical alignment
        print('checking vertial alignment...')
        slides = 0
        for letter in word:
            valid = True
            if valid and letter == matched_letter:
                for i in range(len(word)):
                    y_pos = y - slides + i
                    if (y_pos > 0 and letter != crossword[x][y_pos] and crossword[x][y_pos] != '▀'):
                        valid = False
                        break

                    # check for other interferences

                    # check side to side
                    if not (y_pos == y):
                        if (y_pos > 0 and (crossword[x - 1][y_pos] != '▀' or crossword[x + 1][y_pos] != '▀')):
                            valid = False
                            break
                    # check up
                    if i == len(word) - 1 and y_pos - 1 >= 0 and crossword[x][y_pos - 1] != '▀':
                        valid = False
                        break
                    # check down
                    if (matched_letter == 'l'):
                        print('should be True, True, True')
                        print(i == 0, y_pos + 1 <= len(crossword), crossword[x][y_pos] != '▀', crossword[x][y_pos])
                    if i == 0 and y_pos + 1 <= len(crossword) and crossword[x][y_pos] != '▀':
                        print('this should exit')
                        valid = False
                        break

                # found valid spot
                if (valid):
                    placement = Placement(x, y - slides, False)
                    return placement, True
            slides += 1

        # check horizontal alignment
        print('checking horizontal alignment...')
        slides = 0
        for letter in word:
            valid = True
            if valid and letter == matched_letter:
                for i in range(len(word)):
                    x_pos = x - slides + i
                    print('slides', slides)
                    print('i', i)
                    if (x_pos > 0 and letter != crossword[x_pos][y] and crossword[x_pos][y] != '▀'):
                        valid = False
                        print('check empty space failed')
                        break

                    # check for other interferences

                    # check up and down
                    if not (x_pos == x):
                        print(x_pos > 0, x_pos < len(crossword[0]), crossword[x_pos - 1][y] != '▀', crossword[x_pos + 1][y] != '▀')
                        print(crossword[x_pos][y])                       
                        print(crossword[x_pos][y - 1])
                        print(x_pos, y - 1)
                        if (x_pos > 0 and x_pos < len(crossword[0]) and \
                            (crossword[x_pos - 1][y] != '▀' or crossword[x_pos + 1][y] != '▀')):
                            print('check up and down failed')
                            valid = False
                            break
                    # check left
                    if i == len(word) - 1 and x_pos - 1 >= 0 and crossword[x_pos - 1][y] != '▀':
                        print('checking left failed')
                        valid = False
                        break
                    # check down
                    if i == 0 and x_pos + 1 <= len(crossword) and crossword[x_pos + 1][y] != '▀':
                        print('checking down failed')
                        print('this should exit')
                        valid = False
                        break

                # found valid spot
                if (valid):
                    placement = Placement(x - slides, y, True)
                    return placement, True
            slides += 1

        # check vertical alignment
    return None, False

def place_word(words, maxWords):
    '''
    random.shuffle(words)
    '''
    words = ['april', 'leather', 'cloud']
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
                    new_x = x
                    new_y = y
                    if (not is1d):
                        tmpx = x
                        new_x = y
                        new_y = tmpx
                    print(x, y)
                    if crossword[x][y] == letter:
                        print('matched letter', crossword[x][y], x, y, word)
                        print(crossword)
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