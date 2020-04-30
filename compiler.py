import sys
import pandas as pd

token = []
value = []
index = 0

# input part
print("//press ctrl+d to compile")
print("input source code:\n")
string = sys.stdin.readlines()

tmp = "".join(string)
raw_code = list(tmp)
print(raw_code)

def char_or_not(char): #숫자, 문자, 언더바 판단
    if 48 <= ord(char) <= 57 or 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122 or ord(char) == 95:
        return True
    else:
        return False


# defining special char token as ; + - * / { } ( ) , << >> <= >= && || == !=
def non_char_token(token, value, index, raw_code):
    char = raw_code[index]
    if char == ';':
        token.append("TERMINATING")
        value.append(";")
        return int(index + 1)
    elif char == '+' or char == '-' or char == '*' or char == '/':
        token.append("A_O")
        value.append(char)
        return int(index + 1)
    elif char == '{':
        token.append("LBRAKET")
        value.append("{")
        return int(index + 1)
    elif char == '}':
        token.append("RBRAKET")
        value.append("}")
        return int(index + 1)
    elif char == '(':
        token.append("LPAREN")
        value.append("(")
        return int(index + 1)
    elif char == ')':
        token.append("LPAREN")
        value.append(")")
        return int(index + 1)
    elif char == ',':
        token.append("SEPERATING")
        value.append(",")
        return int(index + 1)
    elif char == '.':
        if 48 <= ord(raw_code[index+1]) <= 57:
            print("Lexical error!! float number must start with digit!")
        return int(index + 1)
    elif char == '<':
        if raw_code[index+1] == '<':
            token.append("B_O")
            value.append('<<')
            return int(index + 2)
        elif raw_code[index+1] == '=':
            token.append('C_O')
            value.append("<=")
            return int(index + 2)
        else:
            token.appen("C_O")
            value.append('<')
            return int(index + 1)
    elif char == '>':
        if raw_code[index+1] == '>':
            token.append("B_O")
            value.append(">>")
            return int(index + 2)
        elif raw_code[index+1] == '=':
            token.append("C_O")
            value.append(">=")
            return int(index + 2)
        else:
            token.append("C_O")
            value.append(">")
            return int(index + 1)
    elif char == "=":
        if raw_code[index+1] == "=":
            token.append("C_0")
            value.append("==")
            return int(index + 2)
        else:
            token.append("Assign_O")
            value.append("=")
            return int(index + 1)
    elif char == "!":
        if raw_code[index+1] == "=":
            token.append("C_O")
            value.append("!=")
            return int(index + 2)
    elif char == "&":
        if raw_code[index+1] == "&":
            token.append('B_O')
            value.append("&&")
            return int(index + 2)
    elif char == "|":
        if raw_code[index+1] == "|":
            token.append("B_O")
            value.append("||")
            return int(index + 2)
    # defining whitespace
    elif char == " " or char == "\t" or char == "\n":
        #token.append("WHITESPACE")
        #value.append(" ")
        return int(index + 1)
    else:
       return int(index + 1)

#defining type, id, keyword
def char_token(token, value, index, raw_code):
    character = True
    block = []
    tmp = int(index)
    while character:
        block.append(raw_code[tmp])
        if char_or_not(raw_code[tmp + 1]):
            tmp = int(tmp + 1)
        else:
            character = False

    chunk = "".join(block)
    if chunk == 'int':
        token.append("TYPE")
        value.append("int")
        return int(tmp+1)
    elif chunk == 'float':
        token.append("TYPE")
        value.append("float")
        return int(tmp+1)
    elif chunk == 'bool':
        token.append("TYPE")
        value.append("bool")
        return int(tmp+1)
    elif chunk == 'string':
        token.append("TYPE")
        value.append("string")
        return int(tmp+1)
    elif chunk == 'if':
        token.append("KEYWORD")
        value.append("if")
        return int(tmp+1)
    elif chunk == 'else':
        token.append("KEYWORD")
        value.append("else")
        return int(tmp+1)
    elif chunk == 'for':
        token.append("KEYWORD")
        value.append("for")
        return int(tmp+1)
    elif chunk == 'while':
        token.append("KEYWORD")
        value.append("while")
        return int(tmp+1)
    elif chunk == 'return':
        token.append("KEYWORD")
        value.append("return")
        return int(tmp+1)
    elif chunk == 'true':
        token.append('BOOL')
        value.append('true')
        return int(tmp+1)
    elif chunk == 'false':
        token.append('BOOL')
        value.append('false')
        return int(tmp+1)
    else:
        token.append("IDENTIFIER")
        value.append(chunk)
        return int(tmp+1)

#defining string
def string_token(token, value, index, raw_code, ascii):
    ended = True
    block = []
    tmp = index
    while ended:
        try:
            block.append(raw_code[tmp])
            asci = ord(raw_code[tmp + 1])
        except IndexError:
            print("Lexical error!!", chr(34), "expected!!")
            return int(tmp + 2)

        if asci == ascii:
            ended = False
        else:
            tmp = int(tmp + 1)
    block.append(chr(ascii))
    chunk = "".join(block)
    token.append("LITERAL STRING")
    value.append(chunk)
    return int(tmp + 2)

#defining numbers like int, float
def numeric_token(token, value, index, raw_code, ascii):
    tmp = index
    block = []
    dot = False
    if ascii == 45:
        block.append(raw_code[tmp])
        tmp += 1
    if raw_code[tmp] == "0":
        block.append(raw_code[tmp])
        if ord(raw_code[tmp + 1]) == 46:
            dot = True
            #block.append(raw_code[tmp+1])
            tmp += 1
        elif ord(raw_code[tmp+1]) != 46 and (ord(raw_code[tmp+1]) <=47 or ord(raw_code[tmp+1]) >= 58):
            return int(tmp + 1)
        else:
            print("Lexical error!! number cannot start with 0!!")
            return int(tmp + 1)
    ended = False
    while not ended:
        block.append(raw_code[tmp])
        if ord(raw_code[tmp + 1]) == 46 and dot == False:
            dot = True
            tmp += 1
        elif ord(raw_code[tmp + 1]) == 46 and dot == True:
            print("Lexical error!! float point number must have one dot!!")
            return int(tmp + 1)
        elif ord(raw_code[tmp+1]) != 46 and (ord(raw_code[tmp+1]) <=47 or ord(raw_code[tmp+1]) >= 58):
            ended = True
        else:
            tmp += 1
    chunk = "".join(block)
    if dot == True and block[-1] == "0" and ord(block[-2]) != 46:
        print("Lexical error!! float must end with non zero digit!!")
        return int(tmp+1)
    if dot == True:
        token.append("FLOAT")
        value.append(chunk)
        return int(tmp + 1)
    else:
        token.append("INT")
        value.append(chunk)
        return int(tmp + 1)





#logic part
while index < len(raw_code):
    ascii = ord(raw_code[index]) #파악할 character를 아스키 문자로 변환
    if (40 <= ascii <= 47) or (58 <= ascii <= 62) or (123 <= ascii <= 125) or ascii == 33: #초기조건: 특수문자 판단 {ao, bo, assign o, co, terminate, lbraket, rbraket, lparen, rparen, seperating, whitespace} 구현
        index = non_char_token(token, value, index, raw_code)
    elif ascii == 34 or ascii == 39:# 초기조건: " 나 ' 가 들어오면 string으로 받음
        index = string_token(token, value, index, raw_code, ascii)
    elif 65 <= ascii <= 90 or 97 <= ascii <= 122 or ascii == 95: #초기조건: 문자인지, 언더바 인지 판단 {type, id, keyword} 구현
        index = char_token(token, value, index, raw_code)
    elif ascii == 45 or 48 <= ascii <= 57: # 초기조건: -부호나 숫자 들어오면 숫자 핀별기로 들어감
        index = numeric_token(token, value, index, raw_code, ascii)
    else: # 정의되지 않은것이 들어오면 그냥 넘김
        index = index + 1




#pandas이용해서 테이블 정리... 추후에 sytax analzer로 넘길때 csv파일로 넘길수 있음
raw_data = {
    'token:': token,
    'value': value
}
token_table = pd.DataFrame(raw_data)
print(token_table)





