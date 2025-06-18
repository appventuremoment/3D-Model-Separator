import os
import bpy

def exportFromBlender(input_path, output_path): # Used to match the precisions of the 2 files
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.wm.obj_import(filepath=input_path)
    bpy.ops.wm.obj_export(filepath=output_path)

def XOR_Models(model1_path, model2_path, output_path):
    with (open(model1_path, 'r') as model1,
          open(model2_path, 'r') as model2,
          open(output_path, 'w') as output):
        m1lines = model1.readlines()
        m2lines = model2.readlines()
        model1.close(); model2.close()

        # Find all the different relevant object types
        m1v = [line.rstrip() for line in m1lines if line[:2] == "v "]
        m1vt = [line.rstrip() for line in m1lines if line[:3] == "vt "]
        m1vn = [line.rstrip() for line in m1lines if line[:3] == "vn "]
        m1vp = [line.rstrip() for line in m1lines if line[:3] == "vp "]
        m1l = [line.rstrip() for line in m1lines if line[:2] == "l "]
        m1f = [line.rstrip() for line in m1lines if line[:2] == "f "]

        m2v = [line.rstrip() for line in m2lines if line[:2] == "v "]
        m2vt = [line.rstrip() for line in m2lines if line[:3] == "vt "]
        m2vn = [line.rstrip() for line in m2lines if line[:3] == "vn "]
        m2vp = [line.rstrip() for line in m2lines if line[:3] == "vp "]
        m2l = [line.rstrip() for line in m2lines if line[:2] == "l "]
        m2f = [line.rstrip() for line in m2lines if line[:2] == "f "]

        # Indices of overlapping objects in model 1
        v1overlap = [idx + 1 for idx, line in enumerate(m1v) if line in m2v]
        vt1overlap = [idx + 1 for idx, line in enumerate(m1vt) if line in m2vt]
        vn1overlap = [idx + 1 for idx, line in enumerate(m1vn) if line in m2vn]
        vp1overlap = [idx + 1 for idx, line in enumerate(m1vp) if line in m2vp]

        # Append non-overlapping objects in model 1 except those using index references
        output.write("\n".join([line for idx, line in enumerate(m1v) if idx + 1 not in v1overlap]))
        output.write("\n".join([line for idx, line in enumerate(m1vt) if idx + 1 not in vt1overlap]))
        output.write("\n".join([line for idx, line in enumerate(m1vn) if idx + 1 not in vn1overlap]))
        output.write("\n".join([line for idx, line in enumerate(m1vp) if idx + 1 not in vp1overlap]) + "\n")

        # Append face type objects in model 1
        for _, face in enumerate(m1f): 
            nodes = face.split(' ')[1:]
            continueflag = False
            for nodeid, node in enumerate(nodes):
                values = node.split('/')
                # Ignores objects with removed references
                if values[0] in list(map(str, v1overlap)) or values[1] in list(map(str, vt1overlap)): continueflag = True; break
                if len(values) == 3 and values[2] in list(map(str, vn1overlap)): continueflag = True; break
                # Lowers index of each object type by the number of objects of the 
                # same type that has a reference before itself that was removed
                tmpv = (values[0] != '' and str(int(values[0]) - len([1 for overlap in v1overlap if overlap < int(values[0])]))) or ''
                tmpvt = (values[1] != '' and str(int(values[1]) - len([1 for overlap in vt1overlap if overlap < int(values[1])]))) or ''
                tmpvn = (len(values) == 3 and values[2] != '' and str(int(values[2]) - len([1 for overlap in vn1overlap if overlap < int(values[2])]))) or ''
                nodes[nodeid] = len(values) == 3 and f"{tmpv}/{tmpvt}/{tmpvn}" or f"{tmpv}/{tmpvt}"
            
            if continueflag: continue
            else: output.write(f"f {' '.join(nodes)}\n")
        
        # Append polyline type objects in model 1
        for _, line in enumerate(m1l):
            nodes = line.split(' ')[1:]
            continueflag = False
            for nodeid, node in enumerate(nodes):
                # Ignores objects with removed references
                if node in list(map(str, v1overlap)): continueflag = True; break
                # Lowers index by the number of vertices that has a reference before itself that was removed
                tmpv = (node != '' and str(int(node) - len([1 for overlap in v1overlap if overlap < int(node)]))) or ''
                nodes[nodeid] = tmpv
            
            if continueflag: continue
            else: output.write(f"l {' '.join(nodes)}\n")

        # Indices of overlapping objects in model 2
        v2overlap = [idx + 1 for idx, line in enumerate(m2v) if line in m1v]
        vt2overlap = [idx + 1 for idx, line in enumerate(m2vt) if line in m1vt]
        vn2overlap = [idx + 1 for idx, line in enumerate(m2vn) if line in m1vn]
        vp2overlap = [idx + 1 for idx, line in enumerate(m2vp) if line in m1vp]

        # Append non-overlapping objects in model 2 except those using index references
        output.write("\n".join([line for idx, line in enumerate(m2v) if idx + 1 not in v2overlap]))
        output.write("\n".join([line for idx, line in enumerate(m2vt) if idx + 1 not in vt2overlap]))
        output.write("\n".join([line for idx, line in enumerate(m2vn) if idx + 1 not in vn2overlap]))
        output.write("\n".join([line for idx, line in enumerate(m2vp) if idx + 1 not in vp2overlap]) + "\n")

        # Append face type objects in model 2
        for _, face in enumerate(m2f): 
            nodes = face.split(' ')[1:]
            continueflag = False
            for nodeid, node in enumerate(nodes):
                values = node.split('/')
                # Ignores objects with removed references
                if values[0] in list(map(str, v2overlap)) or values[1] in list(map(str, vt2overlap)): continueflag = True; break
                if len(values) == 3 and values[2] in list(map(str, vn2overlap)): continueflag = True; break
                # Lowers index of each object type by the number of objects of the 
                # same type that has a reference before itself that was removed
                tmpv = (values[0] != '' and str(int(values[0]) - len([1 for overlap in v2overlap if overlap < int(values[0])]) + (len(m1v) - len(v1overlap)))) or ''
                tmpvt = (values[1] != '' and str(int(values[1]) - len([1 for overlap in vt2overlap if overlap < int(values[1])]) + (len(m1vt) - len(vt1overlap)))) or ''
                tmpvn = (len(values) == 3 and values[2] != '' and str(int(values[2]) - len([1 for overlap in vn2overlap if overlap < int(values[2])]) + (len(m1vn) - len(vn1overlap)))) or ''
                nodes[nodeid] = len(values) == 3 and f"{tmpv}/{tmpvt}/{tmpvn}" or f"{tmpv}/{tmpvt}"
            
            if continueflag: continue
            else: output.write(f"f {' '.join(nodes)}\n")

        # Append polyline type objects in model 2
        for _, line in enumerate(m2l):
            nodes = line.split(' ')[1:]
            continueflag = False
            for nodeid, node in enumerate(nodes):
                # Ignores objects with removed references
                if node in list(map(str, v2overlap)): continueflag = True; break
                # Lowers index by the number of vertices that has a reference before itself that was removed
                tmpv = (node != '' and str(int(node) - len([1 for overlap in v2overlap if overlap < int(node)]) + (len(m1v) - len(v1overlap)))) or ''
                nodes[nodeid] = tmpv
            
            if continueflag: continue
            else: output.write(f"l {' '.join(nodes)}\n")

        output.close()
        print('Write done!')

if __name__ == "__main__":
    model1_path = ""
    model2_path = ""
    temp_path1 = "temp1.obj"
    temp_path2 = "temp2.obj"
    output_path = ""

    os.system('clear')
    exportFromBlender(model1_path, temp_path1)
    exportFromBlender(model2_path, temp_path2)
    XOR_Models(temp_path1, temp_path2, output_path)
    os.remove(temp_path1)
    os.remove(temp_path2)
    os.remove(f"{temp_path1[:-4]}.mtl")
    os.remove(f"{temp_path2[:-4]}.mtl")