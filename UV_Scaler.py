bl_info = {
    "name" : "UV Scaler",
    "author" : "pkjon",
    "version" : (1, 0),
    "blender" : (3, 1, 0),
    "location" : "View3d > UV Scaler",
    "category" : "UV",
    "description" : "Scale in editmode selected UVs by a certain factor."
}

import bpy


class Scalel(bpy.types.Operator):
    bl_idname = "wm.scalel"
    bl_label = "wm scalel"
    
    
    def execute(self, context):
        obj = bpy.context.active_object
        x =  len(bpy.context.object.data.polygons) -1
        scaling = bpy.data.scenes["Scene"].scaling_factor
    
        if bpy.context.active_object.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.hide(unselected=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        while x >= 0:
            obj.data.polygons[x].select = True
            bpy.ops.object.editmode_toggle()
            bpy.ops.uv.select_all(action='SELECT')
            ie = bpy.context.screen.areas[2]
            bpy.ops.transform.resize({"area" : ie}, value=(scaling, scaling, 1),)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.editmode_toggle()
            x -= 1
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='INVERT')
        
        return {'FINISHED'}
        
    

class Panel(bpy.types.Panel):
    bl_label = "UV Scaler"
    bl_idname = "UV_Scaler"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UV Scaler'

    def draw(self, context):
        layout = self.layout
        col = self.layout.column()

        row = layout.row()
        row.operator("wm.scalel", text = 'Scale UVs', icon= 'FULLSCREEN_ENTER')
        row = layout.row()   
        row.label(text="Warning: make a backup", icon='ERROR')
        row = layout.row() 
        row.label(text="of the .blend file incase")
        row = layout.row() 
        row.label(text="something goes wrong.")
        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)
         
        
PROPS = [
    ('scaling_factor', bpy.props.FloatProperty(name='Scaling Factor', description='Factor by wich individual Faces are scaled', default=0.9)),
]

def register():
    bpy.utils.register_class(Panel)
    bpy.utils.register_class(Scalel)
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
def unregister():
    bpy.utils.unregister_class(Panel)
    bpy.utils.unregister_class(Scalel)
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
           
if __name__ == "__main__":
    register()



