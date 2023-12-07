import pandas as pd
from glob import glob
import os
import cv2
import numpy as np
from tqdm import tqdm

PATH_DATA = "\\Users\Gautherot\Documents\code\code_videos\Tetris_godmod\jeu_de_donnees\\"

training_data = pd.DataFrame([], columns=('name', 'path', 'column', 'rotation'))

for folder in glob(f'{PATH_DATA}final_dataframe\\train\\*'):

  folder_name = int(folder.split('\\')[-1])

  data = pd.read_csv(f'{folder}/y_dataframe.csv')

  for line in data.iterrows():

      new_path = f'{folder}/X/'+line[1]['path'].split('/')[-1]

      new_row = pd.DataFrame([[line[1]['name'],
                               new_path,
                               line[1]['column'],
                               line[1]['rotation']]],
                               columns=("name", "path", "column", "rotation"))

      training_data = pd.concat([training_data, new_row])

training_data = training_data.reset_index(drop=True)


for line in tqdm(training_data.iterrows()):
    if not(os.path.exists(line[1]['path'])):
        print(line[1]['path'])
        break

training_data.to_csv(f'{PATH_DATA}training_data.csv', index=False)


training_data_images = np.zeros((training_data.shape[0], 20, 10, 1))

for image_path in tqdm(training_data.iterrows()):

  img = cv2.imread(image_path[1]['path'], cv2.IMREAD_GRAYSCALE)

  training_data_images[image_path[0], :, :, :] = np.expand_dims(img/255, axis=-1)

np.save(f'{PATH_DATA}training_data_images.npy', training_data_images)