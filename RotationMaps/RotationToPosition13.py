import numpy as np

class RotationToPosition13:
    def __init__(self, init_rot_roll, init_rot_pitch):
        self.user_init_rot = np.array([init_rot_roll, init_rot_pitch])
        self.test_init_rot = np.array([2, 12])
        self.user_rot_offsets = self.user_init_rot - self.test_init_rot
        self.keypoints = [
            {'key_value': 1, 'layer': 0, 'rot_roll': 3, 'rot_pitch': 12, 'pos_x': 2.75, 'pos_z': 0.0},
            {'key_value': 2, 'layer': 1, 'rot_roll': 3, 'rot_pitch': 5, 'pos_x': 0.0, 'pos_z': 9.0},
            {'key_value': 3, 'layer': 1, 'rot_roll': 3, 'rot_pitch': -2, 'pos_x': 0.0, 'pos_z': 14.5},
            {'key_value': 4, 'layer': 2, 'rot_roll': 3, 'rot_pitch': 19, 'pos_x': -1.0, 'pos_z': -7.5},
            {'key_value': 5, 'layer': 2, 'rot_roll': 3, 'rot_pitch': 26, 'pos_x': 1.0, 'pos_z': -14.25},
            {'key_value': 6, 'layer': 1, 'rot_roll': -4, 'rot_pitch': 12, 'pos_x': -9.0, 'pos_z': 0.0},
            {'key_value': 7, 'layer': 1, 'rot_roll': 10, 'rot_pitch': 12, 'pos_x': 9.5, 'pos_z': 2.0},
            {'key_value': 8, 'layer': 2, 'rot_roll': -11, 'rot_pitch': 12, 'pos_x': -14.0, 'pos_z': 0.5},
            {'key_value': 9, 'layer': 2, 'rot_roll': 17, 'rot_pitch': 12, 'pos_x': 12.5, 'pos_z': 2.0},
            {'key_value': 10, 'layer': 1, 'rot_roll': -4, 'rot_pitch': 5, 'pos_x': -8.5, 'pos_z': 8.5},
            {'key_value': 11, 'layer': 1, 'rot_roll': 10, 'rot_pitch': 5, 'pos_x': 8.5, 'pos_z': 9.0},
            {'key_value': 12, 'layer': 1, 'rot_roll': -4, 'rot_pitch': 19, 'pos_x': -7.5, 'pos_z': -6.0},
            {'key_value': 13, 'layer': 1, 'rot_roll': 10, 'rot_pitch': 19, 'pos_x': 8, 'pos_z': -6.5}
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

        # CREATE FAKE LOWEST BOUNDS WITH VERY LARGE DISTANCES
        lowest_1 = {'key_value':  10000, 'distance': 1000000}
        lowest_2 = {'key_value':  10000, 'distance': 1000000}
        lowest_3 = {'key_value':  10000, 'distance': 1000000}

        # LOOP THROUGH EACH KEY POINT
        for i in range(0, len(self.keypoints)):

            # FETCH KEY POINT ROTATION VALUES
            key_point_roll = self.keypoints[i]['rot_roll']
            key_point_pitch = self.keypoints[i]['rot_pitch']
            key_point_rot = np.array([key_point_roll, key_point_pitch])

            # CALCULATE DISTANCE BETWEEN KEY POINT ROTATION AND USER ROTATION
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

        # RETURN THE CLOSEST 3 POINTS
        return [ lowest_1, lowest_2, lowest_3 ]


    def calcTriangleArea(self, input_1, input_2, input_3):
        #NOTE: To calculate triangle area, we can use heron's formula. Reference: https://www.britannica.com/science/Herons-formula
        
        # CALCULATE 3 SIDE LENGTHS
        side_length_1 = np.linalg.norm(input_3 - input_2)
        side_length_2 = np.linalg.norm(input_2 - input_1)
        side_length_3 = np.linalg.norm(input_3 - input_1)

        # CALCULATE SEMI PERIMETER
        semi_perimeter = 1/2*(side_length_1 + side_length_2 + side_length_3)

        # CALCULATE TRIANGLE AREA
        triangle_area = np.sqrt(semi_perimeter*(semi_perimeter - side_length_1)*(semi_perimeter - side_length_2)*(semi_perimeter - side_length_3))

        # RETURN TRIANGLE AREA
        return triangle_area

    
    def calcPredictedPosition(self, new_rot_roll, new_rot_pitch):

        closest_keypoints = self.calcThreeClosestKeyPoints(new_rot_roll, new_rot_pitch)

        #print(closest_keypoints)

        # FETCH THE 3 CLOSEST KEY POINT DATA
        key_point_1 = self.keypoints[closest_keypoints[0]['key_value'] - 1]
        key_point_2 = self.keypoints[closest_keypoints[1]['key_value'] - 1]
        key_point_3 = self.keypoints[closest_keypoints[2]['key_value'] - 1]

        # GIVEN THE 3 CLOSEST POINTS, FETCH THE ROTATION DATA
        key_rot_1 = np.array([ key_point_1['rot_roll'], key_point_1['rot_pitch'] ])
        key_rot_2 = np.array([ key_point_2['rot_roll'], key_point_2['rot_pitch'] ])
        key_rot_3 = np.array([ key_point_3['rot_roll'], key_point_3['rot_pitch'] ])

        # FETCH THE USER ROTATION 
        user_rot = np.array([ new_rot_roll, new_rot_pitch ])

        # GIVEN THE 3 CLOSEST POINTS, FETCH THE POSITION DATA
        key_pos_1 = np.array([ key_point_1['pos_x'], key_point_1['pos_z'] ])
        key_pos_2 = np.array([ key_point_2['pos_x'], key_point_2['pos_z'] ])
        key_pos_3 = np.array([ key_point_3['pos_x'], key_point_3['pos_z'] ])

        # IF THE CLOSEST POINT HAS DISTANCE 0 RELATIVE TO USER ROTATION, JUST RETURN THE POSITION OF THAT CLOSEST POINT
        if (closest_keypoints[0]['distance'] < 0.01):
            return key_pos_1
        
        # IF NOT, USE INTERPOLATION
        else:
            # CALCULATE BIG TRIANGLE, and 3 SMALLER TRIANGLES
            total_triangle_area = self.calcTriangleArea(key_rot_1, key_rot_2, key_rot_3)
            key_point_triangle_1 = self.calcTriangleArea(key_rot_2, key_rot_3, user_rot)
            key_point_triangle_2 = self.calcTriangleArea(key_rot_1, key_rot_3, user_rot)
            key_point_triangle_3 = self.calcTriangleArea(key_rot_2, key_rot_1, user_rot)

            # GIVEN AREAS, CALCULATE WEIGHTS FOR EACH KEY POINNT
            key_point_weight_1 = key_point_triangle_1/total_triangle_area
            key_point_weight_2 = key_point_triangle_2/total_triangle_area
            key_point_weight_3 = key_point_triangle_3/total_triangle_area

            # IF TOTAL WEIGHTS NOT CLOSE TO 1, ROTATION DATA IS OUT OF BOUNDS OF WHAT IS ALLOWED
            # RETURN NAN
            if(key_point_weight_1 + key_point_weight_2 + key_point_weight_3 > 1.01 or key_point_weight_1 + key_point_weight_2 + key_point_weight_3 < 0.98):
                return [np.nan, np.nan]

            # CALCULATE USER POSITION BASED ON WEIGHTED AVERAGE
            user_pred_pos = key_point_weight_1*key_pos_1 + key_point_weight_2*key_pos_2 + key_point_weight_3*key_pos_3

            # RETURN CALCULATED USER POSITION
            return user_pred_pos




        
