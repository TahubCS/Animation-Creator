# Milestone 1A verification

Checkpoint: user-reported foot-joint flicker repaired, full preview re-rendered,
and native master/encoded joint checks passed. Ready for review; work stopped at 1A.
Date: 2026-10-04. Approval to begin Milestone 1B has not been requested or given.

## Actual environment

- Local Windows 11, build 26200; 16 logical processors reported by .NET.
- Existing Blender executable:
  `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
- Blender 5.2.2 LTS, build hash `d13f752e3b9c`, built 2026-09-15.
- Blender Python 3.13.13; system Python 3.13.7; existing Pillow 11.3.0.
- NVIDIA RTX 3060 Laptop GPU, 6144 MiB VRAM, driver 595.71, confirmed through
  `nvidia-smi`. Cycles enumerated CUDA and OptiX devices and an AMD Ryzen 9 6900HS
  CPU. Actual OptiX draft and full-resolution frames rendered successfully.
- Blender was absent from PATH but found in Program Files. Standalone FFmpeg
  and ffprobe were absent from PATH. Encoding/decoding uses Blender's bundled
  FFmpeg; no software or Python package installation was needed.
- WMI hardware queries were denied by the execution sandbox. OS, GPU, and CPU
  information above came from successful alternative probes; system RAM was
  not independently measured.

## Scene and motion checks — passed

`verify_scene.py` checks the saved `.blend`, not just the scene-generation code.
See `scene_checks.json` and `logs/scene_checks.log` for actual measurements.

- 289 poses, frames 1–145 at half-frame increments. Includes every delivered
  frame and the virtual loop endpoint. One linear rotation curve, constant
  2.5° per delivered frame, right side rising viewed from negative Y.
- Fixed camera, supports, and axle center: no measured transform drift.
- All tubes rigidly parented; no independent pivots or constraints. Maximum
  relative-matrix error: 8.35e-7; maximum angle error: 5.42e-7 radians.
- Tube centers remain at radius 1.79 m, axial position Y = -0.36 m; their open
  axes retain the specified tangent-plus-25°-outward orientation.
- Conservative continuous full-cycle swept-envelope bounds, including evaluated
  bevel geometry: moving rim/tube assembly clears every support/base by at least
  0.15825 m; clears the ground by 0.29825 m.
- Separate shaft checks certify 0.01497 m radial clearance in bearing bores
  and separation from timber supports. Bearing contact, friction, structural
  strength, and load balance were not simulated.
- Adjacent tube body bounding spheres have a 0.17931 m gap.
- All saddles remain outside the tube cavities, with at least 0.01816 m
  clearance from a conservative cavity exclusion plane.
- Actual evaluated vertices stay inside the locked camera frame throughout
  the sampled cycle: X from 0.0460 to 0.9159; Y from 0.1979 to 0.7481 in
  normalized image coordinates. The continuous clearance proof does not depend
  on the pose sampling.
- Loop endpoint returns to the initial tube transform; output omits frame 145
  to avoid a duplicate endpoint.

The geometry checks initially failed because the verifier tried to evaluate the
non-geometric rotor empty as a mesh. The verifier was corrected to skip empties.
A later mounting diagnostic found one saddle entering the tube cavity; the
build script was corrected and the saved scene regenerated. Final geometric
checks include the regression assertion for every saddle.

## User review correction: flickering floor joints

The user identified alternating black patches where both front A-frame legs
meet the floor sill. The earlier full-view contact-sheet inspection missed
this localized temporal defect; its result did not establish joint stability.

Reproduced the issue in original lossless master frames, before encoding:
frames 1–2 show a black joint patch, frame 3 loses it, and subsequent frames
alternate. Preserved all 144 close-up crops in `renders/joint_review/before/`,
the previous video in `renders/preview_before_joint_fix.mp4`, and previous source
and scene as `build_scene_before_joint_fix.py` and `scene_before_joint_fix.blend`.

Diagnosis: each leg and its sill had overlapping exterior faces at the same
front/rear Y planes (front A-frame approximately Y = -0.97 and -0.83 m).
These coincident faces allowed ambiguous surface hits to change as the scene
was rebuilt during wheel rotation. This is a geometry defect, not an intended
joint opening. Static object transforms and successful wheel-clearance checks
do not detect it.

Repair: `join_frame_feet()` uses the Exact Boolean union to combine each pair
of leg solids with its sill before applying the bevel. This removes coincident
and interior intersection faces rather than hiding them with higher samples or
video processing. Timber proportions, wheel, camera, timing, and render quality
settings are retained. The assembled A-frame remains editable as a mesh, and
its individual timber dimensions remain parameterized in source. This is a
visual geometry representation, not evidence of a specific historical joint.

Targeted validation completed:

- Rendered native-resolution joint-region frames 1–6, 37, 73, 109, and 144 using
  `render_joint_test.py`. Inspected consecutive close-ups; black dropouts were
  absent in these repaired renders.
- Saved-scene checks passed again across 289 poses. Added regression checks:
  both jointed A-frames are manifold, have one connected component, no zero-area
  faces, and positive solid volume (0.15702 m³ each).
- Minimum wheel/support and shaft/bore clearances remain 0.15825 m and 0.01497 m.
- Before-fix close-up metrics: maximum adjacent-frame mean RGB change 5.32
  (left), 5.49 (right); maximum full-cycle channel swing 105 and 107 on a
  0–255 scale. Metrics cover the specified joint regions, not the whole frame.

Revised rendering and verification completed:

- All 144 full-resolution PNGs re-rendered at the same Cycles/OptiX settings;
  last-frame log time 29:36.360 (`logs/joint_fix_final_render.log`).
- The first corrected encode using the earlier HIGH quality preset narrowly
  failed the strict adjacent-frame joint limit on the right (2.059 versus 2.0).
  Geometry masters passed. Increased H.264 encoding quality to custom CRF 12,
  re-encoded, and repeated decode and raster checks without changing the limits.
- `preview_joint_fix.mp4`: H.264, 1080 × 1920, 24 fps, exactly six seconds,
  144 frames, zero audio tracks, 11,664,887 bytes. `preview.mp4` is an identical
  current copy. The original flawed video remains `preview_before_joint_fix.mp4`.
- All 144 encoded frames decoded at both thumbnail and native resolution;
  native frames are in `renders/joint_review/encoded_full/`.
- `review_joints.py --after` passed for both joints in every master and every
  native decoded frame. Original measurements fail the new temporal limits,
  confirming the limits detect the original observed defect.
- Inspected both encoded joint sheets across all 144 frames and the consecutive
  close-ups. Black dropouts are absent. The full-cycle key-frame sheet remains
  correctly framed with rigid wheel/container motion.
- Maximum adjacent-frame mean RGB change: master left 0.585, right 0.756;
  encoded left 1.079, right 1.448. Maximum full-cycle channel swing: master
  26/30, encoded 28/31, versus original 105/107. Values are on a 0–255 scale.
  Small sampling, moving-shadow, and lossy-encoding changes remain; the test
  rejects abrupt changes above the specified thresholds, not all pixel variation.
- Nine source/decoded comparisons passed: PSNR 42.14–43.39 dB, mean absolute
  RGB error 0.821–0.971. No unexpected crop or color-transform change found.
- Added and tested an encoder guard: it refuses a directory containing any
  final PNG older than the saved scene. During the partial re-render this
  correctly failed before writing a corrected MP4 (`logs/incomplete_render_guard.log`).
- Updated source/scene, reproduction wrapper, preview interface, workflow, and
  continuing-agent notes. Python compilation and PowerShell parsing passed;
  relevant production/check scripts executed successfully. The entire wrapper
  was not rerun as a single invocation. GUI player playback remains unobserved.

Saved new joint evidence: `joint_raster_after.json`, the master/encoded crops
and sheets in `renders/joint_review/after/`, and `renders/joint_review/before_after.png`.
The next section records the first revision's render history. Its old sizes and
comparisons are superseded by the corrected results above.

## Draft inspection — executed

- Rendered eight 540 × 960 review frames (32 samples) and a complete
  540 × 960 draft sequence (16 samples). The retained `draft.mp4` was rendered
  before the saddle correction; the eight draft stills were regenerated after
  correction. The final source/scene use the corrected mounting.
- Draft MP4 metadata verified: H.264, 540 × 960, 24 fps, 144 frames, exactly
  6.0 seconds, one video track, zero audio tracks. All 144 frames decoded.
- Inspected the draft key-frame sheet, sequential frame sheets, and corrected
  stills. Bindings move with tubes, the inspection marker traverses the cycle,
  the openings and closed bases are readable, and the camera/supports stay fixed.
- The thumbnail decoder originally used native-size insertion, which cropped
  the review thumbnails. Switched to FIT, re-decoded, and re-inspected. This was
  an inspection-pipeline issue, not a crop in the encoded video.
- A supplementary raster detector found the teal inspection binding in all
  144 draft frames. Its centroid can shift when the front support occludes part
  of a binding; this detector is not a mechanical-clearance test.

## First revision rendering (superseded)

Cycles, GPU OptiX, 1080 × 1920, 24 fps, frames 1–144, 96 maximum samples,
denoising enabled, six bounces, AgX Medium High Contrast, fixed seed 13,
motion blur disabled for readable mechanical review. Original PNGs are retained.

All 144 final PNGs rendered successfully. Blender's log records 29:04.968 at
the last frame (about 29 minutes for this render on this laptop). The PNG masters
total 295,483,123 bytes. This is an observed dry-scene render, not a benchmark
for future water effects or episodes.

Final MP4 checks passed (`media_checks.json`, `logs/media_checks.log`):
H.264, 1080 × 1920, 24 fps, 144 frames, exactly 6.0 seconds, one video track,
zero audio tracks, 3,253,915 bytes. Blender's movie reader decoded every frame
and exported nine full-resolution key frames plus all 144 review thumbnails.

Inspected the final eight-pose key-frame sheet, all four sequential sheets
(frames 1–36, 37–72, 73–108, 109–144), and the full-resolution closing frame.
Also inspected full-resolution master frames 1, 37, 55, 73, and 109 during the
render. The wheel stays framed, the A-frames remain fixed, tubes and bindings
turn together, and consecutive poses progress continuously through the cycle.
The bottom tube is partly occluded by the front support, as documented below.
The closing frame is one regular 2.5° step before the loop start.

`make_review.py` passed. It detected visible teal binding pixels in all 144
decoded frames. Nine source-versus-decoded comparisons passed: PSNR 39.56–41.58
dB and mean absolute RGB error 1.04–1.25 on a 0–255 scale. This checks for
unexpected framing or color-transform changes while allowing lossy H.264
compression. It does not establish real-time GUI playback or eliminate every
possible display artifact. See `raster_checks.json` for all measurements.

Python source compilation and PowerShell wrapper parsing passed. All six
production/check scripts executed successfully in their relevant stages.
No broad repository test suite exists; no unrelated checks were added.

## Saved deliverables

| File | Actual result |
| --- | --- |
| `build_scene.py` | Parameterized, asset-free scene generation; corrected mounts |
| `scene.blend` | Editable scene, geometry, materials, camera, and linear rotation action |
| `renders/preview.mp4` | Final six-second silent vertical preview |
| `renders/preview_joint_fix.mp4` | Current repaired preview, custom H.264 CRF 12 |
| `renders/frames/frame_0001.png` through `frame_0144.png` | Full-resolution lossless masters |
| `renders/review/key_frames.jpg` | Eight representative decoded poses |
| `renders/review/decoded_*.png` | Nine full-resolution decoded frames, including closing frame |
| `renders/review/motion_sheet_1.jpg` through `motion_sheet_4.jpg` | All 144 encoded frames in sequence |
| `settings.json`, `scene_checks.json`, `media_checks.json`, `raster_checks.json` | Actual settings and measured checks |
| `run.ps1`, `render_saved.py`, `encode_preview.py`, `verify_scene.py`, `verify_preview.py`, `make_review.py` | Reproduction and validation source |
| `review.html` | Local video/frame review interface; browser interaction unverified |
| `review_joints.py`, `joint_raster_after.json`, `renders/joint_review/` | Targeted temporal regression and before/after joint evidence |

`renders/draft.mp4` and draft sequences are retained as superseded draft evidence.
The `.blend1` and named `scene_before_joint_fix.blend` backups are superseded;
use `scene.blend` for the current repaired scene.

## Reproduction

From this episode directory:

```powershell
# Generate source-defined scene, drafts, checks, and final preview:
.\run.ps1 -Mode All
# Only re-render/encode/check an existing saved scene:
.\run.ps1 -Mode Final
# Only re-check an existing scene and final preview:
.\run.ps1 -Mode Verify
```

The wrapper invokes Blender in background mode with `--python-exit-code 1`,
captures logs, and checks the actual process exit code. Do not change Windows
execution policy if script execution is blocked; the direct commands work too:

```powershell
$blenderExe = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
& $blenderExe --background --factory-startup --python-exit-code 1 --python .\build_scene.py -- --draft
& $blenderExe --background .\scene.blend --python-exit-code 1 --python .\verify_scene.py
& $blenderExe --background .\scene.blend --python-exit-code 1 --python .\render_saved.py
& $blenderExe --background --factory-startup --python-exit-code 1 --python .\encode_preview.py
& $blenderExe --background --factory-startup --python-exit-code 1 --python .\verify_preview.py
python .\make_review.py
python .\review_joints.py --after
```

The individual scene-generation, draft/final rendering, draft/final encoding,
full decoding, geometry verification, and review-generation commands executed
successfully. The complete `-Mode All` wrapper
has not been rerun as a single invocation. Contact-sheet generation additionally
uses the existing system Python/Pillow and Windows Arial font; Blender scene
generation, rendering, encoding, and metadata/decode checks use no pip packages.

## Limits and unresolved issues

- This is a prescribed dry geometry test, not a physics/fluid simulation.
  River drive, paddles, collection, retention, and discharge are deferred to 1B.
  The mounting angle is specified but its water-handling behavior is unverified.
- The reference supports the general noria mechanism, not these exact supports,
  dimensions, joinery, colors, speed, date, dynasty, or inventor. No such historical
  claim is made. Teal bindings are a review marker.
- The front A-frame occludes part of the bottom tube in this physically intact
  three-quarter camera view. Other positions show the openings clearly.
- No enabled browser/native UI surfaces were returned by Computer Use, so GUI
  player playback was not observed. Decoder success and frame inspection are
  recorded separately; `review.html` provides local video and frame controls,
  whose browser interaction remains unverified.
- Sandbox write restrictions caused a Blender thumbnail-write warning and an
  OptiX-cache warning. Rendering proceeded, the GPU cache fell back to this
  workspace, and no system permissions were changed. HIP initialization warns
  because its optional library is absent; selected NVIDIA OptiX renders work.
- 5.2 emitted deprecation warnings for node settings and strip duration APIs
  expected to change in 6.0. The project is pinned to the tested 5.2.2 release.
- Approval and visual feedback on this milestone are the next action. Stop here;
  do not implement Milestone 1B until the user asks to continue.
