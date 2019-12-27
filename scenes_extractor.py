import os
import random
import shutil

# 494 train, 55 test
if __name__ == '__main__':
    path = '/mindhive/nklab4/users/kev2018/data_256/'
    dst = '/mindhive/nklab4/users/kev2018/scenes_data/'
    remove = {"airfield", "aquarium", "army_base", "auto_factory", "auto_showroom", "bakery_shop",
              "boxing_ring", "corral", "delicatessen", "garage_indoor"}

    if os.path.exists(dst):
        print('scenes_data already exists!')
    else:
        os.mkdir(dst)

        for let in os.listdir(path):
            for cat in os.listdir(path + let):
                if os.listdir(path + let + '/' + cat)[0][-4:] != ".jpg":
                    for sub in os.listdir(path + let + '/' + cat):
                        name = cat + "_" + sub

                        if name not in remove and not os.path.exists(dst + name):
                            os.mkdir(dst + name)
                            os.mkdir(dst + name + '/train')
                            os.mkdir(dst + name + '/test')

                            size = len(os.listdir(path + let + '/' + cat + "/" + sub))
                            if size > 2222:
                                test = random.sample(range(size), int(size/10))
                                for k, img in enumerate(os.listdir(path + let + '/' + cat + "/" + sub)):
                                    if k in test:
                                        shutil.move(path + let + '/' + cat + '/' + sub + '/' + img, dst + name + '/test')
                                    else:
                                        shutil.move(path + let + '/' + cat + '/' + sub + '/' + img, dst + name + '/train')

                else:
                    if cat not in remove and not os.path.exists(dst + cat):
                        os.mkdir(dst + cat)
                        os.mkdir(dst + cat + '/train')
                        os.mkdir(dst + cat + '/test')

                        size = len(os.listdir(path + let + '/' + cat))
                        if size > 2222:
                            test = random.sample(range(size), int(size / 10))
                            for k, img in enumerate(os.listdir(path + let + '/' + cat)):
                                if k in test:
                                    shutil.move(path + let + '/' + cat + '/' + img, dst + cat + '/test')
                                else:
                                    shutil.move(path + let + '/' + cat + '/' + img, dst + cat + '/train')

    print('Success! scenes_data created!')




