import frappe
from frappe import _


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


@frappe.whitelist()
def get_districts(regency=None):
    """Get districts filtered by regency for autocomplete"""
    try:
        filters = {}
        if regency:
            filters["regency"] = regency
        districts = frappe.get_all(
            "District",
            filters=filters,
            fields=["name", "district_name", "district_code", "regency", "province"],
            order_by="district_name asc"
        )
        return {"status": "success", "data": districts}
    except Exception as e:
        frappe.log_error(f"Error fetching districts: {e!s}")
        return {"status": "error", "message": _("Error fetching districts")}

@frappe.whitelist()
def get_villages(district=None):
    """Get villages filtered by district for autocomplete"""
    try:
        filters = {}
        if district:
            filters["district"] = district
        villages = frappe.get_all(
            "Village",
            filters=filters,
            fields=["name", "village_name", "village_code", "district", "regency", "province"],
            order_by="village_name asc"
        )
        return {"status": "success", "data": villages}
    except Exception as e:
        frappe.log_error(f"Error fetching villages: {e!s}")
        return {"status": "error", "message": _("Error fetching villages")}
