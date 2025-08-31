import csv
import frappe
import os
from frappe.utils import cint


def import_all_locations():
    """Import all location data from CSV files."""
    print("Starting location data import...")
    
    # Get the app path
    app_path = frappe.get_app_path("indo_geo")
    data_path = os.path.join(app_path, "..", "data")
    
    # Import in order: Province -> Regency -> District -> Village
    import_provinces(data_path)
    import_regencies(data_path)
    
    print("Location data import completed successfully!")


def import_provinces(data_path):
    """Import provinces from CSV file."""
    file_path = os.path.join(data_path, "provinces.csv")
    
    if not os.path.exists(file_path):
        frappe.throw(f"Province data file not found: {file_path}")
    
    print("Importing provinces...")
    count = 0
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
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
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
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


def get_data_counts():
    """Get count of records in CSV files."""
    app_path = frappe.get_app_path("indo_geo")
    data_path = os.path.join(app_path, "..", "data")
    
    counts = {}
    
    # Count provinces
    file_path = os.path.join(data_path, "provinces.csv")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            counts['provinces'] = sum(1 for row in csv.reader(csvfile) if len(row) == 2)
    
    # Count regencies
    file_path = os.path.join(data_path, "regencies.csv")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            counts['regencies'] = sum(1 for row in csv.reader(csvfile) if len(row) == 2)
    
    return counts


def clear_all_locations():
    """Clear all location data (for testing purposes)."""
    print("Clearing all location data...")
    
    # Delete in reverse order: Regency -> Province
    frappe.db.delete("Regency", {"name": ("!=", "")})
    frappe.db.delete("Province", {"name": ("!=", "")})
    
    frappe.db.commit()
    print("All location data cleared")