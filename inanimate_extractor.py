import os
import shutil


if __name__ == '__main__':
    path = '/om/group/nklab/kev2018/data/'
    dst = '/om/group/nklab/kev2018/inanimate_data/'

    if os.path.exists(dst):
        print('inanimate_data already exists!')
    else:
        os.mkdir(dst)
        desired = set(f.strip() for f in open('inanimate_cats.txt'))
        remove = set(p.strip() for p in open('vehicle_cars_to_remove.txt'))
        for cat in os.listdir(path):
            if cat in desired:
                if cat not in remove:
                    if not os.path.exists(dst + cat):
                        os.mkdir(dst + cat)
                        os.mkdir(dst + cat + '/train')
                        os.mkdir(dst + cat + '/test')

                        for img in os.listdir(path + cat + '/train'):
                            shutil.copy2(path + cat + '/train/' + img, dst + cat + '/train')

                        for img in os.listdir(path + cat + '/test'):
                            shutil.copy2(path + cat + '/test/' + img, dst + cat + '/test')

    print('Success! inanimate_data created!')
