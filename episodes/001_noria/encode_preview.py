"""Blender's bundled FFmpeg encodes PNGs; no standalone encoder dependency.

blender --background --factory-startup --python-exit-code 1 --python encode_preview.py
Append -- --draft for the half-resolution draft sequence.
"""
import sys
import shutil
from pathlib import Path
import bpy

root = Path(__file__).resolve().parent
draft = '--draft' in sys.argv
folder = root/'renders'/('draft_sequence' if draft else 'frames')
files = sorted(folder.glob('frame_*.png'))
assert len(files) == 144 and all(p.stem == f'frame_{i:04d}' for i, p in enumerate(files, 1))
if not draft:
    scene_saved_at = (root/'scene.blend').stat().st_mtime
    assert all(path.stat().st_mtime >= scene_saved_at for path in files), (
        'Final render incomplete: some PNGs predate the current saved scene')
scene = bpy.context.scene
scene.frame_start, scene.frame_end = 1, 144
scene.render.fps = 24
scene.render.resolution_x, scene.render.resolution_y = ((540, 960) if draft else (1080, 1920))
scene.render.resolution_percentage = 100
editor = scene.sequence_editor_create()
strip = editor.strips.new_image('Rendered motion test', str(files[0]), 1, 1)
for path in files[1:]:
    strip.elements.append(path.name)
strip.frame_final_duration = 144
scene.render.use_sequencer = True
# The input PNGs already contain the rendered AgX display transform.
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.render.image_settings.media_type = 'VIDEO'
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'CUSTOM'
scene.render.ffmpeg.custom_constant_rate_factor = 12
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.ffmpeg.audio_codec = 'NONE'
scene.render.filepath = str(root/'renders'/('draft.mp4' if draft else 'preview_joint_fix.mp4'))
scene.render.use_file_extension = True
bpy.ops.render.render(animation=True)
if not draft:
    # Keep the established project path current; distinct filename avoids
    # reopening a cached copy of the user-reported first preview.
    shutil.copy2(root/'renders'/'preview_joint_fix.mp4', root/'renders'/'preview.mp4')
