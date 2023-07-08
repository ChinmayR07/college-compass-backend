import csv
from flask import Blueprint, jsonify, request

dashboard = Blueprint("dashboard", __name__)

years = ["2017", "2018", "2019", "2020", "2021"]

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
                    'population': int(row['grand_total_2021']),
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

        for bar_chart_data in response:
            for category in bar_chart_data:
                if category == 'year':
                    continue
                bar_chart_data[category]['men'] /= num_rows
                bar_chart_data[category]['women'] /= num_rows
                bar_chart_data[category]['men'] = round(bar_chart_data[category]['men'], 2)
                bar_chart_data[category]['women'] = round(bar_chart_data[category]['women'], 2)

    return response


def filter_rows(unit_ids, reader):
    if not unit_ids or len(unit_ids) == 0:
        return [row for row in reader]

    rows = []
    for row in reader:
        if row['unit_id'] in unit_ids:
            rows.append(row)
    return rows



@dashboard.route('/average_price_data', methods=['GET'])
def get_average_price_data():
    unit_ids = request.args.get('unit_ids', '').split(',')
    unit_ids = [uid.strip() for uid in unit_ids if uid.strip()]

    with open('static/complete_dataset_final.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        tuition = {
            'avg_in_dist_on_campus': {year: [] for year in years},
            'avg_in_st_on_campus': {year: [] for year in years},
            'avg_out_st_on_campus': {year: [] for year in years},
            'avg_in_dist_off_campus': {year: [] for year in years},
            'avg_in_st_off_campus': {year: [] for year in years},
            'avg_out_st_off_campus': {year: [] for year in years}
        }

        filtered_rows = filter_rows(unit_ids, reader)

        for row in filtered_rows:
            for year in years:
                tuition['avg_in_dist_on_campus'][year].append(float(row[f'price_in_dist_on_campus_{year}']))
                tuition['avg_in_st_on_campus'][year].append(float(row[f'price_in_st_on_campus_{year}']))
                tuition['avg_out_st_on_campus'][year].append(float(row[f'price_out_st_on_campus_{year}']))
                
                tuition['avg_in_dist_off_campus'][year].append(
                    (float(row[f'price_in_dist_off_campus_{year}']) + float(row[f'price_in_dist_off_campus_family_{year}'])) / 2
                )
                tuition['avg_in_st_off_campus'][year].append(
                    (float(row[f'price_in_st_off_campus_{year}']) + float(row[f'price_in_st_off_campus_family_{year}'])) / 2
                )
                tuition['avg_out_st_off_campus'][year].append(
                    (float(row[f'price_out_st_off_campus_{year}']) + float(row[f'price_out_st_off_campus_family_{year}'])) / 2
                )

        response = {}
        for key in tuition.keys():
            response[key] = [
                {'year': year, 'cost': round(sum(tuition[key][year])/len(tuition[key][year]), 2) if tuition[key][year] else 0}
                for year in years
            ]

    return response
        
@dashboard.route('/sunburst', methods=['GET'])
def get_sunburst_data():
    unit_ids = request.args.get('unit_ids', '').split(',')
    unit_ids = [uid.strip() for uid in unit_ids if uid.strip()]

    with open('static/complete_dataset_final.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        filtered_rows = filter_rows(unit_ids, reader)
        num_rows = len(filtered_rows)

        columns = ['am_ind_alaska_total', 'asian', 'bl_af', 'hisp', 'haw_pac', 'white', 'two_plus_race', 'unk', 'alien']
        labels = ['American Indian / Alaskan Native', 'Asian', 'Black / African', 'Hispanic', 'Hawaiian Pacific', 'White', 'Multiple Races', 'Unknown', 'Non Resident Alien']
        genders = ['men', 'women']

        response = {
            'label': 'year',
            'children': []
        }
        for year in years:
            year_obj = {
                'label': year,
                'children': []
            }
            for idx, column in enumerate(columns):
                column_obj = {
                    'label': labels[idx],
                    'children': []
                }
                for gender in genders:
                    final_column_name = column + '_' + gender + '_' + year
                    gender_obj = {
                        'label': gender,
                        'size': calculate_average(filtered_rows, final_column_name)
                    }
                    column_obj['children'].append(gender_obj)
                year_obj['children'].append(column_obj)
            response['children'].append(year_obj)
    return response
        
def calculate_average(filtered_rows, column_name):
    total = 0
    count = 0
    for row in filtered_rows:
        if column_name in row:
            total += float(row[column_name])
            count += 1
    if count > 0:
        return total / count
    else:
        return 0
    
@dashboard.route('/pcp_data', methods=['GET'])
def get_pcp_data():
    unit_ids = request.args.get('unit_ids', '').split(',')
    unit_ids = [uid.strip() for uid in unit_ids if uid.strip()]

    with open('static/complete_dataset_final_1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        filtered_rows = filter_rows(unit_ids, reader)
        num_rows = len(filtered_rows)

        return [get_pcp_object(row) for row in filtered_rows]

def get_pcp_object(row):
    applications, admissions, enrollments, tuition_on_campus, tuition_off_campus, population = 0,0,0,0,0,0
    for year in years:
        applications = applications + (int(row['applicants_total_'+ year]))
        admissions = admissions + (int(row['admissions_total_' + year]))
        enrollments = enrollments + (int(row['enrolled_total_' + year]))
        population = population + (int(row['grand_total_' + year]))
        tuition_on_campus = tuition_on_campus + (int(row['price_in_dist_on_campus_' + year]) + int(row['price_in_st_on_campus_' + year]) + int(row['price_out_st_on_campus_' + year])) / 3
        tuition_off_campus = tuition_off_campus + (int(row['price_in_dist_off_campus_' + year]) + int(row['price_in_st_off_campus_' + year]) + int(row['price_out_st_off_campus_' + year]) \
                                                +   int(row['price_in_dist_off_campus_family_' + year]) + int(row['price_in_st_off_campus_family_' + year]) + int(row['price_out_st_off_campus_family_' + year])) / 6
    return {
        "unit_id": row["unit_id"],
        "Population": round(population / len(years), 2),
        "Applicants": round(applications / len(years), 2),
        "Admissions": round(admissions / len(years), 2),
        "Enrollments": round(enrollments / len(years), 2),
        "Tuition On Campus": round(tuition_on_campus / len(years), 2),
        "Tuition Off Campus": round(tuition_off_campus / len(years), 2),
        "cluster_num": row["cluster_number"]
    }

