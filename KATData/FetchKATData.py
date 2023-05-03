import pytesseract
import pyautogui
import cv2

class FetchKATData:
    def __init__(self, left, top):
        self.left = left
        self.top = top
        self.width = 478
        self.height = 318


    def getData(self): 

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
        right_foot_roll_str = data_rotation_array[6][5:data_rotation_array[6].index('°')]
        right_foot_pitch_str = data_rotation_array[7][5:data_rotation_array[7].index('°')]

        # Convert the data from string to integer
        left_foot_roll = int(left_foot_roll_str)
        left_foot_pitch = int(left_foot_pitch_str)
        right_foot_roll = int(right_foot_roll_str)
        right_foot_pitch = int(right_foot_pitch_str)


        return left_foot_roll, left_foot_pitch, right_foot_roll, right_foot_pitch





