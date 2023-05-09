import csv
from geopy.geocoders import Nominatim

def head(file_name):
    # open CSV file and create CSV reader
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

    # Open the output CSV file
    with open('output_file.csv', 'w', newline='') as f_out:
        csv_writer = csv.writer(f_out)
        
        # Write the header row to the output file
        csv_writer.writerows([[h] for h in header])

def rename_columns():
    new_names_map = {}
    with open('static/with_missing_values/new_column_names.csv', 'r') as new_names:
        names_rows = csv.reader(new_names)
        for row in names_rows:
            if row[1] != '':
                new_names_map[row[0]] = row[1]

    latitude_map, longitude_map = {}, {}
    with open('static/with_missing_values/zip_lat_long.csv', 'r') as zip_lat_long:
        zip_rows = csv.reader(zip_lat_long)
        next(zip_rows)

        for row in zip_rows:
            latitude_map[int(row[0])] = row[1]
            longitude_map[int(row[0])] = row[2]

    # Open input CSV file and read header row
    with open('static/clean_dataset/combined_data.csv', 'r', newline='') as combined_csv:
        reader = csv.reader(combined_csv)
        header_row = next(reader)

    # Create list of indices of columns to keep
    keep_indices = [i for i, col_name in enumerate(header_row) if col_name in new_names_map]

    # Create new header row with new column names
    new_header_row = [new_names_map[header_row[i]] for i in keep_indices]
    new_header_row.append('latitude')
    new_header_row.append('longitude')

    print(new_header_row)

    # Open input CSV file again and filter rows, keeping only columns with new names
    with open('static/clean_dataset/combined_data.csv', 'r', newline='') as combined_csv, open('static/with_missing_values/combined_with_lat_long.csv', 'w', newline='') as output_file:
        reader = csv.reader(combined_csv)
        next(reader)
        writer = csv.writer(output_file)
        
        # Write new header row to output file
        writer.writerow(new_header_row)
        
        # Iterate over rows in input file and keep only selected columns
        for row in reader:
            selected_columns = [row[i] for i in keep_indices]
            zip_code = int(row[keep_indices[new_header_row.index('zip_code')]].split('-')[0])
            selected_columns.append(latitude_map[zip_code])
            selected_columns.append(longitude_map[zip_code])
            writer.writerow(selected_columns)

rename_columns()
