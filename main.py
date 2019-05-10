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
# main function is used to test the compiler
# the function reads in the test file, pass it through the compiler and saves the results
# in another file
# =========================================================================================
from compiler import compiler
# =========================================================================================
def main():
    user_input = input("Please enter the name of the source code or Q to quit: ")
    while user_input != 'q' and user_input != 'Q':
        try:
            codeFile = open(user_input, 'r')
            print("Calling the compiler...")
            parsed_code = compiler(buffer=codeFile)
            codeFile.close()

            outName = "processed_{}".format(user_input)
            file_boj = open(outName, 'w')
            for p_code in parsed_code:
                # skip the parser markers in the final report unless it indicates an error
                # which is denoted by anything other than $ at p_code[0][1]
                if p_code[0][0] == 'PARSER' and p_code[0][1] == '$':
                    continue
                file_boj.write("Token: {:<15}\t\tLexeme: {:<15}\n".format(p_code[0][0], p_code[0][1]))
                for elem in p_code[1]:
                    file_boj.write("\t{}\n".format(elem))

            file_boj.close()
            print("Done! The result is written to the file <{}>".format(outName))
        except FileNotFoundError:
            print("Invalid file name! Try again.")

        user_input = input("\nPlease enter the name of the source code or Q to quit: ")


if __name__=="__main__":main()
