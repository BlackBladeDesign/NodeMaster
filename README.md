Find the NodeMaster panel in the Shader Node Editor, under the options panel listed as a new tab.
- Streamlined texture loading based on selected material's name.
- Node tree creation (Currently offering two structures, more coming soon)
- Load/Reload function to load textures to corresponding nodes, and reload at any time when updating textures externally.
- Image format definition, helpful for testing multiple image formats, I use this mostly for Substance Painter textures with different levels of compression.
- GLTF output, use this to connect ambient occlusion. 
- Suffix definition. If you have exported textures with different suffixs, "base_Color" instead of "Color", for example, edit the suffix to account for this.

![Nodemaster](https://user-images.githubusercontent.com/126746830/236106941-168c7fbd-fbbc-43ce-8d19-f44f1b198716.png)

**Installation:**
- Download project as a .ZIP file via the green "<> Code" dropdown.
- In Blender, navigate to add-ons via Edit>Preferences>Addons.
- Click install in the top right of the Preferences addon window, and select the downloaded .ZIP file. 
- Use the Checkbox once installed to enable or disable the addon. 
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
