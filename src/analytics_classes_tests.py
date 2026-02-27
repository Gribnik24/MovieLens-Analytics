from movielens_analytics import *
import pytest


class Tests:
    def __init__(self):
        self.movies = Movies('../data/movies.csv')
        self.tags = Tags('../data/tags.csv')
        self.ratings = Ratings('../data/ratings.csv')
        self.links = Links(path_to_the_file='../data/links.csv', n=20)

    def movies_tests(self):

        dist_by_release_result = self.movies.dist_by_release()
        assert type(dist_by_release_result).__name__ == 'dict'

        for value in dist_by_release_result.values():
           assert type(value).__name__ == 'int'
        
        values = list(dist_by_release_result.values())
        assert values == sorted(values, reverse=True)

        dist_by_genres_result = self.movies.dist_by_genres()
        assert type(dist_by_genres_result).__name__ == 'dict'

        for value in dist_by_release_result.values():
           assert type(value).__name__ == 'int'

        values = list(dist_by_genres_result.values())
        assert values == sorted(values, reverse=True)


        dist_most_genres = self.movies.most_genres(10)
        assert type(dist_most_genres).__name__ == 'dict'
        assert len(dist_most_genres) == 10

        values = list(dist_most_genres.values())
        assert values == sorted(values, reverse=True)
       
        empty_result = self.movies.most_genres(0)
        assert isinstance(empty_result, dict)
        assert len(empty_result) == 0

    def tags_tests(self):

        for tag_item in self.tags.tags:
            assert 'user_id' in tag_item
            assert 'movie_id' in tag_item
            assert 'tag' in tag_item
            assert 'timestamp' in tag_item

        dist_most_words = self.tags.most_words(10)
        assert type(dist_most_words).__name__ == 'dict'
        assert len(dist_most_words) == 10
   
        for value in dist_most_words.values():
            assert type(value).__name__ == 'int'
  
        values = list(dist_most_words.values())
        assert values == sorted(values, reverse=True)

        list_longest = self.tags.longest(10)
        assert type(list_longest).__name__ == 'list'
        assert len(list_longest) == 10
        for item in list_longest:
            assert type(item).__name__ == 'str'

        lengths = [len(item) for item in list_longest]
        assert lengths == sorted(lengths, reverse=True)

        list_most_words_and_longest = self.tags.most_words_and_longest(10)
        assert type(list_most_words_and_longest).__name__ == 'list'
        assert len(list_most_words_and_longest) <= 10
        for item in list_most_words_and_longest:
            assert type(item).__name__ == 'str'
        assert list_most_words_and_longest == sorted(list_most_words_and_longest)

        dist_most_popular = self.tags.most_popular(10)
        assert type(dist_most_popular).__name__ == 'dict'
        assert len(dist_most_popular) == 10
     
        for value in dist_most_popular.values():
            assert type(value).__name__ == 'int'

        values = list(dist_most_popular.values())
        assert values == sorted(values, reverse=True)

        tags_with_result = self.tags.tags_with("classic")
        assert type(tags_with_result).__name__ == 'list'
        for item in tags_with_result:
            assert type(item).__name__ == 'str'
        assert tags_with_result == sorted(tags_with_result)
            
    def ratings_tests(self):
        
        assert self.ratings.find_title_by_id('1') == 'Toy Story (1995)'
        assert self.ratings.find_title_by_id('4654') == 'Road House (1989)'  
        
        dict_dist_by_year = self.ratings.dist_by_year()
        assert type(dict_dist_by_year).__name__ == 'dict'
        assert type(dict_dist_by_year[2001]).__name__ == 'int'
        assert list(dict_dist_by_year.keys()) == sorted(dict_dist_by_year.keys())

        dict_dist_by_rating = self.ratings.dist_by_rating()
        assert type(dict_dist_by_rating).__name__ == 'dict'
        assert type(dict_dist_by_rating[4]).__name__ == 'int'
        assert list(dict_dist_by_rating.keys()) == sorted(dict_dist_by_rating.keys())
        
        dict_top_by_num_of_ratings = self.ratings.top_by_num_of_ratings(10)
        assert type(dict_top_by_num_of_ratings).__name__ == 'dict'
        assert list(dict_top_by_num_of_ratings.values()) == sorted(dict_top_by_num_of_ratings.values(), reverse=True)
    
        dict_top_by_ratings = self.ratings.top_by_ratings(10)
        assert type(dict_top_by_ratings).__name__ == 'dict'
        assert list(dict_top_by_ratings.values()) == sorted(dict_top_by_ratings.values(), reverse=True)
        
        dict_top_controversial = self.ratings.top_controversial(n=10)
        assert type(dict_top_controversial).__name__ == 'dict'
        assert list(dict_top_controversial.values()) == sorted(dict_top_controversial.values(), reverse=True)

    def links_tests(self):
        assert type(self.links.links_csv).__name__ == 'list'
        assert len(self.links.links_csv) != 0

        imdb_movie_id = list(map(lambda x: x[1], self.links.links_csv))
        movie_headers = ['title', 'year', 'age rating', 'duration',
                         'director', 'writers', 'main actors', 'release date'
                         'origins', 'languages', 'filming locations', 'production companies',
                         'budget', 'gross_domestics', 'opening weekend domestics', 'worldwide grosses']
        self.links.get_imdb(imdb_movie_id, movie_headers)
        assert type(self.links.current_imdb_info).__name__ == 'list'
        assert type(self.links.current_headers_info).__name__ == 'list'

        dict_top_directors = self.links.top_directors(10)
        assert type(dict_top_directors).__name__ == 'dict'
        assert list(dict_top_directors.values()) == sorted(dict_top_directors.values(), reverse=True)

        dict_most_expensive = self.links.most_expensive(10)
        assert type(dict_most_expensive).__name__ == 'dict'
        assert list(dict_most_expensive.values()) == sorted(dict_most_expensive.values(), reverse=True)

        dict_most_profitable = self.links.most_profitable(10)
        assert type(dict_most_profitable).__name__ == 'dict'
        assert list(dict_most_profitable.values()) == sorted(dict_most_profitable.values(), reverse=True)

        dict_longest = self.links.longest(10)
        assert type(dict_longest).__name__ == 'dict'
        assert list(dict_longest.values()) == sorted(dict_longest.values(), reverse=True)

        dict_top_cost_per_minute = self.links.top_cost_per_minute(10)
        assert type(dict_top_cost_per_minute).__name__ == 'dict'
        assert list(dict_top_cost_per_minute.values()) == sorted(dict_top_cost_per_minute.values(), reverse=True)
