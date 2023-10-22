import KATData.FetchKATData as FetchKAT
import datetime
import csv
import keyboard
import numpy as np

# TO-DO: CHANGE PARAMETERS SINNCE THEY WILL CHANGE
KATGATE_REFERENCE_POS = np.array([-1, -1])
LF_ROTATION_INITIAL = np.array([2, 12])
RF_ROTATION_INITIAL = np.array([4, 13])


def save_data_csv(data):
    # Prompt the user for a filename
    filename = input("Enter a filename for the CSV file: ")
    save_location = './RotationData/' + filename + '.csv'

    with open(save_location, 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.DictWriter(file, fieldnames=data[0].keys())

        # Write the header row
        writer.writeheader()

        # Write each data row to the CSV file
        for row in data:
            writer.writerow(row)


kat_config = FetchKAT.FetchKATData(KATGATE_REFERENCE_POS[0], KATGATE_REFERENCE_POS[1])
rot_data = []


print('')
print('!!!!!!!!!RUNNNING KAT FETCH DATA CODE!!!!!!!!!!!!')
print('To stop and save rotations, press "Escape".')
print('To ONLY stop, press "Backspace".')

while True:
    LF_roll , LF_pitch, RF_roll, RF_pitch = kat_config.getData()
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    rot_data.append([formatted_datetime, LF_roll, LF_pitch, RF_roll, RF_pitch])

    # Check if the user wants to stop
    if keyboard.is_pressed('escape'):
        save_data = []
        for i in range(0, len(rot_data)):
            dict_data = {
                'dateTime': rot_data[i][0],
                'LF_roll': rot_data[i][1],
                'LF_pitch': rot_data[i][2],
                'RF_roll': rot_data[i][3],
                'RF_pitch': rot_data[i][4]
            }

            save_data.append(dict_data)

        # Save the data as a CSV file
        save_data_csv(save_data)
        break

    if keyboard.is_pressed('backspace'):
        break
