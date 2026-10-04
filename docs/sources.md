# Sources used for Milestone 1A

Access date: 2026-10-04. No publication-policy review was needed for this local test.

| Source | Supports | Does not establish |
| --- | --- | --- |
| FAO, *Water lifting devices*, §4.9.4, figs. 151–152: https://www.fao.org/4/ah810e/ah810e12.htm | River-current-driven norias; closed-ended bamboo tubes mounted around a rim; lifting toward a trough | Our exact mounting angle, dimensions, timber supports, bindings, construction period, or speed |
| Blender official LTS/release pages: https://www.blender.org/download/lts/ and https://www.blender.org/releases/ | 5.2 is a supported LTS line; existing installation can be used | A successful local renderer; that was established through executed renders |
| Blender Python API through Context7 `/websites/blender_api_current`: https://docs.blender.org/api/current/info_quickstart.html and https://docs.blender.org/api/current/bpy.types.ActionKeyframeStrip.html | Explicit meshes; action slots, layers, strips, channelbags, and F-curves | Exact 5.2 encoder changes; direct versioned API retrieval failed |

Blender 4.5 API was initially queried while locating the installation. After
finding 5.2.2, the current API was queried and actual 5.2 RNA and method
docstrings were inspected. `Action.slots` exists on action instances even though
a class-level `hasattr` probe returned false. The current Context7 index did
not describe the 5.2 output selector; runtime RNA confirmed that encoding
requires `image_settings.media_type = 'VIDEO'` before selecting `FFMPEG`.

Direct web retrieval of the 5.2 API pages was blocked by a fetch/payment error.
The installed release's actual Python API and successful execution provide the
version-specific validation. No unsupported historical claims were added.

For the floor-joint repair, queried Context7's available Blender API index and
checked the official Exact Boolean solver documentation:
https://docs.staging.blender.org/api/current/bpy.types.BooleanModifier.html
and https://developer.blender.org/docs/release_notes/2.91/modeling/ .
These support using Exact unions to resolve coplanar/overlapping geometry.
The actual union operations ran in Blender 5.2.2, and saved mesh topology was
checked for manifold edges, positive volume, and a single connected component.
