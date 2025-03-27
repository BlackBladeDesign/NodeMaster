# NodeMaster - Node Tree Automation Addon for Blender

Support NodeMaster and other projects:  
[Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=X44329R2WEKGS)

## About the Addon

As a full-time GLB modeler, I found myself repeatedly creating the same node structures hundreds of times a day. While it only takes a few minutes to set up the nodes and load the textures, I wanted a faster, more efficient solution. This addon was created to automate that process.

With a single click, you can select your texture folder for the model, and NodeMaster will automatically generate the required Node(s) and load the corresponding textures for each.

A few times I used this in conjunction with the "Batch Exporter GLB/GLTF" addon too in cases where I needed to export 30+ models from the same collection all with the same material/material name to .GLB, but load the textures specifically for each on export. Saved even more time! 

![Mar-27-2025 10-58-24](https://github.com/user-attachments/assets/031cede4-34b3-41f6-920a-6a69605a29c0)

### Key Features:
- **Streamlined Texture Loading**: Load textures based on the material name automatically.
- **Node Tree Creation**: Automatically generates a custom node tree with image nodes and custom structures.
- **Load/Reload Function**: Reload textures into their corresponding nodes and update them when textures are modified externally.
- **Export and Import Node Structures**: Export and import node structures as JSON files for easy reuse.
- **Image Format Definition**: Useful for testing multiple image formats, especially for textures from tools like Substance Painter with different compression levels.
- **GLTF Output**: Supports ambient occlusion for GLTF exports.
- **Suffix Definition**: Adjust suffix definitions to match your texture naming conventions (e.g., "base_Color" instead of "Color").
- **Duplicate Material/Image Cleaning**: Automatically clean up duplicate materials and images (e.g., materials named ".001", ".002", etc.).

![Screenshot](https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/assets/126746830/a475efe8-d9cc-4708-9dfd-d1b26b9e1d1a)

## Installation

1. Download the project as a .ZIP file via the green "<> Code" dropdown on GitHub.
2. In Blender, go to `Edit > Preferences > Add-ons`.
3. Click `Install` in the top-right of the Add-ons window and select the downloaded `.ZIP` file.
4. Enable or disable the addon by checking the box next to it.
5. Once enabled, the NodeMaster panel will appear in the Shader Node Editor under a new tab.

To access the panel, press the **'N'** key to open the side panel in the Shader Node Editor.

## How to Use

### Load/Reload and Set Texture Path

- The **Set Texture Path** button prompts you to select the texture folder for your model.
- NodeMaster loads textures based on the pattern `MaterialName+Suffix.format`, so ensure the path matches the folder for your specific material (e.g., for a "Trim" material, the path might be `Textures/Trim`).

### Apply To Setting

- **Apply To** determines which materials have their textures loaded. You can choose:
  - Only the selected material
  - All materials attached to the active object
  - All materials in the scene (ideal for shared texture folders across multiple materials).

### Node Structure Settings

- **Load Image Nodes**: Enable or disable the creation of image texture nodes in the node tree.
- **Clear All Nodes**: Clears the existing node tree, ensuring a clean slate before loading the new structure.
- **Load Image Assets**: Determines whether image assets are actually loaded into the material or just the nodes.

### Node Structure

- Select your base node structure from the dropdown. These node structures are located in `/Props/NodeStructures`.

### Material Settings

- This section is deprecated and is no longer in use.

### Texture Suffixes

- This feature is deprecated and no longer in use. Refer instead to the SuffixDictionary in Json/SuffixDictionary.JSON

### Tools

- **Clean Duplicate Materials**: Removes duplicate materials (e.g., materials named ".001", ".002", etc.) and consolidates them into the first occurrence.
- **Clean Duplicate Images**: Removes duplicate image textures.
- **Load Node Tree (JSON)**: Load a previously exported node tree from a JSON file.
- **Export Node Tree (JSON)**: Export the current node tree structure as a JSON file for future use.
- **Add Custom Property**: Add custom properties to your node tree.
- **Apply Property**: Apply custom properties to nodes in the tree.
- **Custom Property**: Manage and assign custom properties to your materials or nodes.

## Report Issues

If you encounter any issues or bugs, please report them here:  
[NodeMaster Issues](https://github.com/BlackBladeDesign/NodeMaster---Blender-node-tree-automation-addon/issues)

## Support NodeMaster and Other Projects

If you find this addon helpful, consider supporting its development:  
[Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=X44329R2WEKGS)
