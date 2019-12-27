import pickle
import os
import shutil
import random
import numpy as np
from PIL import Image


def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


def save(A, dst):
    r = np.reshape(A[0:1024], (32, 32))
    g = np.reshape(A[1024:2048], (32, 32))
    b = np.reshape(A[2048:3072], (32, 32))
    rgb = np.dstack((r, g, b))
    im = Image.fromarray(rgb)
    im.save(dst)


def remove(src, folders):
    for cat in os.listdir(src):
        if cat in folders:
            shutil.rmtree(src + cat)


def create(path, fname, test_size, addtrain=0):
    if os.path.exists(path + fname):
        print(fname + ' already exists!')
    else:
        os.mkdir(path + fname)
        train = unpickle(path + 'train')
        test = unpickle(path + 'test')
        meta = unpickle(path + 'meta')

        c = {k: 0 for k in range(100)}
        for i, train_img in enumerate(train[b'data']):
            cat = meta[b'fine_label_names'][train[b'fine_labels'][i]].decode('utf-8')
            dst = path + fname + '/' + cat + '/train/' + cat + '_' + str(c[train[b'fine_labels'][i]]) + '.jpeg'

            if not os.path.exists(path + fname + '/' + cat):
                os.mkdir(path + fname + '/' + cat)
                os.mkdir(path + fname + '/' + cat + '/train/')
            save(train_img, dst)
            c[train[b'fine_labels'][i]] += 1

        t = {k: 0 for k in range(100)}
        test_set = {j: set(random.sample(range(100), test_size)) for j in range(100)}
        if addtrain != 0:
            to_add = {l: set(random.sample(set(range(100))-test_set[l], addtrain)) for l in range(100)}
        for i, test_img in enumerate(test[b'data']):
            tmp = t[test[b'fine_labels'][i]]
            if tmp in test_set[test[b'fine_labels'][i]]:
                cat = meta[b'fine_label_names'][test[b'fine_labels'][i]].decode('utf-8')
                dst = path + fname + '/' + cat + '/test/' + cat + '_' + str(t[test[b'fine_labels'][i]]) + '.jpeg'

                if not os.path.exists(path + fname + '/' + cat + '/test/'):
                    os.mkdir(path + fname + '/' + cat + '/test/')
                save(test_img, dst)
            elif addtrain != 0 and tmp in to_add:
                cat = meta[b'fine_label_names'][test[b'fine_labels'][i]].decode('utf-8')
                dst = path + fname + '/' + cat + '/train/' + cat + '_' + str(c[test[b'fine_labels'][i]]) + '.jpeg'
                save(test_img, dst)
                c[test[b'fine_labels'][i]] += 1
            t[test[b'fine_labels'][i]] += 1
        print('Success! ' + fname + ' dataset created.')


if __name__ == '__main__':
    path = '/om/group/nklab/kev2018/cifar-100-python/'
    meta = unpickle(path + 'meta')

    # create full database
    create(path, 'cifar100_data', 100)

    # create database w/o cars and people
    create(path, 'cifar100_data_sub', 40, addtrain=60)

    cars = {13, 48, 58, 81, 85, 89}
    people = {2, 11, 35, 46, 98}
    cat_cars = {meta[b'fine_label_names'][p].decode('utf-8') for p in cars}
    cat_people = {meta[b'fine_label_names'][r].decode('utf-8') for r in people}
    remove(path + 'cifar100_data_sub/', cat_cars | cat_people)


