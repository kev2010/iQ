""" extractor.py

This extractor completes the following three tasks:

    1.  Untar files in the ILSVRC2012 data set
    2.  Create a subset of ILSVRC2012 using the categories defined in the synsets
    3.  Randomly generate a train/test data set from the subset without any cars in it.

"""

import os
import random
import shutil
import tarfile
import xml.etree.ElementTree as ET
from PIL import Image
from torchvision import transforms


def untar():
    """
    :return: Extracts tar files from ILSVRC2012 and moves them to new folder
    """
    # check if tar files were extracted
    path = '/om/group/nklab/kev2018/'
    if os.path.exists(path + 'ILSVRC2012_ex'):
        return 'ILSVRC2012 tar files already extracted!'

    # extract each tar file into new folder
    listdir = os.listdir(path + 'ILSVRC2012')
    for filename in listdir:
        if filename[-4:] == '.tar':
            if not os.path.exists(path + 'ILSVRC2012_ex/' + filename[:-4]):
                os.makedirs(path + 'ILSVRC2012_ex/' + filename[:-4])

            tar = tarfile.open(path + 'ILSVRC2012/' + filename)
            tar.extractall(path=path + 'ILSVRC2012_ex/' + filename[:-4])
            tar.close()
    return 'Success! All ILSVRC2012 tar files were extracted.'


def extract_synsets():
    """"
    :return: Creates ILSVRC2012_sub directory using desired files in synsets.txt
    """
    # check if ILSVRC2012_sub exists
    path = '/om/group/nklab/kev2018/'
    if os.path.exists(path + 'ILSVRC2012_sub'):
        ans = input('Are there new categories to be added to ILSVRC2012_sub? (y/n) ')
        if ans == 'y':
            pass
        elif ans == 'n':
            return 'ILSVRC2012_sub already exists!'
        else:
            raise TypeError

    # find all new desired files and copy to new directory
    desired = set(f.strip() for f in open('synsets.txt'))
    for filename in os.listdir(path + 'ILSVRC2012_ex'):
        if filename in desired and not os.path.exists(path + 'ILSVRC2012_sub/' + filename):
            print('adding ' + filename)
            src = path + 'ILSVRC2012_ex/' + filename
            dst = path + 'ILSVRC2012_sub/' + filename
            shutil.copytree(src, dst)
    return 'Success! synsets files copied to ILSVRC2012_sub.'


# def select_categories_no_cars(num):
#     """
#     :param num: (int) number of randomly selected categories
#     :return: Randomly selects 'int num' non-car files from ILSVRC2012_sub to copy
#     """
#     # check if ILSVRC2012_sub_rand(num) exists
#     path = '/om/group/nklab/kev2018/'
#     if os.path.exists(path + 'ILSVRC2012_sub_rand' + str(num)):
#         return 'ILSVRC2012_sub no cars for ' + str(num) + ' random categories already exists!'
#
#     # find subset of files that aren't cars
#     files = set(f for f in os.listdir(path + 'ILSVRC2012_sub'))
#     cars = set(f.strip() for f in open('vehicle_cars_to_remove.txt'))
#     subset = files - cars
#
#     # randomly select from subset and copy to new directory
#     randfiles = random.sample(subset, num)
#     for filename in randfiles:
#         src = path + 'ILSVRC2012_sub/' + filename
#         dst = path + 'ILSVRC2012_sub_rand' + str(num) + '/' + filename
#         shutil.copytree(src, dst)
#     return 'Success! ' + str(num) + ' random files without cars were copied.'


def save_annotate(fpath, apath, dst):
    """
    :param fpath: (str) dir to full image
    :param apath: (str) dir to annotated image
    :param dst: (str) dir to save cropped image
    :return: None; saves cropped image to dst
    """
    def get_bounding_boxes(path_to_file):
        """
        :param path_to_file: (str) path to annotated file
        :return: (tuple) the bounds for the object
        """
        try:
            # find the annotated file
            tree = ET.parse(path_to_file)

            root = tree.getroot()
            boxes = []

            # extract all object bounds
            for obj in root.findall('object'):
                xmin = int(obj.find('bndbox').find('xmin').text)
                ymin = int(obj.find('bndbox').find('ymin').text)
                xmax = int(obj.find('bndbox').find('xmax').text)
                ymax = int(obj.find('bndbox').find('ymax').text)

                if ymin >= ymax or xmin >= xmax:
                    return [None]
                else:
                    boxes.append((xmin, ymin, xmax, ymax))
            return boxes
        except:
            return [None]

    # crop the image from first bound given and save to dst
    image = Image.open(fpath)
    coords = get_bounding_boxes(apath)[0]
    if coords is not None:
        xmin, ymin, xmax, ymax = coords
        i = ymin
        j = xmin
        h = ymax - ymin
        w = xmax - xmin
        cropped = transforms.functional.crop(image, i, j, h, w)
        cropped.save(dst, 'JPEG')


def create_data(num, train, test):
    """
    :param num: (int) number of randomly selected categories
    :param train: (int) number of images to be in train
    :param test: (int) number of images to be in test
    :return: Creates a train and test folder for each randomly selected category
    """
    # check if data exists
    path = '/om/group/nklab/kev2018/'
    if os.path.exists(path + 'data'):
        ans = input('data folder already exists! add additional data? (y/n)')
        if ans == 'y':
            pass
        elif ans == 'n':
            return 'stopping... '
        else:
            raise TypeError

    # find subset of files that aren't cars
    files = set(f for f in os.listdir(path + 'ILSVRC2012_sub'))
    cars = set(f.strip() for f in open('vehicle_cars_to_remove.txt'))
    subset = files - cars
    # randomly select "num" non-car categories from subset
    randfiles = random.sample(subset, num)

    # loop through every image in each of the randomly selected files in desired categories
    for filename in randfiles:
        # if file doesn't exist already, create train and test folders
        if not os.path.exists(path + 'data/' + filename):
            os.makedirs(path + 'data/' + filename + '/train')
            os.makedirs(path + 'data/' + filename + '/test')
        else:
            continue

        # create randtrain and randtest image subsets
        images = set(f for f in os.listdir(path + 'ILSVRC2012_sub/' + filename))
        randtrain = set(random.sample(images, train))
        images_sub = images - randtrain
        randtest = random.sample(images_sub, test)

        # copy each randtrain/randtest image to appropriate folder
        listdir = os.listdir(path + 'ILSVRC2012_sub/' + filename)
        for im in listdir:
            if im[-5:] == '.JPEG':
                src = path + 'ILSVRC2012_sub/' + filename + '/' + im
                if im in randtrain:
                    dst = path + 'data/' + filename + '/' + 'train'
                elif im in randtest:
                    dst = path + 'data/' + filename + '/' + 'test'
                else:
                    continue

                # check if image is already annotated
                annotate = '/om/group/nklab/kdobs/databases/annotations/' + filename + '/' + im[:-5] + '.xml'
                if os.path.exists(annotate):
                    save_annotate(src, annotate, dst + '/a_' + im)
                else:
                    shutil.copy2(src, dst)
    return 'Success! train and test folders created for each category!'


if __name__ == "__main__":
    print(untar())
    print(extract_synsets())
    #print(select_categories_no_cars(600))
    print(create_data(600, 1000, 50))

    # find num of categories in ILSVRC2012_sub with 1050+ images

    # path = '/om/group/nklab/kev2018/ILSVRC2012_sub/'
    # under = 0
    # l_und = []
    # car_und = []
    # over = 0
    # l_ov = []
    # car_ov = []
    # cars = set(f.strip() for f in open('vehicle_cars_to_remove.txt'))
    # for folder in os.listdir(path):
    #     if len(os.listdir(path + folder)) < 1050:
    #         under += 1
    #         l_und.append((len(os.listdir(path + folder)), folder))
    #
    #         if folder in cars:
    #             car_und.append((len(os.listdir(path + folder)), folder))
    #     else:
    #         over += 1
    #         l_ov.append((len(os.listdir(path + folder)), folder))
    #
    #         if folder in cars:
    #             car_ov.append((len(os.listdir(path + folder)), folder))
    # print(under, over)
    # print(sorted(l_und))
    # print(sorted(l_ov))
    # print(sorted(car_und))
    # print(sorted(car_ov))
