import random
import numpy as np
import copy
import statistics
import requests

#TODO:
# switch optimization to time based vs iteration based
# instead of just having a list of words, have a list of word objects
# -- words have word and clue
# return both a filled crossword and an empty crossword with clues attached to spots
# figure out an approach to get denser crosswords
# generate clues based on lyric and a ___ where the word is, do crossword puzzles by artist name
# if a word does not pass through multiple words, put it back in the list
# -- this will take a lot of time, but go through each word and give it a score based on how many words it crosses through
# -- the highest score is placed
# -- in case of tie, place the longest word

# resources
# https://cs.stackexchange.com/questions/123618/algorithm-to-create-dense-style-crossword-puzzles
# https://stackoverflow.com/questions/943113/algorithm-to-generate-a-crossword
# https://www.baeldung.com/cs/generate-crossword-puzzle
# https://github.com/pmaher86/blacksquare/tree/master/blacksquare

EMPTY_CHAR = '▀▀'

class Placement:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

class Clue:
    def __init__(self, num, across, definition, x_y, word):
        self.num = num
        self.across = across
        self.definition = definition
        self.x_y = x_y
        self.word = word

def load_file(filename, limit = 1000):
    words = []
    with open(filename, "r") as file:
        for line in file:
            word = line.strip().lower()
            if (len(word) < 2):
                continue
            word = ''.join(ch for ch in word if ch.isalnum())
            words.append(word)
            string_value = "alphanumeric@123__"
    return words

def gen_empty_row(length):
    row = []
    for i in range(length):
        row.append(EMPTY_CHAR)
    return row

def place(word, crossword, x, y, horizontal):
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
                        crossword.append(EMPTY_CHAR)
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
                if is1d:
                    crossword[x] = word_lst[i]
                else:

                    #crossword[x][y + i] = word_lst[i]
                    crossword[y + i][x] = word_lst[i]

    return crossword

def canPlace(word, crossword, x, y):
    cross_score = 1
    if len(crossword[0]) == 1: # 1d
        # check vertical alignment
        matched_letter = crossword[x][y]

        slides = 0 # number of times we had to slide the word
        for letter in word:
            if letter == matched_letter:
                placement = Placement(x, y - slides, False)
                print('cross score from can place', cross_score)
                return placement, True, cross_score
            slides += 1

        return None, False, 0

    else: #2d
        matched_letter = crossword[x][y]
        
        # check vertical alignment
        slides = 0
        for letter in word:
            valid = True
            cross_score = 0
            if valid and letter == matched_letter:
                for i in range(len(word)):
                    x_pos = x - slides + i
                    if (x_pos < 0 or x_pos >= len(crossword)):
                        continue
                    
                    if (word[i] == crossword[x_pos][y]):
                        cross_score += 1
                    # check for different word interference
                    if (x_pos >= 0 and word[i] != crossword[x_pos][y] and crossword[x_pos][y] != EMPTY_CHAR):
                        valid = False
                        break

                    # check for other interferences

                    # check side to side
                    if not (x_pos == x):
                        if (x_pos < len(crossword) and x_pos > 0):
                            if (y - 1 >= 0 and crossword[x_pos][y - 1] != EMPTY_CHAR):
                                valid = False
                                break
                            if (y + 1 < len(crossword[0]) and crossword[x_pos][y + 1] != EMPTY_CHAR):
                                valid = False
                                break

                    # check down
                    if i == len(word) - 1 and x_pos + 1 < len(crossword) and crossword[x_pos + 1][y] != EMPTY_CHAR:
                        valid = False
                        break
                    # check up
                    if i == 0 and x_pos + 1 >= 0 and crossword[x_pos - 1][y] != EMPTY_CHAR:
                        valid = False
                        break

                # found valid spot
                if (valid):
                    placement = Placement(y, x - slides, False)
                    return placement, True, cross_score
            slides += 1

        # check horizontal alignment

        slides = 0
        for letter in word:
            valid = True
            cross_score = 0
            if valid and letter == matched_letter:
                for i in range(len(word)):
                    #x_pos = x - slides + i
                    y_pos = y - slides + i
                    if (y_pos < 0 or y_pos >= len(crossword[0])):
                        continue

                    if (word[i] == crossword[x][y_pos]):
                        cross_score += 1

                    if not (word[i] == crossword[x][y_pos] or crossword[x][y_pos] == EMPTY_CHAR):
                        valid = False
                        break


                    # check for other interferences

                    # check up and down
                    if not (y_pos == y):
                        if (y_pos < len(crossword[0]) and y_pos >= 0):
                            if (x - 1>= 0 and crossword[x - 1][y_pos] != EMPTY_CHAR):
                                valid = False
                                break
                            if (x + 1 < len(crossword) and crossword[x + 1][y_pos] != EMPTY_CHAR):
                                valid = False
                                break

                    # check left
                    if i == 0 and y_pos - 1 >= 0 and crossword[x][y_pos - 1] != EMPTY_CHAR:
                        valid = False
                        break

                    # check right
                    if i == len(word) - 1 and y_pos + 1 < len(crossword[0]) and crossword[x][y_pos + 1] != EMPTY_CHAR:
                        valid = False
                        break

                # found valid spot
                if (valid):
                    placement = Placement(y - slides, x, True)
                    return placement, True, cross_score
            slides += 1

        # check vertical alignment
    return None, False, 0

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

def generate(words, maxWords, sort_words=True):
    #TODO: optimize
    #TODO: if word gets skipped, put back in word list. if word at end of list gets skipped, then it gets emitted
    #random.shuffle(words)
    crossword_list = {}
    if (sort_words):
        words = random.sample(words, maxWords)
        words = sorted(words, key=len)
    else:
        random.shuffle(words)
    '''
    #words = ['are','lxx','leather']
    #words = ['xxxdax', 'april']
    #words = ['april', 'leather', 'cloud']
    words = ['cloud', 'tinkerbell', 'april', 'cap', 'puma', 'traderjoes', 'leather']
    words = ['visualstudiocode', 'cloud', 'tinkerbell', 'april', 'cap', 'puma', 'traderjoes', 'leather']
    words = ['visualstudiocode', 'cloud', 'tinkerbell', 'cap', 'april', 'traderjoes', 'puma']
    words = ['cap', 'leather', 'tinkerbell', 'cloud', 'april', 'traderjoes', 'visualstudiocode', 'puma']
    words = ['provide', 'choice', 'build', 'special', 'threat', 'set', 'firm', 'popular', 'exactly', 'first', 'word', 'country', 'final', 'doctor', 'article', 'with', 'history', 'ahead', 'least', 'enjoy', 'travel', 'mother', 'away', 'hope', 'dinner', 'offer', 'clear', 'his', 'north', 'option', 'know', 'understand', 'politics', 'truth', 'herself', 'listen', 'culture', 'thank', 'around', 'activity', 'claim', 'too', 'responsibility', 'range', 'court', 'lawyer', 'Democrat', 'east', 'leg', 'believe']
    words = ['responsibility', 'two', 'a', 'as', 'prepare', 'education', 'population', 'project', 'we', 'live', 'east', 'have', 'not', 'recognize', 'evening', 'probably', 'nearly', 'also', 'team', 'compare', 'try', 'health', 'establish', 'charge', 'specific', 'environmental', 'food', 'and', 'you', 'it', 'policy', 'finally', 'blue', 'west', 'firm', 'task', 'ball', 'its', 'data', 'matter', 'pass', 'product', 'offer', 'shoulder', 'rich', 'at', 'line', 'how', 'cold', 'business']
    words = ['dui', 'april', 'leather', 'cloud']
    '''

    word = words.pop()
    horizontal = True
    crossword = place(word, None, 0, 0, horizontal)
    count = 1
    while count < maxWords and len(words) > 0:
        if len(crossword[0]) == 1:
            is1d = True
        else:
            is1d = False
        rows = len(crossword)
        cols = len(crossword[0])
        if is1d:
            rows = 1
            cols = len(crossword)
        spotFound = False
        max_cross_word_score = 0
        max_cross_word_placement = None
        max_cross_word = ''
        for word in words:
            print('checking ' + word)
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
                            placement, ok, cross_score = canPlace(word, crossword, new_x, new_y)
                            if ok:
                                if (cross_score > max_cross_word_score):
                                    print('cross score', cross_score)
                                    max_cross_word_score = cross_score
                                    max_cross_word_placement = placement
                                    max_cross_word = word
                                break

        if (max_cross_word_placement != None):
            # put the max cross word in the crossword
            crossword = place(max_cross_word, crossword, max_cross_word_placement.x, max_cross_word_placement.y, max_cross_word_placement.direction)
            count += 1
            print('max score found for word ' + max_cross_word + ': ' + str(max_cross_word_score))
            print(crossword)
            crossword_list[word] = placement
            if (max_cross_word_placement.x < 0):
                for word_place in crossword_list:
                    print(crossword_list)
                    print(crossword_list[word_place])
                    print(max_cross_word_placement)
                    crossword_list[word_place].x -= max_cross_word_placement.x
            if (max_cross_word_placement.y < 0):
                for word_place in crossword_list:
                    print(crossword_list)
                    print(crossword_list[word_place])
                    print(max_cross_word_placement)
                    crossword_list[word_place].y -= max_cross_word_placement.y
            words.remove(max_cross_word)

    return crossword, count, crossword_list

def generate_score(crossword):
    num_rows = len(crossword)
    num_cols = len(crossword[0])

    sizeRatio = num_rows / num_cols
    if num_rows > num_cols:
        sizeRatio = num_cols / num_rows

    filled = 0
    empty = 0

    for y in range(num_rows):
        for x in range(num_cols):
            if crossword[y][x] == EMPTY_CHAR:
                empty += 1
            else:
                filled += 1
    
    filledRatio = filled / empty
    return (sizeRatio * 10) + (filledRatio * 20)

def write_stats(scores, iterations, filename):
    with open(filename + '.txt', 'w') as f:
        f.write('Over ' + str(iterations) + ' iterations:\n')
        f.write('Mean: ' + str(statistics.mean(scores)) + '\n')
        f.write('Median: ' + str(statistics.median(scores)) + '\n')
        f.write('Max: ' + str(max(scores)) + '\n')
        f.write('Min: ' + str(min(scores)) + '\n')

def repeated_generation(words, maxWords, iterations, threshold, sort_words):
    maxScore = 0
    minScore = 1000
    worstResult = None
    result = None
    saved_count = 0
    save_word_list = copy.deepcopy(words)
    best_crossword_list = None
    scores = []
    for i in range(iterations):
        print("Iteration", i + 1, "of", iterations)
        words = copy.deepcopy(save_word_list)
        crossword, count, crossword_list = generate(words, maxWords, sort_words)
        print(crossword)
        score = generate_score(crossword)
        scores.append(score)
        print(score)
        print(threshold * maxWords)
        if (score > maxScore and count > threshold * maxWords):
            maxScore = score
            result = crossword
            saved_count = count
            best_crossword_list = crossword_list
        if (score < minScore):
            minScore = score
            worstResult = crossword
            saved_worst_count = count
    return result, saved_count, worstResult, saved_worst_count, scores, best_crossword_list

def get_definition(word):
    api = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + word
    response = requests.get(f"{api}")
    if (response.status_code == 200):
        response = response.json()[0]
        definition = response['meanings'][0]['definitions'][0]['definition']
        return definition
    else:
        return None
        print(f"Hello person, there's a {response.status_code} error with your request")

def question_to_word(crossword_list):
    # each word needs to have a number, direction, and definition
    x_y_pairs = {} 
    for word in crossword_list:
        x_y_str = str(crossword_list[word].x) + '_' + str(crossword_list[word].y)

        if x_y_str not in x_y_pairs:
            x_y_pairs[x_y_str] = {}
        x_y_pairs[x_y_str][word] = [crossword_list[word].direction]
    
    clues = []
    count = 1
    unfound_words = []
    for x_y in x_y_pairs:
        for word in x_y_pairs[x_y]:
            direction = x_y_pairs[x_y][word]
            definition = get_definition(word)
            if definition == None:
                unfound_words.append(word)
                definition = "No definition found. Giving this word to you: " + word
            clue = Clue(count, direction, definition, x_y, word)
            clues.append(clue)
        count += 1

    for clue in clues:
        print('num:', clue.num, 'x_y:', clue.x_y, 'word:', clue.word, 'direction', clue.across, clue.definition)
    return clues
        

def write_file(crossword, count, filename, maxWords):
    with open(filename + '.txt', 'w') as f:
        num_rows = len(crossword)
        num_cols = len(crossword[0])
        for row in range(num_rows):
            for col in range(num_cols):
                char = crossword[row][col]
                if (char != EMPTY_CHAR):
                    char += ' '
                if col == num_cols - 1:
                    f.write(char + '\n')
                else:
                    f.write(char + ' ')
        f.write('\n' + 'Total words: ' + str(count) + '/' + str(maxWords))

def print_empty(crossword, clues, filename):
    with open(filename + '.txt', 'w') as f:
        num_rows = len(crossword)
        num_cols = len(crossword[0])
        for clue in clues:
            x, y = clue.x_y.split('_')
            crossword[int(y)][int(x)] = clue.num
        for row in range(num_rows):
            for col in range(num_cols):
                char = crossword[row][col]
                if char != EMPTY_CHAR and not char.isnumeric():
                    char = '__'
                if char.isnumeric() and len(char) < 2:
                    char = str(char) + ' '
                if col == num_cols - 1:
                    f.write(char + '\n')
                else:
                    f.write(char + ' ')
        f.write('\nAcross\n')
        for clue in clues:
            if clue.across[0]:
                f.write(str(clue.num) + ': ' + clue.definition + '\n')
        
        f.write('\n\nDown\n')
        for clue in clues:
            if not clue.across[0]:
                f.write(str(clue.num) + ': ' + clue.definition + '\n')


def main():
    iterations = 1
    f = 'common_words.txt'
    threshold = 0
    words = load_file(f)
    maxWords = 25


    # sorted
    crossword, count, worst_crossword, worst_count, scores, crossword_list = repeated_generation(words, maxWords, iterations, .99, False)
    print(crossword)
    #write_stats(scores, iterations, 'sorted_stats' + '_' + str(iterations) + '_' + sample_size)
    write_file(crossword, count, 'crossword', maxWords)
    write_file(worst_crossword, worst_count, 'worst_crossword', maxWords)
    clues = question_to_word(crossword_list)
    print_empty(crossword, clues, 'empty_puzzle')

    # unsorted
    '''
    crossword, count, worst_crossword, worst_count, scores, crossword_list = repeated_generation(words, maxWords, iterations, .99, False)
    write_stats(scores, iterations, 'unsorted_stats' + '_' + str(iterations) + '_' + sample_size)
    write_file(crossword, count, 'crossword_unsorted', maxWords)
    write_file(worst_crossword, worst_count, 'worst_crossword_unsorted', maxWords)
    '''

if __name__ == '__main__':
    main()