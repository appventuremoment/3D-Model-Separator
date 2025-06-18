import os

def Rescale_Model(obj_path, obj_scaled_path, scale):  # Might not work when there are other object types, untested
    if not os.path.exists(obj_path):
        print(f"File {obj_path} does not exist!!")
        return

    with (open(obj_path, 'r') as source,
          open(obj_scaled_path, 'w') as target):
        for line in source:
            taget_line = line

            if(line[:2] == 'v '):
                coordinates = [float(coordinate) for coordinate in line.split(' ')[1:]]
                rescaled = [c*scale for c in coordinates]
                rescaled_as_str = " ".join([str(c) for c in rescaled])
                taget_line = f'v {rescaled_as_str}\n'

            target.write(taget_line)
        print('Write done!')
        target.close()
        source.close()

if __name__ == "__main__":
    object_path = ""
    output_path = ""
    scale = 1
    scalePrompt = False

    # If not overwritten, prompts user to enter file paths
    if object_path == '': object_path = input('Enter file path: '); scalePrompt = True
    if output_path == '': output_path = input('Enter output file path: '); scalePrompt = True
    if scalePrompt: object_path = input('Enter object scale: ')

    Rescale_Model(object_path, output_path, scale)