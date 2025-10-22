# FlexShape

Blender utility plugin to create armature, lattice and surface deformation shapekeys across multiple meshes at once.

## Installation

1. Download the latest release from the [latest release](https://github.com/Aistify/FlexShape/releases/latest).
2. In Blender, go to **Edit → Preferences → Add-ons → Install from Disk...**
3. Find and select the downloaded zip file, then click **Install from Disk**
4. Enable the add-on by clicking the checkbox. It should be listed as **FlexShape**

If you've done this successfully, you will now see **FlexShape** on the sidebar in the **3D Viewport** (Press `N` to
toggle the sidebar)

## Usage

### Armature Workflow

**Single Operation**:

1. Set Source Armature in the "Source" field
2. Select Target Armature(s)
3. Click "Copy Relations to Selection" and "Copy Transforms to Selection"
4. **(Optional)** Enter a shapekey name in the "Name" field (If no name is set Source Armature name is used)
5. Click "Save (Selection)" for selected objects or "Save (Armature Children)" for all child meshes

"Quick Save" will automatically perform steps 3-5 for selected armatures

**Batch Operation**:

1. Select Source Armature(s)
2. Add them to the list using the + icon
3. Select Target Armature(s)
4. Click "Quick Save List" to copy all Source Armature deformations at once

### Lattice Workflow

**Single Operation**:

1. Set Source Lattice in the "Source" field
2. Select Target Mesh(es)
3. Click "Add Lattice to Selection"
4. **(Optional)** Enter a shapekey name in the "Name" field (If no name is set Source Lattice name is used)
5. Click "Save as Shapekey"

"Quick Save" will automatically perform steps 3-5 for selected meshes

**Batch Operation**:

1. Select Source Lattice(s)
2. Add them to the list using the + icon
3. Select Target Mesh(es)
4. Click "Quick Save List" to copy Lattice deformations at once

### Surface Deform Workflow

**Single Operation**:

1. Set Source Mesh in the "Source" field
2. Select Target Mesh(es)
3. Click "Add Surface Deform to Selection"
4. Enter a shapekey name in the "Name" field
5. Modify the Source Mesh
6. Click "Save as Shapekey"

**Batch Operation**:

1. Set Source Mesh in the "Source" field
2. Select Target Mesh(es)
3. Select any shapekeys you want to copy in the list
4. Click "Save Selected Shapekeys to Selection" to copy all selected shapekeys using Surface Deform at once

---

**Note**: It is recommended to remove zero-impact shape keys after any operation to ensure minimum VRAM usage.
Use the **Utils** panel to clean up shape keys with negligible vertex displacement.
