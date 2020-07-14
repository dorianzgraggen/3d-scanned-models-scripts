import bpy, sys, string, os

meshlabserver = "D:/Software2/VCG/MeshLab/meshlabserver.exe"
filterscript = "D:/3D Scanning/Scripts/01/Meshlab/Reduce_0.5_6T.mlx"
tempFolder = '____meow' # must be a folder that doesn't exist yet, will be deleted at the end of the script
steps = 9 # how many times you want to reduce the mesh
moveX = -0.1
mesh_name = "Nectarine_01"

def makeReadable(n):
    if n < 1000:
        result = str(n)
    else:
        result = str(round(n / 1000)) + "K"
    return result

def main():
    if len(bpy.context.selected_objects) != 1:
        print("Select one single mesh")
        return

    blend_file_path = bpy.data.filepath
    directory = os.path.dirname(blend_file_path)
    original_material = bpy.context.active_object.data.materials[0]

    # EXPORT THE SELECTED FILE
    export_path = os.path.join(directory, tempFolder)
    print(export_path)

    try:
        os.mkdir(export_path)
    except OSError:
        print ("Creation of the directory %s failed" % export_path)
    else:
        print ("Successfully created the directory %s " % export_path)

    target_file = os.path.join(export_path, 'original.obj')
    bpy.ops.export_scene.obj(filepath = target_file, use_selection = True, use_materials = True)


    inputfile = target_file.replace("\\","/")


    # Run the meshlabserver
    for i in range(steps):
        if i != 0:
            inputfile = outputfile # Use the most recent output as the new input mesh
        outputfile = os.path.join(export_path, 'output_' + str(i) + '.obj').replace("\\","/")
        
        command = meshlabserver + ' -i "' + inputfile +  '" -o "' + outputfile + '" -m vc fq wt -s "' + filterscript + '"'

        print()
        print()
        print("Started reducing mesh number " + str(i + 1) + "/" + str(steps))
        print(command)
        os.system(command)
        print("Finished reducing mesh") 
        print()

    # Import all generated meshes
    for i in range(steps):
        importfile = os.path.join(export_path, 'output_' + str(i) + '.obj').replace("\\","/")
        bpy.ops.import_scene.obj(filepath = importfile)

        bpy.ops.transform.translate(value=(moveX * (i + 1), 0, 0))
        bpy.ops.object.shade_smooth()
        current_mesh = bpy.context.selected_objects[0]
        current_mesh.data.materials[0] = original_material
        polygons_num = len(current_mesh.data.polygons)
        
        current_mesh.name = mesh_name + "_" + makeReadable(polygons_num)
        
        
main()