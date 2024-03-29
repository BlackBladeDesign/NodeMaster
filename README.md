# NodeMaster - Node Tree Automation Addon for Blender

- Streamline texture loading based on the selected material's name.
- Automatic Node tree creation with image nodes and custom structures.
- Load/Reload function to load textures to corresponding nodes, and reload at any time when updating textures externally.
- Export node structures in JSON and Import. 
- Image format definition, helpful for testing multiple image formats, I use this mostly for Substance Painter textures with different levels of compression.
- GLTF output, use this to connect ambient occlusion. 
- Suffix definition. If you have exported textures with different suffixes, "base_Color" instead of "Color", for example, edit the suffix to account for this.
- Duplicate image and material cleaning tools. 

![Screenshot 2023-05-17 at 2 55 40 pm](https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/assets/126746830/a475efe8-d9cc-4708-9dfd-d1b26b9e1d1a)

### Installation:
- Download the project as a .ZIP file via the green "<> Code" dropdown.
- In Blender, navigate to add-ons via Edit>Preferences>Addons.
- Click install in the top right of the Preferences addon window, and select the downloaded .ZIP file. 
- Use the Checkbox once installed to enable or disable the addon. 
- Find the NodeMaster panel in the Shader Node Editor, under the options panel listed as a new tab.

The panel for NodeMaster is found in the Shader Node Editor side panel. Access the side panel with the 'N' Key.
## Explained:
#### Load/reload and Set Texture Path
The set texture path button will prompt you to open up your desired texture folder. Since nodemaster loads based on MaterialName+Suffix.format you will want to set the path to the specific texture path for your specific material. For example, if I want to load the set for my "Trim" material, I will set my path to Textures/Trim.

### Apply To
The Apply To setting will determine what materials will load their textures. Whether it loads only the selected material, every material attached to the object, or if it loads texture for every material of every object that is visible in the scene. This is ideal if you have one folder for all textures and materials rather than nested folders for each material. Eg. /Textures/ instead of /Textures/Material1 etc.

### Node Structure Settings
#### Load Image Nodes
This setting will determine whether image texture nodes are created at all.

#### Clear All Nodes
This setting will clear the entire node tree prior to loading - ideal for a clean node structure.

#### Load Image Assets
This setting will determine whether image assets are actually loaded or not.

### Node Structure
Using the dropdown, you can select your base node structure to load on Load/Reload. These structures are found in /Props/NodeStructures.

### Material Settings
Deprecated

### Texture Suffixes
deprecated
### Tools

#### Clean Duplicate Materials
#### Clean Duplicate Images
#### Load Node Tree (JSON)
#### Export Node Tree (Json)
#### Add Custom Property
#### Apply Property
#### Custom Property

## Report Issues: 
https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/issues
## Support NodeMaster and other projects
https://www.paypal.com/donate/?hosted_button_id=X44329R2WEKGS
