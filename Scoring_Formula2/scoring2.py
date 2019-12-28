from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import sys
import math


def clean_sentences(line):
    standard_stop_words = set(stopwords.words('english'))
    tokenized_word = word_tokenize(line)
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    cleaned_sentence = ""
    for word in tokenized_word:
        word = word.strip()
        if word not in standard_stop_words and word not in punctuations: # get rid of punctuations and stopword
            cleaned_sentence += stemming(word) + " "
    cleaned_sentence = cleaned_sentence.strip()
    return cleaned_sentence


def stemming(word):
    stemmer = PorterStemmer()
    result = ""
    stemmed_word = stemmer.stem(word)
    for letter in stemmed_word:
        if letter.isalpha():
            result += letter # get rid of digits
    return result


def get_index_info(line):
    dic = {}
    files = []
    l = line.split(" ")
    for word in l:
        if len(word) > 1:
            dic.setdefault(word, {})
            dic[word], nums = get_file_info(word)
            files += nums
    return dic, files


def get_file_info(word):
    prefix = word[0]
    dic = {}
    files = []
    all_files = os.listdir("/Users/RogerF/Desktop/247/Module4/inv-index")
    for file in all_files:
        if prefix in file:
            f = open("/Users/RogerF/Desktop/247/Module4/inv-index" + "/" + file, errors="ignore")
            next_word = True
            found = False
            for line in f.readlines():
                if next_word is True:
                    line = line.strip()
                    if line == word:
                        next_word = False
                        found = True # found the word
                elif line is "\n":
                    next_word = True
                    found = False
                elif found is True:
                    line = line.strip('\n').strip('\t')
                    l = line.split(":")
                    file_num = l[0]
                    word_times = l[1]
                    positions = l[2].split(",")
                    dic.setdefault(file_num, [])
                    dic[file_num].append(word_times)
                    dic[file_num] += positions
                    if file_num not in files:
                        files.append(file_num)
    return dic, files


def get_shortest_distance(l1, l2):
    shortest = sys.maxsize
    for i in range(len(l1)):
        for j in range(len(l2)):
            if abs(int(l1[i])-int(l2[j])) < shortest and abs(int(l1[i])-int(l2[j])) != 0:
                shortest = abs(int(l1[i])-int(l2[j]))
    return 1/shortest


def get_input_vector(l):
    dic = {}
    sum_word = 0
    vector = []
    for i in l:
        sum_word += 1
        dic.setdefault(i, 0)
        dic[i] += 1
    for k, v in dic.items():
        vector.append(v/sum_word)
    return vector


def get_file_vector(file_num, dic, input_list):
    tmp = []
    denominator = 0
    vector = []
    for word in input_list:
        if file_num in dic[word].keys():
            # count: times of word shown in the file
            count = int(dic[word][file_num][0])
        else:
            count = 1
        # nums of files in which the word is shown
        shown_times = len(dic[word].keys())
        result = (math.log2(count)+1)*(math.log2(1001/shown_times))
        tmp.append(result)
    for i in tmp:
        denominator += i**2
    denominator = denominator**0.5
    for i in tmp:
        vector.append(i/denominator)
    return vector


def get_cosine_value(v1, v2):
    numerator = 0
    denominator_v1 = 0
    denominator_v2 = 0
    for i in range(len(v1)):
        numerator += v1[i] * v2[i]
        denominator_v1 = denominator_v1 + v1[i] ** 2
        denominator_v2 = denominator_v2 + v2[i] ** 2
    denominator = (denominator_v1 * denominator_v2) ** 0.5
    return numerator/denominator


def get_position_score(file_num, dic, word_list):
    score_sum = 0
    size = len(word_list)
    for i in range(0, size-1):
        word1 = word_list[i]
        word2 = word_list[i+1]
        if word1 in dic.keys() and word2 in dic.keys():
            dic1 = dic[word1]
            dic2 = dic[word2]
            if file_num in dic1.keys() and file_num in dic2.keys():
                l1 = dic1[file_num]
                l2 = dic2[file_num]
                score_sum += get_shortest_distance(l1, l2)

    if score_sum == 0:
        return 0
    else:
        return score_sum/len(word_list) if score_sum != 0 else 0


def get_score_rank(files, dic, word_list, input_list):
    score_list = {}
    for file in files:
        vector1 = get_file_vector(file, dic, input_list)
        vector2 = get_input_vector(input_list)
        s = get_position_score(file, dic, word_list) + get_cosine_value(vector1, vector2)
        score_list[file] = s
    sorted_result = sorted(score_list.items(), key=lambda kv: kv[1])
    sorted_result.reverse()
    top_10_result = sorted_result[:10]
    return top_10_result


def get_result_path(file_name):
    result = ""
    for i in range(len(file_name)-1):
        result += file_name[i] + '/'
    result += file_name
    return result
