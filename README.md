Streamline and automate texture and node creation in blender. 
Once enabled, find the NodeMaster panel in the Shader Editor, under the options panel listed as a new tab.
![Nodemaster](https://user-images.githubusercontent.com/126746830/236106941-168c7fbd-fbbc-43ce-8d19-f44f1b198716.png)

- Streamlined texture loading based on selected material's name.
- Node tree creation (Currently offering two structures, more coming soon)
- Load/Reload function to load textures to corresponding nodes, and reload at any time when updating textures externally.
- Image format definition, helpful for testing multiple image formats, I use this mostly for Substance Painter textures with different levels of compression.
- GLTF output, use this to connect ambient occlusion. 
- Suffix definition. If you have exported textures with different suffixs, "base_Color" instead of "Color", for example, edit the suffix to account for this.

To be added:
- Node tree exports to JSON, to support custom structures, potentially imports too. Undecided on whether this will be accessed via File>Export/Import or from the NodeMaster panel in Shader Editor.
- Dynamic Structure list, to handle custom structures, these will be added to a folder in documents, Ideally.
- Add checkboxes for texture coordinantes, mapping, displacement, etc.
