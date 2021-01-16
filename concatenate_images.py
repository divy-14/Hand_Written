from PIL import Image, ImageEnhance
import glob
import os


def get_concat_v(image_list, width, height):

    n = len(image_list)
    count = 1
    dst = Image.new('RGB', (width, height*n))
    curr_height = 0
    print("Starting Process ....")

    for img in image_list:
        print(f"Page Created: {count}, Page left: {n-count}")
        img = img.resize((width, height))
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # 2 here is increasing the contrast
        dst.paste(img, (0, curr_height))
        curr_height += (height-80)
        count += 1

    dst = dst.crop((0, 0, width, curr_height+80))
    return dst


if __name__ == '__main__':
    cv_img = []
    width = 512
    height = 512
