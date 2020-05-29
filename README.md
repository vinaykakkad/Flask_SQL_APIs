# cs50-projects

## 1. FLASK_SQL_API

A book reviews website were users can search for books, leave reviews and see the reviews by others. Using Goodreads API, ratings of the books will also be displayed. Finally, users can query also query for book details and rating through website's API.

### Installation:

  - Clone/download the repository and move to the flask_sql_api folder
  - Install the required packages using:
  ```sh
  pip install -r requirements.txt
  ```
  - In env.py file configure your secret key, database url and Goodreads API key. Database url follows the standard convention:
  [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]. You can get the Goodreads API key from [here](https://www.goodreads.com/api).
  - Now, run the file using:
  ```sh
  set FLASK_DEBUG=1
  set FLASK_ENV=development
  set FLASK_APP=run.py
  python -m flask run
  ```
  - On moving to the provided url, you will be able to see the login page:
  ![alt text](https://github.com/vinaykakkad/cs50-projects/blob/master/flask_sql_api/project_images/login.png?raw=true)
  - Quit the server and import the data using:
  ```sh
  python import.py
  ```
  - Run the file, register, login and you will be able to see the dashboard:
  ![alt text](https://github.com/vinaykakkad/cs50-projects/blob/master/flask_sql_api/project_images/dashboard.png?raw=true)
  <br>
  You can now search books, view ratings, post reviews and query for a book's data using the "url_of_website/api/book_isbn_number" route.
  
