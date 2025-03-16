import numpy as np


# Sequence comparison
# Features are compared individually and weighted according to the coefficients
# The final result is the sum of the weighted scores

def compare_sequences(reference_sequence, window_sequence):

    shapeList=[]
    distanceList=[]


    total_score = 0
    jk=0

    for ref_frame, win_frame in zip(reference_sequence, window_sequence):

        # Finger shape comparison
        shapes_similarity = compare_finger_shapes(ref_frame["shapes"], win_frame["shapes"])
        shapeList.append(shapes_similarity)

        # Comparison of distances between fingers
        distances_similarity = compare_finger_distances(ref_frame["distances"], win_frame["distances"])
        distanceList.append(distances_similarity)

        # characteristics Weighting
        # you can vary these coefficients to test the best matching
        shapes_weight = 0.3
        distances_weight = 0.7

         # this test is to ensure that values less than the threshold are neither at the beginning nor at the end of the sequence.
         # it allows to reduce the number of false positives.
         # this test shows good results with words containig one sign.

        """""
        if distances_similarity < 0.6 or shapes_similarity < 0.6 :
            if (jk not in [ 0,1, 2,3,len(window_sequence)-3,len(window_sequence)-2, len(window_sequence)-1,len(window_sequence)] ) :
                # 4 successive frames less than the threshold and which are not in the extremities of the video give a negative match
                negative=negative+1
                if negative > 3:
                   jk=0
                   negative=0
                   break
            else:
                negative = 0

        else:
            negative=0
"""


        frame_score = shapes_weight * shapes_similarity + distances_weight * distances_similarity # + coordinates_weight * coordinates_similarity
        total_score = total_score+frame_score
        jk=jk+1

    # Calculation of the final score

    print(f"distance similarity, {distanceList}")
    print(f"shape similarity, {shapeList}")
    if (jk>0) & (jk>= len(window_sequence)*0.9) :
         average_score = total_score / jk
         print (f'number of frames compared is { jk }')
    else:
        average_score =0


    return average_score




def compare_finger_shapes(reference_shapes, general_shapes):

    return np.corrcoef(reference_shapes, general_shapes)[0, 1]

def compare_finger_distances(reference_distances, general_distances):

    return np.corrcoef(reference_distances, general_distances)[0, 1]

def compare_finger_coordinates(reference_coordinates, general_coordinates):

    return np.corrcoef(reference_coordinates, general_coordinates)[0, 1]
