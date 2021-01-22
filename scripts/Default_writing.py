from PIL import Image
from fpdf import FPDF
import sys
import cv2
import os
import time

background = Image.open("Fonts/myfont/a4.jpg")
SheetWidth = background.width
margin = 115
lineMargin = 115
allowedCharacters = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ 
                        abcdefghijklmnopqrstuvwxyz 
                        #:,.?-!()[]'<>=%^$@_ 1234567890 "'''

lineGap = 150
wordsPerLine = 96
maxLenPerPage = 3349
pageNum = 1

print("#"*16, "WELCOME TO TEXT TO HANDWRITTEN NOTES", "#"*16)
print("#"*70)
print()
print("[[+]] Program Started ")
print()
print()

FontType = "Fonts/myfont/"
writing = "default"
# Initializing x and y
x, y = margin + 20, margin + lineGap

filePath = "input.txt"
print("Input file path is ./"+filePath)

# Asking for the quality of the output
scale_percent = int(
    input("What percent of quality (btw 40 to 100) you want in output file ? "))

if scale_percent < 0 or scale_percent > 100 or scale_percent < 40:
    print("[-] Please enter the quality btw given range .....")
    time.sleep(5)
    sys.exit()

# Just to add a space


def space():
    global x, y

    space = Image.open("Fonts/myfont/space.png")
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


def check_pageExceed():
    global writing, background, pageNum, margin, lineGap, x, y
    if y >= 3100:
        background.save("Output/{}_output_{}.png".format(writing, pageNum))
        print("[+] Saved page ->", pageNum)
        bg = Image.open("Fonts/myfont/a4.jpg")
        background = bg
        x, y = margin, margin + lineGap
        pageNum += 1


wasDQ = False


def ProcessNwrite(word):
    global x, y, background, pageNum, writing, margin, lineGap, wasDQ

    if x > SheetWidth - wordsPerLine*len(word):
        newLine()

    check_pageExceed()

    path = FontType
    for letter in word:
        if letter in allowedCharacters:
            if letter.isupper():
                path += "upper/{}".format(letter)
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
        newLine
    else:
        data = data.split(" ")
        check_pageExceed()

        for word in data:
            ProcessNwrite(word)
            space()


if __name__ == "__main__":
    try:
        filePath = "input.txt"
        file = open(filePath, "r")
        content = file.read()

        l = len(content)
        content = content.split("\n")

        print("[+] Text Reading Completed.")

        for i in range(len(content)):
            # skipping blank lines
            print(content[i])
            if content[i] == ' ':
                print("True")
                continue
            writeByLine(content[i])
            newLine()  # add a new line for every line

        print("[+] Saved page ->", pageNum)
        background.save("Output/{}_output_{}.png".format(writing, pageNum))

        print("\n[+] Adding lines....")
        # Drawing line on the output
        ImagesPath = [
            "Output/{}_output_{}.png".format(writing, page) for page in range(1, pageNum+1)]
        for path in ImagesPath:
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            x, y = 0, 228

            # Drawing vertical line
            cv2.line(img, (lineMargin-20, 0),
                     (lineMargin-20, 3508), (0, 0, 0), 3)
            cv2.line(img, (x, y), (x+2480, y), (0, 0, 0), 2)

            while y <= 3349:
                cv2.line(img, (x, y), (x+2480, y), (0, 0, 0), 2)
                y += lineMargin

            cv2.imwrite(path, img)

        # Saving results as a pdf
        height, width = Image.open(ImagesPath[0]).size
        pdf = FPDF(unit="pt", format=(height, width))

        for i in range(0, pageNum):
            pdf.add_page()
            pdf.image(ImagesPath[i], 0, 0)

        print("[+] Revoming unnecessary files")
        for path in ImagesPath:
            os.remove(path)

        print("\n[+] Saving the pdf...")
        pdf_name = "PDF_outputs/{}_Output.pdf".format(writing)
        pdf.output(pdf_name, "F")
        print("[+] Done...")
        print("[+] Find your output at " + pdf_name)
        time.sleep(5)
    except Exception as E:
        print(E, "\nTry again...")


# Made By -> Yuvraj Singh Kiraula
