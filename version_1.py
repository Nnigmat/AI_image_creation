from PIL import Image, ImageFilter
import numpy as np
import random

image = 'input.jpg'
num_populations = 10
num_generations = 100
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
    radius = 8
    res = []
    for el in arr:
        density = 0
        for i in range(0, size, radius):
            unique = dict()
            for j in range(0, size, radius):
                if tuple(el[i][j]) in unique:
                    unique[tuple(el[i][j])] += 1
                else:
                    unique[tuple(el[i][j])] = 1
            temp = max(unique.values())
            density += temp / radius**2
        res.append(density)
    best = res.index(max(res))
    res.pop(best)
    second_best = res.index(max(res))
    print('[+] Stop calculating fitness for childrens')
    return arr[best], arr[second_best]

def generate_childrens(mother, father=None):
    if isinstance(father, type(None)):
        print('[+] Father is unknown')
        father = mother

    m_dict = count_colors(mother)
    print("[+] Get mother's unique colors")
    f_dict = count_colors(father)
    print("[+] Get father's unique colors")

    res_dict = dict()
    temp_dict = f_dict

    for key, value in m_dict.items():
        if key in temp_dict:
            res_dict[key] = (value + temp_dict[key]) // 2
            temp_dict.pop(key)
        else:
            res_dict[key] = value // 2
        
    for key, value in temp_dict.items():
        res_dict[key] = value // 2

    del temp_dict

    print('[+] Create resulted unique colors from parents')

    m_list = list(m_dict.keys())
    f_list = list(f_dict.keys())
    while sum(res_dict.values()) < size*size:
        print(f'[+] Not enough colors in resulted dictionary ({sum(res_dict.values())} out of {size*size})')
        res = random.randint(0, 1)
        if res:
            if len(m_dict) != 0:
                key = random.choice(m_list)
                if key in res_dict:
                    res_dict[key] += 1
                else:
                    if m_dict[key] > size*size - len(res_dict):
                        res_dict[key] = size*size - len(res_dict)
                    else:
                        res_dict[key] = m_dict[key]
        else:
            if len(f_dict) != 0:
                key = random.choice(f_list)
                if key in res_dict:
                    res_dict[key] += 1
                else:
                    if m_dict[key] > size*size - len(res_dict):
                        res_dict[key] = size*size - len(res_dict)
                    else:
                        res_dict[key] = m_dict[key]
    print(f'[+] Enough number of colors in resulted dictionary ({sum(res_dict.values())} out of {size*size})')

    #print(sorted(res_dict.items(), key=lambda x: x[1], reverse=True))

    
    print('[+] Start creation of new population')
    res = []
    for pop in range(num_populations):
        print(f'{pop+1} child creation start')
        temp = np.empty((size, size, 3), dtype=np.uint8)
        temp_dict = res_dict
        for i in range(size):
            for j in range(size):
                if sum(res_dict.values()) == 0:
                    break
                temp[i][j] = np.array(list(random.choice(list(temp_dict.keys()))), dtype=np.uint8)
                temp_dict[tuple(temp[i][j])] -= 1
                if temp_dict[tuple(temp[i][j])] == 0:
                    temp_dict.pop(tuple(temp[i][j]))
        res.append(temp)

    return res

    


if __name__ == '__main__':
    im = Image.open(image)
    im = im.convert('RGB')
    print(f'[+] Open image {image}.')
    #im = im.filter(ImageFilter.BoxBlur(10))

    im2arr = np.array(im)
    print('[+] Create numpy array of image')
    mother, father = im2arr, None

    for i in range(num_generations):
        childs = generate_childrens(mother, father)
        mother, father = fitness(childs)


    im = Image.fromarray(mother)
    im.show()



