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


@dashboard.route('/bar_chart_data', methods=['GET'])
def get_bar_chart_data():
    unit_ids = request.args.get('unit_ids', '').split(',')
    unit_ids = [uid.strip() for uid in unit_ids if uid.strip()]

    with open('static/complete_dataset_final.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        years = ["2021", "2020", "2019", "2018", "2017"]

        response = []

        filtered_rows = filter_rows(unit_ids, reader)
        num_rows = len(filtered_rows)

        for year in years:
            bar_chart_data = {
                'year': year,
                'applicants': {'men': 0, 'women': 0},
                'admissions': {'men': 0, 'women': 0},
                'enrollments': {'men': 0, 'women': 0}
            }
            for row in filtered_rows:
                bar_chart_data['applicants']['men'] += int(
                    row[f"applicants_men_{year}"])
                bar_chart_data['applicants']['women'] += int(
                    row[f"applicants_women_{year}"])
                bar_chart_data['admissions']['men'] += int(
                    row[f"admissions_men_{year}"])
                bar_chart_data['admissions']['women'] += int(
                    row[f"admissions_women_{year}"])
                bar_chart_data['enrollments']['men'] += int(
                    row[f"enrollments_men_{year}"])
                bar_chart_data['enrollments']['women'] += int(
                    row[f"enrollments_women_{year}"])
            response.append(bar_chart_data)

        print(response)
        for bar_chart_data in response:
            for category in bar_chart_data:
                if category == 'year':
                    continue
                bar_chart_data[category]['men'] /= num_rows
                bar_chart_data[category]['women'] /= num_rows
                bar_chart_data[category]['men'] = "{:.2f}".format(
                    bar_chart_data[category]['men'])
                bar_chart_data[category]['women'] = "{:.2f}".format(
                    bar_chart_data[category]['women'])

    return jsonify(response)


def filter_rows(unit_ids, reader):
    if not unit_ids or len(unit_ids) == 0:
        return [row for row in reader]

    rows = []
    for row in reader:
        if row['unit_id'] in unit_ids:
            rows.append(row)
    rows
