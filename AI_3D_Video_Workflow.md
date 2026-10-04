# AI 3D Video Workflow

Version: 0.3 — Milestone 1A floor-joint correction verified
Recorded: 2026-10-04 UTC / 2026-10-03 America/New_York
Status: Milestone 1A floor-joint flicker repaired; full preview re-rendered and native-resolution master/encoded joint checks passed. Ready for review; stopped before 1B. See episodes/001_noria/verification.md.

## Start here

This is the project record for this conversation and for any coding or content agent that continues the work. Read it before choosing tools or creating a shot. Update the current checkpoint and decision log after each completed milestone. Distinguish proposed work from implemented and verified work.

**Current task:** Review the corrected Milestone 1A preview at `episodes/001_noria/renders/preview_joint_fix.mp4`. Build and check one mechanism at a time. Water effects, narration, and a complete video remain deferred; do not begin 1B until the user asks to continue.

## 1. User goals and working agreement

- Build one channel around historical engineering and architecture in China and Japan: how structures and practical systems helped people defend themselves or make everyday life easier.
- Use AI to handle topic proposals, research assistance, scripts, 3D scene creation, animation, narration, editing, and eventually publishing preparation.
- The user does not want to learn manual 3D animation, write production code, or create every episode's ideas personally. Agents should do the production work and present concrete outputs for review.
- Work in small steps. Do not build a complete channel automation system before demonstrating the first animation.
- **Accuracy and the quality of the result take priority over speed and cost.** Earlier interest in free software remains useful, but must not justify an inaccurate result or an unsuitable model.
- Give critical feedback. Challenge unsupported assumptions and report failures plainly.
- Business context: the user can give the project six to seven months; $500/month would make it worth pursuing. Whether that means revenue or profit has not been clarified. No revenue forecast or guarantee has been established.
- User-reported computer: Windows 11 with an RTX 3060 Laptop GPU and 6 GB VRAM. This is remembered context, not a fresh hardware inspection.

## 2. Important correction about AI labels

AI-written animation code produces a rendered video. It changes the production technique; it does not automatically exempt that video from disclosure rules or make it eligible for monetization.

YouTube's current guidance distinguishes realistic synthetic content from non-realistic animation and production assistance. Its examples include non-realistic animation and assistance with ideas or scripts that do not require disclosure. It also says disclosure itself does not limit audience or monetization eligibility. Apply this to the finished content, including its audio; do not promise that a label will never appear. [S1]

YouTube separately evaluates originality and whether a channel's content is generic or repetitive. Consistent presentation can be compatible with monetization when episodes provide materially different substance and value. [S2]

For this project:

- Make an original educational animation with a clear explanation.
- Describe historical reconstructions as reconstructions when needed.
- Decide disclosure from the final video and the rules of the destination platform.
- Do not treat metadata removal or a different renderer as a way to avoid disclosure.
- Review TikTok, Facebook, Instagram, and Snapchat requirements separately when publishing becomes an active task. Their rules and account eligibility are not settled by YouTube's examples.

## 3. Selected approach and tool decisions

**Production approach:** AI writes code to construct explicit 3D objects and animate their movement. A renderer creates the frames. Each component's geometry and movement can be inspected and corrected.

This gives us control over geometry and timing. It does not automatically make the mechanism physically correct. The animation must still pass mechanical and historical checks.

**Working default: Blender with Python scripting.** Blender is a free, open-source suite covering modeling, animation, simulation, rendering, compositing, and editing. [S3] Use an official supported release, record its exact version, and verify scripting commands against that release before implementation. Milestone 1A is pinned to local Blender 5.2.2 LTS, build `d13f752e3b9c`, and Cycles/OptiX; its scripts and renders ran successfully.

Why this default: the intended deliverable is an offline 3D video with inspectable geometry, materials, camera, and animation. The pilot has now rendered on the user's laptop. Its measured dry-scene render time is recorded in the episode verification notes; this is not a benchmark for future effects or complete episodes.

- Keep Three.js as a recorded alternative for procedural 3D or browser previews.
- Keep Manim as an alternative for diagrams and explanatory overlays.
- Defer voice, editing automation, local language-model setup, and posting software until the mechanism test works.
- A coding model for this project has not been selected or benchmarked. Choose one on demonstrated ability to build, render, inspect, and correct the pilot, rather than on price alone.
- Avoid installing multiple competing pipelines in the first milestone.

## 4. First test: a bamboo water-lifting wheel

**Working subject:** A simplified noria, showing containers attached around a wheel.

**Why this subject:** It connects to the water-lifting reference already reviewed, has a visible repeated cycle, and can start with a small number of objects.

FAO describes a river-current-driven wheel with closed-ended bamboo tubes around its rim. The tubes collect water near the bottom and discharge into a trough near the top. It documents examples in several Asian countries, including a Chinese-type illustration. [S4]

This source supports the mechanism. It does not establish a particular dynasty, inventor, construction date, or the complete visual design of our eventual scene. Those claims require additional evidence before narration.

### Milestone 1A — geometry and rotation

Deliver a **5–8 second silent motion test** of the wheel, axle, supports, and a small set of containers.

Requirements:

- One stable camera, framed vertically for an eventual short video.
- Simple readable materials and lighting.
- Wheel rotation about a fixed axle.
- Containers firmly attached to the wheel with a documented orientation.
- No unexplained pivots that keep containers upright; any joint or mounting arrangement must be intentional.
- No intersection of the moving wheel with its supports.
- A stationary camera view that makes the components and motion easy to judge.
- No village, people, landscape, narration, music, or assembly sequence in this first test.

Target outputs when implemented: scene-building source, editable Blender scene, preview video, key review frames, and a brief verification record.

### Milestone 1B — collection and discharge

After the geometry and motion are checked, extend the test to roughly **10–15 seconds** and add a simplified river and trough.

Requirements:

- Select and document a container mounting angle that actually permits collection, retention during the rising part of the cycle, and discharge near the top.
- Make river direction, wheel direction, and the rising side consistent.
- Show collection only when the container opening reaches the water.
- Show discharge when the container orientation and trough position permit it.
- Water should enter the trough and travel downhill along it.
- Do not display water passing through closed geometry or appearing in containers without a visible collection step.
- Any simplified water representation must be identified in the production notes as illustrative, not a validated fluid simulation.
- Any sped-up cycle is illustrative timing, not a claim about measured historical operating speed.

The acceptance question is whether the depicted mechanism makes sense, not whether the water looks cinematic.

## 5. Workflow for each milestone

1. **Research and define.** Record the mechanism, supporting sources, unknowns, and the narrow claim the shot will demonstrate.
2. **Specify.** List objects, joints or attachments, dimensions or proportions, motion, camera, and success criteria.
3. **Build.** AI writes a readable, parameterized scene-generation script. Preserve editable geometry and intentional object names.
4. **Render a draft.** Produce useful review frames and a short preview before a high-quality final render.
5. **Inspect.** Check rendered output, attachment behaviour, collisions, flow direction, clarity, and consistency with the stated mechanism.
6. **Correct.** Repair the script and regenerate the scene. Do not rely on undocumented manual edits.
7. **Record.** Save the source, settings, preview, findings, and next step. Report what passed and what remains unresolved.

Suggested future folder layout, to be created when implementation starts:

```text
project/
  AGENTS.md
  docs/
    workflow.md
    decisions.md
    sources.md
  episodes/
    001_noria/
      brief.md
      build_scene.py
      scene.blend
      verification.md
      renders/
```

This is a proposed layout, not an existing repository. Start with these few files; add infrastructure only when a demonstrated need appears.

## 6. Accuracy and quality checks

### Mechanical

- Identify the driving energy source, moving components, and stationary components.
- Ensure supports, mounting arrangements, and degrees of freedom are credible.
- Verify positions through the full cycle, including collection and discharge transitions.
- Check geometry and motion mathematically where useful; inspect representative rendered frames as well.
- Do not call scripted motion a physics simulation unless a simulation was actually run and checked.

### Historical

- Keep a claim-to-source record with URL, relevant section, and access date.
- Distinguish historical evidence from visualization choices such as colour, dimensions, scenery, and camera angle.
- Resolve important claims with appropriate independent evidence. More sources do not compensate for a source that fails to support the actual claim.
- Do not turn the reference video's improvement sequence into an asserted historical invention timeline.
- Do not assign generic Asian imagery to a particular Chinese or Japanese period without support.

### Visual and technical

- Watch the short animation, not just one attractive frame.
- Preserve stable geometry, readable framing, and continuous motion.
- Check the output's dimensions, frame rate, duration, and playback.
- Record the exact renderer, software versions, important settings, and reproduction command when they exist.
- Save the rendered preview and supporting source; do not claim that generating code proves the video is finished.

## 7. Instructions for a continuing agent

- Read this document and the latest episode checkpoint before work.
- Take the next small task; do not rebuild the entire stack or reopen settled decisions without evidence.
- Prioritize accuracy and final output quality over speed and cost.
- Handle creative and implementation work. Do not shift animation or coding tasks to the user merely because a tool is available.
- State the actual execution environment. A cloud workspace is not the user's Windows laptop.
- Verify available software before assuming installation or GPU access. The earlier cloud workspace had Python, Node, and FFmpeg but no Blender on PATH. The subsequent local Windows check found Blender 5.2.2 LTS in Program Files and verified actual RTX 3060 Laptop GPU rendering. Recheck the active environment rather than treating either checkpoint as universal.
- Use current official documentation when a software detail or platform rule matters.
- Use simple readable scripts and avoid unnecessary services or agent frameworks.
- Present a small concrete result for feedback. Ask for user preferences only when they materially affect the next result.
- Update the record after a real change: decisions, source findings, commands, outputs, checks, unresolved issues, and the next action.
- Do not infer a passing check, completed animation, or successful upload from a plan or a repository README.
- No public posting or account connection is part of the current milestone. Address publishing when the user reaches that stage.

## 8. Reference video record

Reference: https://www.youtube.com/shorts/V0bqu2190tc

The provided recordings were reviewed earlier in this conversation. They depict an approximately two-minute explanation progressing from gravity irrigation and carrying water through intermediate lifting mechanisms to a river-driven waterwheel.

Useful storytelling pattern: problem → attempted solution → limitation → improved solution → visible payoff.

The visuals appeared consistent with controlled 3D animation. The exact production software, degree of AI involvement, originality, earnings, and reported 12-million view count were not established by the recordings. Earlier analysis inspected visual frames and on-screen text, not direct audio playback.

Use this as a storytelling reference. Create our own geometry, script, scene design, and narration.

## 9. Tool and model register

These are retained recommendations and alternatives from the discussion. Being listed does not mean a tool is selected, installed, benchmarked, or guaranteed to fit the project. External services and compute can cost money even when a repository is free. Recheck current licensing and relevant versions before adoption.

| Name | Repository / website | Role | Current decision |
| --- | --- | --- | --- |
| Blender | https://www.blender.org/ ; official mirror https://github.com/blender/blender ; canonical source https://projects.blender.org/blender/blender | Modeling, animation, rendering through AI-written scripts | Milestone 1A executed locally with Blender 5.2.2 LTS and Cycles/OptiX |
| Blender Python API | https://docs.blender.org/api/current/ | Scene generation and automation reference | Use documentation matching the selected release |
| Three.js | https://github.com/mrdoob/three.js ; https://threejs.org/ | Code-driven 3D, browser previews | Alternative; MIT software |
| Manim Community | https://github.com/ManimCommunity/manim ; https://www.manim.community/ | Programmatic explanatory diagrams and animation | Alternative or later overlays; MIT software |
| MoviePy | https://github.com/Zulko/moviepy ; https://zulko.github.io/moviepy/ | Assembly, captions, audio and video compositing | Later editing candidate; MIT software |
| FFmpeg | https://ffmpeg.org/ ; https://github.com/FFmpeg/FFmpeg | Encoding, frame extraction and media inspection | Supporting tool; license depends on build configuration |
| Kokoro | https://github.com/hexgrad/kokoro | Local narration generation | Later voice candidate; test pronunciation before selection |
| Kokoro-82M | https://huggingface.co/hexgrad/Kokoro-82M | TTS model weights | Apache-licensed candidate; voice model, not a research or coding model |
| Ollama | https://github.com/ollama/ollama ; https://ollama.com/ | Local model runtime | Optional later; MIT runtime does not determine each model's license |
| Qwen3-4B | https://huggingface.co/Qwen/Qwen3-4B | Local topic and script drafting | Apache-licensed model candidate; not benchmarked here for coding or source verification |
| MoneyPrinterTurbo | https://github.com/harry0703/MoneyPrinterTurbo | Automated script/media/voice/caption assembly | Retained alternative; does not supply our coordinated 3D scene by default |
| ComfyUI | https://github.com/Comfy-Org/ComfyUI ; https://docs.comfy.org/ | Workflow-based image/video generation | Deferred alternative for illustrative material |
| Wan2.2 | https://github.com/Wan-Video/Wan2.2 ; https://docs.comfy.org/tutorials/video/wan/wan2_2 | Generated video model family, including a 5B workflow | Deferred; open model weights do not make compute free; not benchmarked on 6 GB GPU |
| Postiz | https://github.com/gitroomhq/postiz-app ; https://docs.postiz.com/ ; https://postiz.com/ | Scheduling, publishing and analytics | Deferred; AGPL self-hosted software; hosted service and infrastructure may cost money |
| Upload-Post | https://upload-post.com/ ; https://docs.upload-post.com/ | Separate publishing service used by MoneyPrinterTurbo's documented integration | Deferred; external service, not part of MIT software license |
| Remotion | https://github.com/remotion-dev/remotion ; https://www.remotion.dev/ | Programmatic video composition alternative | Retained research alternative; custom licensing, not unrestricted open source; not selected |

Sources for retained capabilities and licenses:

- https://github.com/mrdoob/three.js
- https://github.com/ManimCommunity/manim
- https://github.com/Zulko/moviepy
- https://github.com/hexgrad/kokoro
- https://github.com/ollama/ollama
- https://huggingface.co/Qwen/Qwen3-4B
- https://github.com/harry0703/MoneyPrinterTurbo
- https://github.com/harry0703/MoneyPrinterTurbo/blob/main/config.example.toml
- https://github.com/Wan-Video/Wan2.2
- https://docs.comfy.org/tutorials/video/wan/wan2_2
- https://github.com/gitroomhq/postiz-app
- https://docs.postiz.com/general/platforms/overview
- https://github.com/remotion-dev/remotion/blob/main/LICENSE.md

Additional implementation notes retained from the discussion:

- MoneyPrinterTurbo can use external services even though its code is free. Its documented upload integration uses Upload-Post. Its bundled music should not be assumed cleared for our use; use separately cleared music or none.
- The documented ComfyUI Wan2.2 5B workflow targets fitting in 8 GB VRAM with offloading. A practical unattended configuration on the user's reported 6 GB GPU has not been demonstrated.
- Postiz lists YouTube, TikTok, Instagram, and Facebook Pages. Snapchat was absent from the list checked. Self-hosted provider apps can require setup and approval; this is not a universal zero-setup publishing solution.
- A small local model's availability does not demonstrate that it can independently research history, verify sources, or build accurate 3D mechanisms.

## 10. Source and policy register

Checked on 2026-10-04 UTC unless stated otherwise. URLs are provided so an agent can recheck changing rules. Brief descriptions below are working notes, not complete policy summaries.

- **[S1] YouTube AI disclosure:** https://support.google.com/youtube/answer/14328491 — retrieved; relevant sections cover realistic versus non-realistic content, assistance examples, labels, and monetization eligibility.
- **[S2] YouTube monetization quality:** https://support.google.com/youtube/answer/1311392 — retrieved; original content, materially varied substance, generic/repetitive content.
- **[S3] Blender official mirror:** https://github.com/blender/blender — retrieved; official project identity, supported production functions, and software licensing. Current scripting documentation could not be retrieved in this session; verify before executing implementation-specific commands.
- **[S4] FAO, Water lifting devices, section 4.9.4:** https://www.fao.org/4/ah810e/ah810e12.htm — retrieved; noria mechanism and Asian examples. Historical operating data describes particular examples and must not be generalized to our model.
- **[S5] FAO, Water lifting devices, earlier lifting mechanisms:** https://www.fao.org/4/ah810e/ah810e05.htm — reviewed earlier; retain for later research into windlass and continuous lifting systems.
- **YouTube API uploads:** https://developers.google.com/youtube/v3/docs/videos/insert — reviewed earlier; unverified API projects can have private-upload restrictions.
- **TikTok AI disclosure:** https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content — URL retained; page text was unavailable in this session. Do not claim a complete current policy review.
- **TikTok authenticity guidance:** https://www.tiktok.com/community-guidelines/en/integrity-authenticity — retrieval blocked in this session; recheck before publication.
- **Meta AI labeling:** https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/ — retrieved; updated article discusses labels and detection/disclosure. It does not prove that a code-rendered video will avoid a label.
- **YouTube Partner Program overview:** https://support.google.com/youtube/answer/72851 — retain for monetization planning; verify requirements at the time of planning rather than copying earlier thresholds.
- **YouTube previously discussed policy page:** https://support.google.com/youtube/answer/12843009 — retain for checking announced changes; do not rely on remembered dates or numbers without rereading.
- **YouTube Shorts format guidance:** https://support.google.com/youtube/answer/15424877 — retain for final delivery specifications.
- **TikTok Creator Rewards background:** https://newsroom.tiktok.com/introducing-the-new-creator-rewards-program?lang=en — previously discussed; current account and regional eligibility requires a fresh check.
- **Facebook monetization background:** https://about.fb.com/news/2026/03/creator-fast-track-grow-your-audience-earn-money-on-facebook/amp/ — previously discussed; recheck current program access later.
- **Snapchat monetization:** https://help.snapchat.com/ — retained entry point; a specific current policy URL has not been recorded here. Resolve it before making eligibility claims.

## 11. Current checkpoint and decision log

### Confirmed user decisions

- One channel, one coherent niche.
- AI performs creation; the user should not need to learn manual 3D animation.
- Proceed step by step and document the workflow.
- Accuracy and results outrank speed and cost.

### Working engineering decisions

- Start with explicit, code-generated 3D geometry and motion.
- Use Blender/Python as the working default, with Three.js retained as an alternative.
- Use a bamboo water-lifting wheel as the first test subject because it connects to the reviewed reference and a documented mechanism.
- Check wheel-and-container geometry first; add collection and discharge only after that passes.

### Earlier documentation checkpoint

- Created this reusable project record and tool register.
- Rechecked YouTube's disclosure and monetization-quality guidance.
- Located FAO's noria mechanism description.
- Checked the current cloud workspace for basic tools; Blender was not found on PATH.

### Earlier implementation status (superseded by the local checkpoint below)

- No Blender installation, scene code, rendered animation, narration, or public upload.
- No selected coding-model benchmark or GPU render benchmark.
- No exact historical period, dimensions, capacity, or measured operating speed for our future episode.

### Local Milestone 1A checkpoint — 2026-10-04

- Read this workflow before implementation and created root `AGENTS.md` from
  the continuing-agent instructions.
- Verified the actual Windows laptop environment. Blender was absent from PATH
  but found at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
  Exact release: Blender 5.2.2 LTS, build `d13f752e3b9c`. NVIDIA RTX 3060 Laptop
  GPU and 6144 MiB VRAM confirmed; actual Cycles/OptiX frames rendered.
- Created source, brief, editable scene, draft video, review frames, automated
  geometry checks, and reproduction commands in `episodes/001_noria/`.
- Geometry checks passed for 289 poses and conservative continuous swept
  clearances. Corrected a saddle entering a tube interior; regenerated the
  scene and verified all mounts clear the cavities.
- Draft video verified and fully decoded: six seconds, 24 fps, 144 frames,
  540 × 960, H.264, no audio. Inspected draft frame sequences and corrected stills.
- Final 1080 × 1920 preview rendered at 96 maximum Cycles samples. All 144 PNG
  frames saved; last-frame log time 29:04.968. Final H.264 MP4: six seconds,
  24 fps, 144 frames, zero audio tracks, 3,253,915 bytes. All frames decoded.
- Inspected representative full-resolution frames, all four final sequential
  frame sheets, and the closing frame. Nine PNG/decoded comparisons passed
  (PSNR 39.56–41.58 dB). Motion is continuous, attachments rigid, framing stable.
- No connected browser/native UI surfaces were available; GUI player playback
  remains unverified. Water-handling behavior, historical dimensions/period,
  driving forces, and structural strength are outside the completed checks.
- Actual commands, software details, errors/corrections, outputs, and limits:
  `episodes/001_noria/verification.md`. Decisions: `docs/decisions.md`.
  Claim/API sources: `docs/sources.md`.

### Next task

User review found flicker at both floor joints, missed by the prior full-view
inspection. Reproduced it in PNG masters, repaired coplanar overlapping
leg/sill faces with solid unions, and passed native-resolution close-up renders
and saved-scene checks. All 144 corrected frames re-rendered; repaired six-second
H.264 preview encoded at CRF 12 and fully decoded. Both joints passed temporal
checks in all native master/encoded frames and were inspected in close-up.
Current video is `preview_joint_fix.mp4` (also copied to `preview.mp4`); the old
flawed video is `preview_before_joint_fix.mp4`. See the episode verification
notes for measured before/after results and the encoding-quality correction.
Present the repaired 1A for review and stop. Do not implement 1B or publishing.

### Handoff prompt

> Continue this AI 3D video project. Read AI_3D_Video_Workflow.md, AGENTS.md, and
> episodes/001_noria/verification.md first. Milestone 1A has been implemented;
> use its latest checkpoint to determine what was actually verified. Preserve
> the niche, priorities, source, scene, and tool register. Wait for user review
> before beginning Milestone 1B. Agents handle creation and inspection; accuracy
> and output quality take priority over speed and cost.
