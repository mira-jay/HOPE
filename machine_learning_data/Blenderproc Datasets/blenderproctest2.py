import blenderproc as bproc
import numpy as np
import os
import imageio

# Initialize BlenderProc
bproc.init()

# Create a cube primitive
cube = bproc.object.create_primitive('CUBE', scale=[1, 1, 1])
cube.set_location([0, 0, 0])


# Random camera position


cam_pose = bproc.math.build_transformation_mat(
   [5, -2, 3], [0, 0, 0]
   # [np.random.uniform(-3, 3), np.random.uniform(-3, 3), np.random.uniform(1, 3)],
   # [np.random.uniform(0, np.pi/4), 0, 0]
)
bproc.camera.add_camera_pose(cam_pose)

# Add point light
light = bproc.types.Light()
light.set_type("POINT")
#light.set_location([2, -2, 3])
light.set_location([5, 5, 5])
light.set_energy(2000)

# Create a plane to catch shadows
plane = bproc.object.create_primitive('PLANE', scale=[5, 5, 1])
plane.set_location([0, 0, -1])


# Enable depth rendering
bproc.renderer.enable_depth_output(activate_antialiasing=False)

# Render image
data = bproc.renderer.render()
rgb = data["colors"][0]   # first frame
depth = data["depth"][0]  # first frame
print("Render keys: ", data.keys())

# Output folder (define before using)
output_folder = "/Users/Mira/Projects/Git Repository/HOPE/output"
os.makedirs(output_folder, exist_ok=True)


# Save PNG

bproc.writer.write_hdf5(output_folder, data)


imageio.imwrite(os.path.join(output_folder, "rgb.png"), rgb)
# Normalize depth for PNG
depth_normalized = (depth - depth.min()) / (depth.max() - depth.min())  # scale to 0..1
depth_uint8 = (depth_normalized * 255).astype(np.uint8)

imageio.imwrite(os.path.join(output_folder, "depth.png"), depth_uint8)

print(f"Render complete! PNG saved in {output_folder}")