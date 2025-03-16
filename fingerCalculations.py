
import numpy as np
import cv2
import mediapipe as mp
import json


def extract_finger_movements(video_path, output_json_path):
    # Initialiser le détecteur de main de Mediapipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Liste pour stocker la séquence des mouvements
    finger_movements_sequence = []

    # Ouvrir la vidéo
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("FPS for reference:", fps)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Normaliser les couleurs de l'image
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Détecter les mains dans l'image
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            # Pour chaque main détectée
            for hand_landmarks in results.multi_hand_landmarks:
                # Extraire les coordonnées normalisées des articulations des doigts
                finger_coordinates = np.array([[landmark.x, landmark.y] for landmark in hand_landmarks.landmark])

                # Calculer la forme des doigts
                finger_shapes = calculate_finger_shapes(finger_coordinates)

                # Calculer la distance entre les doigts
                finger_distances = calculate_finger_distances(finger_coordinates)

                # Ajouter la forme des doigts et la distance entre les doigts à la liste
                finger_movements_sequence.append({"shapes": finger_shapes, "distances": finger_distances})


    # Fermer la vidéo
    cap.release()

    # Sauvegarder la séquence des mouvements dans un fichier JSON
    with open(output_json_path, 'w') as json_file:
        json.dump(finger_movements_sequence, json_file)




def calculate_finger_shapes(finger_coordinates):
    # Calculer la longueur de chaque segment du doigt
    finger_lengths = []
    for i in range(1, 5):  # Les doigts ont 4 segments (à l'exception du pouce qui en a 3)
        length = np.linalg.norm(finger_coordinates[i] - finger_coordinates[i - 1])
        finger_lengths.append(length)

    # Calculer le rapport de longueur entre les segments (forme du doigt)
    finger_shapes = []
    for i in range(1, 4):  # Il y a 3 rapports de longueur pour chaque doigt
        shape = finger_lengths[i] / finger_lengths[i - 1]
        finger_shapes.append(shape)

    return finger_shapes

def calculate_finger_distances(finger_coordinates):
    # Calculer la distance entre les articulations des doigts
    finger_distances = []

    for i in range(1, 5):  # Les doigts ont 4 articulations

        distance = np.linalg.norm(finger_coordinates[i] - finger_coordinates[i - 1])
        finger_distances.append(distance)

    return finger_distances

