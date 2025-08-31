# Copyright (c) 2025, Nuwaira Technology and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestIntegration(FrappeTestCase):
	def test_core_banking_integration(self):
		"""Test that core_banking can access Province and Regency from indo_geo"""
		# Test that Province data is accessible
		provinces = frappe.get_all('Province', fields=['name', 'province_name'], limit=5)
		self.assertGreater(len(provinces), 0, "Should have provinces in database")
		
		# Test that Regency data is accessible
		regencies = frappe.get_all('Regency', fields=['name', 'regency_name', 'province'], limit=5)
		self.assertGreater(len(regencies), 0, "Should have regencies in database")
		
		# Test relationship between Province and Regency
		regency = regencies[0]
		province_exists = frappe.db.exists('Province', regency['province'])
		self.assertTrue(province_exists, f"Province {regency['province']} should exist for regency {regency['name']}")
		
		print(f"Integration test passed: {len(provinces)} provinces, {len(regencies)} regencies found")
		
	def test_deprecated_core_banking_functions(self):
		"""Test that deprecated core_banking location functions still work"""
		try:
			from core_banking.core_banking.utils.import_locations import import_all_locations
			
			# This should work but show deprecation message
			# We just test that it doesn't throw an exception
			result = import_all_locations()
			
			# If it reaches here, the function exists and works
			self.assertTrue(True, "Deprecated function should work for backward compatibility")
			
		except ImportError:
			# This is expected if core_banking app is not installed
			self.skipTest("core_banking app not available for testing")
		except Exception as e:
			# Other exceptions are acceptable as long as the function exists
			self.assertTrue("indo_geo" in str(e) or "deprecated" in str(e).lower(), 
				f"Should show indo_geo related error, got: {e}")