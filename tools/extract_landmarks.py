#!/usr/bin/env python3

import os
import csv
import mediapipe as mp

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
_OUTPUT = os.path.join(_DATA_DIR, "landmarks.csv")

_detector = None

def _get_detector():
    global _detector
    if _detector is not None:
        return _detector
    base_options = mp.tasks.BaseOptions(model_asset_path=os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "models", "hand_landmarker.task"
    ))
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.5,
    )
    _detector = mp.tasks.vision.HandLandmarker.create_from_options(options)
    return _detector

def _extract(image_path):
    import cv2
    frame = cv2.imread(image_path)
    if frame is None:
        return None
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = _get_detector().detect(mp_image)
    if not result.hand_landmarks:
        return None
    landmarks = result.hand_landmarks[0]
    ox, oy = landmarks[0].x, landmarks[0].y
    vector = []
    for lm in landmarks:
        vector.extend([lm.x - ox, lm.y - oy])
    return vector

def main():
    rows = []
    for split in ["train", "test"]:
        split_dir = os.path.join(_DATA_DIR, split)
        if not os.path.exists(split_dir):
            continue
        for letter in sorted(os.listdir(split_dir)):
            letter_dir = os.path.join(split_dir, letter)
            if not os.path.isdir(letter_dir):
                continue
            count = 0
            for fname in os.listdir(letter_dir):
                if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                vector = _extract(os.path.join(letter_dir, fname))
                if vector is None:
                    continue
                rows.append([letter] + vector)
                count += 1
            print(f"  {split}/{letter}: {count} landmarks extraídos")

    with open(_OUTPUT, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["label"]
        for i in range(21):
            header.extend([f"x{i}", f"y{i}"])
        writer.writerow(header)
        writer.writerows(rows)
    print(f"\n{len(rows)} amostras salvas em {_OUTPUT}")

if __name__ == "__main__":
    main()