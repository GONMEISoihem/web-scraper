import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"


# Fetch the webpage content

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' 
                  'AppleWebKit/537.36 (KHTML, like Gecko) ' 
                  'Chrome/58.0.3029.110 Safari/537.3'
}


def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        response.encoding = 'utf-8'
        webpage = response.text
        return webpage
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Parse the HTML and Extract data


def parse_books(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())
        books = soup.find_all(name='article', class_='product_pod')
        book_data = []

        for book in books:
            title = book.h3.a['title']
            price = book.find(name='p', class_='price_color').getText()
            availability = book.find(name='p', class_='instock availability').getText().strip()
            link = BASE_URL+book.h3.a['href']

            book_data.append({
                'Title': title,
                'Price': price,
                'Availability': availability,
                'link': link
            })

        return book_data
    except Exception as e:
        print(f'Error parsing books: {e}')

# Handle Pagination


def get_next_page(current_url, soup):
    next_button = soup.find(name='li', class_='next')
    if next_button:
        next_page_url = next_button.a['href']
        full_next_page_url = urljoin(current_url, next_page_url)
        return full_next_page_url
    return None

# Save data to CSV


def save_to_csv(data, filename='books.csv'):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


# Main function to Orchestrate Scraping

def main():
    all_books = []
    url = BASE_URL

    while url:
        print(f'Scraping page: {url}')
        html = fetch_page(url)
        if not html:
            break

        soup = BeautifulSoup(html, 'html.parser')
        books = parse_books(html)
        all_books.extend(books)
        url = get_next_page(url, soup)

        # Avoid overwhelming the target server by adding delays between requests.
        time.sleep(1)  # Wait for 1 second before the next request

    if all_books:
        save_to_csv(all_books)
        print(f'Scraping completed. {len(all_books)} books saved to books.csv')
    else:
        print("No data scraped.")


if __name__ == "__main__":
    main()

















# prices = soup.find_all(name='p', class_='price_color')
# availabilities = soup.find_all(name='p', class_='instock availability')
#
# # print(titles.getText())
# # print(prices.getText())
# # print(availabilities.getText().strip())
#
# for i in range(len(titles)):
#     link = titles[i].find('a')['href']
#     absolute_link = BASE_URL + link
#     # print(absolute_link)
#     book = {
#         'title': titles[i].getText(),
#         'price': prices[i].getText(),
#         'availability': availabilities[i].getText().strip(),
#         'link': absolute_link
#     }
#     book_data.append(book)
#
# print(book_data)


