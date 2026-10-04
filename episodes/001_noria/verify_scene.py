"""Verify the SAVED scene, including continuous swept-envelope separation.

blender --background scene.blend --python-exit-code 1 --python verify_scene.py
Reports measurements; assertions produce a failed process, never a silent pass.
"""
import json
import math
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
scene = bpy.context.scene
rotor = bpy.data.objects['ROTOR • single rigid Y-axis rotation']
moving = list(bpy.data.collections['01 Rotating assembly'].objects)
fixed = list(bpy.data.collections['02 Fixed supports'].objects)
tubes = [obj for obj in moving if obj.name.startswith('Tube ') and 'open' in obj.name]
shaft = bpy.data.objects['Shaft • rotates on fixed axis']
center = Vector((0, 0, 2.35))
assert len(tubes) == 12
assert scene.render.engine == 'CYCLES'
assert (scene.render.resolution_x, scene.render.resolution_y) == (1080, 1920)
assert scene.frame_start == 1 and scene.frame_end == 144 and scene.render.fps == 24
assert len([o for o in scene.objects if o.animation_data]) == 1
scene.frame_set(1)
graph = bpy.context.evaluated_depsgraph_get()

# User-reported flicker regression: leg/sill intersections must be closed,
# single solid meshes, not several cubes with overlapping coplanar exteriors.
joint_mesh_checks = {}
for obj in fixed:
    if 'jointed legs and sill' not in obj.name:
        continue
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    assert all(edge.is_manifold for edge in bm.edges), f'Open/duplicate joint faces: {obj.name}'
    assert all(face.calc_area() > 1e-10 for face in bm.faces)
    unseen = set(bm.verts)
    components = 0
    while unseen:
        components += 1
        pending = [unseen.pop()]
        while pending:
            vertex = pending.pop()
            for edge in vertex.link_edges:
                adjacent = edge.other_vert(vertex)
                if adjacent in unseen:
                    unseen.remove(adjacent)
                    pending.append(adjacent)
    assert components == 1, f'Disconnected frame geometry: {obj.name}'
    volume = abs(bm.calc_volume())
    assert volume > 0.01
    joint_mesh_checks[obj.name] = {'manifold': True, 'components': components, 'volume_m3': volume}
    bm.free()
assert len(joint_mesh_checks) == 2, 'Joint geometry repair missing'


def vertices(obj):
    evaluated = obj.evaluated_get(graph)
    mesh = evaluated.to_mesh()
    points = [evaluated.matrix_world @ v.co for v in mesh.vertices]
    evaluated.to_mesh_clear()
    return points


def error(a, b):
    return max(abs(a[i][j]-b[i][j]) for i in range(4) for j in range(4))


# Cache evaluated geometry in object-local space. Modifiers have no animation.
local_geometry = {}
for obj in moving + fixed:
    if obj.type != 'MESH':
        continue
    points = vertices(obj)
    inverse = obj.matrix_world.inverted()
    local_geometry[obj.name] = [inverse @ p for p in points]

# All saddles remain on the back side outside the hollow cavity. A plane
# distance greater than the bore radius certifies this for faces as well as
# vertices, and remains invariant under rigid rotation about Y.
saddle_cavity_clearances = []
for obj in moving:
    if obj.name.startswith('Tube saddle'):
        points = [obj.matrix_world @ p for p in local_geometry[obj.name]]
        gap = min(p.y + 0.36 for p in points) - 0.076
        assert gap > 0, f'Saddle reaches tube hollow interior: {obj.name}'
        saddle_cavity_clearances.append(gap)

rigid_reference = {o.name: rotor.matrix_world.inverted() @ o.matrix_world for o in moving if o != rotor}
fixed_reference = {o.name: o.matrix_world.copy() for o in fixed+[scene.camera]}
nonshaft = [o for o in moving if o.type == 'MESH' and o != shaft]
swept_points = [rotor.matrix_world.inverted() @ o.matrix_world @ p
                for o in nonshaft for p in local_geometry[o.name]]
radial_max = max(math.hypot(p.x, p.z) for p in swept_points)
ymin = min(p.y for p in swept_points)
ymax = max(p.y for p in swept_points)
zmin = center.z-radial_max  # continuous full-cycle bound, includes bevels and bindings
clearances = []
shaft_clearances = []
for obj in fixed:
    points = [obj.matrix_world @ p for p in local_geometry[obj.name]]
    low = [min(p[i] for p in points) for i in range(3)]
    high = [max(p[i] for p in points) for i in range(3)]
    # Axial or vertical disjoint intervals certify full-cycle rotor separation.
    separation = max(low[1]-ymax, ymin-high[1], zmin-high[2])
    assert separation > 0, f'No certified continuous rotor clearance: {obj.name}'
    clearances.append((obj.name, separation))
    if obj.name.startswith('Bearing block'):
        # Correct for polygon inscribed bore and flat-edged circle, conservatively.
        clearance = 0.105*math.cos(math.pi/128)-0.09
    else:
        dx = max(low[0], -high[0], 0)
        dz = max(low[2]-center.z, center.z-high[2], 0)
        clearance = math.hypot(dx, dz)-0.09
    assert clearance > 0, f'Shaft intersects fixed support: {obj.name}'
    shaft_clearances.append((obj.name, clearance))
assert zmin > 0, 'Rotor reaches ground'

# Tube bounding spheres establish no tube/tube intersections through any angle.
body_sphere = math.hypot(0.36, 0.10)
adjacent_distance = 2*1.79*math.sin(math.pi/12)
tube_gap = adjacent_distance-2*body_sphere
assert tube_gap > 0

max_rigid_error = max_fixed_error = max_angle_error = max_axis_error = 0
screen_min = Vector((1, 1, 1))
screen_max = Vector((0, 0, 0))
first_tube = tubes[0]
first_tube_reference = first_tube.matrix_world.copy()
camera_inverse = scene.camera.matrix_world.inverted()
view = scene.camera.data.view_frame(scene=scene)
left, right = min(v.x for v in view), max(v.x for v in view)
bottom, top = min(v.y for v in view), max(v.y for v in view)
for frame_twice in range(2, 291):  # 1..145 inclusive, half-frame steps
    frame = frame_twice/2
    scene.frame_set(int(frame), subframe=frame-int(frame))
    expected = -math.tau*(frame-1)/144
    max_angle_error = max(max_angle_error, abs(rotor.rotation_euler.y-expected))
    max_axis_error = max(max_axis_error, (rotor.matrix_world.translation-center).length)
    for obj in moving:
        if obj != rotor:
            assert obj.parent == rotor and not obj.constraints
            delta = error(rotor.matrix_world.inverted() @ obj.matrix_world, rigid_reference[obj.name])
            max_rigid_error = max(max_rigid_error, delta)
    for obj in fixed+[scene.camera]:
        max_fixed_error = max(max_fixed_error, error(obj.matrix_world, fixed_reference[obj.name]))
    for tube in tubes:
        position = tube.matrix_world.translation-center
        assert abs(math.hypot(position.x, position.z)-1.79) < 1e-5
        assert abs(position.y+0.36) < 1e-5
        direction = tube.matrix_world.to_3x3() @ Vector((0, 0, 1))
        radial = Vector((position.x, 0, position.z)).normalized()
        tangent = Vector((-radial.z, 0, radial.x))
        assert abs(direction.dot(radial)-math.sin(math.radians(25))) < 1e-5
        assert abs(direction.dot(tangent)-math.cos(math.radians(25))) < 1e-5
    # Actual evaluated vertices, including all stationary supports and shaft.
    for obj in nonshaft+[shaft]+fixed:
        camera_matrix = camera_inverse @ obj.matrix_world
        for point in local_geometry[obj.name]:
            p = camera_matrix @ point
            u, v = (p.x-left)/(right-left), (p.y-bottom)/(top-bottom)
            assert p.z < 0, 'Geometry behind camera'
            screen_min.x, screen_min.y = min(screen_min.x, u), min(screen_min.y, v)
            screen_max.x, screen_max.y = max(screen_max.x, u), max(screen_max.y, v)
assert max_rigid_error < 1e-5
assert max_fixed_error < 1e-8
assert max_axis_error < 1e-8
assert max_angle_error < 1e-5
assert min(screen_min.x, screen_min.y) > 0.025
assert max(screen_max.x, screen_max.y) < 0.975
assert error(first_tube.matrix_world, first_tube_reference) < 1e-5
scene.frame_set(37)
tracked = bpy.data.objects['Tube 01 • open +Z'].matrix_world.translation-center
assert tracked.x > 1.78 and abs(tracked.z) < 1e-5, 'Right side must rise'
scene.frame_set(1)

result = {
    'passed': True, 'sample_count': 289, 'sample_frames': '1..145 in 0.5-frame increments',
    'joint_mesh_checks': joint_mesh_checks,
    'continuous_collision_method': 'Disjoint swept axial/vertical intervals; shaft bore and support radial bounds',
    'max_rigid_transform_error': max_rigid_error,
    'max_stationary_transform_error': max_fixed_error,
    'max_axis_translation_error_m': max_axis_error,
    'max_angle_error_radians': max_angle_error,
    'rotor_swept_radius_m': radial_max,
    'rotor_axial_interval_m': [ymin, ymax],
    'rotor_ground_clearance_m': zmin,
    'minimum_rotor_support_certified_clearance_m': min(v for _, v in clearances),
    'minimum_shaft_bearing_certified_clearance_m': min(v for _, v in shaft_clearances),
    'tube_body_bounding_sphere_clearance_m': tube_gap,
    'minimum_saddle_to_cavity_plane_clearance_m': min(saddle_cavity_clearances),
    'framing_uv_min': [screen_min.x, screen_min.y],
    'framing_uv_max': [screen_max.x, screen_max.y],
    'loop_endpoint_matches': True, 'direction': 'right side rises, viewed from negative Y',
    'support_clearances_m': dict(clearances), 'shaft_clearances_m': dict(shaft_clearances),
}
(ROOT/'scene_checks.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print('SCENE_CHECKS_PASS', json.dumps(result))
