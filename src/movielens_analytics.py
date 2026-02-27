from datetime import datetime
from collections import Counter
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self, path_to_the_file):
        self.ratings_csv = []
        self.movies_csv = []
        self.import_data_ratings(path_to_the_file)
        self.import_data_movies(path_to_the_file.replace('ratings.csv', 'movies.csv'))

    def _import_data_ratings(self, path: str):
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
    
    def _import_data_movies(self, path: str):
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

    def find_title_by_id(self, movie_id: str) -> List[str | None]:
        """
        Finds movie by its id
        """
        for row in self.movies_csv:
            if row[0] == movie_id:
                return row[1]
        return None
             
    def dist_by_year(self):
        """
        The method returns a dict where the keys are years and the values are counts. 
        Sorted by years ascendingly. The years are extracted timestamps.
        """
        timestamps = [row[3] for row in self.ratings_csv]
        years = [datetime.fromtimestamp(ts).year for ts in timestamps]
        ratings_by_year = dict(sorted(Counter(years).items()))
        return ratings_by_year
    
    def dist_by_rating(self, key: str = 'ratings') -> Dict:
        """
        The method returns a dict where the keys are ratings or users (depends on "key" param) 
        and the values are counts. Sorted by ratings ascendingly.
        """
        if key.lower() == 'ratings':
            ratings = [row[2] for row in self.ratings_csv]
        elif key.lower() == 'users':
            ratings = [row[0] for row in self.ratings_csv]
        else:
            raise ValueError('Unknown parameter for key. Insert "ratings" or "users"')
        ratings_distribution = dict(sorted(Counter(ratings).items()))
        return ratings_distribution
    
    def top_by_num_of_ratings(self, n: int = 10) -> Dict:
        """
        The method returns top-n movies by the number of ratings. 
        It is a dict where the keys are movie titles and the values are numbers.
        Sorted by numbers descendingly.
        """
        movie_counts = Counter([row[1] for row in self.ratings_csv])
        top_movies = {}
        for movie_id, count in movie_counts.most_common(n):
            top_movies[self.find_title_by_id(movie_id)] = count
        return top_movies
    
    def top_by_ratings(self, n: int = 10, key: str = 'movies',metric: str = 'average') -> Dict:
        """
        The method returns top-n movies or users (depends on "key" param) by the average or median of the ratings.
        It is a dict where the keys are movie titles and the values are metric values.
        Sorted by metric descendingly.
        """
        each_id_ratings = {}
        if key.lower() == 'movies':
            for row in self.ratings_csv:
                movie_id = row[1]
                rating = row[2]
                if movie_id not in each_id_ratings.keys():
                    each_id_ratings[movie_id] = [rating]
                else:
                    each_id_ratings[movie_id].append(rating)
        elif key.lower() == 'users':
            for row in self.ratings_csv:
                user_id = row[0]
                rating = row[2]
                if user_id not in each_id_ratings.keys():
                    each_id_ratings[user_id] = [rating]
                else:
                    each_id_ratings[user_id].append(rating)
        else:
            raise ValueError('Unknown parameter for key. Insert "movies" or "users"')  

        metric_movies = {}      
        if metric == 'median':
            if key.lower() == 'movies':
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
            else:
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
                    
        elif metric == 'average':
            if key.lower() == 'movies':
                for movie_id, ratings_list in each_id_ratings.items():
                    metric_movies[self.find_title_by_id(movie_id)] = round(sum(ratings_list) / len(ratings_list), 2)
            else:
                for user_id, ratings_list in each_id_ratings.items():
                    metric_movies[user_id] = round(sum(ratings_list) / len(ratings_list), 2)
                    
        else:
            raise ValueError('Unknown metric parameter')
        
        top_movies = dict(sorted(metric_movies.items(), key=lambda x: x[1], reverse=True)[:n])
        
        return top_movies
    
    def top_controversial(self, key: str = 'movies', n: int = 10) -> Dict:
        """
        The method returns top-n movies or users (depends on "key" param) by the variance of the ratings.
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
        if key.lower() == 'movies':
            for row in self.ratings_csv:
                movie_id = row[1]
                rating = row[2]
                if movie_id not in each_id_ratings.keys():
                    each_id_ratings[movie_id] = [rating]
                else:
                    each_id_ratings[movie_id].append(rating)
            movies_with_variance = {self.find_title_by_id(movie_id): find_variance(ratings_list) for movie_id, ratings_list in each_id_ratings.items()}
            top_movies = dict(sorted(movies_with_variance.items(), key=lambda x: x[1], reverse=True)[:n])
            
        elif key.lower() == 'users':
            for row in self.ratings_csv:
                user_id = row[0]
                rating = row[2]
                if user_id not in each_id_ratings.keys():
                    each_id_ratings[user_id] = [rating]
                else:
                    each_id_ratings[user_id].append(rating)
            users_with_variance = {user_id: find_variance(ratings_list) for user_id, ratings_list in each_id_ratings.items()}
            top_movies = dict(sorted(users_with_variance.items(), key=lambda x: x[1], reverse=True)[:n])            
        
        else:
            raise ValueError('Unknown parameter for key. Insert "movies" or "users"')     
        
        movies_with_variance = {movie_id: find_variance(ratings_list) for movie_id, ratings_list in each_id_ratings.items()}
        top_movies = dict(sorted(movies_with_variance.items(), key=lambda x: x[1], reverse=True)[:n])

        return top_movies
        

class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file):
        self.current_imdb_info = []
        self.current_headers_info = []
        self.links_csv = []
        self.import_data_links(path_to_the_file)
    
    def import_data_links(self, path: str, n: List[int | None] = None):
        """
        Import data from links.csv and transform it into array.
        Where each line of array is an array with cells values
        """
        with open(path) as file:
            next(file)
            
            if n is None:
                # Read all remaining lines
                for line in file:
                    self.links_csv.append(line.strip().split(','))
            else:
                # Read exactly n lines
                for _ in range(n):
                    line = file.readline()
                    if not line:  # EOF reached
                        break
                    self.links_csv.append(line.strip().split(','))
    
    def get_imdb(self, list_of_movies: List, list_of_fields: List):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...]
        for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values  are parsed from the IMDB webpages of the movies.
        Sorted by movieId descendingly.
        """
        def money_converter(money_value: str) -> int:
            """
            Function for parsed money values converting into numeric.
            Deleting '$' sign, commas and additional messages. For example:
            '$93,000,000 (extimated)' --> 93000000
            """
            # Handle None or empty values
            if not money_value:
                return 0
            
            # If it's a list with one element, extract that element
            if isinstance(money_value, list):
                if len(money_value) == 1:
                    money_value = money_value[0]  # Extract the string from the list
                else:
                    # If it's a list with multiple elements, process each one
                    return [money_converter(item) for item in money_value]
            
            # Now money_value should be a string
            if not isinstance(money_value, str):
                return 0
            
            try:
                # deleting probal (estimated) part in budget value. Example: $93,000,000 (estimated)
                if '(' in money_value:
                    money_value = money_value.split('(')[0].strip()
                
                # Remove $ sign and commas, then convert to int
                clean_value = money_value.replace('$', '').replace(',', '').strip()
                return int(clean_value) if clean_value else 0
            except (ValueError, AttributeError):
                return 0
        
        def duration_converter(duration_value: str) -> List[int | None]:
            """
            Function for parsed duration values. Converting into minutes count, numeric.
            Deleting 'h' and 'm' signs. For example:
            '2h 58m' --> 178
            """
            converted_duration = duration_value
            try:
                hours, minutes = converted_duration.split()
                hours = int(hours.rstrip('h'))
                minutes = int(minutes.rstrip('m'))
                return minutes + hours * 60
            except:
                return None

        self.current_imdb_info = []
        self.current_headers_info = [field.strip().lower() for field in list_of_fields]
        headers = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)', 'Accept': 'text/html'}
        for movie_id in list_of_movies:
            link = f'http://www.imdb.com/title/tt{str(movie_id)}/'
            try:
                response = requests.get(link, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception:
                raise Exception(f'Error with connecting to url for movieId: {movie_id}')

            # Upper (black) part of IMDB HTML
            try:
                black_part = soup.find('section', attrs={'data-testid': 'hero-parent'})
            except Exception:
                raise Exception(f'Error with parsing upper (black) part for movieId: {movie_id}')
            
            # Lower (white) part of IMDB HTML
            try:
                white_part = soup.find('section', class_='ipc-page-background ipc-page-background--base sc-e1aae3e0-0 kWggHH')
            except Exception:
                raise f'Error with parsing lower (white) part for movieId: {movie_id}'

            # Header part. Includes: title, year, age rating, duration
            original_title, year, age_rating, duration = None, None, None, None
            header_part = black_part.find('div', class_='sc-af040695-0 iOwuHP')
            original_title = header_part.find('div', class_="sc-b41e510f-2 jUfqFl baseAlt").text.split(':')[1].strip()
            list_items = header_part.find("ul", class_="ipc-inline-list").find_all('li')
            try:
                year = list_items[0].text.strip()
            except:
                Exception
            try:
                age_rating = list_items[1].text.strip()
            except:
                Exception
            try:
                duration = list_items[2].text.strip()
            except:
                Exception
            
            # Tags part
            tags = None
            tags_part = black_part.find('div', class_='ipc-chip-list__scroller')
            tags = [tag.text.strip() for tag in tags_part.find_all('span', class_='ipc-chip__text')]

            # Cast part. Includes: director(s), writers, main actors
            directors, writers, main_actors = None, None, None
            cast_part = black_part.find('div', class_='sc-af040695-2 fLTdiX')
            main_team = cast_part.find_all('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")
            directors_info, writers_info, actors_info = main_team

            directors_list = directors_info.find_all('li', class_="ipc-inline-list__item")
            directors = [director.text.strip() for director in directors_list]

            writers_list = writers_info.find_all('li', class_="ipc-inline-list__item")
            writers = [writer.text.strip() for writer in writers_list]

            actors_list = actors_info.find_all('li', class_="ipc-inline-list__item")
            main_actors = [actor.text.strip() for actor in actors_list]

            # Details block. Contains: release dates, origin countries, origin languages, filming locations, production companies
            release_dates, origins, languages, filming_locations, prod_companies = None, None, None, None, None
            details_part = white_part.find('section', class_=["ipc-page-section", "ipc-page-section--base celwidget"], attrs={"data-testid": "Details"})

            release_date_info = details_part.find(class_="ipc-metadata-list__item ipc-metadata-list__item--align-end ipc-metadata-list-item--link", attrs={"data-testid": "title-details-releasedate"})
            release_dates_list = release_date_info.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
            release_dates = [release_date.text.strip() for release_date in release_dates_list.find_all('li', class_="ipc-inline-list__item")]

            origin_info = details_part.find(class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end", "ipc-metadata-list-item--link"], attrs={"data-testid": "title-details-origin"})
            origins_list = origin_info.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
            origins = [origin.text.strip() for origin in origins_list.find_all('li', class_="ipc-inline-list__item")]

            language_info = details_part.find(class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end", "ipc-metadata-list-item--link"], attrs={"data-testid": "title-details-languages"})
            languages_list = language_info.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
            languages = [language.text.strip() for language in languages_list.find_all('li', class_="ipc-inline-list__item")]

            filming_locations_info = details_part.find(class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end", "ipc-metadata-list-item--link"], attrs={"data-testid": "title-details-filminglocations"})
            filming_locations_list = filming_locations_info.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
            filming_locations = [filming_location.text.strip() for filming_location in filming_locations_list.find_all('li', class_="ipc-inline-list__item")]

            prod_companies_info = details_part.find(class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end", "ipc-metadata-list-item--link"], attrs={"data-testid": "title-details-companies"})
            prod_companies_list = prod_companies_info.find('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base")
            prod_companies = [prod_company.text.strip() for prod_company in prod_companies_list.find_all('li', class_="ipc-inline-list__item")]

            # Box office block. Contains: budgets, gross_domestics, opening_weekend_domestics, cumulative_worldwide_grosses
            budgets, gross_domestics, opening_weekend_domestics, cumulative_worldwide_grosses = None, None, None, None
            box_office_part = white_part.find('div', class_="sc-314065ad-0 hZXevt", attrs={"data-testid": "title-boxoffice-section"})
            try:
                budget_info = box_office_part.find('li', class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end sc-1c0b0ec6-2", "cTBfsm"], attrs={"data-testid": "title-boxoffice-budget"})
                budgets = [budget.text.strip() for budget in budget_info.find_all('li', class_="ipc-inline-list__item")]
            except:
                Exception
            
            try:
                gross_domestic_info = box_office_part.find('li', class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end sc-1c0b0ec6-2", "cTBfsm"], attrs={"data-testid": "title-boxoffice-grossdomestic"})
                gross_domestics = [gross_domestic.text.strip() for gross_domestic in gross_domestic_info.find_all('li', class_="ipc-inline-list__item")]
            except:
                Exception

            try:
                opening_weekend_domestic_info = box_office_part.find('li', class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end sc-1c0b0ec6-2", "cTBfsm"], attrs={"data-testid": "title-boxoffice-openingweekenddomestic"})
                opening_weekend_domestics = [opening_weekend_domestic.text.strip() for opening_weekend_domestic in opening_weekend_domestic_info.find_all('li', class_="ipc-inline-list__item")]
            except:
                Exception

            try:
                cumulative_worldwide_gross_info = box_office_part.find('li', class_=["ipc-metadata-list__item", "ipc-metadata-list__item--align-end sc-1c0b0ec6-2", "cTBfsm"], attrs={"data-testid": "title-boxoffice-cumulativeworldwidegross"})
                cumulative_worldwide_grosses = [cumulative_worldwide_gross.text.strip() for cumulative_worldwide_gross in cumulative_worldwide_gross_info.find_all('li', class_="ipc-inline-list__item")]
            except:
                Exception

            current_movie_info = [movie_id]
            for field in self.current_headers_info:
                if field in ('original_title', 'title', 'eng_title'):
                    if original_title:
                        current_movie_info.append(original_title)
                    else:
                        current_movie_info.append(None)
                elif field == 'year':
                    if year:
                        current_movie_info.append(year)
                    else:
                        current_movie_info.append(None)
                elif field in ('age_rating', 'age rating'):
                    if age_rating:
                        current_movie_info.append(age_rating)
                    else:
                        current_movie_info.append(None)
                elif field in ('duration', 'runtime'):
                    if duration:
                        current_movie_info.append(duration_converter(duration))
                    else:
                        current_movie_info.append(None)
                elif field == 'tags':
                    if tags and len(tags) == 1:
                        current_movie_info.append(tags[0])
                    elif tags:
                        current_movie_info.append(tags)
                    else:
                        current_movie_info.append(None)
                elif field in ('directors', 'director'):
                    if directors and len(directors) == 1:
                        current_movie_info.append(directors[0])
                    elif directors:
                        current_movie_info.append(directors)
                    else:
                        current_movie_info.append(None)
                elif field in ('writers', 'writer'):
                    if writers and len(writers) == 1:
                        current_movie_info.append(writers[0])
                    elif writers:
                        current_movie_info.append(writers)
                    else:
                        current_movie_info.append(None)
                elif field in ('main actors', 'main_actors'):
                    if main_actors and len(main_actors) == 1:
                        current_movie_info.append(main_actors[0])
                    elif main_actors:
                        current_movie_info.append(main_actors)
                    else:
                        current_movie_info.append(None)
                elif field in ('release_date', 'release_dates', 'release date', 'release dates'):
                    if release_dates and len(release_dates) == 1:
                        current_movie_info.append(release_dates[0])
                    elif release_dates:
                        current_movie_info.append(release_dates)
                    else:
                        current_movie_info.append(None)
                elif field in ('origins', 'origin countries'):
                    if origins and len(origins) == 1:
                        current_movie_info.append(origins[0])
                    elif origins:
                        current_movie_info.append(origins)
                    else:
                        current_movie_info.append(None)
                elif field in ('languages', 'language'):
                    if languages and len(languages) == 1:
                        current_movie_info.append(languages[0])
                    elif languages:
                        current_movie_info.append(languages)
                    else:
                        current_movie_info.append(None)
                elif field in ('filming_locations', 'filming locations'):
                    if filming_locations and len(filming_locations) == 1:
                        current_movie_info.append(filming_locations[0])
                    elif filming_locations:
                        current_movie_info.append(filming_locations)
                    else:
                        current_movie_info.append(None)
                elif field == ('prod_companies', 'production_companies', 'production companies', 'companies'):
                    if prod_companies and len(prod_companies) == 1:
                        current_movie_info.append(prod_companies[0])
                    elif prod_companies:
                        current_movie_info.append(prod_companies)
                    else:
                        current_movie_info.append(None)
                elif field in ('budgets', 'budget'):
                    if budgets:
                        current_movie_info.append(money_converter(budgets))
                    else:
                        current_movie_info.append(None)
                elif field == 'gross_domestics':
                    if gross_domestics:
                        current_movie_info.append(money_converter(gross_domestics))
                    else:
                        current_movie_info.append(None)
                elif field in ('opening_weekend_domestics', 'opening weekend domestics'):
                    if opening_weekend_domestics:
                        current_movie_info.append(money_converter(opening_weekend_domestics[0]))
                    else:
                        current_movie_info.append(None)
                elif field in ('cumulative_worldwide_grosses', 'worldwide_grosses', 'cumulative worldwide grosses', 'worldwide grosses'):
                    if cumulative_worldwide_grosses:
                        current_movie_info.append(money_converter(cumulative_worldwide_grosses))
                    else:
                        current_movie_info.append(None)
                else:
                    current_movie_info.append(None)

            self.current_imdb_info.append(current_movie_info)
            
        self.current_imdb_info.sort(reverse=True, key=lambda x: x[0])

        return self.current_imdb_info

    def top_directors(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        if not self.current_headers_info:
            raise ValueError('The movie headers info is empty. Run get_imdb method first')
        
        director_field_index = None
        for index, field in enumerate(self.current_headers_info):
            if field in ('directors', 'director'):
                director_field_index = index
        if director_field_index is None:
            raise ValueError('There is no director field in movies data!')
        
        all_directors = []
        for film in self.current_imdb_info:
            directors_data = film[director_field_index]
            if isinstance(directors_data, list):
                all_directors.extend(directors_data)
            elif directors_data:
                all_directors.append(directors_data) 
        directors = dict(Counter(all_directors).most_common(n))

        return directors
        
    def most_expensive(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        if not self.current_headers_info:
            raise ValueError('The movie headers info is empty. Run get_imdb method first')
        
        title_field_index, budget_field_index = None, None
        for index, field in enumerate(self.current_headers_info):
            if field in ('original_title', 'title', 'eng_title'):
                title_field_index = index
            elif field in ('budgets', 'budget'):
                budget_field_index = index
        
        if title_field_index is None:
            raise ValueError('There is no title field in movies data!')
        if budget_field_index is None:
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
        
        return budgets
        
    def most_profitable(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        if not self.current_headers_info:
            raise ValueError('The movie headers info is empty. Run get_imdb method first')
        
        title_field_index, budget_field_index, cum_world_gross_index = None, None, None
        for index, field in enumerate(self.current_headers_info):
            if field in ('original_title', 'title', 'eng_title'):
                title_field_index = index
            elif field in ('budgets', 'budget'):
                budget_field_index = index
            elif field in ('cumulative_worldwide_grosses', 'worldwide_grosses', 'cumulative worldwide grosses', 'worldwide grosses'):
                cum_world_gross_index = index
        
        if title_field_index is None:
            raise ValueError('There is no title field in movies data!')
        if budget_field_index is None:
            raise ValueError('There is no budget field in movies data!')
        if cum_world_gross_index is None:
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
        sorted_movies = sorted(movies_with_profit,
                               key=lambda x: x[1], 
                               reverse=True)
        
        # Create result dict with title (with +1 offset) and profit
        profits = {film[title_field_index + 1]: profit for film, profit in sorted_movies[:n]}
        
        return profits
        
    def longest(self, n: int = 10) -> Dict:
        if not self.current_headers_info:
            raise ValueError('The movie headers info is empty. Run get_imdb method first')
        
        title_field_index, duration_index = None, None
        for index, field in enumerate(self.current_headers_info):
            if field in ('original_title', 'title', 'eng_title'):
                title_field_index = index
            elif field in ('duration', 'runtime'):
                duration_index = index
        
        # Add +1 when accessing data!
        valid_movies = []
        for film in self.current_imdb_info:
            if film[title_field_index + 1] is not None and film[duration_index + 1] is not None:
                valid_movies.append(film)
        
        sorted_movies = sorted(valid_movies, 
                               key=lambda x: x[duration_index + 1], 
                               reverse=True)
        
        runtimes = {film[title_field_index + 1]: film[duration_index + 1] for film in sorted_movies[:n]}
        return runtimes
        
    def top_cost_per_minute(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        if not self.current_headers_info:
            raise ValueError('The movie headers info is empty. Run get_imdb method first')
        
        title_field_index, budget_field_index, duration_index = None, None, None
        for index, field in enumerate(self.current_headers_info):
            if field in ('original_title', 'title', 'eng_title'):
                title_field_index = index
            elif field in ('budgets', 'budget'):
                budget_field_index = index
            elif field in ('duration', 'runtime'):
                duration_index = index
        
        if title_field_index is None:
            raise ValueError('There is no title field in movies data!')
        if budget_field_index is None:
            raise ValueError('There is no budget field in movies data!')
        if duration_index is None:
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
        sorted_movies = sorted(movies_with_cost_per_minute, 
                               key=lambda x: x[1], 
                               reverse=True)
        
        # Create result dict with title (with +1 offset) and rounded cost per minute
        costs = {film[title_field_index + 1]: round(cost_per_minute, 2) for film, cost_per_minute in sorted_movies[:n]}
        
        return costs


class Movies(Ratings):
    """
    Analyzing data from movies.csv
    """
    def __init__(self):
        Ratings.__init__(self) # for _import_data_movies method inheritance from Ratings class
        
    def dist_by_release(self) -> Dict:
        """
        The method returns a dict where the keys are years and the values are counts. 
        The years are extracted from the titles. Sorted by counts descendingly.
        """
        def year_extractor(title):
            year = title.split()[-1].strip('()')
            return year
            
        movie_titles = [row[1] for row in self.movies_csv]
        years = list(map(lambda x: year_extractor(x), movie_titles))
        release_years = dict(sorted(Counter(years).items(), reverse=True))
        return release_years
    
    def dist_by_genres(self) -> Dict:
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sorted by counts descendingly.
        """
        movie_genres = list(map(lambda x: x.split('|'), [row[2] for row in self.movies_csv]))
        genres = {}
        
        for movie in movie_genres:
            for genre in movie:
                if genre not in genres.keys():
                   genres[genre] = 1
                else:
                   genres[genre] += 1
        genres = dict(sorted(genres.items(), reverse=True))  
                
        return genres
        
    def most_genres(self, n: int = 10) -> Dict:
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sorted by numbers descendingly.
        """
        movie_titles = [row[1].split()[:-1] for row in self.movies_csv]
        movie_genres_count = [len(row[2].split('|')) for row in self.movies_csv]
        
        movies_dict = {movie_title: genres_count for movie_title, genres_count in zip(movie_titles, movie_genres_count)} 
        movies = dict(sorted(movies_dict.items(), reverse=True)[:n])
        
        return movies


class Tags:
    """
    Analyzing data from tags.csv
    """
    def __init__(self, path_to_the_file):  
        self.tags = []
        self._load_tags(path_to_the_file)  
    
    def _load_tags(self, path_to_the_file):
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
                        
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File {path_to_the_file} not found")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")

    def most_words(self, n: int = 10) -> Dict:
        """
        The method returns top-n tags with most words inside. It is a dict 
        where the keys are tags and the values are the number of words inside the tag.
        The duplicates are dropped. Sorted by numbers descendingly.
        """   
        try:
            word_count = {}
            
            for tag_item in self.tags:
                tag = tag_item['tag']

                words = tag.split()
                num_words = len(words)
                
                if tag not in word_count or num_words > word_count[tag]:
                    word_count[tag] = num_words

            sorted_tags = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
            
            result = dict(sorted_tags[:n])
            return result
            
        except Exception as e:
            raise Exception(f"Error in most_words: {e}")

    def longest(self, n: int = 10) -> Dict:
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """            
        try:
            length_dict = {}
            
            for tag_item in self.tags:
                tag = tag_item['tag']
                tag_length = len(tag)
                
                if tag not in length_dict or tag_length > length_dict[tag]:
                    length_dict[tag] = tag_length
            
            sorted_tags = sorted(length_dict.items(), key=lambda x: x[1], reverse=True)
            
            result = [tag for tag, _ in sorted_tags[:n]]
            return result
            
        except Exception as e:
            raise Exception(f"Error in longest: {e}")

    def most_words_and_longest(self, n: int = 10) -> List:
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        The duplicates are dropped. It is a list of the tags.
        """    
        try:
            word_count = {}
            for tag_item in self.tags:
                tag = tag_item['tag']
                num_words = len(tag.split())
                if tag not in word_count or num_words > word_count[tag]:
                    word_count[tag] = num_words
            
            top_words = set([tag for tag, _ in sorted(word_count.items(),key=lambda x: x[1],reverse=True)[:n]])
            

            length_dict = {}
            for tag_item in self.tags:
                tag = tag_item['tag']
                tag_length = len(tag)
                if tag not in length_dict or tag_length > length_dict[tag]:
                    length_dict[tag] = tag_length
            
            top_longest = set([tag for tag, _ in sorted(length_dict.items(),key=lambda x: x[1],reverse=True)[:n]])
            

            result = sorted(list(top_words & top_longest))
            return result
            
        except Exception as e:
            raise Exception(f"Error in most_words_and_longest: {e}")

    def most_popular(self, n: int = 10) -> Dict:
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        The duplicates are dropped. Sorted by counts descendingly.
        """            
        try:
            popularity = {}
            
            for tag_item in self.tags:
                tag = tag_item['tag']
                popularity[tag] = popularity.get(tag, 0) + 1
            
            sorted_tags = sorted(popularity.items(), key=lambda x: x[1], reverse=True)
            
            result = dict(sorted_tags[:n])
            return result
            
        except Exception as e:
            raise Exception(f"Error in most_popular: {e}")

    def tags_with(self, word: str) -> List:
        """
        The method returns all unique tags that include the word given as the argument.
        The duplicates are dropped. It is a list of the tags. Sorted by tag names alphabetically.
        """            
        try:
            matching_tags = set()
            word_lower = word.lower()
            
            for tag_item in self.tags:
                tag = tag_item['tag']
                if word_lower in tag.lower():
                    matching_tags.add(tag)
            
            result = sorted(list(matching_tags))
            return result
            
        except Exception as e:
            raise Exception(f"Error in tags_with: {e}")
