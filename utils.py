#====================== BEGIN GPL LICENSE BLOCK ======================
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
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

import bpy
import imp
import importlib
import math
import random
import time
from mathutils import Vector, Matrix
from rna_prop_ui import rna_idprop_ui_prop_get

WGT_PREFIX = "WGT-"  # Prefix for widget objects

WGT_LAYERS = [x == 19 for x in range(0, 20)]  # Widgets go on the last scene layer.

def obj_to_bone(obj, rig, bone_name):
    """ Places an object at the location/rotation/scale of the given bone.
    """
    if bpy.context.mode == 'EDIT_ARMATURE':
        raise MetarigError("obj_to_bone(): does not work while in edit mode")

    bone = rig.data.bones[bone_name]

    mat = rig.matrix_world * bone.matrix_local

    obj.location = mat.to_translation()

    obj.rotation_mode = 'XYZ'
    obj.rotation_euler = mat.to_euler()

    scl = mat.to_scale()
    scl_avg = (scl[0] + scl[1] + scl[2]) / 3
    obj.scale = (bone.length * scl_avg), (bone.length * scl_avg), (bone.length * scl_avg)

def create_widget(rig, bone_name, bone_transform_name=None):
    """ Creates an empty widget object for a bone, and returns the object.
    """
    if bone_transform_name == None:
        bone_transform_name = bone_name

    obj_name = WGT_PREFIX + bone_name
    scene = bpy.context.scene

    # Check if it already exists in the scene
    if obj_name in scene.objects:
        # Move object to bone position, in case it changed
        obj = scene.objects[obj_name]
        obj_to_bone(obj, rig, bone_transform_name)

        return None
    else:
        # Delete object if it exists in blend data but not scene data.
        # This is necessary so we can then create the object without
        # name conflicts.
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].user_clear()
            bpy.data.objects.remove(bpy.data.objects[obj_name])

        # Create mesh object
        mesh = bpy.data.meshes.new(obj_name)
        obj = bpy.data.objects.new(obj_name, mesh)
        scene.objects.link(obj)

        # Move object to bone position and set layers
        obj_to_bone(obj, rig, bone_transform_name)
        obj.layers = WGT_LAYERS

        return obj

def create_sphere_widget(rig, bone_name, bone_transform_name=None):
    """ Creates a basic sphere widget, three pependicular overlapping circles.
    """
    obj = create_widget(rig, bone_name, bone_transform_name)
    if obj != None:
        verts = [(0.3535533845424652, 0.3535533845424652, 0.0), (0.4619397521018982, 0.19134171307086945, 0.0), (0.5, -2.1855694143368964e-08, 0.0), (0.4619397521018982, -0.19134175777435303, 0.0), (0.3535533845424652, -0.3535533845424652, 0.0), (0.19134174287319183, -0.4619397521018982, 0.0), (7.549790126404332e-08, -0.5, 0.0), (-0.1913416087627411, -0.46193981170654297, 0.0), (-0.35355329513549805, -0.35355350375175476, 0.0), (-0.4619397521018982, -0.19134178757667542, 0.0), (-0.5, 5.962440319251527e-09, 0.0), (-0.4619397222995758, 0.1913418024778366, 0.0), (-0.35355326533317566, 0.35355350375175476, 0.0), (-0.19134148955345154, 0.46193987131118774, 0.0), (3.2584136988589307e-07, 0.5, 0.0), (0.1913420855998993, 0.46193960309028625, 0.0), (7.450580596923828e-08, 0.46193960309028625, 0.19134199619293213), (5.9254205098113744e-08, 0.5, 2.323586443253589e-07), (4.470348358154297e-08, 0.46193987131118774, -0.1913415789604187), (2.9802322387695312e-08, 0.35355350375175476, -0.3535533547401428), (2.9802322387695312e-08, 0.19134178757667542, -0.46193981170654297), (5.960464477539063e-08, -1.1151834122813398e-08, -0.5000000596046448), (5.960464477539063e-08, -0.1913418024778366, -0.46193984150886536), (5.960464477539063e-08, -0.35355350375175476, -0.3535533845424652), (7.450580596923828e-08, -0.46193981170654297, -0.19134166836738586), (9.348272556053416e-08, -0.5, 1.624372103492533e-08), (1.043081283569336e-07, -0.4619397521018982, 0.19134168326854706), (1.1920928955078125e-07, -0.3535533845424652, 0.35355329513549805), (1.1920928955078125e-07, -0.19134174287319183, 0.46193966269493103), (1.1920928955078125e-07, -4.7414250303745575e-09, 0.49999991059303284), (1.1920928955078125e-07, 0.19134172797203064, 0.46193966269493103), (8.940696716308594e-08, 0.3535533845424652, 0.35355329513549805), (0.3535534739494324, 0.0, 0.35355329513549805), (0.1913418173789978, -2.9802322387695312e-08, 0.46193966269493103), (8.303572940349113e-08, -5.005858838558197e-08, 0.49999991059303284), (-0.19134165346622467, -5.960464477539063e-08, 0.46193966269493103), (-0.35355329513549805, -8.940696716308594e-08, 0.35355329513549805), (-0.46193963289260864, -5.960464477539063e-08, 0.19134168326854706), (-0.49999991059303284, -5.960464477539063e-08, 1.624372103492533e-08), (-0.4619397521018982, -2.9802322387695312e-08, -0.19134166836738586), (-0.3535534143447876, -2.9802322387695312e-08, -0.3535533845424652), (-0.19134171307086945, 0.0, -0.46193984150886536), (7.662531942287387e-08, 9.546055501630235e-09, -0.5000000596046448), (0.19134187698364258, 5.960464477539063e-08, -0.46193981170654297), (0.3535535931587219, 5.960464477539063e-08, -0.3535533547401428), (0.4619399905204773, 5.960464477539063e-08, -0.1913415789604187), (0.5000000596046448, 5.960464477539063e-08, 2.323586443253589e-07), (0.4619396924972534, 2.9802322387695312e-08, 0.19134199619293213)]
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (0, 15), (16, 31), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (32, 33), (33, 34), (34, 35), (35, 36), (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 42), (42, 43), (43, 44), (44, 45), (45, 46), (46, 47), (32, 47)]
        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()

def create_root_widget(rig, bone_name, bone_transform_name=None):
    """ Creates a widget for the root bone.
    """
    obj = create_widget(rig, bone_name, bone_transform_name)
    if obj != None:
        verts = [(0.7071067690849304, 0.7071067690849304, 0.0), (0.7071067690849304, -0.7071067690849304, 0.0), (-0.7071067690849304, 0.7071067690849304, 0.0), (-0.7071067690849304, -0.7071067690849304, 0.0), (0.8314696550369263, 0.5555701851844788, 0.0), (0.8314696550369263, -0.5555701851844788, 0.0), (-0.8314696550369263, 0.5555701851844788, 0.0), (-0.8314696550369263, -0.5555701851844788, 0.0), (0.9238795042037964, 0.3826834261417389, 0.0), (0.9238795042037964, -0.3826834261417389, 0.0), (-0.9238795042037964, 0.3826834261417389, 0.0), (-0.9238795042037964, -0.3826834261417389, 0.0), (0.9807852506637573, 0.19509035348892212, 0.0), (0.9807852506637573, -0.19509035348892212, 0.0), (-0.9807852506637573, 0.19509035348892212, 0.0), (-0.9807852506637573, -0.19509035348892212, 0.0), (0.19509197771549225, 0.9807849526405334, 0.0), (0.19509197771549225, -0.9807849526405334, 0.0), (-0.19509197771549225, 0.9807849526405334, 0.0), (-0.19509197771549225, -0.9807849526405334, 0.0), (0.3826850652694702, 0.9238788485527039, 0.0), (0.3826850652694702, -0.9238788485527039, 0.0), (-0.3826850652694702, 0.9238788485527039, 0.0), (-0.3826850652694702, -0.9238788485527039, 0.0), (0.5555717945098877, 0.8314685821533203, 0.0), (0.5555717945098877, -0.8314685821533203, 0.0), (-0.5555717945098877, 0.8314685821533203, 0.0), (-0.5555717945098877, -0.8314685821533203, 0.0), (0.19509197771549225, 1.2807848453521729, 0.0), (0.19509197771549225, -1.2807848453521729, 0.0), (-0.19509197771549225, 1.2807848453521729, 0.0), (-0.19509197771549225, -1.2807848453521729, 0.0), (1.280785322189331, 0.19509035348892212, 0.0), (1.280785322189331, -0.19509035348892212, 0.0), (-1.280785322189331, 0.19509035348892212, 0.0), (-1.280785322189331, -0.19509035348892212, 0.0), (0.3950919806957245, 1.2807848453521729, 0.0), (0.3950919806957245, -1.2807848453521729, 0.0), (-0.3950919806957245, 1.2807848453521729, 0.0), (-0.3950919806957245, -1.2807848453521729, 0.0), (1.280785322189331, 0.39509034156799316, 0.0), (1.280785322189331, -0.39509034156799316, 0.0), (-1.280785322189331, 0.39509034156799316, 0.0), (-1.280785322189331, -0.39509034156799316, 0.0), (0.0, 1.5807849168777466, 0.0), (0.0, -1.5807849168777466, 0.0), (1.5807852745056152, 0.0, 0.0), (-1.5807852745056152, 0.0, 0.0)]
        edges = [(0, 4), (1, 5), (2, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12), (9, 13), (10, 14), (11, 15), (16, 20), (17, 21), (18, 22), (19, 23), (20, 24), (21, 25), (22, 26), (23, 27), (0, 24), (1, 25), (2, 26), (3, 27), (16, 28), (17, 29), (18, 30), (19, 31), (12, 32), (13, 33), (14, 34), (15, 35), (28, 36), (29, 37), (30, 38), (31, 39), (32, 40), (33, 41), (34, 42), (35, 43), (36, 44), (37, 45), (38, 44), (39, 45), (40, 46), (41, 46), (42, 47), (43, 47)]
        mesh = obj.data
        mesh.from_pydata(verts, edges, [])
        mesh.update()