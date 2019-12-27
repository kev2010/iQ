import os
import shutil


if __name__ == '__main__':
    path = '/om/group/nklab/kev2018/data/'
    dst = '/om/group/nklab/kev2018/animate_data/'

    if os.path.exists(dst):
        print('animate_data already exists!')
    else:
        os.mkdir(dst)
        desired = set(f.strip() for f in open('animate_cats.txt'))
        for cat in os.listdir(path):
            if cat in desired:
                if not os.path.exists(dst + cat):
                    os.mkdir(dst + cat)
                    os.mkdir(dst + cat + '/train')
                    os.mkdir(dst + cat + '/test')

                    for img in os.listdir(path + cat + '/train'):
                        shutil.copy2(path + cat + '/train/' + img, dst + cat + '/train')

                    for img in os.listdir(path + cat + '/test'):
                        shutil.copy2(path + cat + '/test/' + img, dst + cat + '/test')

    print('Success! animate_data created!')
