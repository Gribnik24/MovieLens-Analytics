from datetime import datetime
from collections import Counter
import requests
from bs4 import BeautifulSoup


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
        

class Links:
    """
    Analyzing data from links.csv
    """
    def __init__(self, path_to_the_file):
        self.links_csv = []
        self.import_data_links(self, path_to_the_file)
    
    def import_data_links(self, path):
        """
        Import data from links.csv and transform it into array.
        Where each line of array is an array with cells values
        """
        with open(path) as file:
            next(file)
            for i in range(1000):
                current_row = file.readline().strip().split(',')
                self.ratings_csv.append(current_row)
    
    def get_imdb(list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...]
        for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values  are parsed from the IMDB webpages of the movies.
        Sorted by movieId descendingly.
        """
        imdb_info = []
        headers = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)', 'Accept': 'text/html'}
        for movie_id in list_of_movies:
            link = f'http://www.imdb.com/title/tt{movie_id}/'
            try:
                response = requests.get(link, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception:
                raise f'Error with connecting to url for movieId: {movie_id}'

            # Upper (black) part of IMDB HTML
            try:
                black_part = soup.find('section', attrs={'data-testid': 'hero-parent'})
            except Exception:
                raise f'Error with parsing upper (black) part for movieId: {movie_id}'
            
            # Lower (white) part of IMDB HTML
            try:
                white_part = soup.find('section', class_='ipc-page-background ipc-page-background--base sc-e1aae3e0-0 kWggHH')
            except Exception:
                raise f'Error with parsing lower (white) part for movieId: {movie_id}'

            # Header part. Includes: title, year, age rating, duration
            rus_title, original_title, year, age_rating, duration = None, None, None, None, None
            header_part = black_part.find('div', class_='sc-af040695-0 iOwuHP')
            rus_title = header_part.find('span', class_="hero__primary-text", attrs={"data-testid": "hero__primary-text"}).text.strip()
            original_title = header_part.find('div', class_="sc-b41e510f-2 jUfqFl baseAlt").text.split(':')[1].strip()
            list_items = header_part.find("ul", class_="ipc-inline-list").find_all('li')
            year = list_items[0].text.strip()
            age_rating = list_items[1].text.strip()
            duration = list_items[2].text.strip()
            
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

            converted_list_of_fields = [field.strip().lower() for field in list_of_fields]
            current_move_info = [movie_id]
            for field in converted_list_of_fields:
                if field in ('original_title', 'title', 'eng_title'):
                    current_move_info.append(original_title)
                elif field == 'year':
                    current_move_info.append(year)
                elif field == 'age_rating':
                    current_move_info.append(age_rating)
                elif field == 'duration':
                    current_move_info.append(duration)
                elif field == 'tags':
                    if len(tags) == 1:
                        current_move_info.append(tags[0])
                    else:
                        current_move_info.append(tags)
                elif field in ('directors', 'director'):
                    if len(directors) == 1:
                        current_move_info.append(directors[0])
                    else:
                        current_move_info.append(directors)
                elif field in ('writers', 'writer'):
                    if len(writers) == 1:
                        current_move_info.append(writers[0])
                    else:
                        current_move_info.append(writers)
                elif field == 'main_actors':
                    if len(main_actors) == 1:
                        current_move_info.append(main_actors[0])
                    else:
                        current_move_info.append(main_actors)
                elif field in ('release_date', 'release_dates'):
                    if len(release_dates) == 1:
                        current_move_info.append(release_dates[0])
                    else:
                        current_move_info.append(release_dates)
                elif field in ('origins', 'origin countries'):
                    if len(origins) == 1:
                        current_move_info.append(origins[0])
                    else:
                        current_move_info.append(origins)
                elif field in ('languages', 'language'):
                    if len(languages) == 1:
                        current_move_info.append(languages[0])
                    else:
                        current_move_info.append(languages)
                elif field == 'filming_locations':
                    if len(filming_locations) == 1:
                        current_move_info.append(filming_locations[0])
                    else:
                        current_move_info.append(filming_locations)
                elif field == ('prod_companies', 'production_companies', 'companies'):
                    if len(prod_companies) == 1:
                        current_move_info.append(prod_companies[0])
                    else:
                        current_move_info.append(prod_companies)
                elif field in ('budgets', 'budget'):
                    if len(budgets) == 1:
                        current_move_info.append(budgets[0])
                    else:
                        current_move_info.append(budgets)
                elif field == 'gross_domestics':
                    if len(gross_domestics) == 1:
                        current_move_info.append(gross_domestics[0])
                    else:
                        current_move_info.append(gross_domestics)
                elif field == 'opening_weekend_domestics':
                    if len(opening_weekend_domestics) == 1:
                        current_move_info.append(opening_weekend_domestics[0])
                    else:
                        current_move_info.append(opening_weekend_domestics)
                elif field in ('cumulative_worldwide_grosses', 'worldwide_grosses'):
                    if len(cumulative_worldwide_grosses) == 1:
                        current_move_info.append(cumulative_worldwide_grosses[0])
                    else:
                        current_move_info.append(cumulative_worldwide_grosses)

            imdb_info.append(current_move_info)
            imdb_info.sort(reverse=True, key=lambda x: x[0])

        return imdb_info
        
    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sorted by numbers descendingly.
        """
        return directors
        
    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sorted by budgets descendingly.
        """
        return budgets
        
    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between cumulative worldwide gross and budget.
        Sorted by the difference descendingly.
        """
        return profits
        
    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. Sorted by runtime descendingly.
        """
        return runtimes
        
    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime.
        The values are rounded to 2 decimals. Sorted by the division descendingly.
        """
        return costs
