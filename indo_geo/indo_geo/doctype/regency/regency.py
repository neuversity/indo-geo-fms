# Copyright (c) 2025, core_banking
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Regency(Document):
    """
    Regency DocType Controller

    This class contains the business logic for the Regency DocType.
    Add your custom methods and validations here.
    """
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        province: DF.Link
        province_code: DF.Data | None
        regency_code: DF.Data
        regency_name: DF.Data
    # end: auto-generated types

    def before_insert(self):
        """Called before inserting the document into the database."""
        pass

    def validate(self):
        """Called during document validation."""
        # Validate regency code is exactly 4 digits
        if not self.regency_code or not self.regency_code.isdigit() or len(self.regency_code) != 4:
            frappe.throw("Regency Code must be exactly 4 digits")

        # Extract province code from regency code (first 2 digits)
        self.province_code = self.regency_code[:2]

        # Validate province code matches linked province
        if self.province:
            province_doc = frappe.get_doc("Province", self.province)
            if province_doc.province_code != self.province_code:
                frappe.throw(f"Province code mismatch. Regency code {self.regency_code} should belong to province {self.province_code}, not {province_doc.province_code}")

        # Set title for display
        self.title = self.regency_name

    def before_save(self):
        """Called before saving the document."""
        pass

    def after_insert(self):
        """Called after inserting the document into the database."""
        pass

    def on_update(self):
        """Called after updating the document."""
        pass

    def on_trash(self):
        """Called when the document is being deleted."""
        pass



@frappe.whitelist()
def get_regencies(province=None):
    """Get regencies filtered by province for autocomplete"""
    try:
        filters = {}
        if province:
            filters["province"] = province

        regencies = frappe.get_all(
            "Regency",
            filters=filters,
            fields=["name", "regency_name", "regency_code", "province"],
            order_by="regency_name asc"
        )
        return {"status": "success", "data": regencies}
    except Exception as e:
        frappe.log_error(f"Error fetching regencies: {e!s}")
        return {"status": "error", "message": _("Error fetching regencies")}

