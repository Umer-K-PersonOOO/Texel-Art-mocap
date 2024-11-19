import bpy

# Create spheres and lines for pink skeleton in Blender
# Sphere for center_hip
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(0.0, 0.0, 0.0)
)
bpy.context.object.name = 'center_hip'

# Sphere for base_of_neck
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(0.6335783004760742, -2.7616443634033203, 9.59019775390625)
)
bpy.context.object.name = 'base_of_neck'

# Sphere for left_hip
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(9.94989471435547, 0.2928161144256592, -0.9559564590454102)
)
bpy.context.object.name = 'left_hip'

# Sphere for right_hip
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(-9.949893188476562, -0.29281580448150635, 0.9559555053710938)
)
bpy.context.object.name = 'right_hip'

# Sphere for center_of_head
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(-0.13897509574890138, -6.465533447265625, 18.846783447265626)
)
bpy.context.object.name = 'center_of_head'

# Sphere for left_shoulder
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(10.617740631103516, -2.2155385971069337, 9.455020904541016)
)
bpy.context.object.name = 'left_shoulder'

# Sphere for right_shoulder
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(-9.350582885742188, -3.307749938964844, 9.725374603271485)
)
bpy.context.object.name = 'right_shoulder'

# Sphere for left_elbow
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(10.827002716064452, -1.6541282653808593, -0.5270133972167969)
)
bpy.context.object.name = 'left_elbow'

# Sphere for left_wrist
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(9.430847930908204, -5.6832328796386715, -9.572291564941406)
)
bpy.context.object.name = 'left_wrist'

# Sphere for right_elbow
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(-10.556906127929688, -1.9870218276977538, -0.113348388671875)
)
bpy.context.object.name = 'right_elbow'

# Sphere for right_wrist
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(-11.83719253540039, -5.784690093994141, -9.27514877319336)
)
bpy.context.object.name = 'right_wrist'

# Sphere for left_knee
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15, location=(8.718451690673827, -0.8123620986938477, -10.818111419677734)
)
bpy.context.object.name = 'left_knee'

# Line connecting center_hip to base_of_neck
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (0.0, 0.0, 0.0, 1)
spline.points[1].co = (0.6335783004760742, -2.7616443634033203, 9.59019775390625, 1)
curve_obj = bpy.data.objects.new(name='center_hip_to_base_of_neck', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting center_hip to left_hip
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (0.0, 0.0, 0.0, 1)
spline.points[1].co = (9.94989471435547, 0.2928161144256592, -0.9559564590454102, 1)
curve_obj = bpy.data.objects.new(name='center_hip_to_left_hip', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting center_hip to right_hip
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (0.0, 0.0, 0.0, 1)
spline.points[1].co = (-9.949893188476562, -0.29281580448150635, 0.9559555053710938, 1)
curve_obj = bpy.data.objects.new(name='center_hip_to_right_hip', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting base_of_neck to center_of_head
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (0.6335783004760742, -2.7616443634033203, 9.59019775390625, 1)
spline.points[1].co = (-0.13897509574890138, -6.465533447265625, 18.846783447265626, 1)
curve_obj = bpy.data.objects.new(name='base_of_neck_to_center_of_head', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting base_of_neck to left_shoulder
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (0.6335783004760742, -2.7616443634033203, 9.59019775390625, 1)
spline.points[1].co = (10.617740631103516, -2.2155385971069337, 9.455020904541016, 1)
curve_obj = bpy.data.objects.new(name='base_of_neck_to_left_shoulder', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting base_of_neck to right_shoulder
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (0.6335783004760742, -2.7616443634033203, 9.59019775390625, 1)
spline.points[1].co = (-9.350582885742188, -3.307749938964844, 9.725374603271485, 1)
curve_obj = bpy.data.objects.new(name='base_of_neck_to_right_shoulder', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting left_shoulder to left_elbow
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (10.617740631103516, -2.2155385971069337, 9.455020904541016, 1)
spline.points[1].co = (10.827002716064452, -1.6541282653808593, -0.5270133972167969, 1)
curve_obj = bpy.data.objects.new(name='left_shoulder_to_left_elbow', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting left_elbow to left_wrist
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (10.827002716064452, -1.6541282653808593, -0.5270133972167969, 1)
spline.points[1].co = (9.430847930908204, -5.6832328796386715, -9.572291564941406, 1)
curve_obj = bpy.data.objects.new(name='left_elbow_to_left_wrist', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting right_shoulder to right_elbow
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (-9.350582885742188, -3.307749938964844, 9.725374603271485, 1)
spline.points[1].co = (-10.556906127929688, -1.9870218276977538, -0.113348388671875, 1)
curve_obj = bpy.data.objects.new(name='right_shoulder_to_right_elbow', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting right_elbow to right_wrist
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (-10.556906127929688, -1.9870218276977538, -0.113348388671875, 1)
spline.points[1].co = (-11.83719253540039, -5.784690093994141, -9.27514877319336, 1)
curve_obj = bpy.data.objects.new(name='right_elbow_to_right_wrist', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

# Line connecting left_hip to left_knee
curve = bpy.data.curves.new(type='CURVE', name='Line')
curve.dimensions = '3D'
spline = curve.splines.new(type='POLY')
spline.points.add(1)
spline.points[0].co = (9.94989471435547, 0.2928161144256592, -0.9559564590454102, 1)
spline.points[1].co = (8.718451690673827, -0.8123620986938477, -10.818111419677734, 1)
curve_obj = bpy.data.objects.new(name='left_hip_to_left_knee', object_data=curve)
bpy.context.scene.collection.objects.link(curve_obj)

