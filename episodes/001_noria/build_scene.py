"""Reproducible dry noria mechanism. Run with Blender 5.2.2 LTS.

blender --background --factory-startup --python build_scene.py -- --draft
blender --background --factory-startup --python build_scene.py -- --render
No external assets or Python packages. All dimensions are visualization choices.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
RADIUS = 1.75
CENTER = Vector((0, 0, 2.35))
TUBES = 12
FPS = 24
FRAMES = 144
TILT = math.radians(25)


def mesh_object(name, vertices, faces, material, collection):
    mesh = bpy.data.meshes.new(name + '_mesh')
    mesh.from_pydata(vertices, [], faces)
    if mesh.validate(verbose=True):
        raise ValueError('Invalid generated mesh: ' + name)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def material(name, color, roughness=0.5, grain=False):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    shader = nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = roughness
    if grain:
        coord = nodes.new('ShaderNodeTexCoord')
        mapping = nodes.new('ShaderNodeVectorMath')
        mapping.operation = 'MULTIPLY'
        mapping.inputs[1].default_value = (16, 16, 0.6)
        links.new(coord.outputs['Generated'], mapping.inputs[0])
        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 5
        noise.inputs['Detail'].default_value = 2
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        ramp = nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position = 0.18
        ramp.color_ramp.elements[0].color = (*(v * 0.68 for v in color), 1)
        ramp.color_ramp.elements[1].position = 0.85
        ramp.color_ramp.elements[1].color = (*(v * 1.12 for v in color), 1)
        links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
        links.new(ramp.outputs['Color'], shader.inputs['Base Color'])
        bump = nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.12
        bump.inputs['Distance'].default_value = 0.006
        links.new(noise.outputs['Fac'], bump.inputs['Height'])
        links.new(bump.outputs['Normal'], shader.inputs['Normal'])
    return mat


def assign(obj, name, mat, collection, parent=None):
    obj.name = name
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    collection.objects.link(obj)
    obj.data.materials.append(mat)
    if parent:
        obj.parent = parent  # coordinates are deliberately parent-local
    return obj


def soften(obj, amount=0.012):
    bevel = obj.modifiers.new('Small edge radius', 'BEVEL')
    bevel.width = amount
    bevel.segments = 3
    obj.modifiers.new('Weighted corner normals', 'WEIGHTED_NORMAL')


def beam(name, start, end, width, depth, mat, collection, parent=None):
    start, end = Vector(start), Vector(end)
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = assign(bpy.context.object, name, mat, collection, parent)
    obj.location = (start + end) / 2
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = (end - start).to_track_quat('Z', 'Y')
    obj.scale = (width, depth, (end - start).length)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    soften(obj)
    return obj


def join_frame_feet(sill, legs):
    """Union leg/sill solids before beveling to remove coincident joint faces.

    Joining objects alone preserves overlapping faces. Exact solid unions
    remove them. The source still specifies each timber's dimensions.
    """
    for obj in [sill] + legs:
        obj.modifiers.clear()
    bpy.context.view_layer.objects.active = sill
    for leg in legs:
        union = sill.modifiers.new('Solid leg-to-sill joint', 'BOOLEAN')
        union.operation = 'UNION'
        union.solver = 'EXACT'
        union.object = leg
        bpy.ops.object.modifier_apply(modifier=union.name)
        bpy.data.objects.remove(leg, do_unlink=True)
    if sill.data.validate():
        raise ValueError('Invalid union geometry: ' + sill.name)
    sill['joint_geometry'] = 'Exact union of two legs and sill; no overlapping faces'
    soften(sill)


def cylinder(name, start, end, radius, mat, collection, parent=None):
    start, end = Vector(start), Vector(end)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius,
                                      depth=(end - start).length)
    obj = assign(bpy.context.object, name, mat, collection, parent)
    obj.location = (start + end) / 2
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = (end - start).to_track_quat('Z', 'Y')
    for p in obj.data.polygons:
        p.use_smooth = len(p.vertices) == 4
    soften(obj, 0.004)
    return obj


def annulus(name, outer, inner, depth, mat, collection, parent=None):
    """A closed manifold annulus around local Z; true bore, no solid hidden core."""
    n = 128
    vertices = []
    for radius, z in ((outer, -depth / 2), (outer, depth / 2),
                      (inner, -depth / 2), (inner, depth / 2)):
        vertices.extend((radius * math.cos(i * math.tau / n),
                         radius * math.sin(i * math.tau / n), z) for i in range(n))
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.extend(((i, j, n + j, n + i),
                      (2*n+i, 3*n+i, 3*n+j, 2*n+j),
                      (i, 2*n+i, 2*n+j, j),
                      (n+i, n+j, 3*n+j, 3*n+i)))
    obj = mesh_object(name, vertices, faces, mat, collection)
    if parent:
        obj.parent = parent
    for i, poly in enumerate(obj.data.polygons):
        poly.use_smooth = i % 4 < 2
    soften(obj, 0.003)
    return obj


def tube_mesh(name, outer_mat, inner_mat, collection, parent):
    """Wall, lip, closed base and cavity floor; local +Z is the open mouth."""
    n = 64
    vertices = []
    for radius, z in ((0.10, -0.36), (0.10, 0.36),
                      (0.076, 0.36), (0.076, -0.335)):
        vertices.extend((radius * math.cos(i * math.tau/n),
                         radius * math.sin(i * math.tau/n), z) for i in range(n))
    faces = []
    for i in range(n):
        j = (i + 1) % n
        faces.extend(((i, j, n+j, n+i), (n+i, n+j, 2*n+j, 2*n+i),
                      (2*n+i, 2*n+j, 3*n+j, 3*n+i)))
    faces.append(tuple(reversed(range(n))))
    faces.append(tuple(range(3*n, 4*n)))
    obj = mesh_object(name, vertices, faces, outer_mat, collection)
    obj.data.materials.append(inner_mat)
    obj.parent = parent
    for i, poly in enumerate(obj.data.polygons):
        if i < 3*n:
            poly.use_smooth = i % 3 != 1
            poly.material_index = 1 if i % 3 == 2 else 0
        elif i == 3*n+1:
            poly.material_index = 1
    soften(obj, 0.002)
    obj['mouth_direction'] = 'local +Z; rigid tangent tilted 25 degrees outward'
    obj['base_thickness_m'] = 0.025
    return obj


def band(name, center, direction, radius, mat, collection, parent):
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.008,
                                   major_segments=48, minor_segments=8)
    obj = assign(bpy.context.object, name, mat, collection, parent)
    obj.location = center
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = Vector(direction).to_track_quat('Z', 'Y')
    for face in obj.data.polygons:
        face.use_smooth = True
    return obj


def aim(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat('-Z', 'Y').to_euler()


def light(name, position, target, energy, size, color):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy, data.shape, data.size, data.color = energy, 'DISK', size, color
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = position
    aim(obj, target)


def build():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    rotor_collection = bpy.data.collections.new('01 Rotating assembly')
    fixed_collection = bpy.data.collections.new('02 Fixed supports')
    studio = bpy.data.collections.new('03 Studio')
    for coll in (rotor_collection, fixed_collection, studio):
        scene.collection.children.link(coll)

    bamboo = material('Bamboo • warm honey', (0.47, 0.265, 0.075), grain=True)
    rim_mat = material('Rim • split bamboo laminate', (0.33, 0.16, 0.043), grain=True)
    inner_mat = material('Tube interior • cut bamboo', (0.30, 0.15, 0.048), 0.68)
    end_mat = material('Bamboo node rings', (0.26, 0.115, 0.025), 0.55)
    wood = material('Support timber', (0.13, 0.063, 0.032), grain=True)
    rope = material('Fiber bindings', (0.17, 0.12, 0.058), 0.8)
    marker = material('Tube 01 • teal inspection binding', (0.025, 0.20, 0.22), 0.68)
    bearing_mat = material('Bearing • dark hardwood', (0.055, 0.036, 0.024), 0.34)
    ground = material('Studio • warm limestone', (0.40, 0.44, 0.46), 0.82)

    rotor = bpy.data.objects.new('ROTOR • single rigid Y-axis rotation', None)
    rotor_collection.objects.link(rotor)
    rotor.location = CENTER
    rotor.empty_display_type = 'ARROWS'
    rotor.empty_display_size = 0.3
    rotor['cycle_seconds'] = FRAMES/FPS
    rotor['motion_note'] = 'Prescribed dry rotation; not simulated river power'

    for side in (-1, 1):
        y = side * 0.20
        ring = annulus('Rim front' if side < 0 else 'Rim rear', RADIUS+0.0375,
                       RADIUS-0.0375, 0.10, rim_mat, rotor_collection, rotor)
        ring.location = (0, y, 0)
        ring.rotation_euler.x = math.pi/2
        for i in range(TUBES):
            angle = i*math.tau/TUBES
            radial = Vector((math.cos(angle), 0, math.sin(angle)))
            start, end = radial*0.15, radial*RADIUS
            start.y = end.y = y
            cylinder(f'Spoke {side:+d} {i+1:02d}', start, end, 0.040,
                     bamboo, rotor_collection, rotor)
            for frac in (0.36, 0.70):
                pos = start.lerp(end, frac)
                band(f'Spoke node {side:+d} {i+1:02d} {frac}', pos,
                     radial, 0.041, end_mat, rotor_collection, rotor)

    for i in range(TUBES):
        angle = -math.pi/2 + i*math.tau/TUBES
        radial = Vector((math.cos(angle), 0, math.sin(angle)))
        tangent = Vector((-math.sin(angle), 0, math.cos(angle)))
        direction = tangent*math.cos(TILT) + radial*math.sin(TILT)
        pos = radial*1.79
        pos.y = -0.36
        tube = tube_mesh(f'Tube {i+1:02d} • open +Z', bamboo, inner_mat,
                         rotor_collection, rotor)
        tube.location = pos
        tube.rotation_mode = 'QUATERNION'
        tube.rotation_quaternion = direction.to_track_quat('Z', 'Y')
        for offset in (-0.20, 0.20):
            mounting = pos + offset*direction
            # Radial projection onto the front rim. Saddle reaches the band,
            # keeping the attachment intentional even on the curved rim.
            anchor = Vector((mounting.x, 0, mounting.z)).normalized()*RADIUS
            anchor.y = -0.20
            back = mounting + Vector((0, 0.125, 0))
            beam(f'Tube saddle {i+1:02d} {offset:+.2f}', anchor, back,
                 0.065, 0.045, wood, rotor_collection, rotor)
            for strand in (-0.008, 0.008):
                band(f'Tube binding {i+1:02d} {offset:+.2f} {strand:+.3f}',
                     mounting + strand*direction, direction, 0.104,
                     marker if i == 0 else rope, rotor_collection, rotor)
        band(f'Tube base node {i+1:02d}', pos-0.31*direction, direction,
             0.099, end_mat, rotor_collection, rotor)
        tie = radial*RADIUS
        cylinder(f'Rim cross-tie {i+1:02d}', (tie.x, -0.25, tie.z),
                 (tie.x, 0.25, tie.z), 0.032, bamboo, rotor_collection, rotor)

    cylinder('Hub', (0, -0.30, 0), (0, 0.30, 0), 0.18,
             wood, rotor_collection, rotor)
    cylinder('Shaft • rotates on fixed axis', (0, -1.20, 0), (0, 1.20, 0),
             0.09, bearing_mat, rotor_collection, rotor)
    for side in (-1, 1):
        y = side*0.90
        # The annular journal block sits on two joined timber legs.
        bearing = annulus(f'Bearing block {side:+d} • bored', 0.205, 0.105,
                          0.22, bearing_mat, fixed_collection)
        bearing.location = (0, y, CENTER.z)
        bearing.rotation_euler.x = math.pi/2
        legs = []
        for x in (-0.80, 0.80):
            legs.append(beam(f'A-frame {side:+d} leg {x:+.2f}', (x, y, 0.09),
                 (x*0.065, y, CENTER.z-0.20), 0.14, 0.16,
                 wood, fixed_collection))
        beam(f'Bearing seat {side:+d}', (-0.22, y, CENTER.z-0.24),
             (0.22, y, CENTER.z-0.24), 0.12, 0.18, wood, fixed_collection)
        sill = beam(f'A-frame {side:+d} • jointed legs and sill',
                    (-0.95, y, 0.07), (0.95, y, 0.07),
                    0.14, 0.24, wood, fixed_collection)
        join_frame_feet(sill, legs)
        beam(f'A-frame tie {side:+d}', (-0.58, y, 0.73), (0.58, y, 0.73),
             0.08, 0.12, wood, fixed_collection)
    for x in (-0.8, 0.8):
        beam(f'Base longitudinal brace {x:+.2f}', (x, -1.1, 0.07),
             (x, 1.1, 0.07), 0.14, 0.14, wood, fixed_collection)

    # Modern layered Action API, checked against the installed Blender release.
    action = bpy.data.actions.new('One revolution • linear • six seconds')
    slot = action.slots.new(rotor.id_type, rotor.name)
    strip = action.layers.new('Rigid rotation').strips.new(type='KEYFRAME')
    bag = strip.channelbag(slot, ensure=True)
    curve = bag.fcurves.new(data_path='rotation_euler', index=1)
    curve.keyframe_points.add(2)
    for key, value in zip(curve.keyframe_points, ((1, 0), (FRAMES+1, -math.tau))):
        key.co = value
        key.interpolation = 'LINEAR'
    anim = rotor.animation_data_create()
    anim.action, anim.action_slot = action, slot
    scene.frame_start, scene.frame_end = 1, FRAMES
    scene.render.fps = FPS
    scene.unit_settings.system = 'METRIC'
    scene.render.resolution_x, scene.render.resolution_y = 1080, 1920
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.image_settings.color_depth = '8'
    scene.render.film_transparent = False
    scene.render.use_motion_blur = False  # sharp attachments for mechanical review
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 96
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 6
    scene.cycles.diffuse_bounces = 3
    scene.cycles.glossy_bounces = 3
    preferences = bpy.context.preferences.addons['cycles'].preferences
    preferences.compute_device_type = 'OPTIX'
    preferences.get_devices()
    available = [d for d in preferences.devices if d.type == 'OPTIX']
    if not available:
        raise RuntimeError('OptiX device unavailable; do not silently change renderer')
    for device in preferences.devices:
        device.use = device.type == 'OPTIX'
    scene.cycles.device = 'GPU'
    scene.cycles.seed = 13
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.55, 0.64, 0.76, 1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.28

    bpy.ops.mesh.primitive_plane_add(size=200)
    assign(bpy.context.object, 'Neutral studio ground', ground, studio)
    light('Key • broad softbox', (-3.5, -4.5, 7), (0, 0, 2), 850, 5.0, (1.0, 0.86, 0.68))
    light('Fill • camera right', (4, -3, 5), (0, 0, 2), 600, 4.0, (0.73, 0.86, 1.0))
    light('Rim • rear softbox', (1.5, 3, 6), (0, 0, 2), 1050, 3.5, (1.0, 0.92, 0.75))
    camera_data = bpy.data.cameras.new('Stable orthographic inspection camera')
    camera = bpy.data.objects.new('Camera • locked', camera_data)
    studio.objects.link(camera)
    camera.location = (3, -12, 6.5)
    aim(camera, (0, 0, 2.15))
    camera_data.type, camera_data.ortho_scale = 'ORTHO', 8.15
    camera_data.lens = 50
    camera_data.clip_end = 250
    scene.camera = camera
    scene.render.filepath = str(ROOT / 'renders' / 'frames' / 'frame_')
    scene['scope'] = 'Milestone 1A only: dry rigid mechanism, no physics or fluid simulation'
    scene.frame_set(1)
    # Useful editable scene opening state.
    bpy.ops.object.select_all(action='DESELECT')
    rotor.select_set(True)
    bpy.context.view_layer.objects.active = rotor
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces.active.region_3d.view_perspective = 'CAMERA'
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / 'scene.blend'))
    (ROOT / 'settings.json').write_text(json.dumps({
        'blender': bpy.app.version_string, 'build_hash': bpy.app.build_hash.decode(),
        'engine': scene.render.engine, 'device': 'OPTIX',
        'gpu': [d.name for d in available], 'samples': scene.cycles.samples,
        'denoise': True, 'motion_blur': False, 'resolution': [1080, 1920],
        'fps': FPS, 'frames': FRAMES, 'seconds': FRAMES/FPS,
        'tube_axis_outward_tilt_degrees': 25, 'tube_mounting': 'rigid',
        'physics_simulation': False, 'water': False,
    }, indent=2) + '\n', encoding='utf-8')
    return scene


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    scene = build()
    if args.draft:
        scene.render.resolution_percentage = 50
        scene.cycles.samples = 32
        for frame in (1, 19, 37, 55, 73, 91, 109, 127):
            scene.frame_set(frame)
            scene.render.filepath = str(ROOT / 'renders' / 'draft' / f'frame_{frame:04d}.png')
            bpy.ops.render.render(write_still=True)
    if args.render:
        bpy.ops.render.render(animation=True)


if __name__ == '__main__':
    main()
