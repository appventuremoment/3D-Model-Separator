import os

def separate_grouped_models(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist!!")
        return

    with open(file_path, 'r') as reference_file:
        directory = os.path.dirname(file_path)
        lines = reference_file.readlines()
        group_idx = [index for index, line in enumerate(lines) if line[:2] == 'g ']
        for i in range(len(group_idx) - 1):
            if not os.path.exists(directory + '/separated_models'): os.mkdir(directory + '/separated_models')
            with open(directory + f'/separated_models/model{i+1}.obj', 'w') as model_file:
                inp = "".join([line for index, line in enumerate(lines[:group_idx[i+1]]) if line[0] != 'f' or (index > group_idx[i] and index < group_idx[i + 1])])
                model_file.write(inp)
                model_file.close()
        reference_file.close()
    print("Models separated successfully.")

if __name__ == "__main__":
    file_path = "" 
    # If not overwritten, prompts user to enter file path
    if file_path == '': file_path = input('Enter file path: ')
    separate_grouped_models(file_path)