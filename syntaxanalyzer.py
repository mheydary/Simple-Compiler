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
# ======================================================================================================================
# author: Mohammadreza Hajy Heydary
# ======================================================================================================================
# Given a list of tokens and lexemes, use an LL1 parser to check the semantics of the input
# ======================================================================================================================
# the table contains the elements for valid entries as list in reverse order for simplicity
# of code. Epsilon is represented as empty list.
Table = [
    [[';', 'E', '=', 'id'], None, None, None, None, None, None, None, None, None, ['ifend', 'Z', 'U', 'S', 'then', 'E', 'if'], None, None, None, ['whileend', 'U', 'S', 'do', 'E', 'while'], None, None],
    [['Q', 'T'], None, None, None, None, ['Q', 'T'], None, None, None, None, None, None, None, None, None, None, None],
    [None, ['Q', 'T', '+'], ['Q', 'T', '-'], None, None, None, [], None, [], None, None, [], None, None, None, [], None],
    [['R', 'F'], None, None, None, None, ['R', 'F'], None, None, None, None, None, None, None, None, None, None, None],
    [None, [], [], ['R', 'F', '*'], ['R', 'F', '/'], None, [], None, [], None, None, [], None, None, None, [], None],
    [['id'], None, None, None, None, ['(', 'E', ')'], None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, ['U', 'S', 'else'], [], None, None, None],
    [['U', 'S'], None, None, None, None, None, None, None, None, None, ['U', 'S'], None, [], [], ['U', 'S'], None, []]
    ]
# ======================================================================================================================
row_map = {'S': 0, 'E': 1, 'Q': 2, 'T': 3, 'R': 4, 'F': 5, 'Z': 6, 'U': 7}
# ======================================================================================================================
col_map = {
    'id': 0, '+': 1, '-': 2, '*': 3, '/': 4, '(': 5, ')': 6, '=': 7, ';': 8, '$': 9, 'if': 10, 'then': 11, 'else': 12,
    'ifend': 13, 'while': 14, 'do': 15, 'whileend': 16
}
# ======================================================================================================================
terminals = {
    'id', '+', '-', '*', '/', '=', '(', ')', ';', '$', 'if', 'then', 'else', 'ifend', 'while', 'do', 'whileend'
}
# ======================================================================================================================
def token_map(token):
    if token[0] == 'IDENTIFIER':
        return 'id'
    elif token[0] == 'OPERATOR':
        return token[1]
    elif token[0] == 'SEPARATOR':
        return token[1]
    elif token[0] == 'PARSER':
        return token[1]
    elif token[0] == 'KEY_WORD':
        return token[1]

def make_report(stack_top, table_entry):
    # inverse the entry
    table_entry.reverse()
    if len(table_entry) == 0:
        table_entry = ['eps']

    tmp = ""
    for elem in table_entry:
        tmp += "< {} > ".format(elem)

    return "{} --> {}".format(stack_top, tmp)

def LL1(values):
    # print(values)
    values.extend([('PARSER', '$')])
    stack = ['$', 'S']
    cur_token_idx = 0
    parsed_code = []
    tmp_output = []
    while len(stack) != 0:
        if stack[-1] in terminals:
            if token_map(values[cur_token_idx]) == stack[-1]:
                # save the analysis for this token
                parsed_code.append([values[cur_token_idx], tmp_output])
                # erase the buffer
                tmp_output = []
                # ready for the next token
                stack.pop()
                cur_token_idx += 1
            else:
                tmp_output = [
                    'Error occurred. Top of the stack <{}> is terminal but does NOT match the current token <{}>'.format(stack[-1], token_map(values[cur_token_idx]))
                ]
                parsed_code.append([values[cur_token_idx], tmp_output])
                # end the parsing
                break

        else:
            table_entry = Table[row_map[stack[-1]]][col_map[token_map(values[cur_token_idx])]]
            if table_entry != None:
                # save the parsing results
                tmp_output.append(make_report(stack[-1], list(table_entry)))
                # update the top of the stack
                x = stack.pop()
                stack.extend(Table[row_map[x]][col_map[token_map(values[cur_token_idx])]])
            else:
                tmp_output = [
                    'Error occurred. Table entry is None when top of the stack is <{}> and the current token is <{}>'.format(stack[-1], token_map(values[cur_token_idx]))
                ]
                parsed_code.append([values[cur_token_idx], tmp_output])
                # end the parsing
                break

    if len(stack) != 0:
        tmp_output = ['Non-empty stack error. Stack = [{}]'.format(stack)]
        parsed_code.append([('None', 'None'), tmp_output])

    return parsed_code

def parser(values):
    parsed_code = []
    processed = 0
    current_idx = 0
    in_while = False
    in_if = False
    # make the parser capable of parsing many lines of code in the buffer.
    while current_idx < len(values):
        if values[current_idx][1] == 'while':
            in_while = True
            current_idx += 1
        elif values[current_idx][1] == 'whileend':
            in_while = False
            current_idx += 1
            parsed_code.extend(LL1(values[processed:current_idx]))
            processed = current_idx

        elif values[current_idx][1] == 'if':
            in_if = True
            current_idx += 1

        elif values[current_idx][1] == 'ifend':
            in_if = False
            current_idx += 1
            parsed_code.extend(LL1(values[processed:current_idx]))
            processed = current_idx

        elif not in_while and not in_if and values[current_idx][1] == ';':
            if (current_idx + 1 < len(values)) and (values[current_idx + 1][1] == 'else'):
                current_idx += 1

            else:
                current_idx += 1
                parsed_code.extend(LL1(values[processed:current_idx]))
                processed = current_idx

        else:
            current_idx += 1

    # make sure there is no code left at the end
    if processed != current_idx:
        parsed_code.extend(LL1(values[processed:]))

    return parsed_code
