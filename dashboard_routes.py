import csv
from flask import Blueprint, jsonify, request

dashboard = Blueprint("dashboard", __name__)

@dashboard.route('/map_data', methods=['GET'])
def get_colleges():
    # Get the unit_ids parameter from the request
    unit_ids = request.args.get('unit_ids', '').split(',')
    unit_ids = [uid.strip() for uid in unit_ids if uid.strip()]

    # Open the CSV file and extract the data
    with open('static/complete_dataset_final.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        colleges = []
        for row in reader:
            if not unit_ids or row['unit_id'] in unit_ids:
                college = {
                    'unit_id': int(row['unit_id']),
                    'name': row['name'],
                    'population': row['grand_total_2021'],
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude'])
                }
                colleges.append(college)

    # Return the JSON response
    response = {'colleges': colleges}
    return jsonify(response)

@dashboard.route('/all_unit_ids', methods=['GET'])
def get_all_unit_ids():

    with open('static/complete_dataset_final.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        unit_ids = [row['unit_id'] for row in reader]
    
    response = {'unit_ids': unit_ids}
    return jsonify(response)