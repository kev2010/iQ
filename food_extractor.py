import os
import random
import shutil


if __name__ == '__main__':
    path = '/om/group/nklab/kev2018/food-101/'
    dst = '/om/group/nklab/kev2018/food_data/'

    if os.path.exists(dst):
        print('food_data already exists')
    else:
        os.mkdir(dst)
        for cat in os.listdir(path + 'images'):
            if not os.path.exists(dst + cat):
                os.mkdir(dst + cat)
                os.mkdir(dst + cat + '/train')
                os.mkdir(dst + cat + '/test')

                test = set(random.sample(range(1000), 100))
                for k, im in enumerate(os.listdir(path + 'images/' + cat)):
                    if k in test:
                        shutil.copy2(path + 'images/' + cat + '/' + im, dst + cat + '/test/')
                    else:
                        shutil.copy2(path + 'images/' + cat + '/' + im, dst + cat + '/train')
