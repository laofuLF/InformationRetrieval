import scoring1


if __name__ == "__main__":
    while True:
        query = input("Your query:\n")
        query_cleaned = scoring1.clean_sentences(query)
        if query_cleaned:
            query_word_list = query_cleaned.split(" ")
            dic, files = scoring1.get_index_info(query_cleaned)
            rank_list = scoring1.get_score_rank(set(files), dic, query_word_list)
            if rank_list:
                print("Top 10 results of your query: " + query + " \n")
                for i in range(len(rank_list)):
                    path = scoring1.get_result_path(rank_list[i][0])
                    print(str(i+1) + '. ' + "aleph.gutenberg.org/" + path)
                print("\n")
            else:
                print("There is no search result of this query\n")
        else:
            print("No results found, type in more specific query and void stop words\n")

