from PIL import Image
import sys
import cv2
import os
import time
import unicodedata
from concatenate_images import get_concat_v

background = Image.open("./images/a4.jpg")
SheetWidth = background.width
SheetHeight = background.height
margin = 115
lineMargin = 115
allowedCharacters = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ
                        abcdefghijklmnopqrstuvwxyz
                        #:,.?-!()[]'<>=%^$@_;1234567890 "'''

wordsPerLine = 75
maxLenPerPage = 3349
pageNum = 1
images_list = []

filePath = "big.txt"
FontType = "Fonts/Style-5/"
lineGap = 120
writing = "Style-5"


# Initializing x and y
x, y = margin + 20, margin + lineGap
scale_percent = 45


def space():
    # Just to add a space
    global x, y

    space = Image.open("./images/space.png")

    width = space.width
    x += width
    background.paste(space, (x, y))
    del space


def newLine():
    global x, y
    x = margin + 20
    y += margin


def writeAlphabet(path):
    global x, y
    letter = Image.open(path)
    background.paste(letter, (x, y))
    x += letter.width


def check_pageExceed(word="h"):
    global writing, pageNum, background, x, y, margin, lineGap, images_list

    if y >= 3100:
        images_list.append(background)
        bg = Image.open("./images/a4.jpg")
        background = bg
        x, y = margin+20, 0
        pageNum += 1


wasDQ = False  # false if we need to use opening inverted double quotes
wasSQ = False


def ProcessNwrite(word):
    global x, y, background, pageNum, writing, margin, lineGap, wasDQ, wasSQ

    check_pageExceed(word)

    # change Line function
    if x > SheetWidth - wordsPerLine*len(word):
        newLine()

    path = FontType

    for letter in word:
        if letter in allowedCharacters:
            if letter.isupper():
                path += "/upper/{}".format(letter)
            elif letter.islower():
                path += "/lower/{}".format(letter)
            elif letter.isnumeric():
                path += "/digits/{}".format(letter)
            else:
                path += "/symbols/"
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
            path += ".png"

            writeAlphabet(path)
            path = FontType
        else:
            writeAlphabet("./images/space.png")


def writeByLine(data):
    global x, y, background, pageNum, writing

    if data == "":
        return

    else:
        data = data.split(" ")
        check_pageExceed()

        for word in data:
            ProcessNwrite(word)
            space()


def do_work(content, name):

    blank_line = 0

    for i in range(len(content)):

        content[i] = unicodedata.normalize("NFKD", content[i])
        if content[i] == "":
            blank_line += 1

        else:
            blank_line = 0

        if blank_line > 1:
            continue

        writeByLine(content[i])
        newLine()

   #######################
    images_list.append(background)
    res_width = int(background.size[0] * scale_percent / 100)
    res_height = int(background.size[0] * scale_percent / 100)
    final_img = get_concat_v(images_list, res_width, res_height)
    ########################
    print("File Created Successfully")
    return final_img


if __name__ == "__main__":
    print("Hello there")

    file = open(filePath, "r")
    content = file.read()

    l = len(content)
    content = content.split("\n")
    blank_line = 0

    for i in range(len(content)):

        content[i] = unicodedata.normalize("NFKD", content[i])
        if content[i] == "":
            blank_line += 1

        else:
            blank_line = 0

        if blank_line > 1:
            continue

        writeByLine(content[i])
        newLine()

   #######################
    images_list.append(background)
    res_width = int(background.size[0] * scale_percent / 100)
    res_height = int(background.size[0] * scale_percent / 100)
    final_img = get_concat_v(images_list, res_width, res_height)
    ########################
    final_img.save('PDF_outputs/output.pdf')
    print("File Created Successfully")
