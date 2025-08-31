# Copyright (c) 2025, Nuwaira Technology and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from indo_geo.indo_geo.utils.import_locations import get_data_counts


class TestRegency(FrappeTestCase):
	def test_regency_data_import(self):
		"""Test that all regencies from CSV are imported."""
		# Get expected count from CSV
		data_counts = get_data_counts()
		expected_count = data_counts.get('regencies', 0)
		
		# Get actual count from database (excluding test records)
		actual_count = frappe.db.count('Regency', {'name': ('not like', '%_Test%'), 'regency_name': ('not like', '%_Test%')})
		
		# Verify counts match
		self.assertEqual(actual_count, expected_count, 
			f"Regency count mismatch: expected {expected_count}, got {actual_count}")
		
		# Test specific regencies exist
		self.assertTrue(frappe.db.exists('Regency', '1101'), "Regency 1101 should exist")
		self.assertTrue(frappe.db.exists('Regency', '3201'), "Regency 3201 should exist")
		
	def test_regency_province_relationship(self):
		"""Test regency-province relationship."""
		if frappe.db.count('Regency') > 0:
			# Get first regency
			regency = frappe.get_doc('Regency', frappe.db.get_list('Regency', limit=1)[0].name)
			
			# Check required fields
			self.assertTrue(regency.regency_code, "Regency code should not be empty")
			self.assertTrue(regency.regency_name, "Regency name should not be empty")
			self.assertTrue(regency.province, "Province link should not be empty")
			self.assertEqual(len(regency.regency_code), 4, "Regency code should be 4 characters")
			
			# Verify province exists
			self.assertTrue(frappe.db.exists('Province', regency.province), 
				f"Linked province {regency.province} should exist")
			
			# Verify province code matches
			expected_province_code = regency.regency_code[:2]
			self.assertEqual(regency.province, expected_province_code, 
				f"Province code should match first 2 digits of regency code")
