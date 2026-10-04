"""Native-resolution border renders of foot joints before spending a full render.

blender --background scene.blend --python-exit-code 1 --python render_joint_test.py
"""
from pathlib import Path
import bpy

root = Path(__file__).resolve().parent
scene = bpy.context.scene
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'
prefs.get_devices()
assert any(d.type == 'OPTIX' for d in prefs.devices)
for device in prefs.devices:
    device.use = device.type == 'OPTIX'
scene.cycles.device = 'GPU'
scene.render.use_border = True
scene.render.use_crop_to_border = True
# Bottom joints and their immediate surroundings, preserving native pixel scale.
scene.render.border_min_x = 0.23
scene.render.border_max_x = 0.70
scene.render.border_min_y = 0.19
scene.render.border_max_y = 0.29
folder = root/'renders'/'joint_review'/'corrected_test'
folder.mkdir(parents=True,exist_ok=True)
for frame in (1,2,3,4,5,6,37,73,109,144):
    scene.frame_set(frame)
    scene.render.filepath = str(folder/f'frame_{frame:04d}.png')
    bpy.ops.render.render(write_still=True)
