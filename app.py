from flask import Flask, render_template, request
import csv
import main
import os

app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    print(os.path.abspath('templates/home.html'))
    return render_template('home.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    main.main()

    with open('books.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        books = list(reader)

    return render_template('results.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)


