// Copyright (c) 2025, core_banking
// For license information, please see license.txt

frappe.ui.form.on('Province', {
    refresh: function(frm) {
        // Called when the form is loaded or refreshed
        
        // Example: Add custom button
        // frm.add_custom_button(__('Custom Action'), function() {
        //     frappe.msgprint('Custom button clicked!');
        // });
    },
    
    validate: function(frm) {
        // Called during form validation
        // Return false to prevent saving
    },
    
    before_save: function(frm) {
        // Called before saving the document
    },
    
    after_save: function(frm) {
        // Called after saving the document
    }
});
