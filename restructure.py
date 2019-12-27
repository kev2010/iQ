import os
import random
import shutil

#  orig: Database name -> cats -> train/test -> images
#  new:  Database name -> train/test -> cats -> images
def change(oldpath, newpath):
    if os.path.exists(newpath):
        print(newpath, " already exists!")
    else:
        os.mkdir(newpath)
        os.mkdir(newpath + 'train')
        os.mkdir(newpath + 'test')
        for cat in os.listdir(oldpath):
            os.mkdir(newpath + 'train/' + cat)
            os.mkdir(newpath + 'test/' + cat)
            for train in os.listdir(oldpath + cat + '/train'):
                shutil.copy2(oldpath + cat + '/train/' + train, newpath + 'train/' + cat)

            for test in os.listdir(oldpath + cat + '/test'):
                shutil.copy2(oldpath + cat + '/test/' + test, newpath + 'test/' + cat)
        print(newpath, " created!")

if __name__ == '__main__':
    # # Scenes
    # change("/mindhive/nklab4/users/kev2018/scenes_data/", "/mindhive/nklab4/users/kev2018/database/data_scenes/")
    #
    # # Inanimate objects
    # change("/mindhive/nklab4/users/kev2018/inanimate_data/", "/mindhive/nklab4/users/kev2018/database/data_inanimate/")
    #
    # # Food
    # change("/om/group/nklab/kev2018/food_data/", "/mindhive/nklab4/users/kev2018/database/data_food/")
    #
    # # ImageNet Objects
    # change("/om/group/nklab/kev2018/data/", "/mindhive/nklab4/users/kev2018/database/data_ILSVRC2012/")
    #
    # # Car
    # change("/om/group/nklab/kev2018/data_car_sub/", "/mindhive/nklab4/users/kev2018/database/data_car/")
    #
    # # Animate objects
    # change("/mindhive/nklab4/users/kev2018/animate_data/", "/mindhive/nklab4/users/kev2018/database/data_animate/")
    #
    # # Cifar objects
    # change("/om/group/nklab/kev2018/cifar100_data_sub/", "/mindhive/nklab4/users/kev2018/database/data_cifar/")

    # face car data
    change("/om/group/nklab/kdobs/databases/data_face_car/", "/mindhive/nklab4/shared/datasets/data_facecar/")