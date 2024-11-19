import json

class SkeletonDataExporter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.index_mapping = {
            0: 'nose',
            1: 'left_eye_inner',
            2: 'left_eye',
            3: 'left_eye_outer',
            4: 'right_eye_inner',
            5: 'right_eye',
            6: 'right_eye_outer',
            7: 'left_ear',
            8: 'right_ear',
            9: 'mouth_left',
            10: 'mouth_right',
            11: 'left_shoulder',
            12: 'right_shoulder',
            13: 'left_elbow',
            14: 'right_elbow',
            15: 'left_wrist',
            16: 'right_wrist',
            17: 'left_pinky',
            18: 'right_pinky',
            19: 'left_index',
            20: 'right_index',
            21: 'left_thumb',
            22: 'right_thumb',
            23: 'left_hip',
            24: 'right_hip',
            25: 'left_knee',
            26: 'right_knee',
            27: 'left_ankle',
            28: 'right_ankle',
            29: 'left_heel',
            30: 'right_heel',
            31: 'left_foot_index',
            32: 'right_foot_index'
        }
        self.frame_keypoints = {}

    def load_keypoints(self):
        """
        Read joint positions from the 'body_coordinates.txt' file.
        """
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.startswith("Frame:"):
                    continue  # Skip frame headers
                params = line.split(", ")
                index = int(params[0])
                coords = (float(params[1]), float(params[2]), float(params[3]))
                self.frame_keypoints[self.index_mapping[index]] = coords

    def export_to_json(self, output_file):
        """
        Save the joint positions into a JSON file.
        """
        with open(output_file, 'w') as json_file:
            json.dump(self.frame_keypoints, json_file, indent=4)
        print(f"Joint positions exported to {output_file}")

# Usage Example
exporter = SkeletonDataExporter('body_coordinates.txt')  # Path to your input file
exporter.load_keypoints()
exporter.export_to_json('joint_positions.json')  # Path to the output file
