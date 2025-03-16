# semi-automated-sign-language-
 Sign Language Dataset Augmentation &amp; Recognition
 This project implements a semi-automated methodology for collecting and recognizing sign language gestures using computer vision and sequence matching techniques. The system extracts hand shapes and motion features from videos, compares them to reference signs, and identifies matching sequences. It enables dataset augmentation by detecting relevant sign instances in general video sources with minimal human intervention.
Given a reference video of a specific sign, the proposed algorithm searches for occurrences of that sign in various available videos, including those from online sources. The user must provide a reference video representing the target sign in sign language, and the algorithm will then analyze generic videos to detect instances of that sign.

Features:
-  Hand detection and feature extraction (shape, distance, movement)
-  Matching algorithm for sign recognition
-  Supports multiple sign languages
-  Generates structured datasets for training models

 Usage: Process a video, extract sign sequences, and expand existing datasets.
 Goal: Facilitate dataset creation for sign language recognition with minimal manual effort.


