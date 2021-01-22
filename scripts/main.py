import streamlit as st
from PIL import Image
import os
import imghdr
from io import BytesIO
import base64
from Default_test import do_shit
from test import compress_shit
import Default_test as dt

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

# faced problems with globals variables so used global variables from default test-> dt as
# dt.background = Image.open("Fonts/myfont/a4.jpg")
# to see the problem see python-test module in C drive

# general download function


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}"><input type="button" value="Download"></a>'


st.markdown("<h1 style='text-align: center; color: Blue;'> Digital to Handwritten text </h1>",
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right; color: Blue;'>by Divy Mohan Rai</h3>",
            unsafe_allow_html=True)

# EXPERIMENTS###################################################################
main_bg = "./images/pyto.png"
main_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)
###################################################################################

# creating a side bar for picking the style of image
style_name = st.sidebar.selectbox(
    'Select HandWriting',
    ("default", "")
)

# path_style = os.path.join(root_style, style_name+".jpg")

# Upload text file functionality
img = None
uploaded_file = st.file_uploader(
    "Choose a text file...", type=["txt"])

show_file = st.empty()

# checking if user has uploaded any file
if not uploaded_file:
    show_file.info("Please Upload the text document")


if uploaded_file is not None:

    size = f' Input File Size in MegaBytes is {"{0:.4f}".format(uploaded_file.size / (1024 * 1024))}'
    st.markdown("%s" % size,
                unsafe_allow_html=True)

    name, _ = uploaded_file.name.split('.')

    convert_button = st.button("Convert To Text")

    # user presses convert
    if convert_button:

        raw_text = str(uploaded_file.read(), "utf-8")

        lines = raw_text.split("\n")  # splitting text on the basis of new line

        dt.background = Image.open("Fonts/myfont/a4.jpg")

        dt.SheetWidth = dt.background.width
        dt.margin = 115
        dt.lineMargin = 115
        dt.allowedCharacters = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ
                                abcdefghijklmnopqrstuvwxyz
                                #:,.?-!()[]'<>=%^$@_;1234567890 "'''

        dt.wordsPerLine = 75
        dt.maxLenPerPage = 3349
        dt.pageNum = 1

        # filePath = "input.txt"
        dt.FontType = "Fonts/UV_font/"
        dt.lineGap = 120
        dt.writing = "UV"

        # Initializing x and y
        dt.x, dt.y = dt.margin + 20, dt.margin + dt.lineGap

        # Asking for the quality of the output
        dt.scale_percent = 45

        pdf_name = do_shit(lines, name)

        file_stats = os.stat(pdf_name)

        size_file = file_stats.st_size / (1024 * 1024)

        s = f'Output File Size in MegaBytes is {"{0:.2f}".format(size_file)}'
        st.markdown("%s" % s,
                    unsafe_allow_html=True)

        root = './Output'
        if size_file > 5:
            st.write("File size greater than 5 MB, Compressing......")
            compress_shit(name, pdf_name)
            path = os.path.join(root, name+'_compressed.pdf')
            st.markdown(get_binary_file_downloader_html(
                path, file_label='File'), unsafe_allow_html=True)

            os.remove(path)

        else:
            st.markdown(get_binary_file_downloader_html(
                pdf_name, file_label='File'), unsafe_allow_html=True)

        os.remove(pdf_name)
