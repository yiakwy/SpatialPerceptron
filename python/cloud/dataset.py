import os
import cv2
import random
import glob
from sklearn.model_selection import train_test_split
import keras
import numpy as np
import pandas as pd


# import config object
from dog_and_cat_train import config

# @todo : TODO
class Preprocess_img():
    
    def __init__(self):
        self.close = False
        self.mean = None
        self.std = None

    def __call__(self, data, labels):
        data = data.astype('float32')
        if  self.close is False:
            # self.mean = np.mean(data, axis=(0, 1, 2, 3))
            # self.std = np.std(data, axis=(0, 1, 2, 3))
            from keras.datasets import cifar10
            # LOADING TRAINING DATA
            (train_data, train_label), (test_data, test_label) = cifar10.load_data()
            train_data = train_data.astype('float32')
            # cifar10 mean-std normalization
            self.mean = np.mean(train_data, axis=(0,1,2,3))
            self.std = np.std(train_data, axis=(0,1,2,3))
            self.close = True

        data = (data - self.mean) / (self.std + 1e-6)
        labels = keras.utils.to_categorical(labels, config.NUM_CLASSES)
        return (data, labels)

def read_img(file_path):
    if not os.path.exists(file_path):
        raise ValueError("Image path [%s] does not exist." % (file_path))
    im = cv2.imread(file_path)
    im = im.astype(np.float32, copy=False)
    # some processing
    im = cv2.resize(im, (config.HEIGHT, config.WIDTH), interpolation=cv2.INTER_CUBIC)
    
    # 
    return im

def LoadBatchOfImages(files):
    count = len(files)
    X = np.ndarray((count, config.HEIGHT, config.WIDTH, config.CHANNEL), dtype=np.uint8)
    for i, image_file in enumerate(files):
        image = read_img(image_file)
        X[i] = image
    return X


# @todo : TODO 
class Dataset:
    
    def __init__(self, name):
        self._name = name
        self._class_names = []
        self._data_path = None
        self._dataset_meta = {}

    @property
    def name(self):
        return self._name 
        
    @property
    def class_names(self):
        return self._class_names
        
    @property
    def data_path(self):
        return self._data_path


class CatDogDataset(Dataset):

    def __init__(self, datapath=None, mode=None, name="dog_and_cat_200"):
        Dataset.__init__(self, "CatDog_%s" % name)
        self._data_path = datapath or os.path.join(config.DATA_DIR, name)
        if not os.path.isdir(self._data_path):
            os.mkdir(self._data_path)
        self._dataset_path = os.path.join(config.ROOT, 'data', "{}.tar.gz".format(name))
        self._mode = mode
        self._RANDOM_SAMPLING_ON=True
        # Follow Cifar10 conventions
        self._class_names = {
                4: 'cat',
                5: 'dog'
                }
        self._catid = 4
        self._dogid = 5
        self._preprocessor = Preprocess_img()
        # Data holders
        self._train_data = None
        self._train_labels = None
        self._test_data = None
        self._test_labels = None

    def load_dataset(self):
        data_cmpr = self._dataset_path
        if os.path.isfile(data_cmpr):
            print("uncmpr %s to %s" % (data_cmpr, self._data_path))
            os.system('tar xf %s -C %s' % (data_cmpr, config.DATA_DIR))
        else:
            print("The dataset <%s> does not exist!" % data_cmpr)
            return

        # Load data
        labeled_images = list(glob.iglob(os.path.join(self._data_path, "*jpg")))
        labeled_images = sorted(labeled_images, key=lambda x: int(os.path.split(x)[1].split('.')[1]))
        print("read %s images info" % len(labeled_images))

        if self._RANDOM_SAMPLING_ON:
            random.shuffle(labeled_images)
        
        # Load labels
        labels = []
        for img_name in labeled_images:
            if "dog" in img_name:
                labels.append(self._dogid)
            else:
                labels.append(self._catid)

        dataframe = pd.DataFrame({
            'data': labeled_images,
            'label': labels
            })
        print("show top 10 images info")
        print(dataframe.head(10))

        train_data, test_data, train_label, test_label = train_test_split(labeled_images, labels, test_size=0.25, random_state=10)

        self._train_data = train_data
        self._train_labels = train_label
        self._test_data = test_data
        self._test_labels = test_label

        return (train_data, test_data, train_label, test_label)

    def train_reader(self):
        X_train = LoadBatchOfImages(self._train_data)
        return self._preprocessor(X_train, self._train_labels)

    def validation_reader(self):
        X_test = LoadBatchOfImages(self._test_data)
        return self._preprocessor(X_test, self._test_labels)

    @property
    def train_data(self):
        return self._train_data

    @property
    def train_labels(self):
        return self._train_labels

    @property
    def test_data(self):
        return self._test_data

    @property
    def test_labels(self):
        return self._test_labels
