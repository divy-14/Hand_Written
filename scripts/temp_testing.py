import tempfile
from PIL import Image
import time
import os

with tempfile.TemporaryDirectory() as tmpdirname:
    print('created temporary directory', tmpdirname)
    x = Image.open("C:\\Users\\divym\\HandWritten\\a1.jpg")
    x.save(os.path.join(tmpdirname, "a1.jpg"))
    time.sleep(30)
