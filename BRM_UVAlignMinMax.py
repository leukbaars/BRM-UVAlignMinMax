bl_info = {
    "name": "BRM_UVAlignMinMax",
    "category": "UV",
    "author": "Bram Eulaers",
    "description": "Align selected uvs to the top, down, left or right uv"
    }

import bpy
import bmesh
from bpy.props import EnumProperty, BoolProperty

def align(dir):

    mesh = bpy.context.object.data
    bm = bmesh.from_edit_mesh(mesh)
    bm.faces.ensure_lookup_table()

    xmin,xmax,ymin,ymax=0,0,0,0

    first = True
    for i,face in enumerate(bm.faces):
        if face.select:
            for o,vert in enumerate(face.loops):
                if vert[bm.loops.layers.uv.active].select:
                    if first:
                        xmin=vert[bm.loops.layers.uv.active].uv.x
                        xmax=vert[bm.loops.layers.uv.active].uv.x
                        ymin=vert[bm.loops.layers.uv.active].uv.y
                        ymax=vert[bm.loops.layers.uv.active].uv.y
                        first=False
                    else:
                        if vert[bm.loops.layers.uv.active].uv.x < xmin:
                            xmin=vert[bm.loops.layers.uv.active].uv.x
                        elif vert[bm.loops.layers.uv.active].uv.x > xmax:
                            xmax=vert[bm.loops.layers.uv.active].uv.x
                        if vert[bm.loops.layers.uv.active].uv.y < ymin:
                            ymin=vert[bm.loops.layers.uv.active].uv.y
                        elif vert[bm.loops.layers.uv.active].uv.y > ymax:
                            ymax=vert[bm.loops.layers.uv.active].uv.y
    
    for i,face in enumerate(bm.faces):
        if face.select:
            for o,vert in enumerate(face.loops):
                if vert[bm.loops.layers.uv.active].select:
                    if dir=="up":
                        vert[bm.loops.layers.uv.active].uv.y=ymax
                    if dir=="down":    
                        vert[bm.loops.layers.uv.active].uv.y=ymin
                    if dir=="left":
                        vert[bm.loops.layers.uv.active].uv.x=xmin
                    if dir=="right":    
                        vert[bm.loops.layers.uv.active].uv.x=xmax

    bmesh.update_edit_mesh(mesh, False, False)
    
class BRM_UVAlignMinMaxUp(bpy.types.Operator):
    """Align Max Y"""
    bl_idname = "uv.alignymax"
    bl_label = "Align Max Y"
    bl_options = {"UNDO"}
    def execute(self, context):  
        align("up")
        return {'FINISHED'}

class BRM_UVAlignMinMaxDown(bpy.types.Operator):
    """Align Min Y"""
    bl_idname = "uv.alignymin"
    bl_label = "Align Min Y"
    bl_options = {"UNDO"}
    def execute(self, context):  
        align("down")
        return {'FINISHED'}

class BRM_UVAlignMinMaxLeft(bpy.types.Operator):
    """Align Min X"""
    bl_idname = "uv.alignxmin"
    bl_label = "Align Min X"
    bl_options = {"UNDO"}
    def execute(self, context):  
        align("left")
        return {'FINISHED'}

class BRM_UVAlignMinMaxRight(bpy.types.Operator):
    """Align Max X"""
    bl_idname = "uv.alignxmax"
    bl_label = "Align Max X"
    bl_options = {"UNDO"}
    def execute(self, context):  
        align("right")
        return {'FINISHED'}

class BRM_UVAlignMinMaxPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    show_panel_tools = BoolProperty(
        name="Show Align Tools in UV Editor",
        default=True
    )
    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        column.prop(self, "show_panel_tools")

class BRM_UVAlignMinMaxPanel(bpy.types.Panel):
    """BRM_UVAlignMinMax Panel"""
    bl_label = "UV Align to Min/Max"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'

    @classmethod
    def poll(cls, context):
        prefs = bpy.context.user_preferences.addons[__name__].preferences
        return prefs.show_panel_tools

    def draw_header(self, _):
        layout = self.layout
        layout.label(text="", icon='LATTICE_DATA')

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Align Selected Vertices to:")

        split = layout.split()

        col = split.column(align=True)
        col.separator()
        col.separator()
        col.operator("uv.alignxmin", text="Left", icon = "TRIA_LEFT_BAR")
        col.separator()

        col = split.column()
        col.operator("uv.alignymax", text="Up", icon = "TRIA_UP_BAR")
        col.operator("uv.alignymin", text="Down", icon = "TRIA_DOWN_BAR")

        col = split.column(align=True)
        col.separator()
        col.separator()
        col.operator("uv.alignxmax", text="Right", icon = "TRIA_RIGHT_BAR")
        
def register():
    bpy.utils.register_class(BRM_UVAlignMinMaxPreferences)
    bpy.utils.register_class(BRM_UVAlignMinMaxUp)
    bpy.utils.register_class(BRM_UVAlignMinMaxDown)
    bpy.utils.register_class(BRM_UVAlignMinMaxLeft)
    bpy.utils.register_class(BRM_UVAlignMinMaxRight)
    bpy.utils.register_class(BRM_UVAlignMinMaxPanel)
    
def unregister():
    bpy.utils.unregister_class(BRM_UVAlignMinMaxPreferences)
    bpy.utils.unregister_class(BRM_UVAlignMinMaxUp)
    bpy.utils.unregister_class(BRM_UVAlignMinMaxDown)
    bpy.utils.unregister_class(BRM_UVAlignMinMaxLeft)
    bpy.utils.unregister_class(BRM_UVAlignMinMaxRight)
    bpy.utils.unregister_class(BRM_UVAlignMinMaxPanel)
    
if __name__ == "__main__":
    register()