import scoring2 as sc


if __name__ == "__main__":
    while True:
        query = input("Your query:\n")
        query_cleaned = sc.clean_sentences(query) # process query stemming and stop word
        if query_cleaned:
            query_word_list = query_cleaned.split(" ")
            dic, files = sc.get_index_info(query_cleaned)
            rank_list = sc.get_score_rank(set(files), dic, query_word_list, query_word_list)
            if rank_list:
                print("Top 10 results with revised scoring formula of your query: " + query + " is\n")
                for i in range(len(rank_list)):
                    part = sc.get_result_path(rank_list[i][0])
                    print(str(i + 1) + '. ' + "aleph.gutenberg.org/" + part)
                print("/n")
            else:
                print("There is no search result of this query\n")
        else:
            print("No results found, type in more specific query and void stop words")
