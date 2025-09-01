# Copyright (c) 2025, Nuwaira Technology and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

from indo_geo.indo_geo.utils.import_locations import clear_all_locations, get_data_counts
from indo_geo.install import after_install


class TestInstall(FrappeTestCase):
	def test_after_install_script(self):
		"""Test the after_install script imports data correctly."""
		# Clear existing data first
		clear_all_locations()

		# Verify data is cleared
		self.assertEqual(frappe.db.count('Province'), 0, "Provinces should be cleared")
		self.assertEqual(frappe.db.count('Regency'), 0, "Regencies should be cleared")

		# Run the install script
		after_install()

		# Verify data was imported
		data_counts = get_data_counts()

		# Check provinces
		expected_provinces = data_counts.get('provinces', 0)
		actual_provinces = frappe.db.count('Province')
		self.assertEqual(actual_provinces, expected_provinces,
			f"Province count mismatch after install: expected {expected_provinces}, got {actual_provinces}")

		# Check regencies
		expected_regencies = data_counts.get('regencies', 0)
		actual_regencies = frappe.db.count('Regency')
		self.assertEqual(actual_regencies, expected_regencies,
			f"Regency count mismatch after install: expected {expected_regencies}, got {actual_regencies}")

		print(f"Install test passed: {actual_provinces} provinces, {actual_regencies} regencies imported")

	def test_install_idempotent(self):
		"""Test that running install multiple times doesn't create duplicates."""
		# Run install twice
		after_install()
		initial_provinces = frappe.db.count('Province')
		initial_regencies = frappe.db.count('Regency')

		after_install()  # Second run
		final_provinces = frappe.db.count('Province')
		final_regencies = frappe.db.count('Regency')

		# Counts should remain the same
		self.assertEqual(initial_provinces, final_provinces,
			"Province count should not change on second install")
		self.assertEqual(initial_regencies, final_regencies,
			"Regency count should not change on second install")

