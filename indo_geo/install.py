import frappe

from indo_geo.indo_geo.utils.import_locations import import_all_locations, import_all_locations_sql


def after_install():
    """Import location data after app installation."""
    try:
        print("Starting post-installation setup for Indo Geo...")
        import_all_locations()
        print("Indo Geo setup completed successfully!")
    except Exception as e:
        frappe.log_error(f"Error during Indo Geo setup: {e!s}")
        print(f"Error during setup: {e!s}")
        raise

