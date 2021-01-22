from wand.image import Image

with Image(filename="C:\\Users\\divym\\HandWritten\\a2.jpg") as img:

    # tinted image using tint() function
    img.tint(color="yellow", alpha="rgb(40 %, 60 %, 80 %)")
    img.save(filename="tina2.jpeg")
