import json
import bpy
from mathutils import Vector

# https://blender.stackexchange.com/questions/7358/python-performance-with-blender-operators
# https://gifguide2code.com/2017/04/09/python-how-to-code-materials-in-blender-cycles/
def generate_materials(structure):
    colors = structure['colors']
            
    for key, value in colors.items():
        material = bpy.data.materials.get(key)
        if material is None:
            material = bpy.data.materials.new(name=key)
            material.use_nodes = True
            tree = material.node_tree
            
            for node in tree.nodes:
                tree.nodes.remove(node)
                
            material_output = tree.nodes.new(type='ShaderNodeOutputMaterial')
            principled_node = tree.nodes.new(type='ShaderNodeBsdfPrincipled')
            principled_node.location = (-300, 0)
            RGB_node = tree.nodes.new(type='ShaderNodeRGB')
            RGB_node.outputs[0].default_value = value
            RGB_node.location = (-600, 0)
            
            tree.links.new(material_output.inputs['Surface'],
                           principled_node.outputs['BSDF'])
            tree.links.new(principled_node.inputs['Base Color'],
                           RGB_node.outputs['Color'])
            tree.links.new(principled_node.inputs['Base Color'],
                           RGB_node.outputs['Color'])
            
    return

def duplicate_atom(atom, cell_parameters, nx, ny, nz):
  
    print("Duplicating atom...")
  
#    ob = bpy.context.object
    ob = atom
    obs = []
    sce = bpy.context.scene

    for i in range(0, nx):
        for j in range(0, ny):
            for k in range(0, nz):
                if nx == 0 and ny == 0 and nz == 0:
                    continue
                else:
                    copy = ob.copy()
                    copy.location += Vector((i*cell_parameters['a'], j*cell_parameters['b'], k*cell_parameters['c']))
    #                copy.data = copy.data.copy() # also duplicate mesh, remove for linked duplicate
                    obs.append(copy)

    for ob in obs:
        sce.objects.link(ob)

    sce.update() # don't place this in either of the above loops!
    return

def generate_lattice(structure, nx, ny, nz):

    print("Generating lattice...")

    cell_parameters = structure['cell']
            
    for atom in structure['atoms']:
        bpy.ops.mesh.primitive_uv_sphere_add(size=structure['sizes'][atom['element']], location=atom['location'])
#        bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=structure['sizes'][atom['element']]/2, location=atom['location'])
        bpy.context.active_object.data.materials.append(bpy.data.materials.get(atom['element']))
        bpy.ops.object.shade_smooth()
        duplicate_atom(bpy.context.active_object, cell_parameters, nx, ny, nz)

with open("C:/Users/pdmurray/Desktop/peyton/Projects/NiCoO_ElectricalEB/Figures/Renders/NiCoO.json", 'r') as f:
     data = json.load(f)

#generate_materials(data)
generate_lattice(data, 50, 50, 1)


