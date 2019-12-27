import os
import random
import h5py
import shutil
import numpy as np
from PIL import Image

# 512 train, 57 test
if __name__ == '__main__':
    path = "/om/user/ershook/pycochleagram_cgrams/data/word_2019x/word_2019x_resampled.hdf5"
    dst = "/mindhive/nklab4/shared/datasets/data_spectograms_1/"
    img_set = h5py.File(path, mode='r')

    f = open("/mindhive/nklab4/shared/datasets/total", mode='r')
    # tot = {t: 0 for t in range(588)}
    # for r, val in enumerate(img_set['is_valid'][:]):
    #     if val == 1 and img_set['labels'][r] != 0:
    #         tot[img_set['labels'][r]] += 1
    #
    # f.write(str(tot))
    # print(tot)
    # f.close()
    # print("total found")

    tot = eval(f.read())

    if os.path.exists(dst):
        print(dst + " already exists!")
    else:
        os.mkdir(dst)
        for i in range(1, 588):
            os.mkdir(dst + str(i))
            os.mkdir(dst + str(i) + '/train/')
            os.mkdir(dst + str(i) + '/test/')

        count = {m: 0 for m in range(1, 588)}
        train = {n: (set(random.sample(range(tot[n]), 512)) if tot[n] > 569 else set()) for n in range(1, 588)}
        test = {p: (set(random.sample(set(range(tot[p])) - train[p], 57)) if tot[p] > 569 else set()) for p in range(1, 588)}
        for k, data in enumerate(img_set['data'][:]):
            lab = img_set['labels'][k]
            if img_set['is_valid'][k] == 1 and lab != 0:
                if count[lab] in train[lab]:
                    newdata = np.reshape(data, (256, 256))
                    newdata = newdata * 255
                    new_p = Image.fromarray(newdata)

                    if new_p.mode != 'RGB':
                        new_p = new_p.convert('RGB')
                    new_p.save(dst + str(lab) + '/' + '/train/' + str(k) + '.jpeg')
                elif count[lab] in test[lab]:
                    newdata = np.reshape(data, (256, 256))
                    newdata = newdata * 255
                    new_p = Image.fromarray(newdata)

                    if new_p.mode != 'RGB':
                        new_p = new_p.convert('RGB')
                    new_p.save(dst + str(lab) + '/' + '/test/' + str(k) + '.jpeg')
                count[lab] += 1
        print("Success!")









