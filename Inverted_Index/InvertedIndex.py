import os


def process_each_file(path, file_num, prefix, dic):
    f = open(path, mode='r', encoding='utf-8-sig', errors='ignore')
    word_count = 0
    for line in f.readlines():
        line = line.strip('\n')
        line = line.strip()
        for word in line.split():
            if len(word) > 1:
                word_count += 1
                if word[0] == prefix:
                    dic.setdefault(word, {})
                    dic[word].setdefault(file_num, [])
                    dic[word][file_num].append(word_count)
    return dic


def dfs_text_files(path, prefix, index_dict):
    if os.path.isdir(path):
        all_files = os.listdir(path)
        for file_name in all_files:
            if file_name.endswith('.txt'):
                index_dict = process_each_file(path + '/' + file_name, file_name[:5], prefix, index_dict)
            else:
                dfs_text_files(path + '/' + file_name, prefix, index_dict)
    else:
        return


def output_individual_index_file(path, dic, prefix):
    f = open(path, mode='w', encoding='utf-8', errors='ignore')
    line = ''
    l = sorted(dic.keys())
    for key in l:
        if str(key).startswith(prefix):
            line += key + "\n"
            for file_name, position_list in dic[key].items():
                line += '\t' + file_name + ":" + str(len(position_list)) + ":"
                for p in position_list:
                    line += str(p) + ","
                line = line.strip(',') + '\n'
            f.write(line + '\n')
            line = ""
    return




