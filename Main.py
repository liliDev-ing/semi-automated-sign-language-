
import numpy as np
import cv2
import mediapipe as mp
import json
import fingerCalculations
from SequenceComparaison import compare_sequences


def match_finger_movements(video_path_general, json_path_reference, output_folder, threshold=0.75):
    # Load the reference video movement sequence from the JSON file
    with open(json_path_reference, 'r') as json_file:
        reference_sequence = json.load(json_file)

    # Initialize Mediapipe's hand detector
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    cap_general = cv2.VideoCapture(video_path_general)
    fps = cap_general.get(cv2.CAP_PROP_FPS)
    print("FPS for general:", fps)
    total_frames_general = int(cap_general.get(cv2.CAP_PROP_FRAME_COUNT))

    # Size of the comparison window (number of frames)
    window_size = len(reference_sequence)
    print (f"window size is{window_size}")
    print(f"total_frames_general{total_frames_general}")

    occurrences = []
    c= 0
    nn=0
    for _ in range(c, total_frames_general - window_size + 1):

        start_frame = c
        nn=nn+1
        print(f'start frame {start_frame}')
        print (c)
        window_sequence = []

        # Moving around the window and extracting specific hand poses
        cap_general.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        for _ in range(window_size):
            ret, frame_general = cap_general.read()
            if not ret:
                break


            frame_general_rgb = cv2.cvtColor(frame_general, cv2.COLOR_BGR2RGB)

            # Detect hands in the general image

            results_general = hands.process(frame_general_rgb)

            if results_general.multi_hand_landmarks:
                # For each hand detected in the general image
                for hand_landmarks_general in results_general.multi_hand_landmarks:

                    finger_coordinates_general = np.array([[landmark.x, landmark.y] for landmark in hand_landmarks_general.landmark])

                    finger_shapes_general = fingerCalculations.calculate_finger_shapes(finger_coordinates_general)

                    # Calculate the distance between the fingers
                    finger_distances_general = fingerCalculations.calculate_finger_distances(finger_coordinates_general)
                    window_sequence.append({"shapes": finger_shapes_general, "distances": finger_distances_general})

        # Comparison with the reference sequence
        match_result = compare_sequences(reference_sequence, window_sequence)
        print(f"match result is {match_result}")

        if match_result >= threshold :
        #if (nn >= window_size -(window_size/4)) & (match_result >= 0.85) :

         #occurrences.append({"frame_index": int(cap_general.get(cv2.CAP_PROP_POS_FRAMES)), "match_result": match_result})
             print ('********************************found match**************************')
             occurrences.append({"start_frame": start_frame, "end_frame": start_frame + window_size - 1})
             print(f'start frame in found {start_frame}')
        if (c + window_size) < (total_frames_general - window_size -1):
            c += window_size

        else:
            break



    cap_general.release()

    # Save occurrences to output folder
    for idx, occurrence in enumerate(occurrences):
        start_frame = occurrence["start_frame"]
        end_frame = occurrence["end_frame"]
        output_path = f'{output_folder}/occurrence_{idx + 1}.mp4'

        # Save the occurrence video
        save_occurrence_video(video_path_general, start_frame, end_frame, output_path)

    return occurrences


def save_occurrence_video(video_path, start_frame, end_frame, output_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can adjust the codec as needed
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Set the video capture to the starting frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Read and write frames within the specified range
    for frame_number in range(start_frame, end_frame + 1):
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)

    # Release video capture and writer
    cap.release()
    out.release()

def  changeFPS (input_v, output_v):
    input_video = cv2.VideoCapture(input_v)

    # Get the FPS of the input video
    fps = input_video.get(cv2.CAP_PROP_FPS)

    # Define the desired FPS for the output video
    desired_fps = 30

    # Open the output video file
    output_video = cv2.VideoWriter(output_v,
                                   cv2.VideoWriter_fourcc(*'mp4v'),
                                   desired_fps,
                                   (int(input_video.get(3)), int(input_video.get(4))))

    # Read and write frames with the desired FPS
    while input_video.isOpened():
        ret, frame = input_video.read()
        if not ret:
            break
        output_video.write(frame)

    # Release video capture and writer objects
    input_video.release()
    output_video.release()


# call of the functions

video_ref_path = "C:/sortie/reference/father/father.mp4"
output_json_path = "C:/sortie/reference/father/ref.json"

fingerCalculations.extract_finger_movements(video_ref_path, output_json_path)

video_path_general = "C:/sortie/test/family/family3.mp4"
output_folder = "C:/sortie/output/father"
occurrences = match_finger_movements(video_path_general, output_json_path, output_folder)




