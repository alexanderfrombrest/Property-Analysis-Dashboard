import io
import pandas as pd
import requests
from pandas import DataFrame
import csv
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(**kwargs) -> pd.DataFrame:


    columns = ["Current date", "Current time", "ID", "Added date", "Update date", "Price", "Area",
            "Rooms", "floor", "rent", "form of ownership", "condition",
            "arrangements", "heating", "market", "advertiser type",
            "building year", "material1", "elevator", "material2", "link"]
    df = pd.DataFrame(columns=columns)

    # Create a session object
    session = requests.Session()
    # Set headers to mimic a browser visit
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
    })

    search_url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow'
    df = scrape_otodom(search_url, df, session)
    return df
    
    
# Main scraping function
def scrape_otodom(search_url, df, session):
    max_pages = get_max_pages(search_url, session)
    raw_links = fetch_raw_links(search_url, max_pages, session)
    for link in raw_links:
        df = fetch_data_from_raw_link(df, link, session)
    return df
    
# Function to determine the number of pages in the search results
def get_max_pages(search_url, session):
    response = session.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pages_count_div = soup.find("div", class_="css-18budxx e18zekwa0")
    if not pages_count_div:
        return 1  # Assume there's at least one page if no navigation is found
    list_page_numbers = pages_count_div.find_all("li", class_="css-1tospdx")
    numbers = [int(item.text) for item in list_page_numbers if item.text.isdigit()]
    return max(numbers) if numbers else 1

# Function to fetch raw links from each page
def fetch_raw_links(search_url, max_number, session):
    raw_links = []
    for i in range(1, max_number + 1):
        page_url = f"{search_url}?page={i}"
        response = session.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all("a", class_="css-16vl3c1 e1x0p3r10")
        for a_tag in a_tags:
            if a_tag and a_tag.get("href"):
                raw_links.append("https://www.otodom.pl" + a_tag.get("href"))

    print(f"Total links fetched: {len(raw_links)}")
    raw_links = list(dict.fromkeys(raw_links))

    print(f"Total links wihout dups: {len(raw_links)}")       
    return raw_links

def fetch_data_from_raw_link(df, link, session):
    response = session.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    #ad id and addition date 
    id = otodom_get_ad_id(soup)
    addition_date = otodom_get_addition_date(soup)
    update_date = otodom_get_update_date(soup)

    #add general info
    price = otodom_get_ad_price(soup)
    area = otodom_get_area(soup)
    rooms = otodom_get_rooms(soup)
    floor = otodom_get_floor(soup)
    rent = otodom_get_rent(soup)
    form_of_ownership = otodom_get_form_of_ownership(soup)
    condition = otodom_get_condition(soup)
    arrangements = otodom_get_arrangements(soup)
    heating = otodom_get_heating(soup)

    #add additional info
    market = otodom_get_market(soup)
    advertiser_type = otodom_get_heating(soup)
    building_year = otodom_get_building_year(soup)
    material1 = otodom_get_material1(soup)
    elevator = otodom_get_elevator(soup)
    material2 = otodom_get_material2(soup)    

    df = append_to_dataframe(df, id, addition_date, update_date, price, area, rooms,
                floor, rent, form_of_ownership, condition,
                    arrangements, heating, market, advertiser_type,
                    building_year, material1, elevator, material2, link)
    return df

def append_to_dataframe(df, id, addition_date, update_date, price, area, rooms,
                        floor, rent, form_of_ownership, condition,
                        arrangements, heating, market, advertiser_type,
                        building_year, material1, elevator, material2, link):
    
    # Generate current timestamp
    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")

    # Prepare the data as a dictionary
    data = {
        "Current date": current_date,
        "Current time": current_time,
        "ID": id,
        "Added date": addition_date,
        "Update date": update_date,
        "Price": price,
        "Area": area,
        "Rooms": rooms,
        "floor": floor,
        "rent": rent, 
        "form of ownership": form_of_ownership, 
        "condition": condition,
        "arrangements": arrangements, 
        "heating": heating, 
        "market": market, 
        "advertiser type": advertiser_type,
        "building year": building_year, 
        "material1": material1, 
        "elevator": elevator, 
        "material2": material2,
        "link": link
    }

    # Append the data to the DataFrame
    df = df.append(data, ignore_index=True)
    return df

#ad id info

def otodom_get_ad_id(soup):
    title_tag = soup.find("title")
    if title_tag:
        title_text = title_tag.get_text(strip=True)
        if matches := re.search(r"(\d+) • www\.otodom\.pl", title_text):
            return int(matches.group(1))
    return None

def otodom_get_addition_date(soup):
    added_date_tag = soup.find('script', id='__NEXT_DATA__')
    if added_date_tag:
        data = json.loads(added_date_tag.string)
        # Access specific fields
        created_at = data['props']['pageProps']['ad']['createdAt']
        return created_at        
    return None

def otodom_get_update_date(soup):
    added_date_tag = soup.find('script', id='__NEXT_DATA__')
    if added_date_tag:
        data = json.loads(added_date_tag.string)
        # Access specific fields
        modified_at = data['props']['pageProps']['ad']['modifiedAt']
        return modified_at   
    return None

#ad general info
def otodom_get_ad_price(soup):
    try:
        ad_price_info = soup.find("strong", class_="css-t3wmkv e1l1avn10")
        ad_price_text = ad_price_info.get_text(strip=True)
        ad_price = re.sub(r"[^\d.]", "", ad_price_text)
        return ad_price or '0'  # Return '0' if ad_price is empty or None
    except Exception as e:
        
        return '0'  # Return a default value in case of an error

def otodom_get_area(soup):
    try:
        area_info = soup.find("div", {"data-testid":"table-value-area"})
        area = area_info.get_text(strip=True)
        return area or '0'
    except Exception as e:
        
        return '0'

def otodom_get_rooms(soup):
    try:
        rooms_info = soup.find("div", {"table-value-rooms_num"})
        rooms = rooms_info.get_text(strip=True)
        return rooms or '0'
    except Exception as e:
        
        return '0'

def otodom_get_floor(soup):
    try:
        floor_info = soup.find("div", {"table-value-floor"})
        floor = floor_info.get_text(strip=True)
        return floor or '0'
    except Exception as e:
        
        return '0'

def otodom_get_rent(soup):
    try:
        rent_info = soup.find("div", {"data-testid":"table-value-rent"})
        rent = rent_info.get_text(strip=True)
        return rent
    except Exception as e:
        
        return '0'

def otodom_get_form_of_ownership(soup):
    try:
        form_of_ownership_info = soup.find("div", {"data-testid":"table-value-building_ownership"})
        form_of_ownership = form_of_ownership_info.get_text(strip=True)
        return form_of_ownership
    except Exception as e:
        
        return '0'

def otodom_get_condition(soup):
    try:
        condition_info = soup.find("div", {"data-testid":"table-value-construction_status"})
        condition = condition_info.get_text(strip=True)
        return condition
    except Exception as e:
        
        return '0'

def otodom_get_arrangements(soup):
    try:
        arrangements_info = soup.find("div", {"data-testid":"table-value-outdoor"})
        arrangements = arrangements_info.get_text(strip=True)
        return arrangements
    except Exception as e:
        
        return '0'

def otodom_get_heating(soup):
    try:
        heating_info = soup.find("div", {"data-testid":"table-value-heating"})
        heating = heating_info.get_text(strip=True)
        return heating
    except Exception as e:
        
        return '0'

# ad additional info

def otodom_get_market(soup):
    try:
        market_info = soup.find("div", {"data-testid": "table-value-market"})
        market = market_info.get_text(strip=True)
        return market
    except Exception as e:
        
        return '0'

def otodom_get_advertiser_type(soup):
    try:
        market_info = soup.find("div", {"data-testid": "table-value-advertiser_type"})
        market = market_info.get_text(strip=True)
        return market
    except Exception as e:
        
        return '0'

def otodom_get_building_year(soup):
    try:
        market_info = soup.find("div", {"data-testid": "table-value-build_year"})
        market = market_info.get_text(strip=True)
        return market
    except Exception as e:
        
        return '0'

def otodom_get_material1(soup):
    try:
        market_info = soup.find("div", {"data-testid": "table-value-building_type"})
        market = market_info.get_text(strip=True)
        return market
    except Exception as e:
        
        return '0'

def otodom_get_elevator(soup):
    try:
        market_info = soup.find("div", {"data-testid": "table-value-lift"})
        market = market_info.get_text(strip=True)
        return market
    except Exception as e:
        
        return '0'

def otodom_get_material2(soup):
    try:
        market_info = soup.find("div", {"data-testid": "table-value-building_material"})
        market = market_info.get_text(strip=True)
        return market
    except Exception as e:
        
        return '0'


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'

