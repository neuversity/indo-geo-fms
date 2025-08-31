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
        district_code: DF.Data | None
    # end: auto-generated types
    
    def before_insert(self):
        """Called before inserting the document into the database."""
        pass
    
    def validate(self):
        """Called during document validation."""
        # Validate village code is exactly 10 digits
        if not self.village_code or not self.village_code.isdigit() or len(self.village_code) != 10:
            frappe.throw("Village Code must be exactly 10 digits")
        
        # Extract district code from village code (first 7 digits)
        self.district_code = self.village_code[:7]
        
        # Validate district code matches linked district
        if self.district:
            district_doc = frappe.get_doc("District", self.district)
            if district_doc.district_code != self.district_code:
                frappe.throw(f"District code mismatch. Village code {self.village_code} should belong to district {self.district_code}, not {district_doc.district_code}")
            
            # Set regency and province from district
            self.regency = district_doc.regency
            self.province = district_doc.province
        
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
