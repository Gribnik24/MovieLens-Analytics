# MovieLens Analytics
## Project Overview

A data analysis project on the MovieLens dataset, built entirely with core Python. This project performs an in-depth analysis of the [MovieLens](https://grouplens.org/datasets/movielens/) dataset. It extracts, processes, and analyzes user ratings, tags, movie metadata, and enriches the data by scraping additional information from IMDb using [IMDb API](https://api.graphql.imdb.com/). The goal is to build a robust analytics pipeline, and present insights in a clear, report-like format.

The analysis is structured into four main data classes, each responsible for a specific CSV file. The final output is a Jupyter Notebook (`movielens_report.ipynb`) that presents the findings in a user-friendly manner.

## Technologies Used

- **BeautifulSoup4** & **requests** (only for web scraping; data analysis is library-free)
- **Jupyter Notebook** (for final reporting)
- **pytest** (for unit testing)

> **Note:** This project intentionally avoids `pandas` to practice of Python fundamentals and data structures.

## Project Structure
```bash
movielens-analytics/
│
├── data/ # Raw MovieLens dataset
│ ├── links.csv
│ ├── movies.csv
│ ├── ratings.csv
│ ├── tags.csv
│ └── README.txt
│
├── src/ # Core source code
│ ├── movielens_analytics.py # Main classes (Movies, Tags, Ratings, Links)
│ ├── analytics_classes_tests.py # Unit tests
│ ├── main.py # Script to run all tests
│ └── movielens_report.ipynb # Jupyter Notebook with analysis results
│
├── drafts/ # Development and debugging scripts
│ ├── links_api_parser.py # Standalone IMDb API scraper prototype
│ └── links_html_parser.py # Standalone IMDb HTML scraper prototype
│
├── logs.log # Application log file
└── README.md # This file
```

## Core Classes & Methods

The heart of the project lies in four classes written in `movielens_analytics.py`, each mirroring a dataset file. All methods are implemented using standard Python data structures (`dict`, `list`, `Counter`).

### 1. `Movies` (from `movies.csv`)
- **`dist_by_release()`**: Distribution of movies by release year. Sorted by count descending.
- **`dist_by_genres()`**: Number of movies per genre. Sorted by count descending.
- **`most_genres(n=10)`**: Top-n movies with the most genres.

### 2. `Tags` (from `tags.csv`)
- **`most_words(n=10)`**: Top-n tags with the most words.
- **`longest(n=10)`**: Longest tags by character count.
- **`most_words_and_longest(n=10)`**: Intersection of the above two.
- **`most_popular(n=10)`**: Most frequently used tags.
- **`tags_with(word)`**: Tags containing a specific word.

### 3. `Ratings` (from `ratings.csv`)
- **`find_title_by_id(movie_id)`**: Maps a movie ID to its title.
- **`dist_by_year()`**: Distribution of ratings by year (from timestamps).
- **`dist_by_rating(key='ratings')`**: Distribution of ratings (or ratings per user).
- **`top_by_num_of_ratings(n=10)`**: Top-n movies by number of ratings.
- **`top_by_ratings(n=10, key='movies', metric='average')`**: Top-n movies/users by average or median rating.
- **`top_controversial(n=10, key='movies')`**: Top-n movies/users by rating variance.

### 4. `Links` (from `links.csv` + IMDb web scraping)
- **`get_imdb(list_of_movies, list_of_fields)`**: Scrapes IMDb for additional movie data (director, budget, runtime, etc.).
- **`top_directors(n=10)`**: Most prolific directors by number of films.
- **`most_expensive(n=10)`**: Movies with the highest budgets.
- **`most_profitable(n=10)`**: Movies with the highest profit (worldwide gross - budget).
- **`longest(n=10)`**: Movies with the longest runtime.
- **`top_cost_per_minute(n=10)`**: Movies with the highest budget per minute of runtime.

## Testing & Quality Assurance

All core methods are covered by unit tests in `analytics_classes_tests.py`. The tests verify:
- Correct return types and data structures.
- Proper sorting and ordering of results.
- Edge cases (e.g., `n=0` for `most_genres`).
- Data integrity for parsed fields.

To run the tests, execute:
```bash
python src/main.py
```

## Drafts

For the testing purposes there were created two files in `drafts/` folder. Each of them contains a set of functions that can be used to test the functionality of the `Links` class.
- **`links_api_parser.py`**: Performs a API scrapping scenario. Was taken as the main approach in `Links` class.
- **`links_html_parser.py`** - performs a web scrapping scenario. Was rejected because of low reliability.

## License

This project is for educational purposes only. The MovieLens dataset is subject to its own [license](https://grouplens.org/datasets/movielens/).