from movielens_analytics import Ratings
import pytest


class Tests:
    def __init__(self):
        self.ratings = Ratings('../data/ratings.csv')
        
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

    #def links_tests(self):
