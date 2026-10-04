"""Targeted consecutive-frame inspection of the two reported stationary joints.

python review_joints.py --before     preserves old master/decoded crops
python review_joints.py --after      checks corrected raw and encoded frames
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageStat

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--before', action='store_true')
parser.add_argument('--after', action='store_true')
args = parser.parse_args()
stage = 'before' if args.before else 'after'
folder = root/'renders'/'joint_review'/stage
folder.mkdir(parents=True,exist_ok=True)
# Native 1080x1920 camera framing. Includes caps and the reported black patches.
regions = {'left': (270,1440,342,1500), 'right': (644,1475,716,1535)}
frames = [1,2,3,4,5,6,19,37,55,73,91,109,127,144]
statistics = {}
sources = {'master': root/'renders'/'frames'}
if args.after:
    sources['encoded'] = root/'renders'/'joint_review'/'encoded_full'
for source_name, source_folder in sources.items():
    for name, box in regions.items():
        crops = []
        for frame in range(1,145):
            with Image.open(source_folder/f'frame_{frame:04d}.png') as image:
                crop = image.convert('RGB').crop(box)
            crops.append(crop)
            crop.save(folder/f'{source_name}_{name}_{frame:04d}.png')
        consecutive = [sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)/3
                       for a,b in zip(crops,crops[1:])]
        envelope_min = crops[0]
        envelope_max = crops[0]
        for crop in crops[1:]:
            envelope_min = ImageChops.darker(envelope_min,crop)
            envelope_max = ImageChops.lighter(envelope_max,crop)
        spread = ImageStat.Stat(ImageChops.difference(envelope_max,envelope_min))
        statistics[f'{source_name}_{name}'] = {
            'maximum_consecutive_mean_rgb_change': max(consecutive),
            'mean_full_cycle_rgb_range': sum(spread.mean)/3,
            'maximum_channel_range': max(high for low,high in spread.extrema)}
        sheet = Image.new('RGB',(7*216,2*206),'#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for i,frame in enumerate(frames):
            x,y=(i%7)*216,(i//7)*206
            sheet.paste(crops[frame-1].resize((216,180),Image.Resampling.NEAREST),(x,y))
            draw.text((x+5,y+184),f'{stage} {source_name} {frame}',fill='black')
        sheet.save(folder/f'{source_name}_{name}_consecutive.png')
        all_frames = Image.new('RGB',(12*144,12*142),'#eeeeee')
        labels = ImageDraw.Draw(all_frames)
        for i,crop in enumerate(crops):
            x,y=(i%12)*144,(i//12)*142
            all_frames.paste(crop.resize((144,120),Image.Resampling.NEAREST),(x,y))
            labels.text((x+4,y+124),f'{source_name} {i+1:03d}',fill='black')
        all_frames.save(folder/f'{source_name}_{name}_all_frames.png')
(root/f'joint_raster_{stage}.json').write_text(json.dumps(statistics,indent=2)+'\n',encoding='utf-8')
print(json.dumps(statistics))
if args.after:
    for name, result in statistics.items():
        # The original black dropouts caused 105/107-level swings. Allow small
        # sampling, moving-shadow and compression variations but reject them.
        assert result['maximum_channel_range'] < 50, f'Joint dropout regression: {name}'
        assert result['maximum_consecutive_mean_rgb_change'] < 2, f'Joint flicker regression: {name}'
