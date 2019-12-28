from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os


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


def output_files(input_file_path, output_file_name):
    new_path = input_file_path.replace(".txt", "") + '_transformed' + '.txt'
    new_path = new_path.replace("input-files", output_file_name) # output path
    os.makedirs(os.path.dirname(new_path), exist_ok=True) # create output path if not exist

    reader = open(input_file_path, mode='r', encoding='utf-8', errors='ignore')
    writer = open(new_path, mode='w', encoding='utf-8')
    for line in reader.readlines():
        new_line = clean_sentences(line)
        writer.write(new_line + '\n')



