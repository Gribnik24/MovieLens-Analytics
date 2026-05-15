import requests

def fetch_movie(imdb_id):
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
        return None

    data = r.json().get("data", {}).get("title", {})
    if not data:
        return None

    # MAIN FIELDS
    title = data.get("titleText", {}).get("text", "N/A")
    genres = []
    for section in data.get("titleGenres", []).get("genres", []):
        genres.append(section.get("genre", {}).get("text"))
    release_year = data.get("releaseDate", {}).get("year")
    runtime = data.get("runtime", {}).get("seconds", 0) // 60
    rating = data.get("ratingsSummary", {}).get("aggregateRating", "N/A")
    rated_count = data.get("ratingsSummary", {}).get("voteCount", "N/A")
    
    # CREDITS
    directors, writers, cast = [], [], []
    for director in data.get("DIRECTORS", {}).get("edges", {}):
        directors.append(director.get("node", {}).get("name", {}).get("nameText", {}).get("text", "N/A"))
    for writer in data.get("WRITERS", {}).get("edges", {}):
        writers.append(writer.get("node", {}).get("name", {}).get("nameText", {}).get("text", "N/A"))
    for actor in data.get("CAST", {}).get("edges", {}):
        cast.append(actor.get("node", {}).get("name", {}).get("nameText", {}).get("text", "N/A"))
        
    # GROSS AND BUDGET
    budget = data.get("productionBudget", {}).get("budget", {}).get("amount", "N/A")
    gross = data.get("lifetimeGross", {}).get("total", {}).get("amount", 0)
    
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

def main():
    movie_data = fetch_movie("tt0120737")
    print(movie_data)
    
if __name__ == '__main__':
    main()