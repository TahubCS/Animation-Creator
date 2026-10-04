"""Contact sheets and raster motion check. Uses already installed Pillow only."""
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

root = Path(__file__).resolve().parent
draft = '--draft' in sys.argv
folder = root/'renders'/('draft_decoded' if draft else 'decoded')
files = sorted(folder.glob('frame_*.png'))
assert len(files) == 144
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 15)
out = root/'renders'/'review'
prefix = 'draft_' if draft else ''
positions = []
for frame, path in enumerate(files, 1):
    with Image.open(path) as img:
        assert img.size == (270, 480)
        # The teal binding is a deliberate inspection marker, not a historical claim.
        pixels = img.convert('RGB')
        points = [(x, y) for y in range(480) for x in range(270)
                  if (lambda c: c[1] > c[0]*1.28 and c[2] > c[0]*1.28
                      and c[1]-c[0] > 25 and c[2]-c[0] > 25)(pixels.getpixel((x,y)))]
        if len(points) >= 3:
            positions.append({'frame': frame,
                              'x': sum(x for x,y in points)/len(points),
                              'y': sum(y for x,y in points)/len(points),
                              'pixels': len(points)})
for page in range(4):
    sheet = Image.new('RGB', (6*180, 6*342), '#eff1f2')
    draw = ImageDraw.Draw(sheet)
    for index in range(36):
        frame = page*36+index+1
        with Image.open(files[frame-1]) as img:
            img = img.resize((180,320), Image.Resampling.LANCZOS)
            x, y = (index%6)*180, (index//6)*342
            sheet.paste(img, (x,y))
            draw.text((x+5,y+322), f'{frame:03d}  {(frame-1)/24:.3f}s', fill='#27303b', font=font)
    sheet.save(out/f'{prefix}motion_sheet_{page+1}.jpg', quality=94)
selected = (1, 19, 37, 55, 73, 91, 109, 127)
sheet = Image.new('RGB', (4*270, 2*508), '#eff1f2')
draw = ImageDraw.Draw(sheet)
for index, frame in enumerate(selected):
    with Image.open(files[frame-1]) as img:
        x, y = (index%4)*270, (index//4)*508
        sheet.paste(img, (x,y))
        draw.text((x+8,y+483), f'Frame {frame:03d}  {(frame-1)/24:.2f}s', fill='#27303b', font=font)
sheet.save(out/f'{prefix}key_frames.jpg', quality=96)
assert len(positions) > 100, 'Marker detection insufficient for raster motion check'
# Front support occludes the marker near the bottom. Report gaps rather than inventing positions.
consecutive = [(a,b) for a,b in zip(positions, positions[1:]) if b['frame'] == a['frame']+1]
steps = [math.hypot(b['x']-a['x'],b['y']-a['y']) for a,b in consecutive]
result = {'tracked_visible_frames': len(positions), 'total_frames': 144,
          'maximum_visible_centroid_step_pixels_at_270x480': max(steps),
          'marker_occlusion': 'front A-frame near bottom; visibility check is supplementary',
          'positions': positions}
if not draft:
    comparisons = []
    for frame in selected + (144,):
        with Image.open(root/'renders'/'frames'/f'frame_{frame:04d}.png') as source:
            with Image.open(out/f'decoded_{frame:04d}.png') as decoded:
                assert source.size == decoded.size == (1080,1920)
                stats = ImageStat.Stat(ImageChops.difference(source.convert('RGB'), decoded.convert('RGB')))
                rms = math.sqrt(sum(v*v for v in stats.rms)/3)
                psnr = 20*math.log10(255/rms) if rms else 100
                assert psnr > 30, f'Encoded frame differs unexpectedly: {frame} ({psnr} dB)'
                comparisons.append({'frame': frame, 'mean_absolute_rgb_error': sum(stats.mean)/3,
                                    'psnr_db': psnr})
    result['source_vs_decoded_key_frames'] = comparisons
(root/('draft_raster_checks.json' if draft else 'raster_checks.json')).write_text(
    json.dumps(result,indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'positions'}))
