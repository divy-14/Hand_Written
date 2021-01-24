import streamlit as st
from PIL import Image
import os
import imghdr
from io import BytesIO
import base64
import tempfile
from PdffromImage import do_work
import PdffromImage as dt
import docx2txt
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}"><input type="button" value="Download"></a>'


st.markdown("<h1 style='text-align: center; color: black; ''> Digital to Handwritten text  <br><br> No more Handwritten Assignments   \U0000270D </h1>",
            unsafe_allow_html=True)

st.markdown("<h3 style='text-align: right; color: black;'><b>by Divy Mohan Rai</b></h3>",
            unsafe_allow_html=True)

main_bg = "./images/t2.jpg"

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


# creating a side bar for picking the style of image
style_name = st.sidebar.selectbox(
    'Select HandWriting',
    ("Style-1", "Style-2", "Style-3", "Style-4", "Style-5")
)
root_style = "./images/"
path_style = os.path.join(root_style, style_name+".jpg")
root_font = "./Fonts/"

# Upload text file functionality
img = None
uploaded_file = st.file_uploader(
    "Choose a text file...", type=["txt", "docx"])

show_file = st.empty()

# checking if user has uploaded any file
if not uploaded_file:
    show_file.info(
        "Please Upload the text/docx document (no .doc only .docx and .txt) ")


if uploaded_file is not None:

    st.image(path_style, caption='Choosen Handwriting', use_column_width=True)

    ###########################
    file_details = {"Filename": uploaded_file.name,
                    "FileType": uploaded_file.type}
    st.write(file_details)

    if uploaded_file.type == "text/plain":
        raw_text = str(uploaded_file.read(), "utf-8")

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

        raw_text = docx2txt.process(uploaded_file)

    ###########################

    size = f' Input File Size in MegaBytes is {"{0:.4f}".format(uploaded_file.size / (1024 * 1024))}'
    st.markdown("%s" % size,
                unsafe_allow_html=True)

    name, _ = uploaded_file.name.split('.')

    convert_button = st.button("Convert To Text")

    # user presses convert
    if convert_button:

        lines = raw_text.split("\n")  # splitting text on the basis of new line

        dt.background = Image.open("./images/a4.jpg")

        dt.SheetWidth = dt.background.width
        dt.SheetHieght = dt.background.height

        dt.margin = 115
        dt.lineMargin = 115
        dt.allowedCharacters = '''ABCDEFGHIJKLMNOPQRSTUVWXYZ
                                abcdefghijklmnopqrstuvwxyz
                                #:,.?-!()[]'<>=%^$@_;1234567890 "'''

        dt.wordsPerLine = 75
        dt.maxLenPerPage = 3349
        dt.pageNum = 1

        dt.FontType = os.path.join(root_font, style_name)

        dt.lineGap = 120
        dt.writing = style_name

        # Initializing x and y
        dt.x, dt.y = dt.margin + 20, dt.margin + dt.lineGap

        # Asking for the quality of the output
        dt.scale_percent = 30
        dt.images_list = []

        final_image = do_work(lines, name)

        path = name + '_' + style_name + '_output.pdf'

        with tempfile.TemporaryDirectory() as tmpdirname:

            final_path = os.path.join(tmpdirname, path)
            final_image.save(final_path)

            file_stats = os.stat(final_path)

            size_file = file_stats.st_size / (1024 * 1024)

            s = f'Output File Size in MegaBytes is {"{0:.2f}".format(size_file)}'
            st.markdown("%s" % s,
                        unsafe_allow_html=True)

            st.markdown(get_binary_file_downloader_html(
                final_path, file_label='File'), unsafe_allow_html=True)
