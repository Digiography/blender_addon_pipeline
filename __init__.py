# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
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

bl_info = {
        "name": "DKS Substance Painter",
        "description": "Substance Painter Pipeline",
        "author": "DigiKrafting.Studio",
        "version": (1, 8, 7),
        "blender": (2, 80, 0),
        "location": "Info Toolbar, File -> Import, File -> Export, Menu",
        "wiki_url":    "https://github.com/DigiKrafting/blender_addon_substance_painter/wiki",
        "tracker_url": "https://github.com/DigiKrafting/blender_addon_substance_painter/issues",
        "category": "Import-Export",
}

import bpy

from . import dks_sp

class dks_sp_addon_prefs(bpy.types.AddonPreferences):

        bl_idname = __package__

        option_sp_exe : bpy.props.StringProperty(
                name="Substance Executable",
                subtype='FILE_PATH',
                default="C:\Program Files\Allegorithmic\Substance Painter\Substance Painter.exe",
        )
        option_export_folder : bpy.props.StringProperty(
                name="Export Folder Name",
                default="eXport",
        )
        option_textures_folder : bpy.props.StringProperty(
                name="Textures Folder Name",
                default="Textures",
        )
        option_save_before_export : bpy.props.BoolProperty(
                name="Save Before Export",
                default=True,
        )
        option_display_type : bpy.props.EnumProperty(
                items=[('Buttons', "Buttons", "Use Buttons"),('Menu', "Menu", "Append a Menu to Main Menu"),('Hide', "Import/Export", "Use only Import/Export Menu's"),],
                name="Display Type",
                default='Buttons',
        )
        option_export_type : bpy.props.EnumProperty(
                items=[('obj', "obj", "obj"),('fbx', "fbx", "fbx"),],
                name="Export Type",
                default='fbx',
        )
        option_import_ext : bpy.props.EnumProperty(
                items=[('png', "png", "png"),('jpeg', "jpeg", "jpeg"),('tiff', "tiff", "tiff"),],
                name="Import Extension",
                default='png',
        )
        option_show_sp_toggle : bpy.props.BoolProperty(
                name="SP Buttons Toggle",
                default=True,
        )
        option_show_sp_toggle_state : bpy.props.BoolProperty(
                name="SP Toggle Button State",
                default=False,
        )
        option_relative : bpy.props.BoolProperty(
                name="Relative Paths",
                description="Use Relative Paths for images.",
                default=True
        )
        option_no_new : bpy.props.BoolProperty(
                name="2018.0.1-2018.3.0 Project File Fix",
                description="Exclude from path for SP 2018.0.1-2018.3.0 to avoid it being added to the textures path.",
                default=False
        )
        option_use_height_maps : bpy.props.BoolProperty(
                name="Use Height Maps",
                description="Combines Height and Normal maps using the Bump Node.",
                default=False,
        )
        option_create_materials : bpy.props.BoolProperty(
                name="Create Materials",
                description="Create Material for Mesh if it does not have one.",
                default=True,
        )
        def draw(self, context):

                layout = self.layout

                box=layout.box()
                box.prop(self, 'option_display_type')
                box.prop(self, 'option_sp_exe')
                box.prop(self, 'option_export_type')
                box.prop(self, 'option_import_ext')

                box=layout.box()
                box.prop(self, 'option_export_folder')
                box.prop(self, 'option_textures_folder')
                box.label(text='Automatically created as a sub folder relative to the saved .blend file. * Do NOT include any "\\".',icon='INFO')

                box=layout.box()
                box.prop(self, 'option_show_sp_toggle')
                box.prop(self, 'option_relative')
                box.prop(self, 'option_save_before_export')
                box.prop(self, 'option_create_materials')                
                box.prop(self, 'option_use_height_maps')

                box=layout.box()
                box.prop(self, 'option_no_new')

class dks_sp_menu(bpy.types.Menu):

    bl_label = " Substance Painter"
    bl_idname = "dks_sp.menu"

    def draw(self, context):

        layout = self.layout

        layout.operator(dks_sp.dks_sp_export_scene.bl_idname,icon="EXPORT")
        layout.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text='Substance Painter (Scene)', icon="IMPORT").import_setting = 'scene'

        layout.operator(dks_sp.dks_sp_export_sel.bl_idname,icon="EXPORT")
        layout.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text='Substance Painter (Selected)', icon="IMPORT").import_setting = 'selected'

        layout.operator(dks_sp.dks_sp_export_col.bl_idname,icon="EXPORT")
        layout.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text='Substance Painter (Collection)', icon="IMPORT").import_setting = 'collection'

def dks_sp_draw_menu(self, context):

    self.layout.menu(dks_sp_menu.bl_idname)

def dks_sp_menu_func_export_scene(self, context):

    self.layout.operator(dks_sp.dks_sp_export_scene.bl_idname)

def dks_sp_menu_func_export_sel(self, context):

    self.layout.operator(dks_sp.dks_sp_export_sel.bl_idname)

def dks_sp_menu_func_export_col(self, context):

    self.layout.operator(dks_sp.dks_sp_export_col.bl_idname)

def dks_sp_menu_func_import_col(self, context):

    self.layout.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text='Substance Painter (Collection)').import_setting = 'collection'

def dks_sp_menu_func_import_scene(self, context):

    self.layout.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text='Substance Painter (Scene)').import_setting = 'scene'

def dks_sp_menu_func_import_sel(self, context):

    self.layout.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text='Substance Painter (Selected)').import_setting = 'selected'

def dks_sp_draw_btns(self, context):

    if context.region.alignment != 'RIGHT':

        layout = self.layout
        row = layout.row(align=True)
        sp_lbl="SP:"

        if bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle:

                if bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle_state:
                        row.operator(dks_sp_toggle.bl_idname,text="SP",icon="TRIA_LEFT")
                else:
                        row.operator(dks_sp_toggle.bl_idname,text="SP",icon="TRIA_RIGHT")
                
                sp_lbl=""

        if bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle_state or not bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle:

                row.operator(dks_sp.dks_sp_export_scene.bl_idname,text=sp_lbl+"Scn",icon="EXPORT")
                row.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text=sp_lbl+'Scn',icon="IMPORT").import_setting = 'scene'

                row.operator(dks_sp.dks_sp_export_sel.bl_idname,text=sp_lbl+"Sel",icon="EXPORT")
                row.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text=sp_lbl+'Sel', icon="IMPORT").import_setting = 'selected'

                row.operator(dks_sp.dks_sp_export_col.bl_idname,text=sp_lbl+"Col",icon="EXPORT")
                row.operator(dks_sp.dks_sp_pbr_nodes.bl_idname, text=sp_lbl+'Col', icon="IMPORT").import_setting = 'collection'

class dks_sp_toggle(bpy.types.Operator):

    bl_idname = "dks_sp.toggle"
    bl_label = "SP"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def execute(self, context):

        if not bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle_state:
                bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle_state=True
        else:
                bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle_state=False

        return {'FINISHED'}

classes = (
    dks_sp_addon_prefs,
    dks_sp_toggle,
)

def register():

        from bpy.utils import register_class
        for cls in classes:
                register_class(cls)

        dks_sp.register()

        bpy.types.TOPBAR_MT_file_export.append(dks_sp_menu_func_export_scene)
        bpy.types.TOPBAR_MT_file_import.append(dks_sp_menu_func_import_scene)
        bpy.types.TOPBAR_MT_file_export.append(dks_sp_menu_func_export_sel)
        bpy.types.TOPBAR_MT_file_import.append(dks_sp_menu_func_import_sel)
        bpy.types.TOPBAR_MT_file_export.append(dks_sp_menu_func_export_col)
        bpy.types.TOPBAR_MT_file_import.append(dks_sp_menu_func_import_col)

        bpy.context.preferences.addons[__package__].preferences.option_show_sp_toggle_state=False

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

                bpy.types.TOPBAR_HT_upper_bar.append(dks_sp_draw_btns)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                register_class(dks_sp_menu)
                bpy.types.TOPBAR_MT_editor_menus.append(dks_sp_draw_menu)

def unregister():

        dks_sp.unregister()

        bpy.types.TOPBAR_MT_file_export.remove(dks_sp_menu_func_export_scene)
        bpy.types.TOPBAR_MT_file_import.remove(dks_sp_menu_func_import_scene)
        bpy.types.TOPBAR_MT_file_export.remove(dks_sp_menu_func_export_sel)
        bpy.types.TOPBAR_MT_file_import.remove(dks_sp_menu_func_import_sel)
        bpy.types.TOPBAR_MT_file_export.remove(dks_sp_menu_func_export_col)
        bpy.types.TOPBAR_MT_file_import.remove(dks_sp_menu_func_import_col)

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

                bpy.types.TOPBAR_HT_upper_bar.remove(dks_sp_draw_btns)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                unregister_class(dks_sp_menu)
                bpy.types.TOPBAR_MT_editor_menus.remove(dks_sp_draw_menu)

        from bpy.utils import unregister_class
        for cls in reversed(classes):
                unregister_class(cls)

if __name__ == "__main__":

	register()
