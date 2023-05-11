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



import csv
from flask import Blueprint, jsonify, request

dashboard = Blueprint("dashboard", __name__)

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
                for year in years:
                    if year not in bar_chart_data:
                        bar_chart_data[year] = {
                            'applicants': {'men': 0, 'women': 0},
                            'admissions': {'men': 0, 'women': 0},
                            'enrollments': {'men': 0, 'women': 0}
                        }
                    bar_chart_data[year]['applicants']['men'] += int(row[f"applicants_men_{year}"])
                    bar_chart_data[year]['applicants']['women'] += int(row[f"applicants_women_{year}"])
                    bar_chart_data[year]['admissions']['men'] += int(row[f"admissions_men_{year}"])
                    bar_chart_data[year]['admissions']['women'] += int(row[f"admissions_women_{year}"])
                    bar_chart_data[year]['enrollments']['men'] += int(row[f"enrollments_men_{year}"])
                    bar_chart_data[year]['enrollments']['women'] += int(row[f"enrollments_women_{year}"])

        if unit_ids:
            total_ids = len(unit_ids)
        else:
            total_ids = len(all_unit_ids)

        for year in bar_chart_data:
            for category in bar_chart_data[year]:
                bar_chart_data[year][category]['men'] /= total_ids
                bar_chart_data[year][category]['women'] /= total_ids
                bar_chart_data[year][category]['men'] = "{:.2f}".format(bar_chart_data[year][category]['men'])
                bar_chart_data[year][category]['women'] = "{:.2f}".format(bar_chart_data[year][category]['women'])

    return jsonify(bar_chart_data)



