import numpy as np
from mathutils import Vector, Quaternion



class Skeleton:
    def __init__(self):
        self.file = open('body_coordinates.txt', 'r')
        self.frame_keypoints = {}
        self.relative_vectors = {}
        self.bone_hierarchy = {}
        self.frames = []
        self.bone_mapping = {}
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
        
        self.define_bone_hierarchy()   
        
    def convert_coords(self, coords):
        x, y, z = coords
        blender_x = x
        blender_y = -z  # Invert Z for Blender's Y
        blender_z = y
        return (blender_x, blender_y, blender_z)
        
        
    def compute_midpoint(self, point_a, point_b):
        return [(a + b) / 2 for a, b in zip(point_a, point_b)]
    
    def compute_base_of_neck(self):
        left_shoulder = self.frame_keypoints.get('left_shoulder')
        right_shoulder = self.frame_keypoints.get('right_shoulder')
        if left_shoulder and right_shoulder:
            return self.compute_midpoint(left_shoulder, right_shoulder)
        else:
            return None  # Handle missing data appropriately
    
    def compute_center_hip(self):
        left_hip = self.frame_keypoints.get('left_hip')
        right_hip = self.frame_keypoints.get('right_hip')
        if left_hip and right_hip:
            return self.compute_midpoint(left_hip, right_hip)
        else:
            return None
        
    def compute_center_of_head(self):
        # Implement as discussed earlier
        if 'left_ear' in self.frame_keypoints and 'right_ear' in self.frame_keypoints:
            return self.compute_midpoint(self.frame_keypoints['left_ear'], self.frame_keypoints['right_ear'])
        elif 'left_eye' in self.frame_keypoints and 'right_eye' in self.frame_keypoints:
            return self.compute_midpoint(self.frame_keypoints['left_eye'], self.frame_keypoints['right_eye'])
        elif 'nose' in self.frame_keypoints:
            return self.frame_keypoints['nose']
        else:
            return None
        
    def update_calculated_frame_keypoints(self, frame_keypoints):
        # Convert frame_keypoints to Blender coordinate system
        self.frame_keypoints = {k: self.convert_coords(v) for k, v in frame_keypoints.items()}
        # Compute intermediate frame_keypoints
        base_of_neck = self.compute_base_of_neck()
        if base_of_neck:
            self.frame_keypoints['base_of_neck'] = base_of_neck
        center_hip = self.compute_center_hip()
        if center_hip:
            self.frame_keypoints['center_hip'] = center_hip
        center_of_head = self.compute_center_of_head()
        if center_of_head:
            self.frame_keypoints['center_of_head'] = center_of_head
        # frame_keypoints are now updated with computed points
        
    def define_bone_hierarchy(self):
        # Define parent-child relationships
        self.bone_hierarchy = {
            'center_hip': ['base_of_neck', 'left_hip', 'right_hip'],
            'base_of_neck': ['center_of_head', 'left_shoulder', 'right_shoulder'],
            'left_shoulder': ['left_elbow'],
            'left_elbow': ['left_wrist'],
            'right_shoulder': ['right_elbow'],
            'right_elbow': ['right_wrist'],
            'left_hip': ['left_knee'],
            'left_knee': ['left_ankle'],
            'left_ankle': ['left_foot_index'],
            'right_hip': ['right_knee'],
            'right_knee': ['right_ankle'],
            'right_ankle': ['right_foot_index'],
            # Add other bones as needed
        }
        
        # Bone mapping to the armature bones in Blender
        self.bone_mapping = {
            'center_hip': 'mixamorig:Hips',
            'base_of_neck': 'mixamorig:Neck',
            'center_of_head': 'mixamorig:Head',
            'left_shoulder': 'mixamorig:LeftShoulder',
            'left_elbow': 'mixamorig:LeftArm',
            'left_wrist': 'mixamorig:LeftForeArm',
            'right_shoulder': 'mixamorig:RightShoulder',
            'right_elbow': 'mixamorig:RightArm',
            'right_wrist': 'mixamorig:RightForeArm',
            'left_hip': 'mixamorig:LeftUpLeg',
            'left_knee': 'mixamorig:LeftLeg',
            'left_ankle': 'mixamorig:LeftFoot',
            'left_foot_index': 'mixamorig:LeftToeBase',
            'right_hip': 'mixamorig:RightUpLeg',
            'right_knee': 'mixamorig:RightLeg',
            'right_ankle': 'mixamorig:RightFoot',
            'right_foot_index': 'mixamorig:RightToeBase',
            # Add other mappings as needed
        }
        
    # Prints for debugging
    def compute_relative_vectors(self):
        #self.relative_vectors = {}
        for parent, children in self.bone_hierarchy.items():
            print(parent)
            print(children)
            parent_coords = self.frame_keypoints.get(parent)
            if parent_coords:
                for child in children:
                    print(child)
                    child_coords = self.frame_keypoints.get(child)
                    if child_coords:
                        # Compute vector from parent to child
                        vector = np.subtract(child_coords, parent_coords)
                        self.relative_vectors[(parent, child)] = vector
                    else:
                        print(f"Child keypoint {child} not found in current frame.")
            else:
                print(f"Parent keypoint {parent} not found in current frame.")
        
    def compute_rotation_between_vectors(self, rest_vector, target_vector):
        rest_vec = Vector(rest_vector).normalized()
        target_vec = Vector(target_vector).normalized()
        rotation_quat = rest_vec.rotation_difference(target_vec)
        return rotation_quat
    
    
    def process_frame(self):
        print("f")
        line = self.file.readline()
        print(line)
        frame_count = 0
        if(not line or line.strip() != 'Frame: 0'):
            print("Error: File in incorrect format.")
            return None
        line = self.file.readline()
        while line:
            if (line.startswith("Frame: ")):
                # Finish working on frame
                
                self.update_calculated_frame_keypoints(self.frame_keypoints)
                self.compute_relative_vectors()
                # Here, we would process frame 
                print(self.frame_keypoints, self.relative_vectors)
                # Clean up for next frame
                self.frame_keypoints = {}
                self.relative_vectors = {}
                frame_count += 1
                return None 
            else:
                params = line.split(", ")
                index = int(params[0])
                normal_vector = (float(params[1]), float(params[2]), float(params[3]))
                self.frame_keypoints[self.index_mapping[index]] = normal_vector
                
                
            line = self.file.readline()
                
            
        
    # For blender specifically:
    def apply_rotations_to_bones(self, armature, frame_number):
        pose_bones = armature.pose.bones
        for (parent, child), target_vector in self.relative_vectors.items():
            bone_name = self.bone_mapping.get(child)
            if bone_name and bone_name in pose_bones:
                bone = pose_bones[bone_name]
                
                # Get the rest pose vector of the bone
                rest_bone = armature.data.bones[bone_name]
                rest_head = Vector(rest_bone.head_local)
                rest_tail = Vector(rest_bone.tail_local)
                rest_vector = rest_tail - rest_head
                
                # Compute the rotation
                rotation_quat = self.compute_rotation_between_vectors(rest_vector, target_vector)
                
                # Apply the rotation
                bone.rotation_mode = 'QUATERNION'
                bone.rotation_quaternion = rotation_quat @ bone.rotation_quaternion
                bone.keyframe_insert(data_path="rotation_quaternion", frame=frame_number)
            else:
                print(f"Bone {bone_name} not found in armature.")
        
hi = Skeleton()    
hi.process_frame()
