from datetime import datetime
from collections import Counter


class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        self.ratings_csv = []
        self.movies_csv = []
        self.import_data_ratings(path_to_the_file)
        self.import_data_movies(path_to_the_file.replace('ratings.csv', 'movies.csv'))

    def import_data_ratings(self, path):
        """
        Import data from ratings.csv and transform it into list.
        Where each line of list is an list with cells values
        """
        with open(path) as file:
            next(file)
            for line in file:
                current_row = line.strip().split(',')
                current_row[2] = float(current_row[2]) # rating
                current_row[3] = int(current_row[3]) # timestamp
                self.ratings_csv.append(current_row)
    
    def import_data_movies(self, path):
        """
        Import data from movies.csv and transform it into list.
        Where each line of list is an list with cells values
        """
        with open(path) as file:
            next(file)
            for line in file:
                parts = line.strip().split(',')
                movie_id = parts[0]
                title = ','.join(parts[1:-1])
                genres = parts[-1]
                self.movies_csv.append([movie_id, title, genres])

    def find_title_by_id(self, movie_id):
        """
        Finds movie by its id
        """
        for row in self.movies_csv:
            if row[0] == movie_id:
                return row[1]
        return None

    class Movies:
        def __init__(self, parent):
            self.parent = parent
             
        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sorted by years ascendingly. The years are extracted timestamps.
            """
            timestamps = [row[3] for row in self.parent.ratings_csv]
            years = [datetime.fromtimestamp(ts).year for ts in timestamps]
            ratings_by_year = dict(sorted(Counter(years).items()))
            return ratings_by_year
        
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
            Sorted by ratings ascendingly.
            """
            ratings = [row[2] for row in self.parent.ratings_csv]
            ratings_distribution = dict(sorted(Counter(ratings).items()))
            return ratings_distribution
        
        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sorted by numbers descendingly.
            """
            movie_counts = Counter([row[1] for row in self.parent.ratings_csv])
            top_movies = {}
            for movie_id, count in movie_counts.most_common(n):
                top_movies[self.parent.find_title_by_id(movie_id)] = count
            return top_movies
        
        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sorted by metric descendingly.
            """
            each_id_ratings = {}
            for row in self.parent.ratings_csv:
                movie_id = row[1]
                rating = row[2]
                if movie_id not in each_id_ratings.keys():
                    each_id_ratings[movie_id] = [rating]
                else:
                    each_id_ratings[movie_id].append(rating)

            metric_movies={}      
            if metric == 'median':
                for movie_id, ratings_list in each_id_ratings.items():
                    if (len_ratings_list := len(ratings_list)) % 2 == 0:
                        mid = len_ratings_list // 2
                        metric_movies[self.parent.find_title_by_id(movie_id)] = ratings_list[mid - 1] + ratings_list[mid + 1]
                    else:
                        metric_movies[self.parent.find_title_by_id(movie_id)] = ratings_list[len_ratings_list // 2]
            elif metric == 'average':
                for movie_id, ratings_list in each_id_ratings.items():
                    metric_movies[self.parent.find_title_by_id(movie_id)] = round(sum(ratings_list) / len(ratings_list), 2)
            else:
                raise ValueError('Unknown metric parameter')
            
            top_movies = dict(sorted(metric_movies.items(), key=lambda x: x[1], reverse=True)[:n])
            
            return top_movies
        
        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
            Sorted by variance descendingly.
            """
            def find_variance(ratings_list):
                mean = sum(ratings_list) / (len_ratings_list := len(ratings_list))
                var_numerator = 0
                for rating in ratings_list:
                    var_numerator += (rating - mean)**2
                return round(var_numerator / len_ratings_list, 2)

            each_id_ratings = {}
            for row in self.parent.ratings_csv:
                movie_id = row[1]
                rating = row[2]
                if movie_id not in each_id_ratings.keys():
                    each_id_ratings[movie_id] = [rating]
                else:
                    each_id_ratings[movie_id].append(rating)
            
            movies_with_variance = {movie_id: find_variance(ratings_list) for movie_id, ratings_list in each_id_ratings.items()}
            top_movies = dict(sorted(movies_with_variance.items(), key=lambda x: x[1], reverse=True)[:n])

            return top_movies

    class Users(Movies):
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are users' id and the values are counts.
            Sorted by ratings ascendingly.
            """
            ratings = [row[0] for row in self.parent.ratings_csv]
            ratings_distribution = dict(sorted(Counter(ratings).items()))
            return ratings_distribution
        
        def top_by_ratings(self, n, metric='average'):
            """
            The method returns top-n users by the average or median of the ratings.
            It is a dict where the keys are users' id and the values are metric values.
            Sorted by metric descendingly.
            """
            each_id_ratings = {}
            for row in self.parent.ratings_csv:
                user_id = row[0]
                rating = row[2]
                if user_id not in each_id_ratings.keys():
                    each_id_ratings[user_id] = [rating]
                else:
                    each_id_ratings[user_id].append(rating)

            metric_users={}      
            if metric == 'median':
                for user_id, ratings_list in each_id_ratings.items():
                    if (len_ratings_list := len(ratings_list)) % 2 == 0:
                        mid = len_ratings_list // 2
                        metric_users[user_id] = ratings_list[mid - 1] + ratings_list[mid + 1]
                    else:
                        metric_users[user_id] = ratings_list[len_ratings_list // 2]
            elif metric == 'average':
                for user_id, ratings_list in each_id_ratings.items():
                    metric_users[user_id] = round(sum(ratings_list) / len(ratings_list), 2)
            else:
                raise ValueError('Unknown metric parameter')
            
            top_users = dict(sorted(metric_users.items(), key=lambda x: x[1], reverse=True)[:n])
            
            return top_users
  
        def top_controversial(self, n):
            """
            The method returns top-n users by the variance of the ratings.
            It is a dict where the keys are users' id and the values are the variances.
            Sorted by variance descendingly.
            """
            def find_variance(ratings_list):
                mean = sum(ratings_list) / (len_ratings_list := len(ratings_list))
                var_numerator = 0
                for rating in ratings_list:
                    var_numerator += (rating - mean)**2
                return round(var_numerator / len_ratings_list, 2)

            each_id_ratings = {}
            for row in self.parent.ratings_csv:
                user_id = row[0]
                rating = row[2]
                if user_id not in each_id_ratings.keys():
                    each_id_ratings[user_id] = [rating]
                else:
                    each_id_ratings[user_id].append(rating)
            
            movies_with_variance = {user_id: find_variance(ratings_list) for user_id, ratings_list in each_id_ratings.items()}
            top_users = dict(sorted(movies_with_variance.items(), key=lambda x: x[1], reverse=True)[:n])

            return top_users