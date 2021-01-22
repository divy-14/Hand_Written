from PIL import Image
from fpdf import FPDF
import sys
import cv2
import os
import time
import unicodedata
from concatenate_images import get_concat_v

background = Image.open("Fonts/myfont/a4.jpg")
SheetWidth = background.width
margin = 115
lineMargin = 115
allowedCharacters = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ
                        abcdefghijklmnopqrstuvwxyz
                        #:,.?-!()[]'<>=%^$@_;1234567890 "'''

wordsPerLine = 75
maxLenPerPage = 3349
pageNum = 1
images_list = []

filePath = "input.txt"
FontType = "Fonts/UV_font/"
lineGap = 120
writing = "UV"

# print("Input file path is ./"+filePath)

# Initializing x and y
x, y = margin + 20, margin + lineGap


# Asking for the quality of the output
scale_percent = 45

# Just to add a space


def space():
    global x, y

    space = Image.open("Fonts/myfont/space.png")
    width = space.width
    x += width
    background.paste(space, (x, y))
    del space


def newLine():
    # print("nl added")
    global x, y
    x = margin + 20
    y += margin


def writeAlphabet(path):
    global x, y
    letter = Image.open(path)
    background.paste(letter, (x, y))
    x += letter.width


def check_pageExceed():
    global writing, pageNum, background, x, y, margin, lineGap, images_list
    # new page
    if y >= 3100:
        # will run when we have more than 1 page
        images_list.append(background)
        background.save("Output/{}_output_{}.png".format(writing, pageNum))
        print("[+] Saved page ->", pageNum)

        bg = Image.open("Fonts/myfont/a4.jpg")
        background = bg
        x, y = margin, margin + lineGap
        pageNum += 1


wasDQ = False


def ProcessNwrite(word):
    global x, y, background, pageNum, writing, margin, lineGap, wasDQ

    # change Line function
    if x > SheetWidth - wordsPerLine*len(word):
        newLine()

    check_pageExceed()

    path = FontType

    for letter in word:
        if letter in allowedCharacters:
            if letter.isupper():
                path += "upper/{}".format(letter)
                # print(path)
            elif letter.islower():
                path += "lower/{}".format(letter)
            elif letter.isnumeric():
                path += "digits/{}".format(letter)
            else:
                path += "symbols/"
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
                elif letter == "'":
                    path += "osq"
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
                    path += "cdq"
                    wasDQ = False
                elif letter == '"':
                    path += "odq"
                    wasDQ = True
            path += ".png"

            writeAlphabet(path)
            path = FontType
        else:
            writeAlphabet("Fonts/myfont/space.png")


def writeByLine(data):
    global x, y, background, pageNum, writing

    if data == "":
        return

    else:
        data = data.split(" ")
        check_pageExceed()

        for word in data:
            # get rids of extra whitespaces
            if word == "":
                continue
            ProcessNwrite(word)
            space()


def do_shit(content, name):

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
    get_concat_v(images_list, res_width, res_height, name)
    ########################

    # this is to save the last page
    background.save("Output/{}_output_{}.png".format(writing, pageNum))
    ImagesPath = [
        "Output/{}_output_{}.png".format(writing, page) for page in range(1, pageNum+1)]

    for path in ImagesPath:
        print(path)
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        x, y = 0, 228

        # Drawing vertical line
        cv2.line(img, (lineMargin-20, 0),
                 (lineMargin-20, 3508), (0, 0, 0), 3)
        cv2.line(img, (x, y), (x+2480, y), (0, 0, 0), 2)

        while y <= 3349:
            cv2.line(img, (x, y), (x+2480, y), (0, 0, 0), 2)
            y += lineMargin

        # Percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        mimage = cv2.resize(img, dim, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(path, mimage)

    # Saving results as a pdf
    height, width = Image.open(ImagesPath[0]).size
    print("hw", height, width)
    pdf = FPDF(unit="pt", format=(height, width))

    for i in range(0, pageNum):
        pdf.add_page()
        pdf.image(ImagesPath[i], 0, 0)

    print("\n[+] Saving the pdf...")

    # writing is the handwriting
    pdf_name = "PDF_outputs/{}_{}_Output.pdf".format(writing, name)
    print(pdf_name)
    pdf.output(pdf_name, "F")
    print("\n[+] Removing unnecessary files")
    for path in ImagesPath:
        os.remove(path)

    print("[+] Done...")
    pdf.close()
    return pdf_name


if __name__ == "__main__":
    try:
        file = open(filePath, "r")
        content = file.read()

        l = len(content)
        content = content.split("\n")

        print("[+] Text Reading Completed.")
        for i in range(len(content)):
            writeByLine(content[i])
            newLine()
        print("[+] Saved Page ->", pageNum)

        background.save("Output/{}_output_{}.png".format(writing, pageNum))

        # Drawing line on the output
        ImagesPath = [
            "Output/{}_output_{}.png".format(writing, page) for page in range(1, pageNum+1)]

        print("\n[+] Adding lines....")
        for path in ImagesPath:
            print(path)
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            x, y = 0, 228

            # Drawing vertical line
            cv2.line(img, (lineMargin-20, 0),
                     (lineMargin-20, 3508), (0, 0, 0), 3)
            cv2.line(img, (x, y), (x+2480, y), (0, 0, 0), 2)

            while y <= 3349:
                cv2.line(img, (x, y), (x+2480, y), (0, 0, 0), 2)
                y += lineMargin

            # Percent of original size
            print(scale_percent)
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)

            mimage = cv2.resize(img, dim, interpolation=cv2.INTER_NEAREST)
            cv2.imwrite(path, mimage)

        # Saving results as a pdf
        height, width = Image.open(ImagesPath[0]).size
        pdf = FPDF(unit="pt", format=(height, width))

        for i in range(0, pageNum):
            pdf.add_page()
            pdf.image(ImagesPath[i], 0, 0)

        print("\n[+] Saving the pdf...")
        pdf_name = "PDF_outputs/{}_Output.pdf".format(writing)
        pdf.output(pdf_name, "F")

        print("\n[+] Removing unnecessary files")
        for path in ImagesPath:
            os.remove(path)

        print("[+] Done...")
        print("[+] Find your output at " + pdf_name)
        time.sleep(5)
    except Exception as E:
        print(E, "\n[-] Try again...")
