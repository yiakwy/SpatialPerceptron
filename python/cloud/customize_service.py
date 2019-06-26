import cv2
from model_service.tfserving_model_service import TfServingBaseService
import numpy as np
from dog_and_cat_train import config
from dataset import Preprocess_img, read_img, CatDogDataset

# output path
EXPORTED_PATH="{}/output/preprocessor.json".format(config.ROOT)

preprocessor = Preprocess_img.load_from(EXPORTED_PATH)
cat_dog_dataset = CatDogDataset()

class dogcat_service(TfServingBaseService):
  # Changed to match the model input preprocessing
  def _preprocess(self, data):
    preprocessed_data = {}
    for k, v in data.items():
      for file_name, file_content in v.items():
        img = read_img(file_content)
        img, _ = preprocessor(img)
        img = img[np.newaxis, :, :, :]
        preprocessed_data[k] = img
    return preprocessed_data

  def _postprocess(self, data):
    outputs = {}
    logits = data['logits'][0]
    label_id = np.argmax(logits)
    label = cat_dog_dataset[label_id]
    # label = "dog" if logits > 0.5 else "cat"
    outputs['predict label'] = label
    # confidence = logits if logits > 0.5 else 1 - logits
    confidence = logits[label_id]
    outputs['message'] = "I am {:.2%} sure this is a {}".format(float(confidence), label)
    return outputs
