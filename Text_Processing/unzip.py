import os
import zipfile


def unzip_single_file(input_zip_path, output_zip_path):
    if zipfile.is_zipfile(input_zip_path):
        file_zipper = zipfile.ZipFile(input_zip_path, 'r')
        for file in file_zipper.namelist():
            file_zipper.extract(file, output_zip_path)


def unzip_all_files(path):
    if os.path.isdir(path):
        all_files = os.listdir(path)
        for file_name in all_files:
            is_zip = zipfile.is_zipfile(path + '/' + file_name)
            if is_zip:
                unzip_single_file(path + '/' + file_name, path)
            else:
                # dfs
                unzip_all_files(path + '/' + file_name)
    else:
        return


# unzip all the zip files in the following path
input_parent_path = "/Users/RogerF/Desktop/247/Module2/input-files/aleph.gutenberg.org/1"
unzip_all_files(input_parent_path)
