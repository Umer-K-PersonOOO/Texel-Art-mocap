import bpy
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
        return (x, y, z)
        
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
        if 'left_ear' in self.frame_keypoints and 'right_ear' in self.frame_keypoints:
            return self.compute_midpoint(self.frame_keypoints['left_ear'], self.frame_keypoints['right_ear'])
        elif 'left_eye' in self.frame_keypoints and 'right_eye' in self.frame_keypoints:
            return self.compute_midpoint(self.frame_keypoints['left_eye'], self.frame_keypoints['right_eye'])
        elif 'nose' in self.frame_keypoints:
            return self.frame_keypoints['nose']
        else:
            return None
        
    def update_calculated_frame_keypoints(self, frame_keypoints):
        self.frame_keypoints = {k: self.convert_coords(v) for k, v in frame_keypoints.items()}
        base_of_neck = self.compute_base_of_neck()
        if base_of_neck:
            self.frame_keypoints['base_of_neck'] = base_of_neck
        center_hip = self.compute_center_hip()
        if center_hip:
            self.frame_keypoints['center_hip'] = center_hip
        center_of_head = self.compute_center_of_head()
        if center_of_head:
            self.frame_keypoints['center_of_head'] = center_of_head
        
    def define_bone_hierarchy(self):
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
        }
        
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
        }
        
    def compute_relative_vectors(self):
        for parent, children in self.bone_hierarchy.items():
            parent_coords = self.frame_keypoints.get(parent)
            if parent_coords:
                for child in children:
                    child_coords = self.frame_keypoints.get(child)
                    if child_coords:
                        vector = np.subtract(child_coords, parent_coords)
                        self.relative_vectors[(parent, child)] = vector
        
    def compute_rotation_between_vectors(self, rest_vector, target_vector):
        rest_vec = Vector(rest_vector).normalized()
        target_vec = Vector(target_vector).normalized()
        rotation_quat = rest_vec.rotation_difference(target_vec)
        return rotation_quat
    
    def create_skeleton_with_rotations(self):
        positions = {'center_hip': (self.frame_width // 2, self.frame_height // 2)}

        for parent, children in self.bone_hierarchy.items():
            if parent in positions:
                parent_pos = Vector((positions[parent][0], positions[parent][1], 0))

                for child in children:
                    if (parent, child) in self.relative_vectors:
                        vector = self.relative_vectors[(parent, child)]
                        rotation_quat = self.compute_rotation_between_vectors((1, 0, 0), vector)

                        unit_vector = Vector((1, 0, 0))
                        rotated_vector = rotation_quat @ unit_vector

                        child_pos = parent_pos + rotated_vector * 100
                        positions[child] = (int(child_pos.x), int(child_pos.y))

        return positions
    
    def format_for_blender(self):
        formatted_data = []
        for (parent, child), vector in self.relative_vectors.items():
            if parent in self.frame_keypoints and child in self.frame_keypoints:
                rest_vector = (1, 0, 0)  # Assuming rest pose is along the x-axis
                rotation_quat = self.compute_rotation_between_vectors(rest_vector, vector)
                bone_name = self.bone_mapping.get(child, child)
                formatted_data.append({
                    'bone_name': bone_name,
                    'rotation': (rotation_quat.w, rotation_quat.x, rotation_quat.y, rotation_quat.z)
                })
        return formatted_data
    
    def process_frame(self):
        line = self.file.readline()
        while line:
            if line.startswith("Frame: "):
                self.update_calculated_frame_keypoints(self.frame_keypoints)
                self.compute_relative_vectors()
                # Example use of the formatted output for Blender
                blender_data = self.format_for_blender()
                self.frame_keypoints = {}
                self.relative_vectors = {}
                
                return blender_data
            else:
                params = line.split(", ")
                index = int(params[0])
                normal_vector = (float(params[1]), float(params[2]), float(params[3]))
                self.frame_keypoints[self.index_mapping[index]] = normal_vector
                
            line = self.file.readline()
        return None
    

class BlenderAnimator:
    def __init__(self, fbx_file_path, output_path):
        # Load the .fbx file into Blender
        bpy.ops.import_scene.fbx(filepath=fbx_file_path)
        self.output_path = output_path
        self.armature = bpy.data.objects['Armature']  # Assuming the armature name is 'Armature'
        print("Armature: ", self.armature)
        for bone in self.armature.pose.bones:
            # print("Bone: ", bone)
            print("Bone name: ", bone.name)
        self.skeleton = Skeleton()
        self.remove = set()
        
        
    def animate_skeleton(self):
        # Process each frame and animate accordingly
        blender_data = self.skeleton.process_frame()
        
        frame_number = 0
        while blender_data:
            
            bpy.context.scene.frame_set(frame_number)
            print("Frame: ", frame_number)
            
            for bone_data in blender_data:
                if frame_number == 0:
                    print("Bone: ", bone_data['bone_name'])
                bone_name = bone_data['bone_name']
                rotation = bone_data['rotation']
                self.remove.add(bone_name)
                if bone_name in self.armature.pose.bones:
                    pose_bone = self.armature.pose.bones[bone_name]
                    quat = Quaternion(rotation)
                    pose_bone.rotation_quaternion = quat
                    pose_bone.keyframe_insert(data_path="rotation_quaternion", frame=frame_number)
            
            frame_number += 1
            blender_data = self.skeleton.process_frame()
        print(self.remove)
        
        # Trial to test if api works
        # bpy.context.scene.frame_start = 1
        # bpy.context.scene.frame_end = 100

        # # Access the armature object by name
        # armature = bpy.data.objects['Armature']

        # # Enter Pose Mode to manipulate bones
        # bpy.context.view_layer.objects.active = armature
        # bpy.ops.object.mode_set(mode='POSE')

        # # Access the specific bone by name
        # bone_name = 'mixamorig:Hips'  # Change to your bone's name
        # bone = armature.pose.bones[bone_name]

        # # Set the frame range and translation distance
        # frame_start = 1
        # frame_end = 100
        # translation_distance = 150

        # # Loop over frames and set keyframes for location
        # for frame in range(frame_start, frame_end + 1):
        #     # Set the current frame
        #     bpy.context.scene.frame_set(frame)
            
        #     # Calculate the translation distance for this frame
        #     distance = translation_distance * (frame - frame_start) / (frame_end - frame_start)
            
        #     # Set the bone's location (translating along the X-axis; adjust if needed)
        #     bone.location = (distance, 0, 0)
            
        #     # Insert a keyframe for the bone's location
        #     bone.keyframe_insert(data_path="location", index=-1)
            
        
        bpy.ops.export_scene.fbx(filepath=self.output_path)


# Usage example
fbx_file_path = "/home/umerkhan/Desktop/code/texel/Texel-Art-mocap/blender/Remy.fbx" # Hard coded path to the .fbx file
fbx_output_path = "/home/umerkhan/Desktop/code/texel/Texel-Art-mocap/blender/RemyCompleted.fbx"
animator = BlenderAnimator(fbx_file_path, fbx_output_path)
animator.animate_skeleton()
