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


import bpy
from mathutils import Vector
from .utils import create_root_widget, create_sphere_widget, WGT_PREFIX

def bonify_lattice(lat):

    bone_dimension = 1.0
    bone_vector = Vector((0.0, 0.0, bone_dimension))
    average_vector = Vector((0, 0, 0))

    pts = lat.data.points
    lat.modifiers.new(name="Armature", type='ARMATURE')
    bpy.ops.object.armature_add()
    rig=bpy.context.object
    lat.modifiers[-1].object = rig

    bpy.ops.object.mode_set(mode='EDIT')
    for pt in pts:
        pt.select = False
    edit_bones = rig.data.edit_bones

    root = edit_bones[0]
    name = root.name

    for i, pt in enumerate(pts):
        eb = rig.data.edit_bones.new(name)
        eb.head = (lat.matrix_world*pt.co.to_4d()).to_3d()
        average_vector += eb.head
        eb.tail = eb.head + bone_vector
        eb.parent = root
        vg=lat.vertex_groups.new(name=eb.name)
        vg.add([i], weight=1, type='ADD')

    root.head = average_vector/len(pts)
    root.tail = root.head + Vector((0.0, bone_dimension, 0.0))

    # Make Widgets
    bpy.ops.object.mode_set(mode='OBJECT')
    pbones = rig.pose.bones
    for pb in pbones:
        if pb.name == name:
            create_root_widget(rig, pb.name, bone_transform_name=None)
            pb.custom_shape = bpy.data.objects[WGT_PREFIX + pb.name]
        else:
            create_sphere_widget(rig, pb.name, bone_transform_name=None)
            pb.custom_shape = bpy.data.objects[WGT_PREFIX + pb.name]



class VIEW3D_PT_LatticeDeformerPanel(bpy.types.Panel):
    bl_label = "Make Lattice Deformer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = 'LatticeDef'

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.operator('lattdef.make_lattdef', text='Make Lattice Deformer')


class OBJECT_OT_CreateLatticeDeformer(bpy.types.Operator):
    """Create a Lattice Deformer"""
    bl_idname = "lattdef.make_lattdef"
    bl_label = "Make Lattice Deformer"

    def execute(self,context):
        scn = context.scene

        lat = bpy.context.active_object
        if lat.name not in bpy.data.lattices.keys():
            return {'FINISHED'}
        else:
            bonify_lattice(lat)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_CreateLatticeDeformer)
    bpy.utils.register_class(VIEW3D_PT_LatticeDeformerPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CreateLatticeDeformer)
    bpy.utils.unregister_class(VIEW3D_PT_LatticeDeformerPanel)