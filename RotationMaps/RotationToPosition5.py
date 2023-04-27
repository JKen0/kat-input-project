import numpy as np

class RotationToPosition5:
    def __init__(self, init_rot_roll, init_rot_pitch):
        self.user_init_rot = np.array([init_rot_roll, init_rot_pitch])
        self.test_init_rot = np.array([2, 12])
        self.user_rot_offsets = self.user_init_rot - self.test_init_rot
        self.keypoints = [
            {'key_value': 1, 'layer': 0, 'rot_roll': 3, 'rot_pitch': 13, 'pos_x': 0, 'pos_z': -2.0},
            {'key_value': 2, 'layer': 2, 'rot_roll': -12, 'rot_pitch': 13, 'pos_x': -13.5, 'pos_z': -2.5},
            {'key_value': 3, 'layer': 2, 'rot_roll': 18, 'rot_pitch': 13, 'pos_x': 13.0, 'pos_z': 1.0},
            {'key_value': 4, 'layer': 2, 'rot_roll': 3, 'rot_pitch': -2, 'pos_x': 0.0, 'pos_z': 14.75},
            {'key_value': 5, 'layer': 2, 'rot_roll': 3, 'rot_pitch': 28, 'pos_x': -0.5, 'pos_z': -14.75}
        ]
        self.user_keypoints = []


    def updateKeypoints(self):
        #NOTE: UPDATE TO USER_KEYPOINTS
        for i in range(0, len(self.keypoints)):
            offset_roll = self.user_rot_offsets[0]
            offset_pitch = self.user_rot_offsets[1]

            new_roll_rot = self.keypoints[i]['rot_roll'] - offset_roll
            new_pitch_rot = self.keypoints[i]['rot_pitch'] - offset_pitch

            self.keypoints[i].update({'rot_roll': new_roll_rot, 'rot_pitch': new_pitch_rot})



    def calcThreeClosestKeyPoints(self, new_rot_roll, new_rot_pitch):
        #NOTE: UPDATE TO USER_KEYPOINTS
        new_user_rot = np.array([new_rot_roll, new_rot_pitch])

        lowest_1 = {'key_value':  10000, 'distance': 1000000}
        lowest_2 = {'key_value':  10000, 'distance': 1000000}
        lowest_3 = {'key_value':  10000, 'distance': 1000000}

        for i in range(0, len(self.keypoints)):
            key_point_roll = self.keypoints[i]['rot_roll']
            key_point_pitch = self.keypoints[i]['rot_pitch']
            key_point_rot = np.array([key_point_roll, key_point_pitch])

            user_key_dist = np.linalg.norm(new_user_rot - key_point_rot)

            #case 1: it is the newest lowest
            if(user_key_dist < lowest_1['distance']):
                #update old 2nd oldest to be the new 3rd lowest
                lowest_3.update({'key_value':  lowest_2['key_value'], 'distance': lowest_2['distance']})
                #update old 1st oldest to be the new 2nd lowest
                lowest_2.update({'key_value':  lowest_1['key_value'], 'distance': lowest_1['distance']})
                #update lowest to the new values
                lowest_1.update({'key_value':  self.keypoints[i]['key_value'], 'distance': user_key_dist})

            #case 2: it is the 2nd lowest
            elif(user_key_dist < lowest_2['distance']):
                #update old 2nd oldest to be the new 3rd lowest
                lowest_3.update({'key_value':  lowest_2['key_value'], 'distance': lowest_2['distance']})
                #update 2nd lowest to the new values
                lowest_2.update({'key_value':  self.keypoints[i]['key_value'], 'distance': user_key_dist})

            #case 3: it is the 3rd lowest
            elif(user_key_dist < lowest_3['distance']):
                #update 3nd lowest to the new values
                lowest_3.update({'key_value':  self.keypoints[i]['key_value'], 'distance': user_key_dist})


        #print(lowest_1)
        #print(lowest_2)
        #print(lowest_3)

        #TO-DO: USE lowest_3 in the event that lowest_3 is TOO LARGE, its outside of the range of our prediction

        return [ lowest_1, lowest_2, lowest_3 ]


    def calcTriangleArea(self, input_1, input_2, input_3):
        #NOTE: To calculate triangle area, we can use heron's formula. Reference: https://www.britannica.com/science/Herons-formula
        side_length_1 = np.linalg.norm(input_3 - input_2)
        side_length_2 = np.linalg.norm(input_2 - input_1)
        side_length_3 = np.linalg.norm(input_3 - input_1)

        semi_perimeter = 1/2*(side_length_1 + side_length_2 + side_length_3)
        triangle_area = np.sqrt(semi_perimeter*(semi_perimeter - side_length_1)*(semi_perimeter - side_length_2)*(semi_perimeter - side_length_3))

        return triangle_area

    
    def calcPredictedPosition(self, new_rot_roll, new_rot_pitch):

        closest_keypoints = self.calcThreeClosestKeyPoints(new_rot_roll, new_rot_pitch)

        #print(closest_keypoints)

        key_point_1 = self.keypoints[closest_keypoints[0]['key_value'] - 1]
        key_point_2 = self.keypoints[closest_keypoints[1]['key_value'] - 1]
        key_point_3 = self.keypoints[closest_keypoints[2]['key_value'] - 1]

        key_rot_1 = np.array([ key_point_1['rot_roll'], key_point_1['rot_pitch'] ])
        key_rot_2 = np.array([ key_point_2['rot_roll'], key_point_2['rot_pitch'] ])
        key_rot_3 = np.array([ key_point_3['rot_roll'], key_point_3['rot_pitch'] ])
        user_rot = np.array([ new_rot_roll, new_rot_pitch ])

        key_pos_1 = np.array([ key_point_1['pos_x'], key_point_1['pos_z'] ])
        key_pos_2 = np.array([ key_point_2['pos_x'], key_point_2['pos_z'] ])
        key_pos_3 = np.array([ key_point_3['pos_x'], key_point_3['pos_z'] ])

        if (closest_keypoints[0]['distance'] < 0.01):
            return key_pos_1
        else:
            
            total_triangle_area = self.calcTriangleArea(key_rot_1, key_rot_2, key_rot_3)
            key_point_triangle_1 = self.calcTriangleArea(key_rot_2, key_rot_3, user_rot)
            key_point_triangle_2 = self.calcTriangleArea(key_rot_1, key_rot_3, user_rot)
            key_point_triangle_3 = self.calcTriangleArea(key_rot_2, key_rot_1, user_rot)


            key_point_weight_1 = key_point_triangle_1/total_triangle_area
            key_point_weight_2 = key_point_triangle_2/total_triangle_area
            key_point_weight_3 = key_point_triangle_3/total_triangle_area

            if(key_point_weight_1 + key_point_weight_2 + key_point_weight_3 > 1.01 or key_point_weight_1 + key_point_weight_2 + key_point_weight_3 < 0.98):
                return [np.nan, np.nan]

            user_pred_pos = key_point_weight_1*key_pos_1 + key_point_weight_2*key_pos_2 + key_point_weight_3*key_pos_3

            return user_pred_pos




        





        




