"""Indo Geo App Installation Script

This script automatically populates Indonesian administrative division data
when the indo_geo app is installed.
"""

import csv
import os
import frappe
from frappe import _


def after_install():
    """Main installation function that imports all location data"""
    print("🏗️  Starting Indo Geo data installation...")
    
    try:
        # Create data import functions
        import_provinces()
        import_regencies()
        import_districts()
        import_villages()
        
        frappe.db.commit()
        print("✅ Indo Geo installation completed successfully!")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Indo Geo Installation Failed")
        print(f"❌ Installation failed: {str(e)}")
        raise


def get_data_file_path(filename):
    """Get absolute path to data file"""
    app_path = frappe.get_app_path("indo_geo")
    return os.path.join(app_path, "..", "data", filename)


def import_provinces():
    """Import provinces data from CSV"""
    print("📍 Importing provinces...")
    
    file_path = get_data_file_path("provinces.csv")
    if not os.path.exists(file_path):
        print(f"⚠️  Province data file not found: {file_path}")
        return
    
    count = 0
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            if len(row) >= 2:
                province_code = row[0]
                province_name = row[1]
                
                # Check if province already exists
                if not frappe.db.exists("Province", province_code):
                    doc = frappe.get_doc({
                        "doctype": "Province",
                        "province_code": province_code,
                        "province_name": province_name
                    })
                    doc.insert()
                    count += 1
    
    print(f"   ✓ Imported {count} provinces")


def import_regencies():
    """Import regencies data from CSV"""
    print("🏘️  Importing regencies...")
    
    file_path = get_data_file_path("regencies.csv")
    if not os.path.exists(file_path):
        print(f"⚠️  Regency data file not found: {file_path}")
        return
    
    count = 0
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            if len(row) >= 2:
                regency_code = row[0]
                regency_name = row[1]
                province_code = regency_code[:2]  # First 2 digits for province
                
                # Get province name
                province = frappe.db.get_value("Province", province_code, "name")
                if not province:
                    print(f"⚠️  Province {province_code} not found for regency {regency_code}")
                    continue
                
                # Check if regency already exists
                if not frappe.db.exists("Regency", regency_code):
                    doc = frappe.get_doc({
                        "doctype": "Regency",
                        "regency_code": regency_code,
                        "regency_name": regency_name,
                        "province": province,
                        "province_code": province_code
                    })
                    doc.insert()
                    count += 1
    
    print(f"   ✓ Imported {count} regencies")


def import_districts():
    """Import districts data from CSV"""
    print("🌆 Importing districts...")
    
    file_path = get_data_file_path("districts.csv")
    if not os.path.exists(file_path):
        print(f"⚠️  District data file not found: {file_path}")
        return
    
    count = 0
    batch_size = 1000  # Process in batches to avoid memory issues
    batch_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            if len(row) >= 2:
                district_code = row[0]
                district_name = row[1]
                regency_code = district_code[:4]  # First 4 digits for regency
                province_code = district_code[:2]  # First 2 digits for province
                
                # Get regency and province
                regency = frappe.db.get_value("Regency", regency_code, "name")
                province = frappe.db.get_value("Province", province_code, "name")
                
                if not regency:
                    print(f"⚠️  Regency {regency_code} not found for district {district_code}")
                    continue
                
                # Check if district already exists
                if not frappe.db.exists("District", district_code):
                    doc = frappe.get_doc({
                        "doctype": "District",
                        "district_code": district_code,
                        "district_name": district_name,
                        "regency": regency,
                        "province": province,
                        "regency_code": regency_code
                    })
                    doc.insert()
                    count += 1
                    batch_count += 1
                    
                    # Commit every batch_size records
                    if batch_count >= batch_size:
                        frappe.db.commit()
                        batch_count = 0
                        print(f"   📦 Processed {count} districts...")
    
    print(f"   ✓ Imported {count} districts")


def import_villages():
    """Import villages data from CSV"""
    print("🏡 Importing villages (this may take a while)...")
    
    file_path = get_data_file_path("villages.csv")
    if not os.path.exists(file_path):
        print(f"⚠️  Village data file not found: {file_path}")
        return
    
    count = 0
    batch_size = 2000  # Process in larger batches for villages
    batch_count = 0
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        for row in reader:
            if len(row) >= 2:
                village_code = row[0]
                village_name = row[1]
                district_code = village_code[:7]  # First 7 digits for district
                regency_code = village_code[:4]   # First 4 digits for regency
                province_code = village_code[:2]  # First 2 digits for province
                
                # Get parent locations
                district = frappe.db.get_value("District", district_code, "name")
                regency = frappe.db.get_value("Regency", regency_code, "name")
                province = frappe.db.get_value("Province", province_code, "name")
                
                if not district:
                    print(f"⚠️  District {district_code} not found for village {village_code}")
                    continue
                
                # Check if village already exists
                if not frappe.db.exists("Village", village_code):
                    doc = frappe.get_doc({
                        "doctype": "Village",
                        "village_code": village_code,
                        "village_name": village_name,
                        "district": district,
                        "regency": regency,
                        "province": province,
                        "district_code": district_code
                    })
                    doc.insert()
                    count += 1
                    batch_count += 1
                    
                    # Commit every batch_size records
                    if batch_count >= batch_size:
                        frappe.db.commit()
                        batch_count = 0
                        print(f"   📦 Processed {count} villages...")
    
    print(f"   ✓ Imported {count} villages")