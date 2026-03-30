from src.poses import FINGER_ORDER, POSES

def _euclidean_distance(vector_cam:list[float], vector_poses:list[float]) -> float:
    """Distância euclidiana entre dois vetores de estados dos dedos."""
    squared_diffs = []
    for cam_val,pose_val in zip(vector_cam, vector_poses):
        squared_diffs.append((cam_val-pose_val)**2)
    squared_sum = sum(squared_diffs)
    distance = squared_sum ** 0.5
    return distance

def recognize(finger_states:dict[str,float]) -> tuple[str,float]:
    """Retorna a letra LIBRAS mais próxima e a confiança (0.0–1.0)."""
    finger_vector = []
    for finger in FINGER_ORDER:
        finger_vector.append(finger_states[finger])
    
    all_distances = {}
    for letter,pose in POSES.items():
        pose_vector = []
        for finger in FINGER_ORDER:
            pose_vector.append(pose[finger])
        distance = _euclidean_distance(finger_vector, pose_vector)
        all_distances[letter] = distance

    closest_letter = min(all_distances, key=all_distances.get)
    closest_distance = all_distances[closest_letter]
    confidence = 1.0 - closest_distance
    return (closest_letter, confidence)