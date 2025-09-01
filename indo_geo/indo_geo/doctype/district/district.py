# Copyright (c) 2025, core_banking
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class District(Document):
    """
    District DocType Controller

    This class contains the business logic for the District DocType.
    Add your custom methods and validations here.
    """
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        district_code: DF.Data
        district_name: DF.Data
        regency: DF.Link
        province: DF.Link | None
        regency_code: DF.Data | None
    # end: auto-generated types

    def before_insert(self):
        """Called before inserting the document into the database."""
        pass

    def validate(self):
        """Called during document validation."""
        # Validate district code is exactly 7 digits
        if not self.district_code or not self.district_code.isdigit() or len(self.district_code) != 7:
            frappe.throw("District Code must be exactly 7 digits")

        # Extract regency code from district code (first 4 digits)
        self.regency_code = self.district_code[:4]

        # Validate regency code matches linked regency
        if self.regency:
            regency_doc = frappe.get_doc("Regency", self.regency)
            if regency_doc.regency_code != self.regency_code:
                frappe.throw(f"Regency code mismatch. District code {self.district_code} should belong to regency {self.regency_code}, not {regency_doc.regency_code}")

            # Set province from regency
            self.province = regency_doc.province

        # Set title for display
        self.title = self.district_name

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
