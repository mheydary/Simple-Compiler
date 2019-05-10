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
# Given a buffer of input, the preprocessor function reads in the file, removes all the
# comments denoted in the comment symbol set, removes blank lines and returns the results
# as a list of lists where each string in the list is a line of code.
# =========================================================================================
comment_symbol = {'!'}
# =========================================================================================
def preprocessor(buffer=None):
    preprocessed_code = []

    in_block_comment = False
    for line in buffer:
        p_line = str()
        comment_found = False
        for char in line:
            # remove tabs (\t)
            if char == '\t':
                continue

            # check if end of line has reached
            if char == '\n':
                # comment has not finished yet, block comment
                if comment_found:
                    in_block_comment = True

                # move to the next line
                continue

            # in a multi-line comment block, ignore characters
            if in_block_comment and not(char in comment_symbol):
                continue

            # end of block comment, set the flags and move on
            if in_block_comment and (char in comment_symbol):
                comment_found = False
                in_block_comment = False
                continue

            # start of a new line of comment
            if (not comment_found) and (char in comment_symbol):
                comment_found = True
                continue

            # end of comment line detected
            if comment_found and (char in comment_symbol):
                comment_found = False
                continue

            # we are in a comment line, continue
            if comment_found:
                continue

            # this char is not a comment or \n or \t, add it to the line
            p_line += char
            # print(p_line)

        # if the returned line is empty, do not insert in the processed line
        if p_line == '':
            continue

        preprocessed_code.append(p_line)

    # print(preprocessed_code)
    return preprocessed_code
