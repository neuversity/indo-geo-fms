# Copyright (c) 2025, Nuwaira Technology and Contributors
# See license.txt

import os
import tempfile
import csv
import frappe
from frappe.tests.utils import FrappeTestCase


class TestDistrict(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		"""Set up test data once for all test methods."""
		super().setUpClass()
		# Load test records for dependencies
		frappe.get_test_records("Province")
		frappe.get_test_records("Regency")
		frappe.get_test_records("District")
	
	def test_import_districts(self):
		"""Test importing districts from CSV file."""
		from indo_geo.indo_geo.utils.import_locations import import_districts
		
		# Create a temporary CSV file with test data
		with tempfile.TemporaryDirectory() as temp_dir:
			csv_file = os.path.join(temp_dir, "districts.csv")
			
			# Write test data to CSV
			test_data = [
				["9901010", "_Test Import District 1", "9901"],
				["9901020", "_Test Import District 2", "9901"],
				["9901030", "_Test Import District 3", "9901"]
			]
			
			with open(csv_file, 'w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				for row in test_data:
					writer.writerow(row)
			
			# Import districts
			import_districts(temp_dir)
			
			# Verify districts were imported
			for row in test_data:
				district_code = row[0]
				district_name = row[1]
				regency_code = row[2]
				
				# Check if district exists
				self.assertTrue(
					frappe.db.exists("District", district_code),
					f"District {district_code} should have been imported"
				)
				
				# Verify district data
				district = frappe.get_doc("District", district_code)
				self.assertEqual(district.district_name, district_name)
				self.assertEqual(district.regency, regency_code)
				self.assertEqual(district.province, "99")  # Province code from regency
	
	def test_import_districts_with_missing_regency(self):
		"""Test importing districts when regency doesn't exist."""
		from indo_geo.indo_geo.utils.import_locations import import_districts
		
		# Create a temporary CSV file with district referencing non-existent regency
		with tempfile.TemporaryDirectory() as temp_dir:
			csv_file = os.path.join(temp_dir, "districts.csv")
			
			# Write test data with non-existent regency
			test_data = [
				["8801010", "_Test Invalid District", "8801"]  # Regency 8801 doesn't exist
			]
			
			with open(csv_file, 'w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				for row in test_data:
					writer.writerow(row)
			
			# Import should handle missing regency gracefully
			import_districts(temp_dir)
			
			# Verify district was not imported
			self.assertFalse(
				frappe.db.exists("District", "8801010"),
				"District with invalid regency should not be imported"
			)
	
	def test_import_districts_duplicate_handling(self):
		"""Test that duplicate districts are not imported twice."""
		from indo_geo.indo_geo.utils.import_locations import import_districts
		
		# Create a test district first
		if not frappe.db.exists("District", "9901099"):
			district = frappe.new_doc("District")
			district.district_code = "9901099"
			district.district_name = "_Test Existing District"
			district.regency = "9901"
			district.province = "99"
			district.insert(ignore_permissions=True)
			frappe.db.commit()
		
		# Create a temporary CSV file with the same district
		with tempfile.TemporaryDirectory() as temp_dir:
			csv_file = os.path.join(temp_dir, "districts.csv")
			
			test_data = [
				["9901099", "_Test Updated District Name", "9901"]
			]
			
			with open(csv_file, 'w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				for row in test_data:
					writer.writerow(row)
			
			# Import districts
			import_districts(temp_dir)
			
			# Verify the district name wasn't updated (duplicate handling)
			district = frappe.get_doc("District", "9901099")
			self.assertEqual(
				district.district_name, 
				"_Test Existing District",
				"Existing district should not be updated"
			)
	
	def tearDown(self):
		"""Clean up test data."""
		# Delete test districts created during import tests
		test_districts = frappe.db.get_list(
			"District",
			filters={"district_name": ("like", "%_Test Import%")},
			pluck="name"
		)
		for district_code in test_districts:
			frappe.delete_doc("District", district_code, force=True, ignore_permissions=True)
		
		# Delete the duplicate test district
		if frappe.db.exists("District", "9901099"):
			frappe.delete_doc("District", "9901099", force=True, ignore_permissions=True)
		
		frappe.db.commit()