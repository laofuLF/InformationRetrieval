from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import sys


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
                        # match
                        next_word = False
                        found = True
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


# return count score for one file
def get_count_score(file_num, dic, word_list):

    result = 0
    for word in word_list:
        if word in dic.keys():
            word_dic = dic[word]
            if file_num in word_dic.keys():
                result += int(word_dic[file_num][0])
    return result


def get_shortest_distance(l1, l2):
    shortest = sys.maxsize
    for i in range(len(l1)):
        for j in range(len(l2)):
            if abs(int(l1[i])-int(l2[j])) < shortest:
                shortest = abs(int(l1[i])-int(l2[j]))
    return 1/shortest


# compare every two adjacent cleaned query words and add to position score
def get_position_score(file_num, dic, query_list):
    position_score = 0
    for i in range(0, len(query_list) - 1):
        word1 = query_list[i]
        word2 = query_list[i + 1]
        if word1 in dic.keys() and word2 in dic.keys():
            dic1 = dic[word1]
            dic2 = dic[word2]
            if file_num in dic1.keys() and file_num in dic2.keys():
                l1 = dic1[file_num]
                l2 = dic2[file_num]
                position_score += get_shortest_distance(l1, l2)
    return position_score


def get_score_rank(files, dic, word_list):
    score_list = {}
    for file in files:
        s = get_position_score(file, dic, word_list) + get_count_score(file, dic, word_list)
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

