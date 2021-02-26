import datetime
import random
import string
import sys
from os import listdir
from os.path import isdir, isfile, join

from PIL import Image
from random_word import RandomWords


def display_vinyls(vinyls, output, input_path):
    background = Image.new('RGBA', (3200, 3200), (245, 245, 220, 255))
    n = len(vinyls)
    coords = [(320, 320), (320, 1280), (320, 2240), (1280, 320),
              (1280, 1280), (2240, 320), (2240, 1280)]
    # TODO generate coords
    assert(n == len(coords))
    for i in range(n):
        ip = input_path + vinyls[i]
        curr = Image.open(ip, "r")
        background.paste(curr, coords[i])
    background.save('./complete/{}.png'.format(output))
    print("Output to ./complete/" + output)


def get_filenames(input_path):
    files = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    return files  # list of strings that correspond to each file name


def pick_vinyls(choices, k):
    return random.sample(choices, k)


def main():
    if len(sys.argv) != 2 or not isdir(sys.argv[1]):
        print("Usage:\npython3 display_images.py \"./path_to_input_images\"")
        exit()
    random_label = True
    manual = "manual_title"
    input_path = sys.argv[1]
    k = 7
    n = 1
    all_saved_vinyls = get_filenames(input_path)

    for _ in range(n):
        r = RandomWords()
        label = r.get_random_word() if random_label else manual
        display_vinyls(pick_vinyls(all_saved_vinyls, k), label, input_path)


if __name__ == "__main__":
    main()
