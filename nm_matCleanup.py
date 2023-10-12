import bpy
from bpy.types import Operator

#using an answer from aliasguru at blender.stackexchange.com

class matCleanup(Operator):
    bl_label = "Material Cleanup"
    bl_idname = "node.matcleaner"
    def execute(self, context):
        def replace_material(bad_mat, good_mat):
            bad_mat.user_remap(good_mat)
            bpy.data.materials.remove(bad_mat)
            
            
        def get_duplicate_materials(og_material):
            
            common_name = og_material.name
            
            if common_name[-3:].isnumeric():
                common_name = common_name[:-4]
            
            duplicate_materials = []
            
            for material in bpy.data.materials:
                if material is not og_material:
                    name = material.name
                    if name[-3:].isnumeric() and name[-4] == ".":
                        name = name[:-4]
                    
                    if name == common_name:
                        duplicate_materials.append(material)
            
            text = "{} duplicate materials found"
            print(text.format(len(duplicate_materials)))
            
            return duplicate_materials


        def remove_all_duplicate_materials():
            i = 0
            while i < len(bpy.data.materials):
                
                og_material = bpy.data.materials[i]
                
                print("og material: " + og_material.name)
                
                # get duplicate materials
                duplicate_materials = get_duplicate_materials(og_material)
                
                # replace all duplicates
                for duplicate_material in duplicate_materials:
                    replace_material(duplicate_material, og_material)
                
                # adjust name to no trailing numbers
                if og_material.name[-3:].isnumeric() and og_material.name[-4] == ".":
                    og_material.name = og_material.name[:-4]
                    
                i = i+1
            

        remove_all_duplicate_materials()
        return {'FINISHED'}

class imgCleanup(Operator):
    bl_label = "Image Cleanup"
    bl_idname = "node.imgcleaner"
    
    def execute(self, context):
        
        def replace_image(bad_img, good_img):
            for mat in bpy.data.materials:
                if mat.node_tree:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image == bad_img:
                            node.image = good_img
                            
            for tex in bpy.data.textures:
                if tex.type == 'IMAGE' and tex.image == bad_img:
                    tex.image = good_img
                
            bpy.data.images.remove(bad_img)
            
        def get_duplicate_images(og_image):
            common_name = og_image.name
            
            if common_name[-3:].isnumeric():
                common_name = common_name[:-4]
                
            duplicate_images = []
            
            for image in bpy.data.images:
                if image is not og_image:
                    name = image.name
                    if name[-3:].isnumeric() and name[-4] == ".":
                        name = name[:-4]
                        
                    if name == common_name:
                        duplicate_images.append(image)
            
            text = "{} duplicate images found"
            print(text.format(len(duplicate_images)))
            
            return duplicate_images
        
        def remove_all_duplicate_images():
            i = 0
            while i < len(bpy.data.images):
                og_image = bpy.data.images[i]
                
                print("og image: " + og_image.name)
                
                # get duplicate images
                duplicate_images = get_duplicate_images(og_image)
                
                # replace all duplicates
                for duplicate_image in duplicate_images:
                    replace_image(duplicate_image, og_image)
                
                # adjust name to no trailing numbers
                if og_image.name[-3:].isnumeric() and og_image.name[-4] == ".":
                    og_image.name = og_image.name[:-4]
                    
                i = i+1
            
        remove_all_duplicate_images()
        return {'FINISHED'}
