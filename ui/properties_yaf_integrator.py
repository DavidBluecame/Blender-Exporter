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
from bpy.types import Panel
from bl_ui.properties_render import RenderButtonsPanel


class YAFA_V3_PT_render(RenderButtonsPanel, Panel):
    bl_label = "Integrator"
    COMPAT_ENGINES = {'YAFA_V3_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "intg_light_method")

        if scene.intg_light_method == "Direct Lighting":
            if scene.intg_use_caustics:
                split = layout.split()
                col = split.column()
                col.prop(scene, "intg_photon_maps_processing")
                if scene.intg_photon_maps_processing == "load" or scene.intg_photon_maps_processing == "reuse-previous":
                    row = layout.row()
                    row.label("If the loaded/reused maps do not match exactly the scene, crashes and/or incorrect renders may happen, USE WITH CARE!", icon="ERROR")
            
            row = layout.row()
            col = row.column(align=True)
            col.prop(scene, "intg_use_caustics", toggle=True)
            if scene.intg_use_caustics:
                col.prop(scene, "intg_caustic_depth")
                col.prop(scene, "intg_photons")
                col.prop(scene, "intg_caustic_radius")
                col.prop(scene, "intg_caustic_mix")

            col = row.column(align=True)
            col.prop(scene, "intg_use_AO", toggle=True)
            if scene.intg_use_AO:
                col.prop(scene, "intg_AO_color")
                col.prop(scene, "intg_AO_samples")
                col.prop(scene, "intg_AO_distance")


        elif scene.intg_light_method == "Photon Mapping":
            row = layout.row()

            row.prop(scene, "intg_bounces")

            if scene.intg_photonmap_enable_diffuse or scene.intg_photonmap_enable_caustics:
                split = layout.split()
                col = split.column()
                col.prop(scene, "intg_photon_maps_processing")
                if scene.intg_photon_maps_processing == "load" or scene.intg_photon_maps_processing == "reuse-previous":
                    row = layout.row()
                    row.label("If the loaded/reused maps do not match exactly the scene, crashes and/or incorrect renders may happen, USE WITH CARE!", icon="ERROR")
                        
            row = layout.row()
            col = row.column(align=True)
            col.prop(scene, "intg_photonmap_enable_diffuse", icon='MOD_PHYSICS', toggle=True)
            if scene.intg_photonmap_enable_diffuse:
                col.prop(scene, "intg_photons")
                col.prop(scene, "intg_diffuse_radius")
                col.prop(scene, "intg_search")

            col = row.column(align=True)
            col.prop(scene, "intg_photonmap_enable_caustics", icon='MOD_PARTICLES', toggle=True)
            if scene.intg_photonmap_enable_caustics:
                col.prop(scene, "intg_cPhotons")
                col.prop(scene, "intg_caustic_radius")
                col.prop(scene, "intg_caustic_mix")

            if scene.intg_photonmap_enable_diffuse:
                row = layout.row()
                row.prop(scene, "intg_final_gather", toggle=True, icon='FORCE_FORCE')

                if scene.intg_final_gather:
                    col = layout.row()
                    col.prop(scene, "intg_fg_bounces")
                    col.prop(scene, "intg_fg_samples")
                    col = layout.row()
                    col.prop(scene, "intg_show_map", toggle=True)
                

        elif scene.intg_light_method == "Pathtracing":
            col = layout.row()
            col.prop(scene, "intg_caustic_method")
                
            col = layout.row()
            if scene.intg_caustic_method in {"Path+Photon", "Photon"}:

                col.prop(scene, "intg_photon_maps_processing")
                if scene.intg_photon_maps_processing == "load" or scene.intg_photon_maps_processing == "reuse-previous":
                    row = layout.row()
                    row.label("If the loaded/reused maps do not match exactly the scene, crashes and/or incorrect renders may happen, USE WITH CARE!", icon="ERROR")

                col.prop(scene, "intg_photons", text="Photons")
                col.prop(scene, "intg_caustic_mix", text="Caus. Mix")
                col = layout.row()
                col.prop(scene, "intg_caustic_depth", text="Caus. Depth")
                col.prop(scene, "intg_caustic_radius", text="Caus. Radius")
                split = layout.split()
                col = split.column()

            col = layout.row()
            col.prop(scene, "intg_path_samples")
            col.prop(scene, "intg_bounces")
            col.prop(scene, "intg_russian_roulette_min_bounces")
            col = layout.row()
            col.prop(scene, "intg_no_recursion")

        elif scene.intg_light_method == "Debug":
            layout.row().prop(scene, "intg_debug_type")
            layout.row().prop(scene, "intg_show_perturbed_normals")

        elif scene.intg_light_method == "SPPM":
            row = layout.row()
            col = row.column()
            col.prop(scene, "intg_photons", text="Photons")
            col.prop(scene, "intg_pass_num")
            col.prop(scene, "intg_bounces", text="Bounces")
            col = row.column()
            col.prop(scene, "intg_times")
            col.prop(scene, "intg_diffuse_radius")
            col.prop(scene, "intg_search")
            col.prop(scene, "intg_pm_ire")

        elif scene.intg_light_method == "Bidirectional":
            col = layout.column()
            col.label("The Bidirectional integrator is UNSTABLE.", icon="ERROR")
            col.label("It might give unexpected and perhaps even incorrect render results.")
            col.label("Use at your own risk.")

if __name__ == "__main__":  # only for live edit.
    import bpy
    bpy.utils.register_module(__name__)
