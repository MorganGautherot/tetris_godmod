import cv2
import os
import numpy as np
import pandas as pd


def video_to_images(file_name:str, 
                    outpout_folder_name:str)->np.ndarray:
    """
    Transform a video with name 'file_name' into series of images in a folder named
    'output_folder_name'. And return the path of every image in a np.ndarray

    Args:
        - file_name(str): name of the video file
        - output_folder_name(str): name fo the folder where will be saved images of the video

    Returns: 
        - (np.ndarray): list of the path of every images saved in 'output_folder_name' 
    """
    cam = cv2.VideoCapture(file_name)
    
    data = np.array([])

    try:
        
        # creating a folder named data
        if not os.path.exists(outpout_folder_name):
            os.makedirs(outpout_folder_name)
    
    # if not created then raise error
    except OSError:
        print ('Error: Creating directory of data')
    
    # frame
    currentframe = 0
    
    while(True):
        
        # reading from frame
        ret,frame = cam.read()
    
        if ret:
            # if video is still left continue creating images
            name = f'./{outpout_folder_name}/frame' + str(currentframe) + '.jpg'
            #print ('Creating...' + name)
            data = np.append(data, name)
            # writing the extracted images
            cv2.imwrite(name, frame)
    
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break
    
    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    return data

def transform_image_into_matrix(board_game_image:np.ndarray, threshold_intensity=70, threshold_header=66)->np.ndarray:
    """ 
    Transform image of tetris into 20x10 matrix

    Args:
        image(np.ndarray): image of the board game

    Returns:
        np.ndarray: matrix 20x10 of the board game
    """

    game_board = board_game_image[threshold_header:, :, :]
    resize_image = cv2.resize(game_board, (10, 20), interpolation = cv2.INTER_AREA)
    resize_image_sum = np.sum(resize_image, axis=-1)
    thresh_resize_image = np.where(resize_image_sum>threshold_intensity, 255, 0)

    return thresh_resize_image

def transform_next_tetromino_to_matrix(board_game_image:np.ndarray, threshold_intensity=90)->np.ndarray:
    """ 
    Transform game image of tetris into the next tetromino with a 5x2 matrix

    Args:
        image(np.ndarray): image of the board game

    Returns:
        np.ndarray: matrix 5x2 of the next tetromino
    """

    game_board_next_tetromino = board_game_image[:58, 155:, :]
  
    resize_image = cv2.resize(game_board_next_tetromino, (5, 2), interpolation = cv2.INTER_AREA)

    resize_image_sum = np.sum(resize_image, axis=-1)

    thresh_resize_image = np.where(resize_image_sum>threshold_intensity, 255, 0)

    return thresh_resize_image

def detect_tetromino(tetromino_matrix:np.ndarray)->str:
    """
    Detect tetromino from tetromino matrix 5x2

    Args:
        tetromino(np.ndarray): matrix 5x2 of the tetromino

    Returns:
        str: name of the tetromino
    """

    match tetromino_matrix:
        case _ if np.array_equal(tetromino_matrix, [[0, 0, 255, 255, 0], [0, 255, 255, 0, 0]]):
            return 'right_snake'
        case _ if np.array_equal(tetromino_matrix, [[0, 255, 255, 0, 0], [0, 0, 255, 255, 0]]):
            return 'left_snake'    
        case _ if np.array_equal(tetromino_matrix, [[0, 255, 255, 255, 0], [0, 255, 0, 0, 0]]):
            return 'right_gun'    
        case _ if np.array_equal(tetromino_matrix, [[0, 255, 255, 255, 0], [0, 0, 0, 255, 0]]):
            return 'left_gun'  
        case _ if np.array_equal(tetromino_matrix, [[0, 255, 255, 255, 0], [0, 255, 255, 255, 0]]):
            return 'square'  
        case _ if np.array_equal(tetromino_matrix, [[0, 255, 255, 255, 0], [0, 0, 255, 0, 0]]):
            return 'hat'  
        case _ if np.array_equal(tetromino_matrix, [[255, 255, 255, 255, 255], [255, 255, 255, 255, 255]]):
            return 'long' 
        
def determined_is_tetromino_start(game_board_matrix:np.ndarray)->bool:
    '''
    Is there a tetromino in the beginning part of the board? 

    Args:
        - game_board_matrix(np.ndarray): situation of the current game board

    Returns:
        - (bool): True if this is the beginning for the current tetromino
    '''

    return np.any(game_board_matrix[:4, :])

def determined_is_clean_four_lines(game_board_matrix:np.ndarray)->bool:
    """
    Determined if the current tetromino clean four lines in the same time.

    Args: 
        - game_board_matrix(np.ndarray): situation of the current game board

    Returns:
        - (bool): True if the current tetromino cleaned four lines False otherwise
    """

    return np.all(game_board_matrix)

def create_current_tetromino_dataframe(list_image:np.ndarray, threshold_intensity=70, threshold_header=66)->pd.DataFrame:
    """ 
    Create the dataframe of useable image to create training data.

    Args: 
        list_image(np.array): list of the game board image

    Returns:
        pd.DataFrame: dataframe of the usable image to create training dataframe
    """

    dataframe = pd.DataFrame([], columns=('image_path', 'x_y', 'id_pair'))

    id_pair = 0
    is_tetromino_start = True
    is_tetromino_start_last_image = False
    clear_four_lines = False
    for image_path in list_image:
        x_image = cv2.imread(image_path)

        game_board_matrix = transform_image_into_matrix(x_image, threshold_intensity=threshold_intensity, threshold_header=threshold_header)
    
        is_clear_four_lines = determined_is_clean_four_lines(game_board_matrix)

        if id_pair != 0 :
            slow_remove_line = np.any(np.sum(last_game_board_matrix-game_board_matrix)>0)
        else :
            slow_remove_line = False

        if not(is_clear_four_lines) and not(slow_remove_line):

            is_tetromino_start = determined_is_tetromino_start(game_board_matrix)

            

            if is_tetromino_start and is_tetromino_start != is_tetromino_start_last_image:

                if id_pair != 0 and not(clear_four_lines):
                    dataframe = pd.concat([dataframe, pd.DataFrame([[last_image_path, 'y', id_pair]], columns=('image_path', 'x_y', 'id_pair'))])
                else :
                    clear_four_lines = False
                id_pair += 1
                dataframe = pd.concat([dataframe, pd.DataFrame([[image_path, 'x', id_pair]], columns=('image_path', 'x_y', 'id_pair'))])

        elif is_clear_four_lines and not(clear_four_lines) :
            dataframe = pd.concat([dataframe, pd.DataFrame([[last_image_path, 'y', id_pair]], columns=('image_path', 'x_y', 'id_pair'))])
            clear_four_lines = True

        elif slow_remove_line and not(clear_four_lines):
            dataframe = pd.concat([dataframe, pd.DataFrame([[last_image_path, 'y', id_pair]], columns=('image_path', 'x_y', 'id_pair'))])
            clear_four_lines = True


        is_tetromino_start_last_image = is_tetromino_start
        last_image_path = image_path
        last_game_board_matrix = game_board_matrix


    dataframe = dataframe.reset_index(drop=True)

    if len(np.unique(dataframe.iloc[-2:, -1])) == 2:
        dataframe.drop(dataframe.iloc[-1:, :].index, axis=0, inplace=True)

    return dataframe
    
def get_start_column(matrix_difference:np.ndarray)->int:
    """
    Return the number of the column where the current tetromino is placed

    Args: 
        - matrix_difference(np.ndarray): difference between the game_board matrix at the begining and the final position of the current tetromino

    Returns: 
        - (int): columns where the current tetromino is placed
    """
    is_tetromino_column = np.sum(matrix_difference, axis=0)
    for id_column in np.arange(10):
        if is_tetromino_column[id_column] > 0:
            return id_column
        
def get_tetromino_from_difference(matrix_difference:np.ndarray)->np.ndarray:
    """
    Return a small matrix with the current tetromino

    Args: 
        - matrix_difference(np.ndarray): difference between the game_board matrix at the begining and the final position of the current tetromino

    Returns: 
        - (np.ndarray): small matrix with the current tetromino

    """
    # Find the indices where the tetromino starts and ends
    start_row, end_row = None, None
    start_col, end_col = None, None

    for i in range(matrix_difference.shape[0]):
        if np.any(matrix_difference[i] != 0):
            start_row = i
            break

    for i in range(matrix_difference.shape[0] - 1, -1, -1):
        if np.any(matrix_difference[i] != 0):
            end_row = i
            break

    for j in range(matrix_difference.shape[1]):
        if np.any(matrix_difference[:, j] != 0):
            start_col = j
            break

    for j in range(matrix_difference.shape[1] - 1, -1, -1):
        if np.any(matrix_difference[:, j] != 0):
            end_col = j
            break

    # Extract the tetromino
    tetromino = matrix_difference[start_row:end_row + 1, start_col:end_col + 1]

    return tetromino

def get_tetromino_name_and_rotation(current_tetromino_matrix:np.ndarray)->tuple:
    """
    From a matrix with only a tetromino extract the name and the rotation

    Args: 
        - current_tetromino_matrix(np.ndarray): small matrix with the current tetromino
    
    Returns: 
        - name(str): name of the tetromino
        - rotation(int): rotation of the tetromino

    """
    match current_tetromino_matrix:
        case _ if np.array_equal(current_tetromino_matrix, [[0, 255, 255], 
                                                            [255, 255, 0]]):
            return 'right_snake', 0
        case _ if np.array_equal(current_tetromino_matrix, [[255, 0], 
                                                            [255, 255],
                                                            [0, 255]]):
            return 'right_snake', 1
        

        case _ if np.array_equal(current_tetromino_matrix, [[255, 255, 0], 
                                                            [0, 255, 255]]):
            return 'left_snake', 0
        case _ if np.array_equal(current_tetromino_matrix, [[0, 255], 
                                                            [255, 255],
                                                            [255, 0]]):
            return 'left_snake', 1      
        
        case _ if np.array_equal(current_tetromino_matrix, [[0, 0, 255], 
                                                            [255, 255, 255]]):
            return 'right_gun', 0
        case _ if np.array_equal(current_tetromino_matrix, [[255, 0], 
                                                            [255, 0],
                                                            [255, 255]]):
            return 'right_gun', 1
        case _ if np.array_equal(current_tetromino_matrix, [[255, 255, 255], 
                                                            [255, 0, 0]]):
            return 'right_gun', 2
        case _ if np.array_equal(current_tetromino_matrix, [[255, 255], 
                                                            [0, 255],
                                                            [0, 255]]):
            return 'right_gun', 3

        case _ if np.array_equal(current_tetromino_matrix, [[255, 0, 0], 
                                                            [255, 255, 255]]):
            return 'left_gun', 0
        case _ if np.array_equal(current_tetromino_matrix, [[255, 255], 
                                                            [255, 0],
                                                            [255, 0]]):
            return 'left_gun', 1
        case _ if np.array_equal(current_tetromino_matrix, [[255, 255, 255], 
                                                            [0, 0, 255]]):
            return 'left_gun', 2
        case _ if np.array_equal(current_tetromino_matrix, [[0, 255], 
                                                            [0, 255],
                                                            [255, 255]]):
            return 'left_gun', 3
        

        case _ if np.array_equal(current_tetromino_matrix, [[255, 255], 
                                                            [255, 255]]):
            return 'square', 0

 
        case _ if np.array_equal(current_tetromino_matrix, [[0, 255, 0], 
                                                            [255, 255, 255]]):
            return 'hat', 0 
        case _ if np.array_equal(current_tetromino_matrix, [[255, 0], 
                                                            [255, 255], 
                                                            [255, 0]]):
            return 'hat', 1
        case _ if np.array_equal(current_tetromino_matrix, [[255, 255, 255], 
                                                            [0, 255, 0]]):
            return 'hat', 2
        case _ if np.array_equal(current_tetromino_matrix, [[0, 255], 
                                                            [255, 255], 
                                                            [0, 255]]):
            return 'hat', 3
    
        case _ if np.array_equal(current_tetromino_matrix, [[255, 255, 255, 255]]):
            return 'long', 0
        case _ if np.array_equal(current_tetromino_matrix, [[255], 
                                                            [255], 
                                                            [255], 
                                                            [255]]):
            return 'long', 1
        
def get_tetromino_final_position(x_game_board_matrix:np.ndarray, y_game_board_matrix:np.ndarray)->np.ndarray:
    """
    From begining matrix and finale matrix for a current tetromino extract the name the rotation and the position column
    
    Args: 
        - x_game_board_matrix(np.ndarray): game board matrix when the current tetromino comme to the screen
        - y_game_board_matrix(np.ndarray): game board matrix when the current tetromino is finally placed

    Returns: 
        - name(str): name of the tetromino
        - rotation(int): rotation of the tetromino
        - start_column(int): final position column of the current tetromino
    """
    matrix_difference = y_game_board_matrix[4:, :] - x_game_board_matrix[4:, :]
    
    start_column = get_start_column(matrix_difference)

    current_tetromino_matrix = get_tetromino_from_difference(matrix_difference)

    name, rotation = get_tetromino_name_and_rotation(current_tetromino_matrix)

    return name, rotation, start_column

def integrate_tetromino_in_board(tetromino_name:str, 
                                 game_board_matrix:np.ndarray,
                                 is_current:bool=True):
    match tetromino_name:
        case 'long':
            if is_current:
                game_board_matrix[0, 0] = 255
                game_board_matrix[0, 1] = 255
                game_board_matrix[0, 2] = 255
                game_board_matrix[0, 3] = 255
            else:
                game_board_matrix[0, -1] = 255
                game_board_matrix[0, -2] = 255
                game_board_matrix[0, -3] = 255
                game_board_matrix[0, -4] = 255                   
        case 'right_gun':
            if is_current:
                game_board_matrix[4, 0] = 255
                game_board_matrix[4, 1] = 255
                game_board_matrix[4, 2] = 255
                game_board_matrix[3, 2] = 255
            else:
                game_board_matrix[4, -1] = 255
                game_board_matrix[4, -2] = 255
                game_board_matrix[4, -3] = 255
                game_board_matrix[3, -1] = 255                    
        case 'square':
            if is_current:
                game_board_matrix[6, 0] = 255
                game_board_matrix[6, 1] = 255
                game_board_matrix[7, 0] = 255
                game_board_matrix[7, 1] = 255
            else:
                game_board_matrix[6, -1] = 255
                game_board_matrix[6, -2] = 255
                game_board_matrix[7, -1] = 255
                game_board_matrix[7, -2] = 255
        case 'left_gun':
            if is_current:
                game_board_matrix[10, 0] = 255
                game_board_matrix[10, 1] = 255
                game_board_matrix[10, 2] = 255
                game_board_matrix[9, 0] = 255
            else:
                game_board_matrix[10, -1] = 255
                game_board_matrix[10, -2] = 255
                game_board_matrix[10, -3] = 255
                game_board_matrix[9, -3] = 255
        case 'left_snake':
            if is_current:
                game_board_matrix[12, 0] = 255
                game_board_matrix[12, 1] = 255
                game_board_matrix[13, 1] = 255
                game_board_matrix[13, 2] = 255   
            else:
                game_board_matrix[12, -3] = 255
                game_board_matrix[12, -2] = 255
                game_board_matrix[13, -2] = 255
                game_board_matrix[13, -1] = 255
        case 'hat':
            if is_current:
                game_board_matrix[15, 0] = 255
                game_board_matrix[15, 1] = 255
                game_board_matrix[15, 2] = 255
                game_board_matrix[14, 1] = 255   
            else:
                game_board_matrix[15, -1] = 255
                game_board_matrix[15, -2] = 255
                game_board_matrix[15, -3] = 255
                game_board_matrix[14, -2] = 255  
        case 'right_snake':
            if is_current:
                game_board_matrix[19, 0] = 255
                game_board_matrix[19, 1] = 255
                game_board_matrix[18, 1] = 255
                game_board_matrix[18, 2] = 255
            else :
                game_board_matrix[18, -1] = 255
                game_board_matrix[18, -2] = 255
                game_board_matrix[19, -2] = 255
                game_board_matrix[19, -3] = 255
    return game_board_matrix

def dataframe_to_training_data(folder, dataframe, threshold_intensity=70, threshold_header=66):

    max_id_pair = np.max(dataframe['id_pair'])

    os.mkdir(f'training_data//X_{folder}')

    training_dataframe = pd.DataFrame([], columns=('name', 'path', 'column', 'rotation'))

    for id_pair in np.arange(1, max_id_pair+1):
        
        x_image_path = dataframe[np.logical_and(dataframe['id_pair']==id_pair, dataframe['x_y']=='x')]
        y_image_path = dataframe[np.logical_and(dataframe['id_pair']==id_pair, dataframe['x_y']=='y')]
        
        x_image = cv2.imread(np.squeeze(x_image_path['image_path']))
        x_game_board_matrix = transform_image_into_matrix(x_image, threshold_intensity=threshold_intensity, threshold_header=threshold_header)


        y_image = cv2.imread(np.squeeze(y_image_path['image_path']))
        y_game_board_matrix = transform_image_into_matrix(y_image, threshold_intensity=threshold_intensity, threshold_header=threshold_header)

        try : 
            name, rotation, column = get_tetromino_final_position(x_game_board_matrix, y_game_board_matrix)


            final_matrix = np.zeros((20, 22))

            final_matrix[4:, 6:-6] = x_game_board_matrix[4:, :]

            final_matrix_current = integrate_tetromino_in_board(name,
                                                                final_matrix,
                                                                is_current=True)
            
            next_tetromino_matrix = transform_next_tetromino_to_matrix(x_image, threshold_intensity=threshold_intensity)
            next_tetromino_name = detect_tetromino(next_tetromino_matrix)

            final_matrix_current_next = integrate_tetromino_in_board(next_tetromino_name,
                                                                final_matrix_current,
                                                                is_current=False)
            
            new_path = f'X_{folder}//{id_pair}_{name}.png'

            training_dataframe = pd.concat([training_dataframe, 
                                            pd.DataFrame([[name,
                                                        new_path,
                                                        column,
                                                        rotation
                                                            ]], columns=('name', 'path', 'column', 'rotation'))])



            cv2.imwrite(f'training_data//{new_path}', final_matrix_current_next)
        except:
            pass
        

    training_dataframe.to_csv(f'training_data//y_{folder}_dataframe.csv', index=False)