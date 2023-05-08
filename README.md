# College Compass Backend

This is the backend for the College Compass application, implemented in Flask. This README file will guide you through the installation, setup and usage of this backend.

The College Compass application is a web-based platform that provides information and guidance for students who are planning to attend college. The main goal of the application is to help students find the right college that suits their academic and personal needs. The platform will provide students with a personalized college search engine that allows them to filter colleges based on various factors such as location, size, academic programs, and cost.

The College Compass application will use a variety of data sources to provide accurate and up-to-date information about colleges. These data sources include the US Department of Education, the National Center for Education Statistics, and other relevant public and private databases. The application will also incorporate user-generated content such as reviews, ratings, and comments from current and past college students.

The backend of the College Compass application will be responsible for managing and processing all the data used by the platform. This includes retrieving and storing data from various sources, cleaning and processing data to make it suitable for analysis, and providing APIs for the frontend to retrieve data for display.

The Flask framework was chosen for the backend of the College Compass application due to its ease of use, flexibility, and ability to handle complex web applications. Flask is a lightweight framework that allows developers to quickly build web applications with minimal setup and configuration. Flask also provides powerful tools for handling data processing, database management, and API development.

## Requirements

To run this backend, you will need:

- Python 3.8 or higher
- Flask 2.0.1 or higher
- pandas 1.3.3 or higher
- scikit-learn 1.0.1 or higher

## Setup

1. Clone this repository to your local machine.
2. Make sure you have Python 3 installed on your machine.
3. Create a new virtual environment by running `python3 -m venv compass-backend`.
4. Activate the virtual environment by running `.\compass-backend\bin\activate`.
5. Install the required dependencies by running `pip3 install -r requirements.txt`.
6. Create a `.env` file in the root directory and set the required environment variables.

## Environment Variables

Here's a list of the environment variables that you'll need to set in the `.env` file:

- `FLASK_APP`: The name of the Flask application (should be `app`).
- `FLASK_ENV`: The environment in which Flask is running (`development`, `production`, etc.).
- `DATABASE_URI`: The URI for the database you'll be using.

## Running the Application

Once you've set up the virtual environment and environment variables, you can run the application using the following command:

```
flask run
```

By default, this will start the application on port `5000`.

or

To start the Flask server, run the following command in the terminal:

```python
python run.py
```

This will start the server at `http://localhost:5000`.

## Endpoints

This backend has the following endpoints:

### GET /colleges

Returns a JSON array of all the colleges in the database. The response format is as follows:

```json
[
  {
    "name": "Harvard University",
    "city": "Cambridge",
    "state": "MA",
    "zip": "02138",
    "latitude": 42.377,
    "longitude": -71.1167,
    "tuition_in_state": 48949,
    "tuition_out_state": 48949,
    "other_expenses_in_state": 18044,
    "other_expenses_out_state": 18044,
    "total_enrollment": 31120,
    "admission_rate": 0.0439,
    ...
  },
  ...
]
```

### GET /colleges/:id

Returns a JSON object of a specific college with the given `id`. The response format is the same as the `/colleges` endpoint.

### POST /predict

Accepts a JSON object with the following keys:

- `tuition_in_state`: The in-state tuition fee for the college.
- `tuition_out_state`: The out-of-state tuition fee for the college.
- `other_expenses_in_state`: The in-state other expenses for the college.
- `other_expenses_out_state`: The out-of-state other expenses for the college.

Returns a JSON object with the predicted values for the following keys:

- `total_enrollment`: The predicted total enrollment for the college.
- `admission_rate`: The predicted admission rate for the college.
- `sat_score_25th_percentile_critical_reading`: The predicted 25th percentile SAT critical reading score for the college.
- `sat_score_75th_percentile_critical_reading`: The predicted 75th percentile SAT critical reading score for the college.
- `sat_score_25th_percentile_math`: The predicted 25th percentile SAT math score for the college.
- `sat_score_75th_percentile_math`: The predicted 75th percentile SAT math score for the college.
- `sat_score_25th_percentile_writing`: The predicted

## Things to Be Careful

- Make sure to keep the `.env` file secure and not share it with anyone.
- Always activate the virtual environment before running the application or installing new dependencies.
- Be careful when making changes to the database schema, as this could affect the functionality of the application.

## Other Information

- The `migrations` directory contains the database migrations generated by Flask-Migrate.
- The `app` directory contains the Flask application code.
- The `tests` directory contains the unit tests for the application.
