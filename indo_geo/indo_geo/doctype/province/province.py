# Copyright (c) 2025, core_banking
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Province(Document):
    """
    Province DocType Controller

    This class contains the business logic for the Province DocType.
    Add your custom methods and validations here.
    """
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        province_code: DF.Data
        province_name: DF.Data
    # end: auto-generated types

    def before_insert(self):
        """Called before inserting the document into the database."""
        pass

    def validate(self):
        """Called during document validation."""
        # Validate province code is exactly 2 digits
        if not self.province_code or not self.province_code.isdigit() or len(self.province_code) != 2:
            frappe.throw("Province Code must be exactly 2 digits")

        # Set title for display
        self.title = self.province_name

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
def get_provinces():
    """Get all provinces for autocomplete"""
    try:
        provinces = frappe.get_all(
            "Province",
            fields=["name", "province_name", "province_code"],
            order_by="province_name asc"
        )
        return {"status": "success", "data": provinces}
    except Exception as e:
        frappe.log_error(f"Error fetching provinces: {e!s}")
        return {"status": "error", "message": _("Error fetching provinces")}

