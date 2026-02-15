import requests
from bs4 import BeautifulSoup


def main():
    headers = {'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64)', 'Accept': 'text/html'}
    movie_id = '0120737'
    link = f'http://www.imdb.com/title/tt{movie_id}/'
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')


    # Upper (black) part of IMDB HTML
    black_part = soup.find('section', attrs={'data-testid': 'hero-parent'})
    

    # Header part. Includes: title, year, age rating, duration
    print('Title, year, age rating, duration:')
    rus_title, original_title, year, age_rating, duration = None, None, None, None, None
    header_part = black_part.find('div', class_='sc-af040695-0 iOwuHP')
    rus_title = header_part.find('span', class_="hero__primary-text", attrs={"data-testid": "hero__primary-text"}).text.strip()
    original_title = header_part.find('div', class_="sc-b41e510f-2 jUfqFl baseAlt").text.split(':')[1].strip()
    list_items = header_part.find("ul", class_="ipc-inline-list").find_all('li')
    year = list_items[0].text.strip()
    age_rating = list_items[1].text.strip()
    duration = list_items[2].text.strip()
    print(rus_title, original_title, year, age_rating, duration, sep=' | ', end='\n\n\n')


    # Tags part
    print('Tags:')
    tags = None
    tags_part = black_part.find('div', class_='ipc-chip-list__scroller')
    tags = [tag.text.strip() for tag in tags_part.find_all('span', class_='ipc-chip__text')]
    print(tags, end='\n\n\n')


    # Cast part. Includes: director(s), writers, main actors
    print('Director(s), writers, main actors:')
    directors, writers, main_actors = None, None, None
    cast_part = black_part.find('div', class_='sc-af040695-2 fLTdiX')
    main_team = cast_part.find_all('ul', class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt")

    directors_info = main_team[0]
    directors_list = directors_info.find_all('li', class_="ipc-inline-list__item")
    directors = [director.text.strip() for director in directors_list]

    writers_info = main_team[1]
    writers_list = writers_info.find_all('li', class_="ipc-inline-list__item")
    writers = [writer.text.strip() for writer in writers_list]
    
    actors_info = main_team[2]
    actors_list = actors_info.find_all('li', class_="ipc-inline-list__item")
    main_actors = [actor.text.strip() for actor in actors_list]

    print(directors, writers, main_actors, sep='\n', end='\n\n\n')


    # Lower (white) part of IMDB HTML
    white_part = soup.find('section', class_='ipc-page-background ipc-page-background--base sc-e1aae3e0-0 kWggHH')


    # Details block. Contains: release dates, origin countries, origin languages, filming locations, production companies
    print('release_dates, origins, languages, filming_locations, prod_companies:')
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

    print(release_dates, origins, languages, filming_locations, prod_companies, sep='\n', end='\n\n\n')


    # Box office block. Contains: budgets, gross_domestics, opening_weekend_domestics, cumulative_worldwide_grosses
    print('budgets, gross_domestics, opening_weekend_domestics, cumulative_worldwide_grosses:')
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

    print(budgets, gross_domestics, opening_weekend_domestics, cumulative_worldwide_grosses, sep='\n')

    #with open('HTMLs/full_film_page.html', 'w') as file: file.write(response.text)
    #with open('HTMLs/black_part.html', 'w') as file: file.write(black_part.prettify())
    #with open('HTMLs/header_part.html', 'w') as file: file.write(header_part.prettify())
    #with open('HTMLs/cast_part.html', 'w') as file: file.write(cast_part.prettify())
    #with open('HTMLs/white_part.html', 'w') as file: file.write(white_part.prettify())


if __name__ == '__main__':
    main()