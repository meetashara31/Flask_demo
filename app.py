from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import time
import random

app = Flask(__name__)

def scrape_books():
    all_books = []

    for i in range(1, 5):
        url = f'https://books.toscrape.com/catalogue/page-1.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all('article', class_='product_pod')

        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text.strip()
            availability = book.find('p', class_='instock availability').text.strip()
            link = 'https://books.toscrape.com/catalogue/' + book.h3.a['href']

            # Inner product page
            product_response = requests.get(link)
            product_soup = BeautifulSoup(product_response.text, 'html.parser')

            # Description
            meta_tag = product_soup.find('meta', attrs={'name': 'description'})
            description = meta_tag['content'].strip() if meta_tag else 'No description'

            # Rating
            rating_tag = product_soup.find('p', class_='star-rating')
            rating = rating_tag['class'][1] if rating_tag else 'No rating'

            all_books.append({
                'Title': title,
                'Price': price,
                'Availability': availability,
                'Product URL': link,
                'Rating': rating,
                'Description': description
            })

            time.sleep(random.uniform(0.5, 1.2))

    return all_books

@app.route('/')
def home():
    return '✅ Flask is working!'

@app.route('/scrape-books', methods=['GET'])
def scrape_route():
    try:
        books_data = scrape_books()
        return jsonify({'status': 'success', 'total': len(books_data), 'data': books_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
