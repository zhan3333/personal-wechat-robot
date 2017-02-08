import os
import random


def get_img_list(path):
    return os.listdir(path)


def get_random_one_img_list(path):
    img_list = get_img_list(path)
    img_length = len(img_list)
    img_number = random.randint(0, img_length-1)
    return path + img_list[img_number]

if __name__ == '__main__':
    path = 'E:/Pictures/is me/'
    print(get_random_one_img_list(path))