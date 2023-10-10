**NodeMaster - Node Tree Automation Addon for Blender**

- Streamline texture loading based on selected material's name.
- Node tree creation (Currently offering two structures, more coming soon)
- Load/Reload function to load textures to corresponding nodes, and reload at any time when updating textures externally.
- Image format definition, helpful for testing multiple image formats, I use this mostly for Substance Painter textures with different levels of compression.
- GLTF output, use this to connect ambient occlusion. 
- Suffix definition. If you have exported textures with different suffixs, "base_Color" instead of "Color", for example, edit the suffix to account for this.
- Duplicate image and material cleaning tools. 

![Screenshot 2023-05-17 at 2 55 40 pm](https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/assets/126746830/a475efe8-d9cc-4708-9dfd-d1b26b9e1d1a)

**Installation:**
- Download project as a .ZIP file via the green "<> Code" dropdown.
- In Blender, navigate to add-ons via Edit>Preferences>Addons.
- Click install in the top right of the Preferences addon window, and select the downloaded .ZIP file. 
- Use the Checkbox once installed to enable or disable the addon. 
- Find the NodeMaster panel in the Shader Node Editor, under the options panel listed as a new tab.

If any issues persist, please create an issue referencing the bug and how to reproduce via: https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/issues

**How to use:**
- Ensure the texture names match your models material names. For example, if your material is "Handle", make sure your textures are named "Handle_Normal", "Handle_Color" etc.
Nodemaster will use this name to find textures and streamline the loading process for each. 
- Access the shader node editor, and then the option panel with the 'N' key.
- Choose where the node tree will be applied. To all materials on all visible models, to every material attatched to the selected object, or to only the material select.
- Choose the node structure you'd like to use in 'Node Structure Settings'. we'll use the ORM structure for this rundown. 
- Choose whether to add Image Texture Nodes, and then whether those nodes will load image texture assets when you set a path or load/reload. 
- Choose the file type in 'File Settings'.
- In Material Settings, choose whether to add a GLTF/GLB output node, for GLB files. (Note that Tex Co-Ord and Displacement are non functional currently)
- Adjust the suffixes for each texture in 'Texture Suffixes'. Eg. if your texture name in your files is "MaterialName_NormalMap.jpg" instead of MaterialName_Normal.jpg, change the suffix for it to find the file. Same with Color, BaseColor etc.
- Once satisfied with the settings, use the "Set Texture Path" button to find your texture folder. Once you are in the folder, click to load. This will automatically load the textures.
- to reload the textures again - helpful when making changes to textures from substance and re-exporting, simply use the Load/Reload button.

**Tools:**
- Clean Duplicate Materials. (Dangerous, ensure all your unique materials are named correctly and not indexed. This will remove any indexed material.
If you have materials called 'Material', 'Material.001' and 'Material.002', for example, Nodemaster will remove every numbered instance and set all materials using that name to the first 'Material".
- Clean Duplicate Images. This will clean all duplicate instances of texture/image assets. If you have normalMap, normalMap.001, normalMap.002, for example, this will remove the indexed duplicates and use the original on everything. Helpful for large projects that are completed over a long time, or projects with many changes to textures. 


**Exporter known supported nodes (Needs work):**
- Image textures (Does not save path)
- Normal
- Principled BSDF
- Seperate Color
- Material Output

**To be added:**
- Dynamic Structure list, to handle custom structures, these will be added to a folder in documents, Ideally.
- Add checkbox functionality for texture coordinantes, mapping, displacement, etc.
- Custom property mass add tool, for object properties or materials

**Expand Automation with Super Batch Export**
Using some of the current NodeMaster functionality you can add some lines to the Super Batch Export (By MrTripie) addon's __init__.py to automatically load textures for all selected models and export all, 
this is helpful if you have a variety of models with unique textures but using the same material names, so you no longer have to load texture - export - repeat etc. See here where I added the lines:
![Screenshot 2023-10-10 at 4 39 10 pm](https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/assets/126746830/3927cc86-f089-44cc-977a-bcb28b40a635)
![Screenshot 2023-10-10 at 4 39 44 pm](https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/assets/126746830/8aa7da0f-2a89-46cb-af85-4f487e58598f)
We call the texture load from the texture path set in NodeMaster for each object exported using the object name. So "Textures/Object 1" will automatically load etc. 
Then we reset the path at the end of the export function in preparation for the next export.
Lines to use:

In this function: def export_selection(self, itemname, context, base_dir):

Add this at the start of the function: textureFolder = 
            bpy.data.scenes["Scene"].nm_props.texturePath
Add this to the object for loop:    
            tex_dir = textureFolder + '/' + obj.name
            bpy.data.scenes["Scene"].nm_props.texturePath = tex_dir
            bpy.data.scenes["Scene"].nm_props.apply_to = "ALL_ATTACHED"
            bpy.ops.node.autoload()
Add this to the very end of the function: 
            bpy.data.scenes["Scene"].nm_props.texturePath = textureFolder


