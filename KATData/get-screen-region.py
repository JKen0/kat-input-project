import pytesseract
import cv2


# Set the region of the screen to capture
left, top, width, height = 1288, 281, 478, 318

# Take a screenshot of the region
#screenshot = pyautogui.screenshot(region=(left, top, width, height))

screenshot = cv2.imread('KATData/static-kat-sensor-data-image/all-image.png')


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


print((left_foot_roll, left_foot_pitch))
print((right_foot_roll, right_foot_pitch))






