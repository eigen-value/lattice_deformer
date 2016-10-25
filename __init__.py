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

bl_info = {
    "name": "LatticeDeformer",
    "version": (0, 1),
    "author": "Lucio Rossi",
    "blender": (2, 76, 0),
    "description": "Use Lattice as Deformer",
    "location": "View3D > Tools > LatticeDef",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}

if "bpy" in locals():
    import imp
    imp.reload(ui)

else:
    from . import ui


######## REGISTER ########

def register():

    ui.register()

def unregister():

    ui.unregister()

if __name__ == "__main__":
    register()
