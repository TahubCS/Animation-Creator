"""Render the saved scene, either a low-resolution draft or final PNG sequence."""
import sys
from pathlib import Path
import bpy

root = Path(__file__).resolve().parent
scene = bpy.context.scene
draft = '--draft' in sys.argv
preferences = bpy.context.preferences.addons['cycles'].preferences
preferences.compute_device_type = 'OPTIX'
preferences.get_devices()
assert any(d.type == 'OPTIX' for d in preferences.devices), 'OptiX GPU unavailable'
for device in preferences.devices:
    device.use = device.type == 'OPTIX'
scene.cycles.device = 'GPU'
if draft:
    scene.render.resolution_percentage = 50
    scene.cycles.samples = 16
scene.render.filepath = str(root/'renders'/('draft_sequence' if draft else 'frames')/'frame_')
Path(scene.render.filepath).parent.mkdir(parents=True, exist_ok=True)
bpy.ops.render.render(animation=True)
