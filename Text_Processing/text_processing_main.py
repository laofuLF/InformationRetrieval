import os
import processing


def text_processing(input_file_path, output_file_name):
    if os.path.isdir(input_file_path):
        all_files = os.listdir(input_file_path)
        for file_name in all_files:
            if file_name.endswith('.txt'):
                processing.output_files(input_file_path + '/' + file_name, output_file_name)
                print(file_name + " is processed")
            else:
                text_processing(input_file_path + '/' + file_name, output_file_name)
    else:
        return


if __name__ == '__main__':
    input_path = "/Users/RogerF/Desktop/247/Module2/input-files/aleph.gutenberg.org/1"
    output_folder_name = "input-transform2"
    print("start processing documents...")
    text_processing(input_path, output_folder_name)
