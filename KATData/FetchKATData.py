import pytesseract
import pyautogui
import cv2

class FetchKATData:
    def __init__(self, left_foot_grid_centre_x, left_foot_grid_centre_y):
        '''
            On KAT Gateway Software, there exists 2 grids which represent the rotations of each foot.
            To generate the same image, we need to use the same reference point to get the same boundaries.
            The reference point we will use will be the center of the Left Foot Grid
            
            left_foot_grid_centre_x: X coordinate of the centre of the left foot grid.
            left_foot_grid_centre_y: Y coordinate of the centre of the left foot grid.
        '''
        self.left = left_foot_grid_centre_x - 202
        self.top = left_foot_grid_centre_y - 67
        self.width = 154
        self.height = 262


    def getData(self): 
        '''
            Get the reading of KAT Gateway and return those values in Python.

            Output: 4 integers: left_foot_roll, left_foot_pitch, right_foot_roll, right_foot_pitch
        '''

        # IF either parameter is negative, fetch data from test image
        if(self.left < 0 or self.top < 0):
            screenshot = cv2.imread('KATData/static-kat-sensor-data-image/test-rotation-image.png')
        # ELSE, fetch data from actual program
        else:
            screenshot = pyautogui.screenshot(region=(self.left, self.top, self.width, self.height))

        # Use pytesseract to extract text from the screenshot
        data_rotation_str = pytesseract.image_to_string(screenshot)
        data_rotation_str = data_rotation_str.strip()


        # Format data in an array where each element in our array is each line from the string
        data_rotation_array = data_rotation_str.split('\n')


        # Extract the data we want as string
        left_foot_roll_str = data_rotation_array[1][5:data_rotation_array[1].index('°')]
        left_foot_pitch_str = data_rotation_array[2][5:data_rotation_array[2].index('°')]
        right_foot_roll_str = data_rotation_array[5][5:data_rotation_array[5].index('°')]
        right_foot_pitch_str = data_rotation_array[6][5:data_rotation_array[6].index('°')]


        # Convert the data from string to integer
        left_foot_roll = int(left_foot_roll_str)
        left_foot_pitch = int(left_foot_pitch_str)
        right_foot_roll = int(right_foot_roll_str)
        right_foot_pitch = int(right_foot_pitch_str)


        return left_foot_roll, left_foot_pitch, right_foot_roll, right_foot_pitch





