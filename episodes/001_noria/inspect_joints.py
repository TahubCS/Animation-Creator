"""Diagnose lower-joint cofacial overlap in the saved Blender scene."""
import json
from pathlib import Path
import bpy

root = Path(__file__).resolve().parent
bpy.context.scene.frame_set(1)
graph = bpy.context.evaluated_depsgraph_get()
records = {}
for obj in bpy.data.collections['02 Fixed supports'].objects:
    evaluated = obj.evaluated_get(graph)
    mesh = evaluated.to_mesh()
    points = [evaluated.matrix_world @ vertex.co for vertex in mesh.vertices]
    bounds = [[min(p[i] for p in points), max(p[i] for p in points)] for i in range(3)]
    front = []
    for polygon in mesh.polygons:
        face = [points[i] for i in polygon.vertices]
        if max(p.y for p in face)-min(p.y for p in face) < 1e-7:
            front.append({'y': sum(p.y for p in face)/len(face),
                          'xz': [[p.x,p.z] for p in face], 'area': polygon.area})
    records[obj.name] = {'bounds': bounds, 'y_planes': front}
    evaluated.to_mesh_clear()
(root/'joint_geometry_before.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
for name, record in records.items():
    if name.startswith(('A-frame -1', 'Base longitudinal')):
        print(name, 'bounds', record['bounds'],
              'main Y planes', [(face['y'],face['area']) for face in record['y_planes'] if face['area'] > 0.01])
