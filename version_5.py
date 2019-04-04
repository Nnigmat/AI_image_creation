from PIL import Image, ImageFilter, ImageOps
import numpy as np
import random
from good_colors import good_colors
from multiprocessing import Process
import datetime

image = 'input.jpg'
num_populations = 10
num_generations = 10
blur = False
size = 512

def count_colors(im):
    '''
    ' Return number of unique colors into the image
    '''
    colors_in_im = dict()
    for row in im:
        for pixel in row:
            if tuple(pixel) in colors_in_im:
                colors_in_im[tuple(pixel)] += 1
            else:
                colors_in_im[tuple(pixel)] = 1
    return colors_in_im

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
    for i in range(len(arr)):
        p = Process(target=_fitness, args=(arr[i], i, ))
        p.start()
        p.join()
        
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
        temp = np.absolute((mother +
        np.array(Image.fromarray(father.astype('uint8')).rotate(90-random.randint(-10, 10))) + random.randint(-10, 20)) // 2 % 256)
        res.append(temp)
    return res

if __name__ == '__main__':
    start = datetime.datetime.now()
    im = Image.open(image)
    im = im.convert('RGB')
    print(f'[+] Open image {image}.')
    im = im.filter(ImageFilter.BoxBlur(2))
    im = ImageOps.invert(im)

    im2arr = np.array(im)
    print('[+] Create numpy array of image')
    mother, father = im2arr, None

    counter = 0 
    for i in range(num_generations):
        childs = generate_childrens(mother, father)
        mother, father = fitness(childs)
        '''
        counter += 1
        if counter % 10 == 0:
            im = Image.fromarray(mother.astype('uint8'))
            im.save(f'results/{counter}.png')
        '''

    im = Image.fromarray(mother.astype('uint8'))
    print(f'Result is {datetime.datetime.now()-start}')
    im.show()



