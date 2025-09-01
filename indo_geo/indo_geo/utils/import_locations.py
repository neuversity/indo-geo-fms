import csv
import os
import time

import frappe
from frappe.utils import cint


def import_all_locations():
    """Import all location data from CSV files."""
    print("Starting location data import...")

    import_all_locations_sql()

    # # Get the app path
    # app_path = frappe.get_app_path("indo_geo")
    # data_path = os.path.join(app_path, "..", "data")
    #
    # # Import in order: Province -> Regency -> District -> Village
    # import_provinces(data_path)
    # import_regencies(data_path)
    # import_districts(data_path)
    # import_villages(data_path)
    #
    # print("Location data import completed successfully!")


def import_provinces(data_path):
    """Import provinces from CSV file."""
    file_path = os.path.join(data_path, "provinces.csv")

    if not os.path.exists(file_path):
        frappe.throw(f"Province data file not found: {file_path}")

    print("Importing provinces...")
    count = 0

    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 2:
                continue

            province_code, province_name = row[0].strip(), row[1].strip()

            # Check if already exists
            if frappe.db.exists("Province", province_code):
                continue

            # Create new province
            doc = frappe.new_doc("Province")
            doc.province_code = province_code
            doc.province_name = province_name
            doc.insert(ignore_permissions=True)
            count += 1

            if count % 10 == 0:
                frappe.db.commit()

    frappe.db.commit()
    print(f"Imported {count} provinces")


def import_regencies(data_path):
    """Import regencies from CSV file."""
    file_path = os.path.join(data_path, "regencies.csv")

    if not os.path.exists(file_path):
        frappe.throw(f"Regency data file not found: {file_path}")

    print("Importing regencies...")
    count = 0
    errors = []

    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) != 2:
                continue

            regency_code, regency_name = row[0].strip(), row[1].strip()

            # Check if already exists
            if frappe.db.exists("Regency", regency_code):
                continue

            # Extract province code
            province_code = regency_code[:2]

            # Check if province exists
            if not frappe.db.exists("Province", province_code):
                errors.append(f"Province {province_code} not found for regency {regency_code}")
                continue

            # Create new regency
            doc = frappe.new_doc("Regency")
            doc.regency_code = regency_code
            doc.regency_name = regency_name
            doc.province = province_code
            doc.insert(ignore_permissions=True)
            count += 1

            if count % 50 == 0:
                frappe.db.commit()

    frappe.db.commit()
    print(f"Imported {count} regencies")

    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors[:10]:
            print(f"  - {error}")
#
def import_districts(data_path):
    """Import districts from CSV file."""
    file_path = os.path.join(data_path, "districts.csv")
    if not os.path.exists(file_path):
        frappe.throw(f"District data file not found: {file_path}")
    print("Importing districts...")
    count = 0
    errors = []
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Handle both 2-column (actual data) and 3-column (test data) formats
            if len(row) == 2:
                # Actual data format: district_code, district_name
                district_code, district_name = row[0].strip(), row[1].strip()
                # Extract regency code from district code (first 4 digits)
                regency_code = district_code[:4]
            elif len(row) == 3:
                # Test data format: district_code, district_name, regency_code
                district_code, district_name, regency_code = row[0].strip(), row[1].strip(), row[2].strip()
            else:
                continue

            # Check if already exists
            if frappe.db.exists("District", district_code):
                continue
            # Check if regency exists
            if not frappe.db.exists("Regency", regency_code):
                errors.append(f"Regency {regency_code} not found for district {district_code}")
                continue
            # Create new district
            doc = frappe.new_doc("District")
            doc.district_code = district_code
            doc.district_name = district_name
            doc.regency = regency_code
            doc.province = regency_code[:2]  # Province code is first 2 digits of regency code
            doc.insert(ignore_permissions=True)
            count += 1
            if count % 100 == 0:
                frappe.db.commit()
    frappe.db.commit()
    print(f"Imported {count} districts")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors[:10]:
            print(f"  - {error}")

def import_villages(data_path):
    """Import villages from CSV file."""
    file_path = os.path.join(data_path, "villages.csv")
    if not os.path.exists(file_path):
        frappe.throw(f"Village data file not found: {file_path}")
    print("Importing villages...")
    count = 0
    errors = []
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Handle both 2-column (actual data) and 3-column (test data) formats
            if len(row) == 2:
                # Actual data format: village_code, village_name
                village_code, village_name = row[0].strip(), row[1].strip()
                # Extract district code from village code (first 7 digits)
                district_code = village_code[:7]
            elif len(row) == 3:
                # Test data format: village_code, village_name, district_code
                village_code, village_name, district_code = row[0].strip(), row[1].strip(), row[2].strip()
            else:
                continue

            # Check if already exists
            if frappe.db.exists("Village", village_code):
                continue
            # Check if district exists
            if not frappe.db.exists("District", district_code):
                errors.append(f"District {district_code} not found for village {village_code}")
                continue
            # Create new village
            doc = frappe.new_doc("Village")
            doc.village_code = village_code
            doc.village_name = village_name
            doc.district = district_code
            doc.regency = district_code[:4]  # Regency code is first 4 digits of district code
            doc.province = district_code[:2]  # Province code is first 2 digits of district code
            doc.insert(ignore_permissions=True)
            count += 1
            if count % 200 == 0:
                frappe.db.commit()
    frappe.db.commit()
    print(f"Imported {count} villages")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors[:10]:
            print(f"  - {error}")

def get_data_counts():
    """Get count of records in CSV files."""
    app_path = frappe.get_app_path("indo_geo")
    data_path = os.path.join(app_path, "..", "data")

    counts = {}

    # Count provinces
    file_path = os.path.join(data_path, "provinces.csv")
    if os.path.exists(file_path):
        with open(file_path, encoding='utf-8') as csvfile:
            counts['provinces'] = sum(1 for row in csv.reader(csvfile) if len(row) == 2)

    # Count regencies
    file_path = os.path.join(data_path, "regencies.csv")
    if os.path.exists(file_path):
        with open(file_path, encoding='utf-8') as csvfile:
            counts['regencies'] = sum(1 for row in csv.reader(csvfile) if len(row) == 2)

    return counts


# ===============================================
# SQL BULK IMPORT METHODS (HIGH PERFORMANCE)
# ===============================================

def import_all_locations_sql():
    """Import all location data using SQL bulk import (fast method)."""
    print("Starting HIGH-PERFORMANCE SQL bulk import...")
    start_time = time.time()

    # Get the app path
    app_path = frappe.get_app_path("indo_geo")
    sql_path = os.path.join(app_path, "..", "data", "sql")

    if not os.path.exists(sql_path):
        print(f"SQL directory not found: {sql_path}")
        print("Please run dump_locations.convert_csv_to_sql() first to generate SQL files")
        return

    # Import in order: Province -> Regency -> District -> Village
    import_provinces_sql(sql_path)
    import_regencies_sql(sql_path)
    import_districts_sql(sql_path)
    import_villages_sql(sql_path)

    end_time = time.time()
    print(f"HIGH-PERFORMANCE SQL bulk import completed in {end_time - start_time:.2f} seconds!")


def import_provinces_sql(sql_path):
    """Import provinces using SQL bulk insert."""
    file_path = os.path.join(sql_path, "provinces.sql")

    if not os.path.exists(file_path):
        print(f"SQL file not found: {file_path}")
        return

    print("Bulk importing provinces...")
    start_time = time.time()

    # Check if data already exists
    existing_count = frappe.db.count("Province")
    if existing_count > 0:
        print(f"Found {existing_count} existing provinces. Skipping import to avoid duplicates.")
        return

    # Execute SQL file
    with open(file_path, encoding='utf-8') as f:
        sql_content = f.read()

    if sql_content.strip():
        frappe.db.sql(sql_content)
        frappe.db.commit()

    # Get count of imported records
    imported_count = frappe.db.count("Province")
    end_time = time.time()

    print(f"Bulk imported {imported_count} provinces in {end_time - start_time:.2f} seconds")


def import_regencies_sql(sql_path):
    """Import regencies using SQL bulk insert."""
    file_path = os.path.join(sql_path, "regencies.sql")

    if not os.path.exists(file_path):
        print(f"SQL file not found: {file_path}")
        return

    print("Bulk importing regencies...")
    start_time = time.time()

    # Check if data already exists
    existing_count = frappe.db.count("Regency")
    if existing_count > 0:
        print(f"Found {existing_count} existing regencies. Skipping import to avoid duplicates.")
        return

    # Validate dependencies first
    province_count = frappe.db.count("Province")
    if province_count == 0:
        print("Error: No provinces found. Please import provinces first.")
        return

    # Execute SQL file
    with open(file_path, encoding='utf-8') as f:
        sql_content = f.read()

    if sql_content.strip():
        frappe.db.sql(sql_content)
        frappe.db.commit()

    # Get count of imported records
    imported_count = frappe.db.count("Regency")
    end_time = time.time()

    print(f"Bulk imported {imported_count} regencies in {end_time - start_time:.2f} seconds")


def import_districts_sql(sql_path):
    """Import districts using SQL bulk insert."""
    file_path = os.path.join(sql_path, "districts.sql")

    if not os.path.exists(file_path):
        print(f"SQL file not found: {file_path}")
        return

    print("Bulk importing districts...")
    start_time = time.time()

    # Check if data already exists
    existing_count = frappe.db.count("District")
    if existing_count > 0:
        print(f"Found {existing_count} existing districts. Skipping import to avoid duplicates.")
        return

    # Validate dependencies first
    regency_count = frappe.db.count("Regency")
    if regency_count == 0:
        print("Error: No regencies found. Please import regencies first.")
        return

    # Execute SQL file
    with open(file_path, encoding='utf-8') as f:
        sql_content = f.read()

    if sql_content.strip():
        frappe.db.sql(sql_content)
        frappe.db.commit()

    # Get count of imported records
    imported_count = frappe.db.count("District")
    end_time = time.time()

    print(f"Bulk imported {imported_count} districts in {end_time - start_time:.2f} seconds")


def import_villages_sql(sql_path):
    """Import villages using SQL bulk insert."""
    file_path = os.path.join(sql_path, "villages.sql")

    if not os.path.exists(file_path):
        print(f"SQL file not found: {file_path}")
        return

    print("Bulk importing villages...")
    start_time = time.time()

    # Check if data already exists
    existing_count = frappe.db.count("Village")
    if existing_count > 0:
        print(f"Found {existing_count} existing villages. Skipping import to avoid duplicates.")
        return

    # Validate dependencies first
    district_count = frappe.db.count("District")
    if district_count == 0:
        print("Error: No districts found. Please import districts first.")
        return

    # Execute SQL file in chunks to avoid memory issues
    print("Reading village SQL file...")
    with open(file_path, encoding='utf-8') as f:
        content = f.read()

    # Split by chunks (look for "-- Chunk" markers)
    chunks = []
    current_chunk = []

    for line in content.split('\n'):
        if line.strip().startswith('-- Chunk') and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
        current_chunk.append(line)

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    # Execute each chunk
    total_chunks = len([c for c in chunks if 'INSERT INTO' in c])
    if total_chunks == 0:
        # Fallback: execute entire file
        print("No chunks found, executing entire file...")
        if content.strip():
            frappe.db.sql(content)
            frappe.db.commit()
    else:
        print(f"Executing {total_chunks} chunks...")
        for i, chunk in enumerate(chunks, 1):
            if 'INSERT INTO' in chunk:
                print(f"  Processing chunk {i}/{total_chunks}...")
                frappe.db.sql(chunk)
                if i % 5 == 0:  # Commit every 5 chunks
                    frappe.db.commit()

        frappe.db.commit()

    # Get count of imported records
    imported_count = frappe.db.count("Village")
    end_time = time.time()

    print(f"Bulk imported {imported_count} villages in {end_time - start_time:.2f} seconds")


def benchmark_import_methods():
    """Benchmark CSV vs SQL import methods."""
    print("=" * 60)
    print("IMPORT PERFORMANCE BENCHMARK")
    print("=" * 60)

    # Clear existing data
    clear_all_locations()

    print("\n1. Testing CSV Import Method (Original)...")
    start_time = time.time()
    import_all_locations()
    csv_time = time.time() - start_time
    csv_counts = get_location_counts()

    # Clear and test SQL method
    clear_all_locations()

    print("\n2. Testing SQL Import Method (Optimized)...")
    start_time = time.time()
    import_all_locations_sql()
    sql_time = time.time() - start_time
    sql_counts = get_location_counts()

    # Results
    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print("CSV Import Method:")
    print(f"  Time: {csv_time:.2f} seconds")
    print(f"  Records: {csv_counts}")
    print("\nSQL Import Method:")
    print(f"  Time: {sql_time:.2f} seconds")
    print(f"  Records: {sql_counts}")

    if sql_time > 0:
        improvement = ((csv_time - sql_time) / csv_time) * 100
        speedup = csv_time / sql_time
        print("\nPerformance Improvement:")
        print(f"  Speed increase: {speedup:.1f}x faster")
        print(f"  Time reduction: {improvement:.1f}%")

        # Projection for 80K villages
        if 'villages' in csv_counts and csv_counts['villages'] > 0:
            villages_per_second_csv = csv_counts['villages'] / csv_time
            villages_per_second_sql = sql_counts['villages'] / sql_time

            estimated_80k_csv = 80000 / villages_per_second_csv
            estimated_80k_sql = 80000 / villages_per_second_sql

            print("\nProjection for 80,000 Villages:")
            print(f"  CSV method: ~{estimated_80k_csv/60:.1f} minutes")
            print(f"  SQL method: ~{estimated_80k_sql/60:.1f} minutes")


def get_location_counts():
    """Get counts of location records in database."""
    return {
        'provinces': frappe.db.count("Province"),
        'regencies': frappe.db.count("Regency"),
        'districts': frappe.db.count("District"),
        'villages': frappe.db.count("Village")
    }


def clear_all_locations():
    """Clear all location data (for testing purposes)."""
    print("Clearing all location data...")

    # Delete in reverse order to respect foreign key constraints
    frappe.db.delete("Village", {"name": ("!=", "")})
    frappe.db.delete("District", {"name": ("!=", "")})
    frappe.db.delete("Regency", {"name": ("!=", "")})
    frappe.db.delete("Province", {"name": ("!=", "")})

    frappe.db.commit()
    print("All location data cleared")

