import os
allowedletters = '''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#:,.?-!()[]'<>=%^$@_;1234567890"'''

root = "./Fonts"

for xpath in os.listdir(root):
    new_path = os.path.join(root, xpath)
    files = []
    files += os.listdir(new_path+'/upper/')
    files += os.listdir(new_path+'/lower/')
    files += os.listdir(new_path+'/digits/')
    files += os.listdir(new_path + '/symbols/')

    files = set(files)

    for letter in allowedletters:
        path = ""
        wasSQ = False
        wasDQ = False

        if letter == ",":
            path += "comma"
        elif letter == ".":
            path += "fullstop"
        elif letter == "!":
            path += "exclamation"
        elif letter == "-":
            path += "hiphen"
        elif letter == "#":
            path += "hash"
        elif letter == "?":
            path += "question"
        elif letter == "(":
            path += "bracketop"
        elif letter == ")":
            path += "bracketcl"
        elif letter == ":":
            path += "colon"
        elif letter == ";":
            path += "semicolon"
        elif letter == "{":
            path += "Cbracketop"
        elif letter == "}":
            path += "Cbracketcl"
        elif letter == "[":
            path += "osb"
        elif letter == "]":
            path += "csb"
        elif letter == "<":
            path += "oab"
        elif letter == ">":
            path += "cab"
        elif letter == "=":
            path += "equals"
        elif letter == "'" and wasSQ:
            path += "csq"
            wasSQ = False
        elif letter == "'":
            path += "osq"
            wasSQ = True
        elif letter == "%":
            path += "percent"
        elif letter == "&":
            path += "empersand"
        elif letter == "$":
            path += "dollar"
        elif letter == "@":
            path += "at"
        elif letter == "*":
            path += "asterisk"
        elif letter == "_":
            path += "underscore"
        elif letter == "^":
            path += "cap"
        elif letter == '"' and wasDQ:
            path += "cdq"  # closing double quotes
            wasDQ = False
        elif letter == '"':
            path += "odq"
            wasDQ = True
        else:
            path += letter
        if path+".png" not in files:
            print("Not found: ", letter, path, xpath)
