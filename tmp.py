import os
from natsort import natsorted
import json

def merge_txt_files(input_folder, output_file):
    """
    Merge all .txt files in the specified folder into a single file, sorted naturally by filename.

    Parameters:
        input_folder (str): Path to the folder containing .txt files.
        output_file (str): Path to the output file where merged content will be saved.
    """
    with open(output_file, 'w', encoding='utf-8') as outfile:
        files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
        for filename in natsorted(files):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n')  # Ensure each file's content is separated by a newline

# Example usage
# Provide the path to the folder containing your .txt files and the desired output file path.
input_folder = 'tmp2'
output_file = 'tmp2/reranked_output.txt'
merge_txt_files(input_folder, output_file)

