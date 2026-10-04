# Continuing-agent workflow

Read `AI_3D_Video_Workflow.md` and the latest episode's `brief.md` and
`verification.md` before choosing tools or working. The workflow document is
the project record; distinguish proposals from executed and verified results.

## Scope and priorities

- Build original educational 3D animations about historical engineering and
  architecture in China and Japan. Keep historical claims tied to sources.
- Work on the next small milestone. Do not rebuild the stack or reopen settled
  decisions without evidence. Accuracy and output quality outrank speed and cost.
- Agents handle creative work, code, scene generation, animation, rendering,
  inspection, and corrections. Do not transfer these tasks to the user.
- Use Blender/Python as the working default and simple parameterized scripts.
  Avoid unnecessary services, dependencies, or agent frameworks.
- Preserve user changes and follow the global working agreement supplied in the
  session: correctness, simplicity, maintainability, robustness, demonstrated
  scalability, then delivery speed.

## Environment and sources

- State the actual execution environment; a cloud workspace is not the user's
  laptop. Verify installations, exact versions, and GPU access before assuming
  they work. Do not treat earlier environment findings as current facts.
- Use current official documentation when software behavior or platform rules
  matter. Use Context7 for third-party APIs when available, plus runtime checks
  against the installed release. Record documentation gaps explicitly.
- Maintain claim-to-source notes with URL, relevant section, and access date.
  Separate evidence from chosen dimensions, colors, framing, and timing.
- Do not invent dynasties, dates, inventors, performance data, or historical
  sequences. Do not call scripted motion a physics or fluid simulation.

## Each milestone

1. Research the narrow mechanism claim and record unknowns.
2. Specify objects, dimensions, attachments, degrees of freedom, motion, camera,
   and acceptance criteria.
3. Save readable, reproducible source with editable, intentionally named objects.
4. Render draft frames and a short preview; inspect before final rendering.
5. Check attachment behavior, clearances throughout the cycle, direction,
   continuous motion, readable framing, and representative rendered frames.
   Inspect small stationary joints in native-resolution consecutive crops,
   including encoded output. Full-view thumbnails and static transforms missed
   the first preview's floor-joint flicker; run `review_joints.py --after` for 1A.
6. Correct the source and regenerate; avoid undocumented manual scene edits.
7. Save the editable scene, preview, review frames, settings, reproduction
   commands, checks, failures, unresolved issues, and next action. Update the
   workflow checkpoint and decision log after actual work.

Present a small concrete result for review. Ask preferences only when they
materially affect the next result. Never infer success from source, a plan, or a
README; report exactly what executed and what remains unverified.

## Current milestone boundary

Milestone 1A is a 5–8 second silent vertical wheel-and-container motion test:
fixed axle axis, stable camera, simple readable materials and lighting, rigid
documented container mounting, and no moving-wheel/support intersections.
Save source, `.blend`, video, review frames, and verification notes. No water,
trough, village, people, landscape, narration, music, or assembly sequence.
Stop after presenting 1A for review. Begin 1B only after user authorization.

Public posting, account connections, voice, channel automation, and publication
policy decisions are outside the current milestone. Code-generated animation
does not automatically remove disclosure duties or establish monetization
eligibility.
