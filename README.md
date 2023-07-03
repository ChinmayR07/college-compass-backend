## College Compass Backend Sub Module
Welcome to the backend repository of College Compass! This is the server-side component of our application, responsible for handling data processing, database interactions, and serving API endpoints to the frontend. College Compass is a comprehensive platform that helps students make informed decisions about colleges and universities.

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

## Project Structure

The backend follows a standard Flask application structure:

- `run.py`: The main application file that initializes the Flask app.
- `dashboard_routes.py`: Contains REST API endpoints to enable backend communication for the college compass frontend.
- `data_cleaning.py`: Includes scripts that were used to process the raw IPEDS data and make them available for viewing on the dashboard.
- `College-compass-backend-dataset.ipynb`: This file contains additional processing scripts that were run in the initial data processing phase.
- `requirements.txt`: Lists all the Python packages required for the project.

## Running the Application

Once you've set up the virtual environment and environment variables, you can run the application using the following command: `flask run`

By default, this will start the application on port `5000`.

or

To start the Flask server, run the following command in the terminal: `python python run.py`

This will start the server at `http://localhost:6969`.


## API Endpoints

The backend exposes various API endpoints to interact with the database and provide data to the frontend. These endpoints include:

- `/api/colleges`: Retrieve a list of colleges and their details.
- `/api/colleges/<college_id>`: Retrieve detailed information about a specific college.
- `/api/majors`: Retrieve a list of available majors and programs.
- `/api/majors/<major_id>`: Retrieve detailed information about a specific major.

## Contribution Guidelines

We welcome contributions to improve College Compass! If you want to contribute, please follow these steps:

1. Fork this repository and create a new branch for your feature or bug fix.
2. Make your changes and test thoroughly.
3. Submit a pull request, describing the changes you've made.

Before submitting a pull request, ensure that your code adheres to our coding standards and passes all tests.

## Contact

If you have any questions or need further assistance, please contact me at jayaram.krovvidi@outlook.com. We appreciate your interest in College Compass!

