# Milestone 1A: wheel and container motion

Scope: six seconds, 24 fps, 1080 × 1920, silent, one stationary camera.
Demonstrate a rigid wheel rotating about a fixed horizontal axis, with visibly
open, closed-ended bamboo tubes secured around the rim. No water or trough.

Source: FAO *Water lifting devices*, section 4.9.4 and figure 152:
https://www.fao.org/4/ah810e/ah810e12.htm (accessed 2026-10-04).
The source supports rim-mounted closed-ended bamboo tubes and river-driven
norias. Our proportions, tube angle, supports, bindings, materials, and speed
are visualization choices, not a measured reconstruction of a dated artifact.

## Geometry and degrees of freedom

- Units: meters; wheel plane XZ, shaft axis Y, axle center (0, 0, 2.35).
- Twin rims: radius 1.75, radial thickness 0.075, axial depth 0.10,
  centered at Y = ±0.20; twelve paired bamboo spokes and rim cross-ties.
- Twelve hollow tubes: length 0.72, outer radius 0.10, inner radius 0.076,
  base thickness 0.025; centers at radius 1.79, Y = -0.36.
- Tube open end: local +Z. Its axis is the counterclockwise tangent tilted
  25° outward in the wheel plane. At the rightmost position its mouth points
  upward and outward. This mounting stays rigid throughout the cycle; it has
  no independent pivot. Collection/retention/discharge suitability is unverified.
- Two binding bands and two rim saddles per tube make the attachment explicit.
- Wheel, hub, tubes, bindings, ties, and shaft rotate as one assembly. Only one
  animated rotational degree of freedom. Shaft axis does not translate.
- Two stationary A-frames carry annular bearing blocks at Y = ±0.90.
  Shaft radius 0.09; bearing bore radius 0.105, with radial running clearance.
  Support and bearing geometry lies outside the rotor's axial swept envelope.
- Each A-frame's legs and sill form one closed, solid-unioned render mesh.
  This removes overlapping coplanar exterior faces that caused foot-joint
  flicker in the first preview. Source retains the individual timber dimensions.
- A neutral studio ground plane provides contact shadows; no landscape.

## Motion and acceptance

One complete revolution over six seconds, constant angular velocity, right side
rising as viewed from the camera side (negative Y). Timing is illustrative;
there is no river force or physics solver in this dry mechanism test.
Frame 1 is angle 0; frame 145 is the virtual loop endpoint. Deliver frames
1–144 to avoid a duplicate endpoint. A distinguishable binding on tube 01
allows the full cycle to be tracked despite twelve repeated containers.

Check every output frame for stationary camera/support transforms, fixed shaft
center, rigid tube transforms, expected angle and radius, tube separation,
camera framing, and moving/stationary clearance. Check additional subframes
and the loop endpoint. Inspect draft and final review frames and the rendered
sequence. Save exact executed results separately in `verification.md`.
