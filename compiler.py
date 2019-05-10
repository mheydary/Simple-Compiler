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
# =========================================================================================
# The compiler function is the main function that calls different procedures to convert the
# HLL to assembly code in multiple stages. This function shall be completed later in  the
# semester
# =========================================================================================
from preprocessor import preprocessor
from lexer import lexer
from syntaxanalyzer import parser
# =========================================================================================
COMMENTS = {'!'}
# =========================================================================================
def compiler(buffer=None):
    if not buffer:
        raise ValueError

    preprocessed_code = preprocessor(buffer=buffer)
    # print(preprocessed_code)
    token_lexeme_code = lexer(preprocessed_code)
    # print(token_lexeme_code)
    parsed_code = parser(token_lexeme_code)
    # print(parsed_code)

    return parsed_code


