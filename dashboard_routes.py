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



@dashboard.route('/bar_chart_data', methods=['GET'])
def get_bar_chart_data():
    unit_ids = request.args.get('unit_ids', '').split(',')
    unit_ids = [uid.strip() for uid in unit_ids if uid.strip()]

    with open('static/complete_dataset_final.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        years = ["2021", "2020", "2019", "2018", "2017"]
        
        bar_chart_data = {}
        all_unit_ids = set()
        input_unit_ids_set = set(unit_ids)

        for row in reader:
            unit_id = row['unit_id']
            all_unit_ids.add(unit_id)
            if not unit_ids or unit_id in unit_ids:
                if unit_id not in bar_chart_data:
                    bar_chart_data[unit_id] = {
                        'applicants': {'men': 0, 'women': 0},
                        'admissions': {'men': 0, 'women': 0},
                        'enrollments': {'men': 0, 'women': 0}
                    }
                for year in years:
                    for category in ['applicants', 'admissions', 'enrollments']:
                        bar_chart_data[unit_id][category]['men'] += int(row[f"{category}_men_{year}"]) / len(years)
                        bar_chart_data[unit_id][category]['women'] += int(row[f"{category}_women_{year}"]) / len(years)

    if not input_unit_ids_set.intersection(all_unit_ids):
        return jsonify(bar_chart_data)
    else:
        filtered_data = {uid: bar_chart_data[uid] for uid in unit_ids if uid in bar_chart_data}
        return jsonify(filtered_data)
