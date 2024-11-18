import math

# Function to generate circle coordinates
def generate_circle_coordinates(radius, num_points):
    coordinates = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        coordinates.append((x, y))
    return coordinates

# Write to body_coordinates.txt
with open('body_coordinates.txt', 'w') as file:
    
    radius = 1  # Radius of the circle
    num_points = 100  # Number of points to make the circle
    circle_coords = generate_circle_coordinates(radius, num_points)
    
    for i, (x, y) in enumerate(circle_coords):
        file.write('Frame: 0\n')
        file.write('11, 0.0, 0.0, 0.0, 0.0\n')
        file.write(f'13, {x}, {y}, 0.0, 0.0\n')