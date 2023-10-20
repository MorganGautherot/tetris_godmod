import numpy as np
import pandas as pd
import cv2
from imutils import contours
from glob import glob

imprime_ecran_path = 'imprime_ecran'
matrix_convert_path = 'matrix_convert'
train_data = 'training_data'

# Dev function

def extract_roi(tetris_game:np.ndarray, image_path:str, folder_name:str)->tuple:
    """ Extract the matrix from a tetris image and the next tetromino"""

    matrix_path = f'{matrix_convert_path}/{folder_name}/{image_path.split("/")[-1][:-4]}'
    
    roi_matrix = None
    
    original = tetris_game.copy()
    gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    (cnts, 
     _) = contours.sort_contours(cnts, method="left-to-right")
    num = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w > 5:
            roi = original[y+9:y+h-9, x+9:x+w-9]

            if num == 0:
                roi_matrix = roi

                cv2.imwrite(f'{matrix_path}_roi_{num}.png', roi_matrix)

            num += 1
            
    return roi_matrix

def roi_to_training_example(roi_image:np.ndarray)->np.ndarray:
    

    gray = cv2.cvtColor(roi_image,cv2.COLOR_BGR2GRAY)
    thresh_gray = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO)[1]
    resize_image = cv2.resize(thresh_gray, (10, 20), interpolation = cv2.INTER_AREA)

    thresh_resize_image = np.where(resize_image>50, 255, 0)

    return thresh_resize_image

def find_tetromino_column(matrix_x:np.ndarray, matrix_y:np.ndarray)->int:
    
    matrix_with_last_tetromino = matrix_y[2:, :]-matrix_x[2:, :] 
    
    column_with_tetromino = (np.sum(matrix_with_last_tetromino, axis=0)!=0)
    
    first_column_with_tetromino = column_with_tetromino.argmax(axis=0)
    
    return first_column_with_tetromino

def find_tetromino(matrix:np.ndarray)->np.ndarray:

    column_with_tetromino = (np.sum(matrix, axis=0)!=0)
    
    first_x_with_tetromino = column_with_tetromino.argmax(axis=0)    
    
    last_x_with_tetromino = np.max(np.nonzero(column_with_tetromino))
    

    line_with_tetromino = (np.sum(matrix, axis=1)!=0)  
    
    first_y_with_tetromino = line_with_tetromino.argmax(axis=0)  
    
    last_y_with_tetromino = np.max(np.nonzero(line_with_tetromino))

    return matrix[first_y_with_tetromino:last_y_with_tetromino+1, first_x_with_tetromino:last_x_with_tetromino+1]

def find_tetromino_rotation(matrix_x:np.ndarray, matrix_y:np.ndarray)->int:
    
    input_tetromino = find_tetromino(matrix_x[:2, :])
    
    matrix_with_last_tetromino = matrix_y[2:, :]-matrix_x[2:, :]
    
    output_tetromino = find_tetromino(matrix_with_last_tetromino)
    
    if input_tetromino.shape == output_tetromino.shape and np.all(np.equal(input_tetromino, input_tetromino)):
        return 0
    elif np.rot90(input_tetromino, k=1).shape == output_tetromino.shape and np.all(np.equal(input_tetromino, input_tetromino)):
        return 1
    elif np.rot90(input_tetromino, k=2).shape == output_tetromino.shape and np.all(np.equal(input_tetromino, input_tetromino)):
        return 2
    elif np.rot90(input_tetromino, k=3).shape == output_tetromino.shape and np.all(np.equal(input_tetromino, input_tetromino)):
        return 3
    
    data_frame = pd.DataFrame([], columns=('name', 'training_path', 'column', 'rotation'))

# Main

for path_image in glob(f'{imprime_ecran_path}/X/*'):
        
        path_x_image = path_image.replace("\\", "/")
        path_y_image = f"{imprime_ecran_path}/Y/"+path_image.replace("\\", "/").split('/')[-1]

        x_image = cv2.imread(path_x_image)
        y_image = cv2.imread(path_y_image)
        
        roi_x_matrix = extract_roi(x_image, path_x_image, 'X')
        roi_y_matrix = extract_roi(y_image, path_y_image, 'Y')       
        
        matrix_training_x_example = roi_to_training_example(roi_x_matrix)
        matrix_training_y_example = roi_to_training_example(roi_y_matrix)
                
        y_column = find_tetromino_column(matrix_training_x_example, matrix_training_y_example)
        
        y_rotation = find_tetromino_rotation(matrix_training_x_example, matrix_training_y_example)
        
        path_training_data = f'{train_data}/X/'+path_x_image.split('/')[-1]
                                               
        cv2.imwrite(path_training_data, matrix_training_x_example)
        
        new_row = {"name":path_training_data.split('_')[-1][:-4],
                   "training_path":path_training_data,
                   "column":y_column,
                   "rotation":y_rotation}
        
        data_frame = data_frame.append(new_row, ignore_index=True)
        
data_frame.reset_index(drop=True)
data_frame.to_csv(f'{train_data}/data.csv')
        
        