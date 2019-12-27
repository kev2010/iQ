""" extractor_car.py

This extractor completes the following tasks:

    1.  Creates a dataset of car images

"""

import os
import shutil
import random
from PIL import Image
from torchvision import transforms


def save_annotate(fpath, apath, dst):
    """
    :param fpath: (str) dir to full image
    :param apath: (str) dir to annotated file
    :param dst: (str) dir to save cropped image
    :return: None; saves cropped image to dst
    """
    def get_bounding_boxes(path_to_file):
        """
        :param path_to_file: (str) path to annotated file
        :return: (tuple) the bounds for the object
        """
        f = open(path_to_file, 'r')
        f.readline()
        f.readline()
        c = tuple([int(num) for num in f.readline()[:-1].split()])

        return c

    # crop the image from first bound given and save to dst
    image = Image.open(fpath)
    coords = get_bounding_boxes(apath)

    xmin, ymin, xmax, ymax = coords
    i = ymin
    j = xmin
    h = ymax - ymin
    w = xmax - xmin
    cropped = transforms.functional.crop(image, i, j, h, w)
    cropped.save(dst, 'JPEG')


def create_data_car():
    path = '/om/group/nklab/kev2018/'
    if os.path.exists(path + 'data_car'):
        ans = input('data_car folder already exists! add additional data? (y/n)')
        if ans == 'y':
            pass
        elif ans == 'n':
            return 'stopping... '
        else:
            raise TypeError

    for cat in os.listdir(path + 'orig_car/image'):
        for mod in os.listdir(path + 'orig_car/image/' + cat):
            if not os.path.exists(path + 'data_car/' + cat + '_' + mod):
                os.makedirs(path + 'data_car/' + cat + '_' + mod)

            for year in os.listdir(path + 'orig_car/image/' + cat + '/' + mod):
                for img in os.listdir(path + 'orig_car/image/' + cat + '/' + mod + '/' + year):
                    poss1 = path + 'data_car/' + cat + '_' + mod + '/' + img[:-4] + '_' + year + '.jpg'
                    poss2 = path + 'data_car/' + cat + '_' + mod + '/a_' + img[:-4] + '_' + year
                    if os.path.exists(poss1) or os.path.exists(poss2):
                        continue

                    # print('processing ' + img + '...')
                    src = path + 'orig_car/image/' + cat + '/' + mod + '/' + year + '/' + img
                    dst = path + 'data_car/' + cat + '_' + mod
                    # check if image is already annotated
                    annotate = path + 'orig_car/label/' + cat + '/' + mod + '/' + year + '/' + img[:-4] + '.txt'
                    if os.path.exists(annotate):
                        try:
                            save_annotate(src, annotate, dst + '/a_' + img[:-4] + '_' + year)
                        except:
                            shutil.copy2(src, dst)
                            os.rename(dst + '/' + img, dst + '/' + img[:-4] + '_' + year + '.jpg')
                    else:
                        shutil.copy2(src, dst)
                        os.rename(dst + '/' + img, dst + '/' + img[:-4] + '_' + year + '.jpg')
    return 'Success! car data created!'


def car_subset(threshold, train_size, test_size):
    path = '/om/group/nklab/kev2018/data_car/'
    if os.path.exists('/om/group/nklab/kev2018/data_car_sub/'):
        return 'data car subset already exists!'

    for cat in os.listdir(path):
        if len(os.listdir(path + cat)) >= threshold:
            if not os.path.exists('/om/group/nklab/kev2018/data_car_sub/' + cat):
                os.makedirs('/om/group/nklab/kev2018/data_car_sub/' + cat + '/train')
                os.makedirs('/om/group/nklab/kev2018/data_car_sub/' + cat + '/test')
            else:
                continue

            images = set(f for f in os.listdir(path + cat))
            randtrain = set(random.sample(images, train_size))
            images_sub = images - randtrain
            randtest = set(random.sample(images_sub, test_size))
            for img in os.listdir(path + cat):
                src = path + cat + '/' + img
                if img in randtrain:
                    dst = '/om/group/nklab/kev2018/data_car_sub/' + cat + '/train'
                elif img in randtest:
                    dst = '/om/group/nklab/kev2018/data_car_sub/' + cat + '/test'
                else:
                    continue
                shutil.copy2(src, dst)
    return 'Success! data car subset created!'


if __name__ == "__main__":
    # print(create_data_car())
    # print(car_subset(50, 45, 5))

    # p = set()
    # for a in os.listdir('/om/group/nklab/kev2018/orig_car/image'):
    #     for b in os.listdir('/om/group/nklab/kev2018/orig_car/image/' + a ):
    #         for c in os.listdir('/om/group/nklab/kev2018/orig_car/image/' + a + '/' + b):
    #             for d in os.listdir('/om/group/nklab/kev2018/orig_car/image/' + a + '/' + b + '/' + c):
    #                 p.add(d)
    # #print('orig_car', p)
    # print()

    path = '/om/group/nklab/kev2018/data_car/'
    # for cat in os.listdir(path):
    #     for fol in os.listdir(path + cat):
    #         for im in os.listdir(path + cat + '/' + fol):
    #             if im[-5:] != '.jpeg':
    #                 os.rename(path + cat + '/' + fol + '/' + im, path + cat + '/' + fol + '/' + im + '.jpeg')

    for cat in os.listdir(path):
            for im in os.listdir(path + cat):
                try:
                    im=Image.open(path + cat + '/' + im)
                except IOError:
                    print(path + cat + '/' + im + ' oops!!')




