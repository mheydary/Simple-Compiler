#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =========================================================================================
# author: Mohammadreza Hajy Heydary
# group members: Melissa Riddle
# =========================================================================================
# The lexer function performs lexical analysis on the preprocessed code provided in as a
# list of strings. Lexer uses FSM to perform the analysis. The returned output is a
# list of tuples where the first entry is the token and the second entry is the lexeme
# =========================================================================================
# indexed from 1, adjust the indexes in the code accordingly
Table = [
    [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 1],
    [2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
# =========================================================================================
# column map of the symbols to index
col_map = {
    'l': 0, 'num': 1, '{': 2, '}': 3, '(': 4, ')': 5, '[': 6, ']': 7, ',': 8, ':': 9,
    ';': 10, '.': 11, '\'': 12, '+': 13, '-': 14, '=': 15, '/': 16, '>': 17, '<':18,
    '%': 19, '*': 20, 'eps': 21
}
# =========================================================================================
# special states
FINAL_STATE = {3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24}
SEP_STATES = {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}
OPERATOR_STATES = {17, 18, 19, 20, 21, 22, 23, 24}
# =========================================================================================
# set of all key words
KEY_WORDS = {'int', 'float', 'bool', 'if', 'else', 'then', 'do', 'while', 'whileend',
             'doend', 'for', 'and', 'or', 'function', 'ifend'}
# =========================================================================================
# determine whether the input is a number
def isDigit(char):
    if char.isdigit():
        return True
    else:
        return False
# =========================================================================================
# determine whether the input is a letter or $
def isL(char):
    if char.isalpha() or char == '$':
        return True
    else:
        return False
# =========================================================================================
def numType(digit):
    dot_ctr = 0
    for char in digit:
        if char == '.':
            dot_ctr += 1

    if dot_ctr == 1:
        return "REAL"
    elif dot_ctr == 0:
        return "INTEGER"
    else:
        print("Error in the floating point number '{}' representation.".format(digit))
        raise ValueError
# =========================================================================================
def parser(line):
    if len(line) == 0:
        return None

    state = 1
    previous_idx = 0
    current_idx = 0
    tokens = []
    while current_idx < len(line):
        # map the current char to a column
        col_num = None
        if isL(line[current_idx]):
            col_num = col_map['l']
        elif isDigit(line[current_idx]):
            col_num = col_map['num']
        elif line[current_idx] == ' ':
            col_num = col_map['eps']
        else:
            col_num = col_map[line[current_idx]]

        # move to the next state
        state = Table[state - 1][col_num]

        # is this a final state? or end of file
        if not (state in FINAL_STATE):
            # if this is the last char, pass an absence of input (move to the final state)
            if (current_idx + 1) == len(line):
                state = Table[state - 1][col_map['eps']]
                current_idx += 1
            else:
                current_idx += 1
                continue

        # ==== the current state at this point is final, resolve and move forward ===

        # ignore any white spaces at the beginning of the token
        while previous_idx < current_idx:
            if line[previous_idx] == ' ':
                previous_idx += 1
            else:
                break

        # if all the characters were white space and removed, end of the line is reached
        if (previous_idx == current_idx) and (state == 1):
            break

        # keyword or identifier
        if state == 3:
            # determine whether this identifier is a keyword
            if line[previous_idx:current_idx] in KEY_WORDS:
                tokens.append(('KEY_WORD', line[previous_idx:current_idx]))
            else:
                tokens.append(('IDENTIFIER', line[previous_idx:current_idx]))

            # move to the next element in the line
            previous_idx = current_idx
            state = Table[state -1][col_num]

        # number
        elif state == 5:
            # determine the number type and add it to the list
            tokens.append((numType(line[previous_idx:current_idx]), line[previous_idx:current_idx]))
            # move to the next element in the line
            previous_idx = current_idx
            state = Table[state - 1][col_num]

        # determine separators
        elif state in SEP_STATES:
            tokens.append(('SEPARATOR', line[previous_idx:current_idx + 1]))
            current_idx += 1
            previous_idx = current_idx
            state = Table[state - 1][col_num]

        # determine operators
        elif state in OPERATOR_STATES:
            tokens.append(('OPERATOR', line[previous_idx:current_idx + 1]))
            current_idx += 1
            previous_idx = current_idx
            state = Table[state - 1][col_num]
        else:
            # if the loop reaches this point, something has gone wrong
            print('The state is: {}'.format(state))
            print(line)
            print(previous_idx)
            print(current_idx)
            print('Something went wrong while processing the states')
            raise StopIteration

    return tokens
# =========================================================================================
def lexer(code_list=None):
    if not code_list:
        raise ValueError

    parsed_code = []
    for line in code_list:
        tmp = parser(line)
        if tmp == None:
            continue

        parsed_code.extend(tmp)

    return parsed_code
