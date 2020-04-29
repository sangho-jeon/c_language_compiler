import sys
import pandas as pd


#raw_data = {
#    'IDENTIFIER:': ["num", "foo"],
#    'TYPE:': ["int", 'float']
#}
#table = pd.DataFrame(raw_data)

print("//press ctrl+d to compile")
print("input source code:\n")


string = sys.stdin.readlines()

tmp = "".join(string)
char = list(tmp)
print(char)

