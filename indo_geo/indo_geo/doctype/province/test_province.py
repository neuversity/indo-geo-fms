# Copyright (c) 2025, Nuwaira Technology and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from indo_geo.indo_geo.utils.import_locations import get_data_counts


class TestProvince(FrappeTestCase):
	def test_province_data_import(self):
		"""Test that all provinces from CSV are imported."""
		# Get expected count from CSV
		data_counts = get_data_counts()
		expected_count = data_counts.get('provinces', 0)
		
		# Get actual count from database (excluding test records)
		actual_count = frappe.db.count('Province', {'name': ('not like', '%_Test%'), 'province_name': ('not like', '%_Test%')})
		
		# Verify counts match
		self.assertEqual(actual_count, expected_count, 
			f"Province count mismatch: expected {expected_count}, got {actual_count}")
		
		# Test specific provinces exist
		self.assertTrue(frappe.db.exists('Province', '11'), "Province 11 (Aceh) should exist")
		self.assertTrue(frappe.db.exists('Province', '32'), "Province 32 (Jawa Barat) should exist")
		
	def test_province_structure(self):
		"""Test province data structure."""
		if frappe.db.count('Province') > 0:
			# Get first province
			province = frappe.get_doc('Province', frappe.db.get_list('Province', limit=1)[0].name)
			
			# Check required fields
			self.assertTrue(province.province_code, "Province code should not be empty")
			self.assertTrue(province.province_name, "Province name should not be empty")
			self.assertEqual(len(province.province_code), 2, "Province code should be 2 characters")
