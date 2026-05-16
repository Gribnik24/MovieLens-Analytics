from datetime import datetime
from collections import Counter
import requests
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO, filename="../logs.log",filemode="w")

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        self.ratings_csv = []
        self.movies_csv = []
        self._import_data_ratings(path_to_the_file)
        self._import_data_movies(path_to_the_file.replace('ratings.csv', 'movies.csv'))

    def _import_data_ratings(self, path: str):
        """
        Import data from ratings.csv and transform it into list.
        Where each line of list is an list with cells values
        """
        logging.debug('Ratings._import_data_ratings starting.')
        try:
            with open(path) as file:
                next(file)
                for line in file:
                    current_row = line.strip().split(',')
                    current_row[2] = float(current_row[2]) # rating
                    current_row[3] = int(current_row[3]) # timestamp
                    self.ratings_csv.append(current_row)
                    logging.debug(f'{current_row} was added to self.ratings_csv.')
            logging.info('ratings.csv import in Ratings class was done successfully.')
        except Exception as e:
            logging.error(f'Error in function Ratings._import_data_rating: {e}.')
            raise ValueError(e)
        
    
    def _import_data_movies(self, path: str):
        """
        Import data from movies.csv and transform it into list.
        Where each line of list is an list with cells values
        """
        logging.debug('Ratings._import_data_movies starting.')
        try:
            with open(path) as file:
                next(file)
                for line in file:
                    parts = line.strip().split(',')
                    movie_id = parts[0]
                    title = ','.join(parts[1:-1])
                    genres = parts[-1]
                    self.movies_csv.append([movie_id, title, genres])
                    logging.debug(f'{movie_id}, {title}, {genres} was added to self.movies_csv.')
            logging.info('movies.csv import in Ratings class was done successfully.')
        except Exception as e:
            logging.error(f'Error in function Ratings._import_data_movies: {e}.')
            raise ValueError(e)

    def find_title_by_id(self, movie_id: str) -> List[str | None]:
        """
        Finds movie by its id
        """
        logging.debug(f'Starting Ratings.find_title_by_id for finding title for {movie_id} id')
        for row in self.movies_csv:
            if row[0] == movie_id:
                title = row[1]
                logging.info(f'The movie title for id {movie_id} was found successfully: {title}.')
                return title
        logging.warning(f'Failed to find movie title for id {movie_id}.')
        return None
             
    def dist_by_year(self):
        """
        The method returns a dict where the keys are years and the values are counts. 
        Sorted by years ascendingly. The years are extracted timestamps.
        """
        logging.info(f'Ratings.dist_by_year starting.')
        try:
            timestamps = [row[3] for row in self.ratings_csv]
            logging.debug('Timestamps were parsed successfully')
            years = [datetime.fromtimestamp(ts).year for ts in timestamps]
            logging.debug('Years were allocated successfully')
            ratings_by_year = dict(sorted(Counter(years).items()))
            logging.info('Distrbution was created successfully')
        except Exception as e:
            logging.error(f'Failed to create distribution. Error message: {e}')
            raise ValueError(e)
        logging.info('The result dict was created successfully')
        return ratings_by_year
    
    def dist_by_rating(self, key: str = 'ratings') -> Dict:
        """
        The method returns a dict where the keys are ratings or users (depends on "key" param) 
        and the values are counts. Sorted by ratings ascendingly.
        """
        logging.info('Starting Ratings.dist_by_rating')
        try:
            if key.lower() == 'ratings':
                target_key = [row[2] for row in self.ratings_csv]
                logging.debug('Ratings were successfully allocated')
            elif key.lower() == 'users':
                target_key = [row[0] for row in self.ratings_csv]
                logging.debug('Users were successfully allocated')
            else:
                logging.error(f"Exception raising. Inappropriate 'key' parameter was given: {key}")
                raise ValueError('Unknown parameter for key. Insert "ratings" or "users"')
            ratings_distribution = dict(sorted(Counter(target_key).items()))
            logging.info('Distribution was created successfully')
        except Exception as e:
            logging.error(f'Failed to create distribution. Error message: {e}')
            raise ValueError(e)
        logging.info('The result dict was created successfully')
        return ratings_distribution
    
    def top_by_num_of_ratings(self, n: int = 10) -> Dict:
        """
        The method returns top-n movies by the number of ratings. 
        It is a dict where the keys are movie titles and the values are numbers.
        Sorted by numbers descendingly.
        """
        logging.info('Starting Ratings.top_by_num_of_ratings')
        try:
            movie_counts = Counter([row[1] for row in self.ratings_csv])
            logging.debug('Counter was successfully created')
            top_movies = {}
            for movie_id, count in movie_counts.most_common(n):
                top_movies[self.find_title_by_id(movie_id)] = count
            logging.debug(f'Top {n} movies dict was successfully created')
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        logging.info('The result dict was created successfully')
        return top_movies
    
    def top_by_ratings(self, n: int = 10, key: str = 'movies', metric: str = 'average') -> Dict:
        """
        The method returns top-n movies or users (depends on "key" param) by the average or median of the ratings.
        It is a dict where the keys are movie titles and the values are metric values.
        Sorted by metric descendingly.
        """
        logging.info('Starting Ratings.top_by_num_of_ratings')
        try:
            each_id_ratings = {}
            if key.lower() == 'movies':
                logging.debug('Starting creating a movies id dict')
                for row in self.ratings_csv:
                    movie_id = row[1]
                    rating = row[2]
                    if movie_id not in each_id_ratings.keys():
                        each_id_ratings[movie_id] = [rating]
                    else:
                        each_id_ratings[movie_id].append(rating)
                logging.debug('Creating was successfully finished')
                    
            elif key.lower() == 'users':
                logging.debug('Starting creating a users id dict')
                for row in self.ratings_csv:
                    user_id = row[0]
                    rating = row[2]
                    if user_id not in each_id_ratings.keys():
                        each_id_ratings[user_id] = [rating]
                    else:
                        each_id_ratings[user_id].append(rating)
                logging.debug('Creating was successfully finished')
            else:
                logging.error('Unknown parameter for key was in the method')
                raise ValueError('Unknown parameter for key. Insert "movies" or "users"')  

            metric_movies = {}      
            if metric == 'median':
                if key.lower() == 'movies':
                    logging.debug('Started finding the median for movies data')
                    for movie_id, ratings_list in each_id_ratings.items():
                        # Sort ratings for median calculation
                        sorted_ratings = sorted(ratings_list)
                        length = len(sorted_ratings)
                        
                        if length % 2 == 0:  # Even length
                            mid = length // 2
                            # Average of two middle numbers
                            median_value = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
                        else:  # Odd length
                            median_value = sorted_ratings[length // 2]
                        
                        metric_movies[self.find_title_by_id(movie_id)] = round(median_value, 2)
                    logging.debug('The median for movies data was found successfully')
                else:
                    logging.debug('Started finding the median for user data')
                    for user_id, ratings_list in each_id_ratings.items():
                        # Sort ratings for median calculation
                        sorted_ratings = sorted(ratings_list)
                        length = len(sorted_ratings)
                        
                        if length % 2 == 0:  # Even length
                            mid = length // 2
                            # Average of two middle numbers
                            median_value = (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
                        else:  # Odd length
                            median_value = sorted_ratings[length // 2]
                        
                        metric_movies[user_id] = round(median_value, 2)
                    logging.debug('The median for movies data was found successfully')
                        
            elif metric == 'average':
                logging.info('Started finding the average for movies data')
                if key.lower() == 'movies':
                    for movie_id, ratings_list in each_id_ratings.items():
                        metric_movies[self.find_title_by_id(movie_id)] = round(sum(ratings_list) / len(ratings_list), 2)
                    logging.debug('The average for movies data was found successfully')
                else:
                    logging.debug('Started finding the average for user data')
                    for user_id, ratings_list in each_id_ratings.items():
                        metric_movies[user_id] = round(sum(ratings_list) / len(ratings_list), 2)
                    logging.debug('The average for user data was found successfully')
                        
            else:
                raise ValueError('Unknown metric parameter')
            
            top_movies = dict(sorted(metric_movies.items(), key=lambda x: (-x[1], x[0]))[:n])
            logging.info('The result dict was created successfully')
            
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)

        return top_movies
    
    def top_controversial(self, key: str = 'movies', n: int = 10) -> Dict:
        """
        The method returns top-n movies or users (depends on "key" param) by the variance of the ratings.
        It is a dict where the keys are movie titles and the values are the variances.
        Sorted by variance descendingly.
        """
        
        logging.info('Starting Ratings.top_controversial')
        try:
            def find_variance(ratings_list):
                mean = sum(ratings_list) / (len_ratings_list := len(ratings_list))
                var_numerator = 0
                for rating in ratings_list:
                    var_numerator += (rating - mean)**2
                return round(var_numerator / len_ratings_list, 2)

            each_id_ratings = {}
            if key.lower() == 'movies':
                logging.debug('Started finding the variance for movies data')
                for row in self.ratings_csv:
                    movie_id = row[1]
                    rating = row[2]
                    if movie_id not in each_id_ratings.keys():
                        each_id_ratings[movie_id] = [rating]
                    else:
                        each_id_ratings[movie_id].append(rating)
                movies_with_variance = {self.find_title_by_id(movie_id): find_variance(ratings_list) for movie_id, ratings_list in each_id_ratings.items()}
                top_movies = dict(sorted(movies_with_variance.items(), key=lambda x: (-x[1], x[0]))[:n])
                logging.debug('The controversal for movies data was found successfully')
                logging.info('The result dict was created successfully')
                           
            elif key.lower() == 'users':
                logging.debug('Started finding the variance for users data')
                for row in self.ratings_csv:
                    user_id = row[0]
                    rating = row[2]
                    if user_id not in each_id_ratings.keys():
                        each_id_ratings[user_id] = [rating]
                    else:
                        each_id_ratings[user_id].append(rating)
                users_with_variance = {user_id: find_variance(ratings_list) for user_id, ratings_list in each_id_ratings.items()}
                top_movies = dict(sorted(users_with_variance.items(), key=lambda x: (-x[1], x[0]))[:n])
                logging.debug('The controversal for movies data was found successfully')
                logging.info('The result dict was created successfully')            
            
            else:
                logging.error('Unknown key parameter in method.')
                raise ValueError('Unknown parameter for key. Insert "movies" or "users"')     
            
            movies_with_variance = {movie_id: find_variance(ratings_list) for movie_id, ratings_list in each_id_ratings.items()}
            top_movies = dict(sorted(movies_with_variance.items(), key=lambda x: (-x[1], x[0]))[:n])
        
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)

        return top_movies
        

class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file:str, n: List[int | None] = None):
        self.current_imdb_info = []
        self.current_headers_info = []
        self.links_csv = []
        self._import_data_links(path_to_the_file, n)
    
    def _import_data_links(self, path: str, n: List[int | None] = None):
        """
        Import data from links.csv and transform it into array.
        Where each line of array is an array with cells values
        """
        logging.debug('Links._import_data_links method starting')
        try:
            with open(path) as file:
                next(file)
                
                if n is None:
                    # Read all remaining lines
                    for line in file:
                        self.links_csv.append(line.strip().split(','))
                        logging.debug(f'{line} was added to self.ratings_csv.')
                else:
                    # Read exactly n lines
                    for i in range(n):
                        line = file.readline()
                        if not line:  # EOF reached
                            break
                        self.links_csv.append(line.strip().split(','))
                        logging.debug(f'{line} was added to self.ratings_csv.')
            logging.info('links.csv import in Links class was done successfully.')
        except Exception as e:
            logging.warning(f'Error in function Links._import_data_links: {e}.')
            raise ValueError(e)
    
    @staticmethod
    def _fetch_movie(imdb_id) -> Dict:
        """
        Method for finding information about movie through IMDb API
        """
        url = "https://api.graphql.imdb.com/"

        query = """
        query GetMovieData($id: ID!) {
            title(id: $id) {
                
                # MAIN FIELDS
                titleText { text }
                titleGenres { genres { genre { text } } }
                releaseDate { day month year }
                runtime { seconds }
                ratingsSummary {aggregateRating voteCount}
                
                # CREDITS
                DIRECTORS: credits(first: 5, filter: { categories: ["director"] }) {
                    edges { node { name { nameText { text } } } } }
                WRITERS: credits(first: 5, filter: { categories: ["writer"] }) {
                    edges { node { name { nameText { text } } } } }
                CAST: credits(first: 5, filter: { categories: ["actor", "actress"] }) {
                    edges { node { name { nameText { text } } } } }
                
                # GROSS AND BUDGET
                productionBudget { budget { amount } }
                lifetimeGross(boxOfficeArea: WORLDWIDE) { total { amount } }
            }
        }
        """
        
        payload = {"query": query, "variables": {"id": imdb_id}}

        try:
            r = requests.post(url, json=payload, timeout=10)
            r.raise_for_status()
        except requests.RequestException:
            logging.error('Can not get the response from https://api.graphql.imdb.com/.')
            return None

        data = r.json().get("data", {}).get("title", {})
        if not data:
            logging.error('The response is empty.')
            return None

        # MAIN FIELDS
        try:
            title = data.get("titleText", {}).get("text", None)
            logging.info(f'The name of the movie is {title}')
        except Exception as e:
            logging.warning(f"Can not find the title for movie_id {imdb_id}: {e}")
            title = None
        try:
            genres = []
            for section in data.get("titleGenres", []).get("genres", []):
                genres.append(section.get("genre", {}).get("text"))
        except Exception as e:
            logging.warning(f"Can not find the genres for movie_id {imdb_id}: {e}")
            genres = []
        try:
            release_year = data.get("releaseDate", {}).get("year")
        except Exception as e:
            logging.warning(f"Can not find the release_year for movie_id {imdb_id}: {e}")
            release_year = None
        try:
            runtime = data.get("runtime", {}).get("seconds", 0) // 60
        except Exception as e:
            logging.warning(f"Can not find the runtime for movie_id {imdb_id}: {e}")
            runtime = 0
        try:
            rating = data.get("ratingsSummary", {}).get("aggregateRating", None)
        except Exception as e:
            logging.warning(f"Can not find the rating for movie_id {imdb_id}: {e}")
            rating = None
        try:
            rated_count = data.get("ratingsSummary", {}).get("voteCount", None)
        except Exception as e:
            logging.warning(f"Can not find the rated_count for movie_id {imdb_id}: {e}")
            rated_count = None
        
        # CREDITS
        try:
            directors = []
            for director in data.get("DIRECTORS", {}).get("edges", {}):
                directors.append(director.get("node", {}).get("name", {}).get("nameText", {}).get("text", None))
        except Exception as e:
            logging.warning(f"Can not find the directors for movie_id {imdb_id}: {e}")
            directors = []
        try:
            writers = []
            for writer in data.get("WRITERS", {}).get("edges", {}):
                writers.append(writer.get("node", {}).get("name", {}).get("nameText", {}).get("text", None))
        except Exception as e:
            logging.warning(f"Can not find the writers for movie_id {imdb_id}: {e}")
            writers = []
        try:
            cast = []
            for actor in data.get("CAST", {}).get("edges", {}):
                cast.append(actor.get("node", {}).get("name", {}).get("nameText", {}).get("text", None))
        except Exception as e:
            logging.warning(f"Can not find the cast for movie_id {imdb_id}: {e}")
            cast = []
            
        # GROSS AND BUDGET
        try:
            budget = data.get("productionBudget", {}).get("budget", {}).get("amount", None)
        except Exception as e:
            logging.warning(f"Can not find the budget for movie_id {imdb_id}: {e}")
            budget = None
        try:
            gross = data.get("lifetimeGross", {}).get("total", {}).get("amount", None)
        except Exception as e:
            logging.warning(f"Can not find the gross for movie_id {imdb_id}: {e}")
            gross = None
                    
        return {
            "imdb_id": imdb_id,
            "title": title,
            "genres": genres,
            "release_year": release_year,
            "runtime": runtime,
            "rating": rating,
            "rated_count": rated_count,
            "directors": directors,
            "writers": writers,
            "cast": cast,
            "budget": budget,
            "gross": gross,
        }
    
    def get_imdb(self, list_of_movies: List, list_of_fields: List):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...]
        for the list of movies given as the argument (movieId)
        and a list of fields containing movie info (list_of_fileds).
        For example, [movieId, directors, budget].
        The values are parsed from the IMDB webpages of the movies.
        Sorted by movieId descendingly.
        
        Appropriate movie info fileds:
        "imdb_id", "title", "genres", "release_year", "runtime", "rating",
        "rated_count", "directors", "writers", "cast", "budget", "gross"
        """

        self.current_imdb_info = []
        self.current_headers_info = [field.strip().lower() for field in list_of_fields]
        
        for movie_id in list_of_movies:
            logging.info(f'Started the movie_id tt{movie_id} proccessing.')
            movie_dict = self._fetch_movie('tt' + movie_id)
            
            current_movie_info = [movie_dict['imdb_id'].lstrip('tt')]
            for field in self.current_headers_info:
                if field in movie_dict.keys():
                    current_movie_info.append(movie_dict[field])
                else:
                    logging.warning(f'There is no filed "{field}" in movie_id {movie_id}')
            
            logging.info(f'Adding the current movie info the all movies info list.')
            self.current_imdb_info.append(current_movie_info)
            
        self.current_imdb_info.sort(reverse=True, key=lambda x: x[0])

    def top_directors(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        logging.info('Starting Links.top_directors')
        try:
            if not self.current_headers_info:
                logging.error('There is no movie headers for starting this method.')
                raise ValueError('The movie headers info is empty. Run get_imdb method first')
            
            director_field_index = None
            for index, field in enumerate(self.current_headers_info):
                if field == 'directors':
                    director_field_index = index
            if director_field_index is None:
                logging.error('There is no director field in movies data.')
                raise ValueError('There is no director field in movies data.')
            
            all_directors = []
            for film in self.current_imdb_info:
                directors_data = film[director_field_index]
                if isinstance(directors_data, list):
                    all_directors.extend(directors_data)
                elif directors_data:
                    all_directors.append(directors_data) 
            directors = dict(Counter(all_directors).most_common(n))
            logging.info('The result dict was created successfully')
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)

        return directors
        
    def most_expensive(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        logging.info('Starting Links.most_expensive')
        try:
            if not self.current_headers_info:
                logging.error('There is no movie headers for starting this method.')
                raise ValueError('The movie headers info is empty. Run get_imdb method first')
            
            title_field_index, budget_field_index = None, None
            for index, field in enumerate(self.current_headers_info):
                if field == 'title':
                    title_field_index = index
                elif field == 'budget':
                    budget_field_index = index
            
            if title_field_index is None:
                logging.error('There is no title field in movies data.')
                raise ValueError('There is no title field in movies data!')
            if budget_field_index is None:
                logging.error('There is no budget field in movies data.')
                raise ValueError('There is no budget field in movies data!')

            # Add +1 when accessing data to account for movie_id at position 0
            valid_movies = []
            for film in self.current_imdb_info:
                # Check if both title and budget exist and budget is not None and > 0
                if (film[title_field_index + 1] is not None and 
                    film[budget_field_index + 1] is not None and
                    film[budget_field_index + 1] > 0):  # Only include movies with actual budget
                    valid_movies.append(film)
            
            # Sort by budget (with +1 offset)
            sorted_movies = sorted(valid_movies,
                                key=lambda x: x[budget_field_index + 1],
                                reverse=True)
            
            # Create result dict with title (with +1 offset) and budget (with +1 offset)
            budgets = {film[title_field_index + 1]: film[budget_field_index + 1] for film in sorted_movies[:n]}
            logging.info('The result dict was created successfully')
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        return budgets
        
    def most_profitable(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        logging.info('Starting Links.most_expensive')
        try:
            if not self.current_headers_info:
                logging.error('There is no movie headers for starting this method.')
                raise ValueError('The movie headers info is empty. Run get_imdb method first')
            
            title_field_index, budget_field_index, cum_world_gross_index = None, None, None
            for index, field in enumerate(self.current_headers_info):
                if field == 'title':
                    title_field_index = index
                elif field == 'budget':
                    budget_field_index = index
                elif field == 'gross':
                    cum_world_gross_index = index
            
            if title_field_index is None:
                logging.error('There is no title field in movies data.')
                raise ValueError('There is no title field in movies data!')
            if budget_field_index is None:
                logging.error('There is no budget field in movies data.')
                raise ValueError('There is no budget field in movies data!')
            if cum_world_gross_index is None:
                logging.error('There is no cumulative world gross field in movies data.')
                raise ValueError('There is no cumulative world gross field in movies data!')
            
            # Add +1 when accessing data to account for movie_id at position 0
            valid_movies = []
            for film in self.current_imdb_info:
                # Check if all required fields exist and are valid
                if (film[title_field_index + 1] is not None and 
                    film[budget_field_index + 1] is not None and
                    film[cum_world_gross_index + 1] is not None and
                    film[budget_field_index + 1] > 0 and  # Budget should be positive
                    film[cum_world_gross_index + 1] > 0):  # Gross should be positive
                    valid_movies.append(film)
            
            # Calculate profit and sort (with +1 offsets)
            movies_with_profit = []
            for film in valid_movies:
                profit = film[cum_world_gross_index + 1] - film[budget_field_index + 1]
                movies_with_profit.append((film, profit))
            
            # Sort by profit descending
            sorted_movies = sorted(movies_with_profit, key=lambda x: (-x[1], x[0]))
            
            # Create result dict with title (with +1 offset) and profit
            profits = {film[title_field_index + 1]: profit for film, profit in sorted_movies[:n]}
            logging.info('The result dict was created successfully')
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)

        return profits
        
    def longest(self, n: int = 10) -> Dict:
        logging.info('Starting Links.longest')
        try:
            if not self.current_headers_info:
                logging.error('There is no movie headers for starting this method.')
                raise ValueError('The movie headers info is empty. Run get_imdb method first')
            
            title_field_index, duration_index = None, None
            for index, field in enumerate(self.current_headers_info):
                if field == 'title':
                    title_field_index = index
                elif field == 'runtime':
                    duration_index = index
                    
            if title_field_index is None:
                logging.error('There is no title field in movies data.')
                raise ValueError('There is no title field in movies data!')
            if duration_index is None:
                logging.error('There is no duration field in movies data.')
                raise ValueError('There is no duration field in movies data!')
            
            # Add +1 when accessing data!
            valid_movies = []
            for film in self.current_imdb_info:
                if film[title_field_index + 1] is not None and film[duration_index + 1] is not None:
                    valid_movies.append(film)
            
            sorted_movies = sorted(valid_movies, 
                                key=lambda x: x[duration_index + 1], 
                                reverse=True)
            
            
            runtimes = {film[title_field_index + 1]: film[duration_index + 1] for film in sorted_movies[:n]}
            logging.info('The result dict was created successfully')
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        return runtimes
        
    def top_cost_per_minute(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        logging.info('Starting Links.top_cost_per_minute')
        try:
            if not self.current_headers_info:
                logging.error('There is no movie headers for starting this method.')
                raise ValueError('The movie headers info is empty. Run get_imdb method first')
            
            title_field_index, budget_field_index, duration_index = None, None, None
            for index, field in enumerate(self.current_headers_info):
                if field == 'title':
                    title_field_index = index
                elif field == 'budget':
                    budget_field_index = index
                elif field == 'runtime':
                    duration_index = index
            
            if title_field_index is None:
                logging.error('There is no title field in movies data.')
                raise ValueError('There is no title field in movies data!')
            if budget_field_index is None:
                logging.error('There is no budget field in movies data.')
                raise ValueError('There is no budget field in movies data!')
            if duration_index is None:
                logging.error('There is no duration field in movies data.')
                raise ValueError('There is no duration field in movies data!')
            
            # Add +1 when accessing data to account for movie_id at position 0
            valid_movies = []
            for film in self.current_imdb_info:
                # Check if all required fields exist and are valid
                if (film[title_field_index + 1] is not None and 
                    film[budget_field_index + 1] is not None and
                    film[duration_index + 1] is not None and
                    film[budget_field_index + 1] > 0 and  # Budget should be positive
                    film[duration_index + 1] > 0):  # Duration should be positive
                    valid_movies.append(film)
            
            # Calculate cost per minute and sort (with +1 offsets)
            movies_with_cost_per_minute = []
            for film in valid_movies:
                cost_per_minute = film[budget_field_index + 1] / film[duration_index + 1]
                movies_with_cost_per_minute.append((film, cost_per_minute))
            
            # Sort by cost per minute descending
            sorted_movies = sorted(movies_with_cost_per_minute, key=lambda x: (-x[1], x[0]))
            
            # Create result dict with title (with +1 offset) and rounded cost per minute
            costs = {film[title_field_index + 1]: round(cost_per_minute, 2) for film, cost_per_minute in sorted_movies[:n]}
            logging.info('The result dict was created successfully')
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)            
        return costs


class Movies:
    """
    Analyzing data from movies.csv
    """
    def __init__(self, path_to_the_file):
        self.movies_csv = []
        self._import_data_movies(path_to_the_file)
    
    def _import_data_movies(self, path: str):
        """
        Import data from movies.csv and transform it into list.
        Where each line of list is an list with cells values
        """
        logging.debug('Movies._import_data_movies starting.')
        try:
            with open(path, encoding='UTF-8') as file:
                next(file)
                for line in file:
                    parts = line.strip().split(',')
                    movie_id = parts[0]
                    title = ','.join(parts[1:-1])
                    genres = parts[-1]
                    self.movies_csv.append([movie_id, title, genres])
        except Exception as e:
            logging.error(f'Error in function Movies._import_data_movies: {e}.')
            raise ValueError(e)

            
    def dist_by_release(self) -> Dict:
        """
        The method returns a dict where the keys are years and the values are counts. 
        The years are extracted from the titles. Sorted by counts descendingly.
        """
        logging.debug('Movies.dist_by_release starting.')
        def year_extractor(title):
            try:
                year = title.split()[-1].strip('()')
            except Exception:
                year = None
                logging.warning(f'Can not parse year for incoming: {title}. Returning None.')
            return year
        try:
            movie_titles = [row[1] for row in self.movies_csv]
            years = list(map(lambda x: year_extractor(x), movie_titles))
            release_years = dict(sorted(Counter(years).items(), key=lambda x: (-x[1], x[0])))
        except Exception as e:
            logging.error(f'Failed to create distribution. Error message: {e}')
            raise ValueError(e)  
        logging.info('The result dict was created successfully')
                
        return release_years
    
    def dist_by_genres(self) -> Dict:
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sorted by counts descendingly.
        """
        logging.info(f'Movies.dist_by_genres starting.')
        try:
            movie_genres = list(map(lambda x: x.split('|'), [row[2] for row in self.movies_csv]))
            genres = {}
            
            for movie in movie_genres:
                for genre in movie:
                    if genre not in genres.keys():
                        genres[genre] = 1
                    else:
                        genres[genre] += 1
            genres = dict(sorted(genres.items(), key=lambda x: (-x[1], x[0])))
        except Exception as e:
            logging.error(f'Failed to create distribution. Error message: {e}')
            raise ValueError(e)   
        logging.info('The result dict was created successfully')         
        return genres
        
    def most_genres(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sorted by numbers descendingly.
        """
        logging.info(f'Movies.most_genres starting.')
        try:
            movie_titles = [' '.join(row[1].split()[:-1]) for row in self.movies_csv]
            movie_genres_count = [len(row[2].split('|')) for row in self.movies_csv]
            
            movies_dict = {movie_title: genres_count for movie_title, genres_count in zip(movie_titles, movie_genres_count)} 
            movies = dict(sorted(movies_dict.items(), key=lambda x: (-x[1], x[0]))[:n])
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        logging.info('The result dict was created successfully')         
        return movies


class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file):  
        self.tags = []
        self._load_tags(path_to_the_file)  
    
    def _load_tags(self, path_to_the_file):
        logging.debug('Tags._load_tags starting.')
        try:
            with open(path_to_the_file) as file:
                next(file)  

                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        user_id = parts[0]
                        movie_id = parts[1]
                        
                        if len(parts) > 4:
                            tag = ','.join(parts[2:-1])
                        else:
                            tag = parts[2]
                        
                        timestamp = parts[-1]
                        
                        self.tags.append({
                            'user_id': user_id,
                            'movie_id': movie_id,
                            'tag': tag.strip(),
                            'timestamp': timestamp
                        })
                        
        except Exception as e:
            logging.error(f'Error in function Tags._load_tags: {e}.')
            raise ValueError(e)

    def most_words(self, n: int = 10) -> Dict:
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        The duplicates are dropped. Sorted by numbers descendingly.
        """  
        logging.info('Starting Tags.most_words') 
        try:
            word_count = {}
            
            for tag_item in self.tags:
                tag = tag_item['tag']

                words = tag.split()
                num_words = len(words)
                
                if tag not in word_count or num_words > word_count[tag]:
                    word_count[tag] = num_words

            sorted_tags = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
            result = dict(sorted_tags[:n])
            logging.info('The result dict was created successfully')

        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        return result

    def longest(self, n: int = 10) -> List:
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """   
        logging.info('Starting Tags.longest')
        try:
            length_dict = {}
            
            for tag_item in self.tags:
                tag = tag_item['tag']
                tag_length = len(tag)
                
                if tag not in length_dict or tag_length > length_dict[tag]:
                    length_dict[tag] = tag_length
            
            sorted_tags = sorted(length_dict.items(), key=lambda x: (-x[1], x[0]))
            
            result = [tag for tag, _ in sorted_tags[:n]]
            logging.info('The result list was created successfully')
            
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        
        return result

    def most_words_and_longest(self, n: int = 10) -> List:
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        The duplicates are dropped. It is a list of the tags.
        """ 
        logging.info('Starting Tags.most_words_and_longest')   
        try:
            word_count = {}
            for tag_item in self.tags:
                tag = tag_item['tag']
                num_words = len(tag.split())
                if tag not in word_count or num_words > word_count[tag]:
                    word_count[tag] = num_words
            
            top_words = set([tag for tag, _ in sorted(word_count.items(), key=lambda x: (-x[1], x[0]))[:n]])
            

            length_dict = {}
            for tag_item in self.tags:
                tag = tag_item['tag']
                tag_length = len(tag)
                if tag not in length_dict or tag_length > length_dict[tag]:
                    length_dict[tag] = tag_length
            
            top_longest = set([tag for tag, _ in sorted(length_dict.items(), key=lambda x: (-x[1], x[0]))[:n]])
            

            result = sorted(list(top_words & top_longest))
            logging.info('The result list was created successfully')
            
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        
        return result

    def most_popular(self, n: int = 10) -> Dict:
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        The duplicates are dropped. Sorted by counts descendingly.
        """
        logging.info('Starting Tags.most_popular')       
        try:
            popularity = {}
            
            for tag_item in self.tags:
                tag = tag_item['tag']
                popularity[tag] = popularity.get(tag, 0) + 1
            
            sorted_tags = sorted(popularity.items(), key=lambda x: (-x[1], x[0]))
            
            result = dict(sorted_tags[:n])
            logging.info('The result dict was created successfully')
            
        except Exception as e:
            logging.error(f'Failed return top {n}. Error message: {e}')
            raise ValueError(e)
        
        return result

    def tags_with(self, word: str) -> List:
        """
        The method returns all unique tags that include the word given as the argument.
        The duplicates are dropped. It is a list of the tags. Sorted by tag names alphabetically.
        """  
        logging.info('Starting Tags.tags_with')          
        try:
            matching_tags = set()
            word_lower = word.lower()
            
            for tag_item in self.tags:
                tag = tag_item['tag']
                if word_lower in tag.lower():
                    matching_tags.add(tag)
            
            result = sorted(list(matching_tags))
            logging.info('The result list was created successfully')
            
        except Exception as e:
            logging.error(f'Failed return unique tags with "{word}" inside. Error message: {e}')
            raise ValueError(e)
        
        return result
