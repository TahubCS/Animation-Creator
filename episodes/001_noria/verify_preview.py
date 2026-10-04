"""Inspect MP4 metadata and decode every frame with Blender's movie reader.

Use -- --draft for draft video. Uses the bundled decoder, no external packages.
"""
import json
import struct
import sys
import shutil
from pathlib import Path
import bpy

root = Path(__file__).resolve().parent
draft = '--draft' in sys.argv
path = root/'renders'/('draft.mp4' if draft else 'preview.mp4')
data = path.read_bytes()


def boxes(payload):
    offset = 0
    while offset+8 <= len(payload):
        length, name = struct.unpack_from('>I4s', payload, offset)
        header = 8
        if length == 1:
            length = struct.unpack_from('>Q', payload, offset+8)[0]
            header = 16
        elif length == 0:
            length = len(payload)-offset
        assert length >= header and offset+length <= len(payload), 'Malformed MP4 box'
        yield name.decode('ascii'), payload[offset+header:offset+length]
        offset += length


def child(payload, name):
    return next(value for key, value in boxes(payload) if key == name)


movie = child(data, 'moov')
tracks = []
for key, track in boxes(movie):
    if key != 'trak':
        continue
    mdia = child(track, 'mdia')
    kind = child(mdia, 'hdlr')[8:12].decode('ascii')
    mdhd = child(mdia, 'mdhd')
    if mdhd[0] == 0:
        timescale, ticks = struct.unpack_from('>II', mdhd, 12)
    else:
        timescale = struct.unpack_from('>I', mdhd, 20)[0]
        ticks = struct.unpack_from('>Q', mdhd, 24)[0]
    info = {'type': kind, 'duration_seconds': ticks/timescale}
    if kind == 'vide':
        stbl = child(child(mdia, 'minf'), 'stbl')
        stts = child(stbl, 'stts')
        count = struct.unpack_from('>I', stts, 4)[0]
        samples = [struct.unpack_from('>II', stts, 8+i*8) for i in range(count)]
        assert all(timescale/delta == 24 for number, delta in samples)
        tkhd = child(track, 'tkhd')
        width, height = struct.unpack_from('>II', tkhd, len(tkhd)-8)
        info.update({'codec': child(stbl, 'stsd')[12:16].decode('ascii'),
                     'width': width >> 16, 'height': height >> 16,
                     'frame_count': sum(number for number, delta in samples),
                     'fps': 24})
    tracks.append(info)
assert len(tracks) == 1 and tracks[0]['type'] == 'vide', 'Unexpected track/audio'
expected_size = (540, 960) if draft else (1080, 1920)
video = tracks[0]
assert (video['width'], video['height']) == expected_size
assert video['duration_seconds'] == 6 and video['frame_count'] == 144
assert video['codec'] == 'avc1', 'Expected H.264'

scene = bpy.context.scene
scene.frame_start, scene.frame_end = 1, 144
scene.render.fps = 24
scene.render.resolution_x, scene.render.resolution_y = 270, 480
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
strip = scene.sequence_editor_create().strips.new_movie('Actual encoded preview', str(path), 1, 1,
                                                        fit_method='FIT')
assert strip.frame_duration == 144, 'Decoder frame count mismatch'
assert (strip.elements[0].orig_width, strip.elements[0].orig_height) == expected_size
scene.render.use_sequencer = True
folder = root/'renders'/('draft_decoded' if draft else 'decoded')
folder.mkdir(exist_ok=True)
scene.render.filepath = str(folder/'frame_')
bpy.ops.render.render(animation=True)
files = sorted(folder.glob('frame_*.png'))
assert len(files) == 144
if not draft:
    scene.render.resolution_x, scene.render.resolution_y = expected_size
    # FIT writes scale factors at insertion time; restore native size for key frames.
    strip.transform.scale_x = strip.transform.scale_y = 1
    # A small localized temporal defect was missed in full-view thumbnails.
    # Keep native decoded frames for joint-region checks throughout the cycle.
    native_folder = root/'renders'/'joint_review'/'encoded_full'
    native_folder.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(native_folder/'frame_')
    bpy.ops.render.render(animation=True)
    assert len(list(native_folder.glob('frame_*.png'))) == 144
    for frame in (1, 19, 37, 55, 73, 91, 109, 127, 144):
        shutil.copy2(native_folder/f'frame_{frame:04d}.png',
                     root/'renders'/'review'/f'decoded_{frame:04d}.png')
result = {'passed': True, 'file': path.name, 'bytes': path.stat().st_size,
          'tracks': tracks, 'audio_tracks': 0, 'decoded_frames': len(files),
          'decoder': 'Blender bundled FFmpeg, VSE movie strip',
          'gui_playback': 'not verified; no enabled computer/browser surfaces'}
(root/('draft_media_checks.json' if draft else 'media_checks.json')).write_text(
    json.dumps(result, indent=2)+'\n', encoding='utf-8')
print('MEDIA_CHECKS_PASS', json.dumps(result))
