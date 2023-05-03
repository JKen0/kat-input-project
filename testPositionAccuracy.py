'''
only need to install the following modules, code should run
pip install numpy
pip install matplotlib
'''

import RotationMaps.RotationToPosition5 as rtp5
import RotationMaps.RotationToPosition13 as rtp13
import numpy as np

a = rtp5.RotationToPosition5(2, 12)
b = rtp13.RotationToPosition13(2, 12)

# ALL TEST POINTS
test_points = [
    {'key_value': 0, 'layer': -1, 'rot_roll': 2, 'rot_pitch': 12, 'pos_x': 0.0, 'pos_z': 0.0},
    {'key_value': 14, 'layer': -1, 'rot_roll': -3, 'rot_pitch': 8, 'pos_x': -8.0, 'pos_z': 6.5},
    {'key_value': 15, 'layer': -1, 'rot_roll': 11, 'rot_pitch': 20, 'pos_x': 8.5, 'pos_z': -7.5},
    {'key_value': 16, 'layer': -1, 'rot_roll': 8, 'rot_pitch': 16, 'pos_x': 6.0, 'pos_z': -3.0},
    {'key_value': 17, 'layer': -1, 'rot_roll': 11, 'rot_pitch': 4, 'pos_x': 8.0, 'pos_z': 10.0},
    {'key_value': 18, 'layer': -1, 'rot_roll': -2, 'rot_pitch': 21, 'pos_x': -5.5, 'pos_z': -7.0},
    {'key_value': 19, 'layer': -1, 'rot_roll': -5, 'rot_pitch': 6, 'pos_x': -8.0, 'pos_z': -9.0},
]

# LOOP THROUGH ALL TEST POINTS
for i in range(0, len(test_points)):
    key_value = test_points[i]['key_value']
    ground_truth = np.array([ test_points[i]['pos_x'] , test_points[i]['pos_z'] ])

    rot_roll = test_points[i]['rot_roll']
    rot_pitch = test_points[i]['rot_pitch']

    # ESTIMATE VLAUES
    predictPos5 = a.calcPredictedPosition(rot_roll, rot_pitch)
    predictPos13 = b.calcPredictedPosition(rot_roll, rot_pitch)

    # CALCULATE ERRORS
    error5 = np.linalg.norm(predictPos5 - ground_truth)
    error13 = np.linalg.norm(predictPos13 - ground_truth)

    # PRINT RESULTS
    print('key_value:', key_value, '  ground_truth:', ground_truth, '  predict5:', predictPos5, '  predict13:', predictPos13, '  error5: ', error5, '  error13:', error13)




#c = 8
#d = 16
#a.calcPredictedPosition(c,d)
#b.calcPredictedPosition(c,d)
#a.calcPredictedPosition(11,20)
#a.calcPredictedPosition(2,13)
#b.calcPredictedPosition(2,13)


#area_a = a.calcTriangleArea(np.array([2, 21]), np.array([8, 12]), np.array([11, 26]))
#print(area_a)
