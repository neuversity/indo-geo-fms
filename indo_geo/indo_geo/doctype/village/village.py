# Copyright (c) 2025, core_banking
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Village(Document):
    """
    Village DocType Controller

    This class contains the business logic for the Village DocType.
    Add your custom methods and validations here.
    """
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        village_code: DF.Data
        village_name: DF.Data
        district: DF.Link
        regency: DF.Link | None
        province: DF.Link | None
    # end: auto-generated types

    def before_insert(self):
        """Called before inserting the document into the database."""
        pass

    def validate(self):
        """Called during document validation."""
        # Validate village code is exactly 10 digits
        if not self.village_code or not self.village_code.isdigit() or len(self.village_code) != 10:
            frappe.throw("Village Code must be exactly 10 digits")

        # Set title for display
        self.title = self.village_name

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
