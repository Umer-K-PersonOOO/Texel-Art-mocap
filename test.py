import numpy as np
from mathutils import Vector, Quaternion
import cv2

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

        # Define frame dimensions for the visualization
        self.frame_width = 640
        self.frame_height = 480

        # Initialize video writer for saving the video
        self.video_writer = cv2.VideoWriter(
            'skeleton_visualization.mp4',                  # Output file name
            cv2.VideoWriter_fourcc(*'mp4v'),               # Codec
            30,                                            # Frame rate
            (self.frame_width, self.frame_height)          # Frame dimensions
        )
        
        self.define_bone_hierarchy()
        
    def convert_coords(self, coords):
        x, y, z = coords
        return (x, z, y)
        
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
                        # if parent == 'left_shoulder' and child == 'left_elbow':
                        #     print(f"Rotation quaternion between {parent} and {child}: {rotation_quat}")
                        # if parent == 'right_shoulder' and child == 'right_elbow':
                        #     print(f"Rotation quaternion between {parent} and {child}: {rotation_quat}")
                        unit_vector = Vector((1, 0, 0))
                        rotated_vector = rotation_quat @ unit_vector

                        child_pos = parent_pos + rotated_vector * 100
                        positions[child] = (int(child_pos.x), int(child_pos.y))
        
        # positions = {'left_shoulder': (self.frame_width // 2, self.frame_height // 2)}
        # for parent, children in self.bone_hierarchy.items():
        #     if parent == 'left_shoulder' and parent in positions:
        #         parent_pos = Vector((positions[parent][0], positions[parent][1], 0))

        #         for child in children:
        #             if (parent, child) in self.relative_vectors:
        #                 vector = self.relative_vectors[(parent, child)]
        #                 rotation_quat = self.compute_rotation_between_vectors((1, 0, 0), vector)
        #                 unit_vector = Vector((1, 0, 0))
        #                 rotated_vector = rotation_quat @ unit_vector

        #                 child_pos = parent_pos + rotated_vector * 100
        #                 positions[child] = (int(child_pos.x), int(child_pos.y))

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
        frame_count = 0
        if not line or line.strip() != 'Frame: 0':
            print("Error: File in incorrect format.")
            return None
        line = self.file.readline()
        while line:
            if line.startswith("Frame: "):
                self.update_calculated_frame_keypoints(self.frame_keypoints)
                self.compute_relative_vectors()
                print(frame_count)
                if(frame_count == 10):
                    print("Exporting blue skeleton to Blender-compatible Python script...")
                    self.export_blue_skeleton('blue_skeleton.py')
                    break
                self.visualize_frame()
                # Example use of the formatted output for Blender
                blender_data = self.format_for_blender()
                self.frame_keypoints = {}
                self.relative_vectors = {}
                frame_count += 1
            else:
                params = line.split(", ")
                index = int(params[0])
                normal_vector = (float(params[1]), float(params[2]), float(params[3]))
                self.frame_keypoints[self.index_mapping[index]] = normal_vector
                
            line = self.file.readline()
    
    def visualize_frame(self):
        frame = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.uint8)

        for keypoint, coords in self.frame_keypoints.items():
            x, y, _ = self.convert_coords(coords)
            x = int(x * self.frame_width / 2 + self.frame_width / 2)
            y = int(y * self.frame_height / 2 + self.frame_height / 2)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        for (parent, child), vector in self.relative_vectors.items():
            if parent in self.frame_keypoints and child in self.frame_keypoints:
                parent_coords = self.frame_keypoints[parent]
                child_coords = self.frame_keypoints[child]
                x1, y1, _ = self.convert_coords(parent_coords)
                x2, y2, _ = self.convert_coords(child_coords)
                x1, y1 = int(x1 * self.frame_width / 2 + self.frame_width / 2), int(y1 * self.frame_height / 2 + self.frame_height / 2)
                x2, y2 = int(x2 * self.frame_width / 2 + self.frame_width / 2), int(y2 * self.frame_height / 2 + self.frame_height / 2)
                cv2.arrowedLine(frame, (x1, y1), (x2, y2), (255, 0, 0), 2, tipLength=0.3)

        rotated_positions = self.create_skeleton_with_rotations()

        for parent, children in self.bone_hierarchy.items():
            if parent in rotated_positions:
                parent_x, parent_y = rotated_positions[parent]

                for child in children:
                    if child in rotated_positions:
                        child_x, child_y = rotated_positions[child]
                        cv2.arrowedLine(frame, (parent_x, parent_y), (child_x, child_y), (255, 105, 180), 2, tipLength=0.3)

        cv2.imshow('Skeleton Visualization (Absolute, Relative, and Rotations)', frame)
        cv2.waitKey(60)
        self.video_writer.write(frame)
        
    def export_blue_skeleton(self, output_path):
        """
        Exports the blue skeleton as a Blender-compatible Python script.
        """
        with open(output_path, 'w') as file:
            file.write("import bpy\n\n")
            file.write("# Create spheres and lines for blue skeleton in Blende rdtfyguhiojpk;l['r\n")
            
            # Add spheres for keypoints
            for keypoint, coords in self.frame_keypoints.items():
                x, y, z = coords
                x = int(x * self.frame_width / 2) / 10
                y = int(y * self.frame_height / 2) / 10
                z*=-20
                # z = 0  # Since this is a 2D visualization, Z is set to 0
                file.write(f"# Sphere for {keypoint}\n")
                file.write("bpy.ops.mesh.primitive_uv_sphere_add(\n")
                file.write(f"    radius=0.15,  # Adjust size of spheres\n")
                file.write(f"    location=({x}, {y}, {z})\n")
                file.write(")\n")
                file.write(f"bpy.context.object.name = '{keypoint}'\n\n")
            
            # Add lines for connections
            for (parent, child), vector in self.relative_vectors.items():
                if parent in self.frame_keypoints and child in self.frame_keypoints:
                    parent_coords = self.frame_keypoints[parent]
                    child_coords = self.frame_keypoints[child]
                    x1, y1, z1 = parent_coords
                    x2, y2, z2 = child_coords
                    x1 = int(x1 * self.frame_width / 2 ) / 10
                    y1 = int(y1 * self.frame_height / 2 ) / 10
                    x2 = int(x2 * self.frame_width / 2 ) / 10
                    y2 = int(y2 * self.frame_height / 2 ) / 10
                    z1*=-20
                    z2*=-20
                    
                    file.write(f"# Line connecting {parent} to {child}\n")
                    file.write("curve = bpy.data.curves.new(type='CURVE', name='Line')\n")
                    file.write("curve.dimensions = '3D'\n")
                    file.write("spline = curve.splines.new(type='POLY')\n")
                    file.write("spline.points.add(1)\n")
                    file.write(f"spline.points[0].co = ({x1}, {y1}, {z1}, 1)\n")
                    file.write(f"spline.points[1].co = ({x2}, {y2}, {z2}, 1)\n")
                    file.write(f"curve_obj = bpy.data.objects.new(name='{parent}_to_{child}', object_data=curve)\n")  # Fixed f-string
                    file.write("bpy.context.scene.collection.objects.link(curve_obj)\n\n")

            
            print(f"Blender script for blue skeleton written to {output_path}")

    def export_pink_skeleton(self, output_path):
        """
        Exports the pink skeleton (rotation-only, 3D) as a Blender-compatible Python script.
        """
        rotated_positions = self.create_skeleton_with_rotations()

        with open(output_path, 'w') as file:
            file.write("import bpy\n\n")
            file.write("# Create spheres and lines for pink skeleton in Blender\n")
            
            # Add spheres for rotated positions
            for joint, coords in rotated_positions.items():
                x, y, z = coords
                # z = 0  # Assuming flat Z for now; adjust if needed for 3D
                x = x / 10  # Adjust scaling factor as needed
                y = y / 10
                z = z / 10
                
                file.write(f"# Sphere for {joint}\n")
                file.write("bpy.ops.mesh.primitive_uv_sphere_add(\n")
                file.write(f"    radius=0.15,  # Adjust size of spheres\n")
                file.write(f"    location=({x}, {y}, {z})\n")
                file.write(")\n")
                file.write(f"bpy.context.object.name = '{joint}'\n\n")
            
            # Add lines for connections
            for parent, children in self.bone_hierarchy.items():
                if parent in rotated_positions:
                    parent_x, parent_y, parent_z = rotated_positions[parent]
                    parent_x /= 10
                    parent_y /= 10
                    parent_z /= 10
                    # parent_z = 0 / 10  # Adjust Z if needed
                    
                    for child in children:
                        if child in rotated_positions:
                            child_x, child_y, child_z = rotated_positions[child]
                            child_x /= 10
                            child_y /= 10
                            child_z /= 10
                            # child_z = 0 / 10  # Adjust Z if needed
                            
                            file.write(f"# Line connecting {parent} to {child}\n")
                            file.write("curve = bpy.data.curves.new(type='CURVE', name='Line')\n")
                            file.write("curve.dimensions = '3D'\n")
                            file.write("spline = curve.splines.new(type='POLY')\n")
                            file.write("spline.points.add(1)\n")
                            file.write(f"spline.points[0].co = ({parent_x}, {parent_y}, {parent_z}, 1)\n")
                            file.write(f"spline.points[1].co = ({child_x}, {child_y}, {child_z}, 1)\n")
                            file.write(f"curve_obj = bpy.data.objects.new(name='{parent}_to_{child}', object_data=curve)\n")
                            file.write("bpy.context.scene.collection.objects.link(curve_obj)\n\n")

            print(f"Blender script for pink skeleton written to {output_path}")


if __name__ == "__main__":
    hi = Skeleton()
    hi.process_frame()
    # hi.export_blue_skeleton('blue_skeleton.py')