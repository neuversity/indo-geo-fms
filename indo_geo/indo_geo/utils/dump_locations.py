import os

import frappe
from frappe.utils import now_datetime


def dump_all_locations():
    """Export all location data to SQL files for fast bulk import."""
    print("Starting location data dump...")

    # Get the app path
    app_path = frappe.get_app_path("indo_geo")
    sql_path = os.path.join(app_path, "..", "data", "sql")

    # Create SQL directory if it doesn't exist
    os.makedirs(sql_path, exist_ok=True)

    # Dump in order: Province -> Regency -> District -> Village
    dump_provinces(sql_path)
    dump_regencies(sql_path)
    dump_districts(sql_path)
    dump_villages(sql_path)

    print("Location data dump completed successfully!")


def dump_provinces(sql_path):
    """Export provinces to SQL file."""
    file_path = os.path.join(sql_path, "provinces.sql")

    print("Dumping provinces...")

    # Get all provinces
    provinces = frappe.db.sql("""
        SELECT name, province_code, province_name, creation, modified, modified_by, owner
        FROM tabProvince
        ORDER BY province_code
    """, as_dict=True)

    if not provinces:
        print("No provinces found to dump")
        return

    # Generate SQL INSERT statements
    sql_content = generate_province_sql(provinces)

    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)

    print(f"Dumped {len(provinces)} provinces to {file_path}")


def dump_regencies(sql_path):
    """Export regencies to SQL file."""
    file_path = os.path.join(sql_path, "regencies.sql")

    print("Dumping regencies...")

    # Get all regencies
    regencies = frappe.db.sql("""
        SELECT name, regency_code, regency_name, province, province_code,
               creation, modified, modified_by, owner
        FROM tabRegency
        ORDER BY regency_code
    """, as_dict=True)

    if not regencies:
        print("No regencies found to dump")
        return

    # Generate SQL INSERT statements
    sql_content = generate_regency_sql(regencies)

    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)

    print(f"Dumped {len(regencies)} regencies to {file_path}")


def dump_districts(sql_path):
    """Export districts to SQL file."""
    file_path = os.path.join(sql_path, "districts.sql")

    print("Dumping districts...")

    # Get all districts
    districts = frappe.db.sql("""
        SELECT name, district_code, district_name, regency, province, regency_code,
               creation, modified, modified_by, owner
        FROM tabDistrict
        ORDER BY district_code
    """, as_dict=True)

    if not districts:
        print("No districts found to dump")
        return

    # Generate SQL INSERT statements
    sql_content = generate_district_sql(districts)

    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)

    print(f"Dumped {len(districts)} districts to {file_path}")


def dump_villages(sql_path):
    """Export villages to SQL file."""
    file_path = os.path.join(sql_path, "villages.sql")

    print("Dumping villages...")

    # Get all villages
    villages = frappe.db.sql("""
        SELECT name, village_code, village_name, district, regency, province, district_code,
               creation, modified, modified_by, owner
        FROM tabVillage
        ORDER BY village_code
    """, as_dict=True)

    if not villages:
        print("No villages found to dump")
        return

    # Generate SQL INSERT statements in chunks to avoid memory issues
    chunk_size = 1000
    total_chunks = (len(villages) + chunk_size - 1) // chunk_size

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("-- Village data dump\n")
        f.write(f"-- Total records: {len(villages)}\n\n")

        for i in range(0, len(villages), chunk_size):
            chunk = villages[i:i + chunk_size]
            chunk_num = (i // chunk_size) + 1
            print(f"  Processing chunk {chunk_num}/{total_chunks} ({len(chunk)} records)")

            sql_content = generate_village_sql(chunk)
            f.write(f"-- Chunk {chunk_num}\n")
            f.write(sql_content)
            f.write("\n")

    print(f"Dumped {len(villages)} villages to {file_path}")


def generate_province_sql(provinces):
    """Generate SQL INSERT statements for provinces."""
    if not provinces:
        return ""

    sql = "-- Province data\n"
    sql += "INSERT INTO tabProvince (name, creation, modified, modified_by, owner, docstatus, idx, province_code, province_name) VALUES\n"

    values = []
    for province in provinces:
        values.append("('{}', '{}', '{}', '{}', '{}', 0, 0, '{}', '{}')".format(
            escape_sql_string(province.name),
            province.creation.strftime('%Y-%m-%d %H:%M:%S.%f') if province.creation else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            province.modified.strftime('%Y-%m-%d %H:%M:%S.%f') if province.modified else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            escape_sql_string(province.modified_by or 'Administrator'),
            escape_sql_string(province.owner or 'Administrator'),
            escape_sql_string(province.province_code),
            escape_sql_string(province.province_name)
        ))

    sql += ",\n".join(values)
    sql += ";\n"

    return sql


def generate_regency_sql(regencies):
    """Generate SQL INSERT statements for regencies."""
    if not regencies:
        return ""

    sql = "-- Regency data\n"
    sql += "INSERT INTO tabRegency (name, creation, modified, modified_by, owner, docstatus, idx, regency_code, regency_name, province, province_code) VALUES\n"

    values = []
    for regency in regencies:
        values.append("('{}', '{}', '{}', '{}', '{}', 0, 0, '{}', '{}', '{}', '{}')".format(
            escape_sql_string(regency.name),
            regency.creation.strftime('%Y-%m-%d %H:%M:%S.%f') if regency.creation else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            regency.modified.strftime('%Y-%m-%d %H:%M:%S.%f') if regency.modified else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            escape_sql_string(regency.modified_by or 'Administrator'),
            escape_sql_string(regency.owner or 'Administrator'),
            escape_sql_string(regency.regency_code),
            escape_sql_string(regency.regency_name),
            escape_sql_string(regency.province or ''),
            escape_sql_string(regency.province_code or '')
        ))

    sql += ",\n".join(values)
    sql += ";\n"

    return sql


def generate_district_sql(districts):
    """Generate SQL INSERT statements for districts."""
    if not districts:
        return ""

    sql = "-- District data\n"
    sql += "INSERT INTO tabDistrict (name, creation, modified, modified_by, owner, docstatus, idx, district_code, district_name, regency, province, regency_code) VALUES\n"

    values = []
    for district in districts:
        values.append("('{}', '{}', '{}', '{}', '{}', 0, 0, '{}', '{}', '{}', '{}', '{}')".format(
            escape_sql_string(district.name),
            district.creation.strftime('%Y-%m-%d %H:%M:%S.%f') if district.creation else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            district.modified.strftime('%Y-%m-%d %H:%M:%S.%f') if district.modified else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            escape_sql_string(district.modified_by or 'Administrator'),
            escape_sql_string(district.owner or 'Administrator'),
            escape_sql_string(district.district_code),
            escape_sql_string(district.district_name),
            escape_sql_string(district.regency or ''),
            escape_sql_string(district.province or ''),
            escape_sql_string(district.regency_code or '')
        ))

    sql += ",\n".join(values)
    sql += ";\n"

    return sql


def generate_village_sql(villages):
    """Generate SQL INSERT statements for villages."""
    if not villages:
        return ""

    sql = "INSERT IGNORE INTO tabVillage (name, creation, modified, modified_by, owner, docstatus, idx, village_code, village_name, district, regency, province, district_code) VALUES\n"

    values = []
    for village in villages:
        values.append("('{}', '{}', '{}', '{}', '{}', 0, 0, '{}', '{}', '{}', '{}', '{}', '{}')".format(
            escape_sql_string(village.name),
            village.creation.strftime('%Y-%m-%d %H:%M:%S.%f') if village.creation else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            village.modified.strftime('%Y-%m-%d %H:%M:%S.%f') if village.modified else now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f'),
            escape_sql_string(village.modified_by or 'Administrator'),
            escape_sql_string(village.owner or 'Administrator'),
            escape_sql_string(village.village_code),
            escape_sql_string(village.village_name),
            escape_sql_string(village.district or ''),
            escape_sql_string(village.regency or ''),
            escape_sql_string(village.province or ''),
            escape_sql_string(village.district_code or '')
        ))

    sql += ",\n".join(values)
    sql += ";\n"

    return sql


def escape_sql_string(value):
    """Escape single quotes and other special characters in SQL strings."""
    if value is None:
        return ''
    return str(value).replace("'", "''").replace("\\", "\\\\")


def convert_csv_to_sql():
    """Convert existing CSV files to SQL format."""
    print("Converting CSV files to SQL format...")

    app_path = frappe.get_app_path("indo_geo")
    data_path = os.path.join(app_path, "..", "data")
    sql_path = os.path.join(data_path, "sql")

    # Create SQL directory if it doesn't exist
    os.makedirs(sql_path, exist_ok=True)

    # Convert each CSV file
    convert_provinces_csv_to_sql(data_path, sql_path)
    convert_regencies_csv_to_sql(data_path, sql_path)
    convert_districts_csv_to_sql(data_path, sql_path)
    convert_villages_csv_to_sql(data_path, sql_path)

    print("CSV to SQL conversion completed!")


def convert_provinces_csv_to_sql(data_path, sql_path):
    """Convert provinces.csv to provinces.sql."""
    import csv

    csv_file = os.path.join(data_path, "provinces.csv")
    sql_file = os.path.join(sql_path, "provinces.sql")

    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        return

    print("Converting provinces.csv...")

    with open(csv_file, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        values = []
        for row in reader:
            if len(row) != 2:
                continue

            province_code, province_name = row[0].strip(), row[1].strip()
            now_str = now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f')

            values.append(f"('{escape_sql_string(province_code)}', '{now_str}', '{now_str}', 'Administrator', 'Administrator', 0, 0, '{escape_sql_string(province_code)}', '{escape_sql_string(province_name)}')")

    if values:
        sql = "-- Provinces from CSV\n"
        sql += "INSERT INTO tabProvince (name, creation, modified, modified_by, owner, docstatus, idx, province_code, province_name) VALUES\n"
        sql += ",\n".join(values)
        sql += ";\n"

        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write(sql)

        print(f"Converted {len(values)} provinces to {sql_file}")


def convert_regencies_csv_to_sql(data_path, sql_path):
    """Convert regencies.csv to regencies.sql."""
    import csv

    csv_file = os.path.join(data_path, "regencies.csv")
    sql_file = os.path.join(sql_path, "regencies.sql")

    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        return

    print("Converting regencies.csv...")

    with open(csv_file, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        values = []
        for row in reader:
            if len(row) != 2:
                continue

            regency_code, regency_name = row[0].strip(), row[1].strip()
            province_code = regency_code[:2]
            now_str = now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f')

            values.append(f"('{escape_sql_string(regency_code)}', '{now_str}', '{now_str}', 'Administrator', 'Administrator', 0, 0, '{escape_sql_string(regency_code)}', '{escape_sql_string(regency_name)}', '{escape_sql_string(province_code)}', '{escape_sql_string(province_code)}')")

    if values:
        sql = "-- Regencies from CSV\n"
        sql += "INSERT INTO tabRegency (name, creation, modified, modified_by, owner, docstatus, idx, regency_code, regency_name, province, province_code) VALUES\n"
        sql += ",\n".join(values)
        sql += ";\n"

        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write(sql)

        print(f"Converted {len(values)} regencies to {sql_file}")


def convert_districts_csv_to_sql(data_path, sql_path):
    """Convert districts.csv to districts.sql."""
    import csv

    csv_file = os.path.join(data_path, "districts.csv")
    sql_file = os.path.join(sql_path, "districts.sql")

    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        return

    print("Converting districts.csv...")

    with open(csv_file, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        values = []
        for row in reader:
            if len(row) == 2:
                district_code, district_name = row[0].strip(), row[1].strip()
                regency_code = district_code[:4]
            elif len(row) == 3:
                district_code, district_name, regency_code = row[0].strip(), row[1].strip(), row[2].strip()
            else:
                continue

            province_code = regency_code[:2]
            now_str = now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f')

            values.append(f"('{escape_sql_string(district_code)}', '{now_str}', '{now_str}', 'Administrator', 'Administrator', 0, 0, '{escape_sql_string(district_code)}', '{escape_sql_string(district_name)}', '{escape_sql_string(regency_code)}', '{escape_sql_string(province_code)}', '{escape_sql_string(regency_code)}')")

    if values:
        sql = "-- Districts from CSV\n"
        sql += "INSERT INTO tabDistrict (name, creation, modified, modified_by, owner, docstatus, idx, district_code, district_name, regency, province, regency_code) VALUES\n"
        sql += ",\n".join(values)
        sql += ";\n"

        with open(sql_file, 'w', encoding='utf-8') as f:
            f.write(sql)

        print(f"Converted {len(values)} districts to {sql_file}")


def convert_villages_csv_to_sql(data_path, sql_path):
    """Convert villages.csv to villages.sql."""
    import csv

    csv_file = os.path.join(data_path, "villages.csv")
    sql_file = os.path.join(sql_path, "villages.sql")

    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        return

    print("Converting villages.csv...")

    chunk_size = 1000
    chunk_num = 0

    with open(csv_file, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        with open(sql_file, 'w', encoding='utf-8') as sqlfile:
            sqlfile.write("-- Villages from CSV\n\n")

            values = []
            total_count = 0

            for row in reader:
                if len(row) == 2:
                    village_code, village_name = row[0].strip(), row[1].strip()
                    district_code = village_code[:7]
                elif len(row) == 3:
                    village_code, village_name, district_code = row[0].strip(), row[1].strip(), row[2].strip()
                else:
                    continue

                regency_code = district_code[:4]
                province_code = district_code[:2]
                now_str = now_datetime().strftime('%Y-%m-%d %H:%M:%S.%f')

                values.append(f"('{escape_sql_string(village_code)}', '{now_str}', '{now_str}', 'Administrator', 'Administrator', 0, 0, '{escape_sql_string(village_code)}', '{escape_sql_string(village_name)}', '{escape_sql_string(district_code)}', '{escape_sql_string(regency_code)}', '{escape_sql_string(province_code)}', '{escape_sql_string(district_code)}')")

                total_count += 1

                # Write in chunks to avoid memory issues
                if len(values) >= chunk_size:
                    chunk_num += 1
                    sqlfile.write(f"-- Chunk {chunk_num} ({len(values)} records)\n")
                    sqlfile.write("INSERT INTO tabVillage (name, creation, modified, modified_by, owner, docstatus, idx, village_code, village_name, district, regency, province, district_code) VALUES\n")
                    sqlfile.write(",\n".join(values))
                    sqlfile.write(";\n\n")
                    values = []

                    if chunk_num % 10 == 0:
                        print(f"  Processed {total_count} villages...")

            # Write remaining values
            if values:
                chunk_num += 1
                sqlfile.write(f"-- Chunk {chunk_num} ({len(values)} records)\n")
                sqlfile.write("INSERT INTO tabVillage (name, creation, modified, modified_by, owner, docstatus, idx, village_code, village_name, district, regency, province, district_code) VALUES\n")
                sqlfile.write(",\n".join(values))
                sqlfile.write(";\n")

    print(f"Converted {total_count} villages to {sql_file}")

