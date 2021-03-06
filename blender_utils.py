# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy

def faces_from_mesh(ob, apply_modifier=False, triangulate=True):
    '''
    From an object, return a generator over a list of faces.

    Each faces is a list of his vertexes. Each vertex is a tuple of
    his coordinate.

    apply_modifier
        Apply the preview modifier to the returned liste

    triangulate
        Split the quad into two triangles
    '''

    # get the modifiers
    try:
        mesh = ob.to_mesh(bpy.context.scene, apply_modifier, "PREVIEW")
    except RuntimeError:
        raise StopIteration

    mesh.transform(ob.matrix_world)

    if triangulate:
        # From a list of faces, return the face triangulated if needed.
        def iter_face_index():
            for face in mesh.faces:
                vertices = face.vertices[:]
                if len(vertices) == 4:
                    yield vertices[0], vertices[1], vertices[2]
                    yield vertices[2], vertices[3], vertices[0]
                else:
                    yield vertices
    else:
        def iter_face_index():
            for face in mesh.faces:
                yield face.vertices[:]

    vertices = mesh.vertices

    for indexes in iter_face_index():
        yield [vertices[index].co.copy() for index in indexes]

    bpy.data.meshes.remove(mesh)


def vertices_from_mesh(ob):
    '''
    '''

    # get the modifiers
    try:
        mesh = ob.to_mesh(bpy.context.scene, False, "PREVIEW")
    except RuntimeError:
        raise StopIteration

    matrix = ob.matrix_world.copy()
    
    for v in mesh.vertices:
        yield (matrix*v.co)

    bpy.data.meshes.remove(mesh)

def edges_from_mesh(ob):
    '''
    '''

    # get the modifiers
    try:
        mesh = ob.to_mesh(bpy.context.scene, False, "PREVIEW")
    except RuntimeError:
        raise StopIteration

    for e in mesh.edges:
        yield list(e.vertices)

    bpy.data.meshes.remove(mesh)
