import pandas as pd
from glob import glob
import os
import cv2
import numpy as np
from tqdm import tqdm

data_folder_name = "beginning_game"
split_test = 'test'

PATH_DATA = "\\Users\Gautherot\Documents\code\code_videos\Tetris_godmod\jeu_de_donnees\\"

dataframe = pd.DataFrame([], columns=('name', 'path', 'column', 'rotation'))

for folder in glob(f'{PATH_DATA}{data_folder_name}\\{split_test}\\*'):

  if not('csv' in folder):

    folder_name = folder.split('\\')[-1]

    folder_id = folder.split('_')[-1]

    data = pd.read_csv(f'{PATH_DATA}{data_folder_name}\\{split_test}\\y_{folder_id}_dataframe.csv')

    for line in data.iterrows():

        new_path = f'{folder}/'+line[1]['path'].split('/')[-1]

        new_row = pd.DataFrame([[line[1]['name'],
                                new_path,
                                line[1]['column'],
                                line[1]['rotation']]],
                                columns=("name", "path", "column", "rotation"))

        dataframe = pd.concat([dataframe, new_row])

dataframe = dataframe.reset_index(drop=True)


for line in tqdm(dataframe.iterrows()):
    if not(os.path.exists(line[1]['path'])):
        print(line[1]['path'])
        break

dataframe.to_csv(f'{PATH_DATA}{split_test}_data-{data_folder_name}.csv', index=False)


dataframe_images = np.zeros((dataframe.shape[0], 20, 10, 1))

for image_path in tqdm(dataframe.iterrows()):

  img = cv2.imread(image_path[1]['path'], cv2.IMREAD_GRAYSCALE)

  dataframe_images[image_path[0], :, :, :] = np.expand_dims(img/255, axis=-1)

np.save(f'{PATH_DATA}{split_test}_data_images-{data_folder_name}.npy', dataframe_images)