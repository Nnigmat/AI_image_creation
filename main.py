from PIL import Image, ImageFilter, ImageOps
import numpy as np
import random
from good_colors import good_colors
from multiprocessing import Process
import datetime

image = 'lev.png'
num_populations = 10
num_generations = 10
blur = True
invert = False
size = 512


def fitness(arr):
    res = [0 for i in range(len(arr))]

    def _fitness(el, i):
        good = 0
        for i in range(size):
            for j in range(size):
                if tuple(el[i][j]) in good_colors:
                    good += 1
        res.append(good)

    print('[+] Start calculating fitness for childrens')
    procs = []
    for i in range(len(arr)):
        procs.append(Process(target=_fitness, args=(arr[i], i, )))
        procs[i].start()

    for i in range(len(procs)):
        procs[i].join()
        
    best = res.index(max(res))
    res[best] = -1
    second_best = res.index(max(res))
    print('[+] Stop calculating fitness for childrens')
    return arr[best], arr[second_best]

    
def generate_childrens(mother, father=None):
    if isinstance(father, type(None)):
        father = mother
    res = []
    for i in range(num_populations):
        rotated_father = np.array(Image.fromarray(father.astype('uint8')).rotate(90-random.randint(-5, 5)))
        noise = np.random.randint(low=-10, high=10, size=(512,512, 3))
        temp = np.absolute((mother + rotated_father) + noise)
        temp = temp // 2 % 256
        res.append(temp)
    return res

if __name__ == '__main__':
    start = datetime.datetime.now()
    im = Image.open(image)
    im = im.convert('RGB')
    print(f'[+] Open image {image}.')
    if blur:
        im = im.filter(ImageFilter.BoxBlur(3))
    if invert:
        im = ImageOps.invert(im)

    im2arr = np.array(im)
    print('[+] Create numpy array of image\n')
    mother, father = im2arr, None

    counter = 0 
    for i in range(num_generations):
        print(f'[+] {i+1} generation.')
        childs = generate_childrens(mother, father)
        mother, father = fitness(childs)
        print('\n')


    im = Image.fromarray(mother.astype('uint8'))
    print(f'Result is {datetime.datetime.now()-start}')
    im.show()
