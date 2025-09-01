# Copyright (c) 2025, Nuwaira Technology and Contributors
# See license.txt

import csv
import os
import tempfile

import frappe
from frappe.tests.utils import FrappeTestCase

test_records = frappe.get_test_records("Village")


class TestVillage(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		"""Set up test data once for all test methods."""
		super().setUpClass()
		# Load test records for dependencies
		frappe.get_test_records("Province")
		frappe.get_test_records("Regency")
		frappe.get_test_records("District")
		frappe.get_test_records("Village")

		# Ensure the test districts exist for village tests
		for district_code, district_name in [("9901001", "_Test District 1"), ("9901002", "_Test District 2")]:
			if not frappe.db.exists("District", district_code):
				district = frappe.new_doc("District")
				district.district_code = district_code
				district.district_name = district_name
				district.regency = "9901"
				district.province = "99"
				district.insert(ignore_permissions=True)
				frappe.db.commit()

	def test_import_villages(self):
		"""Test importing villages from CSV file."""
		from indo_geo.indo_geo.utils.import_locations import import_villages

		# Create a temporary CSV file with test data
		with tempfile.TemporaryDirectory() as temp_dir:
			csv_file = os.path.join(temp_dir, "villages.csv")

			# Write test data to CSV
			test_data = [
				["9901001101", "_Test Import Village 1", "9901001"],
				["9901001102", "_Test Import Village 2", "9901001"],
				["9901002101", "_Test Import Village 3", "9901002"]
			]

			with open(csv_file, 'w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				for row in test_data:
					writer.writerow(row)

			# Import villages
			import_villages(temp_dir)

			# Verify villages were imported
			for row in test_data:
				village_code = row[0]
				village_name = row[1]
				district_code = row[2]

				# Check if village exists
				self.assertTrue(
					frappe.db.exists("Village", village_code),
					f"Village {village_code} should have been imported"
				)

				# Verify village data
				village = frappe.get_doc("Village", village_code)
				self.assertEqual(village.village_name, village_name)
				self.assertEqual(village.district, district_code)
				self.assertEqual(village.regency, "9901")  # Regency code from district
				self.assertEqual(village.province, "99")  # Province code from district

	def test_import_villages_with_missing_district(self):
		"""Test importing villages when district doesn't exist."""
		from indo_geo.indo_geo.utils.import_locations import import_villages

		# Create a temporary CSV file with village referencing non-existent district
		with tempfile.TemporaryDirectory() as temp_dir:
			csv_file = os.path.join(temp_dir, "villages.csv")

			# Write test data with non-existent district
			test_data = [
				["8801010001", "_Test Invalid Village", "8801010"]  # District 8801010 doesn't exist
			]

			with open(csv_file, 'w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				for row in test_data:
					writer.writerow(row)

			# Import should handle missing district gracefully
			import_villages(temp_dir)

			# Verify village was not imported
			self.assertFalse(
				frappe.db.exists("Village", "8801010001"),
				"Village with invalid district should not be imported"
			)

	def test_import_villages_duplicate_handling(self):
		"""Test that duplicate villages are not imported twice."""
		from indo_geo.indo_geo.utils.import_locations import import_villages

		# Create a test village first
		if not frappe.db.exists("Village", "9901001099"):
			village = frappe.new_doc("Village")
			village.village_code = "9901001099"
			village.village_name = "_Test Existing Village"
			village.district = "9901001"
			village.regency = "9901"
			village.province = "99"
			village.insert(ignore_permissions=True)
			frappe.db.commit()

		# Create a temporary CSV file with the same village
		with tempfile.TemporaryDirectory() as temp_dir:
			csv_file = os.path.join(temp_dir, "villages.csv")

			test_data = [
				["9901001099", "_Test Updated Village Name", "9901001"]
			]

			with open(csv_file, 'w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				for row in test_data:
					writer.writerow(row)

			# Import villages
			import_villages(temp_dir)

			# Verify the village name wasn't updated (duplicate handling)
			village = frappe.get_doc("Village", "9901001099")
			self.assertEqual(
				village.village_name,
				"_Test Existing Village",
				"Existing village should not be updated"
			)

	def test_import_villages_regency_province_extraction(self):
		"""Test that regency and province codes are correctly extracted from district code."""
		from indo_geo.indo_geo.utils.import_locations import import_villages

		# Create a temporary CSV file
		with tempfile.TemporaryDirectory() as temp_dir:
			csv_file = os.path.join(temp_dir, "villages.csv")

			test_data = [
				["9901002101", "_Test Village Extract", "9901002"]
			]

			with open(csv_file, 'w', newline='', encoding='utf-8') as f:
				writer = csv.writer(f)
				for row in test_data:
					writer.writerow(row)

			# Import villages
			import_villages(temp_dir)

			# Verify codes were correctly extracted
			if frappe.db.exists("Village", "9901002101"):
				village = frappe.get_doc("Village", "9901002101")
				self.assertEqual(
					village.regency,
					"9901",  # First 4 digits of district code
					"Regency code should be extracted from district code"
				)
				self.assertEqual(
					village.province,
					"99",  # First 2 digits of district code
					"Province code should be extracted from district code"
				)

	def tearDown(self):
		"""Clean up test data."""
		# Delete test villages created during import tests
		test_villages = frappe.db.get_list(
			"Village",
			filters={"village_name": ("like", "%_Test Import%")},
			pluck="name"
		)
		test_villages.extend(frappe.db.get_list(
			"Village",
			filters={"village_name": ("like", "%_Test Existing%")},
			pluck="name"
		))
		test_villages.extend(frappe.db.get_list(
			"Village",
			filters={"village_name": ("like", "%_Test Village Extract%")},
			pluck="name"
		))

		for village_code in test_villages:
			frappe.delete_doc("Village", village_code, force=True, ignore_permissions=True)

		# Delete specific test villages
		for code in ["9901001099", "9901002101"]:
			if frappe.db.exists("Village", code):
				frappe.delete_doc("Village", code, force=True, ignore_permissions=True)

		frappe.db.commit()

