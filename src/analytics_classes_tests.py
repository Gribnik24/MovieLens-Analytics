from movielens_analytics import *
import pytest


class Tests:
    def __init__(self):
        self.ratings = Ratings('../data/ratings.csv')
        self.links = Links('data/links.csv')
        
    def ratings_tests(self):
        assert len(self.ratings.ratings_csv) == 1000 # Checking the ratings_csv containing 1000 rows
        
        assert self.ratings.find_title_by_id('1') == 'Toy Story (1995)'
        assert self.ratings.find_title_by_id('4654') == 'Road House (1989)'
        with pytest.raises(TypeError):
            self.ratings.find_title_by_id()    
        
        dict_dist_by_year = self.ratings.Movies(self.ratings).dist_by_year()
        assert type(dict_dist_by_year).__name__ == 'dict'
        assert type(dict_dist_by_year[2001]).__name__ == 'int'
        assert list(dict_dist_by_year.keys()) == sorted(dict_dist_by_year.keys())

        dict_dist_by_rating = self.ratings.Movies(self.ratings).dist_by_rating()
        assert type(dict_dist_by_rating).__name__ == 'dict'
        assert type(dict_dist_by_rating[4]).__name__ == 'int'
        assert list(dict_dist_by_rating.keys()) == sorted(dict_dist_by_rating.keys())
        
        dict_top_by_num_of_ratings = self.ratings.Movies(self.ratings).top_by_num_of_ratings(10)
        assert type(dict_top_by_num_of_ratings).__name__ == 'dict'
        assert list(dict_top_by_num_of_ratings.values()) == sorted(dict_top_by_num_of_ratings.values(), reverse=True)
        with pytest.raises(TypeError):
            self.ratings.Movies.top_by_num_of_ratings()
    
        dict_top_by_ratings = self.ratings.Movies(self.ratings).top_by_ratings(10)
        assert type(dict_top_by_ratings).__name__ == 'dict'
        assert list(dict_top_by_ratings.values()) == sorted(dict_top_by_ratings.values(), reverse=True)
        with pytest.raises(TypeError):
            self.ratings.Movies.top_by_ratings()
        
        dict_top_controversial = self.ratings.Movies(self.ratings).top_controversial(10)
        assert type(dict_top_controversial).__name__ == 'dict'
        assert list(dict_top_controversial.values()) == sorted(dict_top_controversial.values(), reverse=True)
        with pytest.raises(TypeError):
            self.ratings.Movies.top_controversial()
        
        dict_dist_by_rating = self.ratings.Users(self.ratings).dist_by_rating()
        assert type(dict_dist_by_rating).__name__ == 'dict'
        assert type(dict_dist_by_rating['1']).__name__ == 'int'
        assert list(dict_dist_by_rating.keys()) == sorted(dict_dist_by_rating.keys())
        
        dict_top_by_ratings = self.ratings.Users(self.ratings).top_by_ratings(10)
        assert type(dict_top_by_ratings).__name__ == 'dict'
        assert list(dict_top_by_ratings.values()) == sorted(dict_top_by_ratings.values(), reverse=True)
        with pytest.raises(TypeError):
            self.ratings.Users.top_by_ratings()
        
        dict_top_controversial = self.ratings.Users(self.ratings).top_controversial(10)
        assert type(dict_top_controversial).__name__ == 'dict'
        assert list(dict_top_controversial.values()) == sorted(dict_top_controversial.values(), reverse=True)
        with pytest.raises(TypeError):
            self.ratings.Users.top_controversial()

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
