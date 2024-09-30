import bpy

# Set rendering parameters (update for new engine)
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Remove all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a cube
bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
cube = bpy.context.object

# Create a camera if none exists
if 'Camera' not in bpy.data.objects:
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, -10, 5), rotation=(1.1, 0, 0))
    camera = bpy.context.object
    bpy.context.scene.camera = camera  # Set it as the active camera

# Set keyframe at frame 1
bpy.context.scene.frame_set(1)  # Go to frame 1
cube.location = (0, 0, 0)       # Set cube location
cube.keyframe_insert(data_path="location", index=-1)  # Insert keyframe

# Set keyframe at frame 50
bpy.context.scene.frame_set(50)  # Go to frame 50
cube.location = (5, 5, 5)        # Change cube location
cube.keyframe_insert(data_path="location", index=-1)  # Insert keyframe

# Set end frame for animation
bpy.context.scene.frame_end = 50

# Export the scene to GLTF
output_path = 'blender/blender_output/animation.gltf'  # Set your export path
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLTF_SEPARATE')

print("Exported animation to GLTF format")
