from PIL import Image, ImageFilter, ImageOps
import numpy as np
import random

image = 'homer.png'
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
    print('[+] Start calculating fitness for childrens')
    radius = 16
    res = []
    for el in arr:
        density = 0
        for i in range(0, size, radius):
            unique = dict()
            for j in range(0, size, radius):
                for x in range(i, i+radius):
                    for y in range(j, j+radius):
                        if tuple(el[x][y]) in unique:
                            unique[tuple(el[x][y])] += 1
                        else:
                            unique[tuple(el[x][y])] = 1
                temp = max(unique.values())
                density += temp / radius**2
        res.append(density)
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
        temp = np.absolute((mother + np.rot90(father) + random.randint(-10, 20)) // 2 % 256)
        res.append(temp)
    return res


if __name__ == '__main__':
    im = Image.open(image)
    im = im.convert('RGB')
    print(f'[+] Open image {image}.')
    #im = im.filter(ImageFilter.BoxBlur(10))
    im = ImageOps.invert(im)

    im2arr = np.array(im)
    print('[+] Create numpy array of image')
    mother, father = im2arr, None

    for i in range(num_generations):
        childs = generate_childrens(mother, father)
        mother, father = fitness(childs)


    print(mother)
    im = Image.fromarray(mother.astype('uint8'))
    im.show()



