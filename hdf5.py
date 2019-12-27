import os
import h5py
import numpy as np
from PIL import Image
import io

# original: data -> category names -> test/train -> images
# new:      data -> category name hdf5 [inside contains train group and test group]


def convert_folder(in_dir, out_dir, train_size, test_size, view=False):
    # in = '/om/group/nklab/kev2018/data/cat/'
    # out = '/om/group/nklab/kev2018/data_hdf5/cat.hdf5'
    img_set = h5py.File(out_dir, mode='w')
    img_set.create_dataset('train_imgs', (train_size,), dtype=h5py.special_dtype(vlen=np.dtype('uint8')))
    img_set.create_dataset('test_imgs', (test_size,), dtype=h5py.special_dtype(vlen=np.dtype('uint8')))

    i = 0
    for train_img in os.listdir(in_dir + 'train'):
        f = open(in_dir + 'train/' + train_img, 'rb')
        binary_data = f.read()
        img_set['train_imgs'][i] = np.frombuffer(binary_data, dtype='uint8')
        i += 1

    j = 0
    for test_img in os.listdir(in_dir + 'test'):
        f = open(in_dir + 'test/' + test_img, 'rb')
        binary_data = f.read()
        img_set['test_imgs'][j] = np.frombuffer(binary_data, dtype='uint8')
        j += 1

    return img_set


def view(file_path):
    f = h5py.File(file_path, 'r')
    print(f['train_imgs'])
    print(f['test_imgs'])

    print('Viewing train_imgs... ')
    for i in range(len(f['train_imgs'])):
        img = Image.open(io.BytesIO(f['train_imgs'][i]))
        img.show()

        a = input('next? (y/n)')
        while a != 'y' and a != 'n':
            a = input('next? (y/n)')

        if a == 'y':
            pass
        elif a == 'n':
            break

    print('Viewing test_imgs... ')
    for j in range(len(f['test_imgs'])):
        img = Image.open(io.BytesIO(f['test_imgs'][j]))
        img.show()

        a = input('next? (y/n)')
        while a != 'y' and a != 'n':
            a = input('next? (y/n)')

        if a == 'y':
            pass
        elif a == 'n':
            break


if __name__ == '__main__':
    # test_path = '/Users/fengy/Documents/MIT/Summer19/iQ/'
    # name = 'test.jpeg'
    # convert_img(test_path + name, test_path + 'test.hdf5', view=True)

    # f = h5py.File('test.hdf5', 'r')
    # print(list(f.keys()))
    # d = f['binary_data']
    # print(d.shape, d.dtype)
    # print(d[:])

    path = '/om/group/nklab/kev2018/data_car_sub/'
    dst = '/om/group/nklab/kev2018/data_car_sub_hdf5/'

    if os.path.exists(dst):
        print('data_hdf5 already exists!')
    else:
        os.makedirs(dst)
        for cat in os.listdir(path):
            if os.path.exists(dst + cat):
                print(cat + '.hdf5 already exists!')
            else:
                convert_folder(path + cat + '/', dst + cat + '.hdf5', 45, 5)
        print('Success! hdf5 files were created!')
    #view('/om/group/nklab/kev2018/test_set_hdf5/n01443537.hdf5')

    # path = '/om/group/nklab/kev2018/data/'
    # dst = '/om/group/nklab/kev2018/data_hdf5/'
    # for cat in os.listdir(path):
    #     for train_img in os.listdir(path + cat + '/' + 'train'):
    #         temp = dst + cat + '/' + 'train/' + train_img[:-5] + '.hdf5'
    #         if os.path.exists(temp):
    #             print(train_img[:-5] + '.hdf5 already exists!')
    #         else:
    #             convert_img(path + cat + '/' + 'train/' + train_img, temp)
    #
    #     for test_img in os.listdir(path + cat + '/' + 'test'):
    #         temp = dst + cat + '/' + 'test/' + test_img[:-5] + '.hdf5'
    #         if os.path.exists(temp):
    #             print(test_img[:-5] + '.hdf5 already exists!')
    #         else:
    #             convert_img(path + cat + '/' + 'test/' + test_img, temp)

