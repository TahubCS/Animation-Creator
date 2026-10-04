# Milestone 1A decisions — 2026-10-04

- Read the original workflow first; created root `AGENTS.md` from its
  continuing-agent instructions while preserving the supplied global agreement.
- Use existing local Blender 5.2.2 LTS, build `d13f752e3b9c`. No Blender install,
  alternative engine, account, or cloud rendering service was needed.
- Use Cycles/OptiX on the detected RTX 3060 Laptop GPU. Actual dry-scene draft
  renders establish this path works; this is not a general production benchmark.
- Use twelve tubes, twin rims, a rotating shaft in stationary bored bearing
  blocks, and two A-frames. Prescribed rigid motion; no rigid-body solver.
- Six seconds at 24 fps, one revolution, no duplicate endpoint, locked vertical
  camera. Timing is illustrative, not measured historical operating speed.
- Fixed 25° outward tilt from the counterclockwise tangent. Validate water
  collection, retention, and top discharge only in a separately approved 1B.
- Draft review identified a saddle entering a tube cavity. Shortened the saddle
  and certified all mounts remain outside the cavity. The retained `draft.mp4`
  precedes this correction; the editable scene and final preview use the repair.
- Use lossless PNG frame masters plus H.264 MP4 via Blender's bundled FFmpeg.
  No standalone FFmpeg was found on PATH; no package installation was required.
- The decoder initially cropped thumbnail frames because `ORIGINAL` preserves
  native movie size. Changed its insertion fit to `FIT` and regenerated the
  inspection images. The encoded video itself was not cropped by this issue.
- No browser/native UI surfaces are connected. Check all encoded frames using
  the decoder and inspect representative frames and sequential contact sheets.
  GUI playback remains explicitly unverified.
- Stop at 1A review. No water, trough, narration, music, public upload, or 1B work.
- Final result: all 144 Cycles frames rendered (last-frame log time 29:04.968),
  1080 × 1920 six-second H.264 preview encoded with zero audio tracks, all
  144 frames decoded, nine master/decoded comparisons passed, and full-cycle
  frame sheets inspected. Geometry and media checks are saved. GUI playback
  remains unverified. Milestone 1A is ready for review; work stopped.
- User review then found floor-joint flicker missed by full-view frame sheets.
  Confirmed it in PNG masters; unioned each pair of legs with its sill using
  Exact solid unions before beveling. Re-rendered all 144 frames (29:36.360).
  Added manifold/connected-mesh checks and native master/encoded joint tests.
- The earlier HIGH encoding preset narrowly failed the new right-joint
  stability threshold. Switched to custom H.264 CRF 12, retaining the threshold;
  all four master/encoded joint checks passed, and both encoded close-up
  sequences were inspected. Saved `preview_joint_fix.mp4` and kept the original
  as `preview_before_joint_fix.mp4`; `preview.mp4` now matches the repaired video.
- Added and exercised an incomplete-render guard to prevent mixing old and
  corrected PNGs. All actual results and remaining GUI-playback limitation are
  recorded. Work stopped at repaired Milestone 1A review.
- Initialized a local Git repository on `main` at the user's request. Commit
  workflow documentation, production source, verification records, and reviewed
  outputs separately. Keep regenerable frame sequences, decoder crops, Python
  caches, and automatic Blender backups local and ignored; retain named scene
  archives and before/after review evidence. No remote is configured.
