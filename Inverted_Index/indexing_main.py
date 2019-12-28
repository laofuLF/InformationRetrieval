import InvertedIndex as helper
import os


# process all index files
if __name__ == '__main__':
    input_file_path = "/Users/RogerF/Desktop/247/Module3/input-transform/aleph.gutenberg.org/1"
    output_path = "/Users/RogerF/Desktop/247/Module3/inv-index2/"
    letters = "abcdefghijklmnopqrstuvwxyz"
    print("start processing... \n")
    for i in range(len(letters)):
        dic = {}
        temp_output_path = output_path + letters[i] + ".txt"
        os.makedirs(os.path.dirname(temp_output_path), exist_ok=True)
        helper.dfs_text_files(input_file_path, letters[i], dic)
        helper.output_individual_index_file(temp_output_path, dic, letters[i])
        print("index file " + letters[i] + ".txt has been processed")
