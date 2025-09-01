# Indo Geo

A Frappe application providing comprehensive Indonesian administrative division data with hierarchical structure and validation.

## Overview

Indo Geo manages Indonesia's complete 4-tier administrative hierarchy:

- **Province** (Provinsi) - 33 provinces
- **Regency/City** (Kabupaten/Kota) - 514 regencies
- **District** (Kecamatan) - 7,215 districts
- **Village** (Desa/Kelurahan) - 80,534 villages

Total: 88,296+ administrative division records with validated hierarchical relationships.

## Features

### Complete Administrative Data

- All Indonesian provinces, regencies, districts, and villages
- Hierarchical relationships with automatic validation
- Standard Indonesian administrative codes (Kemendagri format)

### Smart Hierarchical Linking

- Automatic parent reference population
- Code-based relationship validation
- Prevents inconsistent hierarchical data

### API Integration

- RESTful endpoints for data retrieval
- Hierarchical filtering support
- Optimized for autocomplete functionality
- Cross-app integration ready

## Installation

### Prerequisites

- Frappe Framework 15.x
- Python 3.10+
- ERPNext (optional but recommended)

### Install Steps

1. **Get the app**

```bash
cd frappe-bench
bench get-app https://github.com/neuversity/indo-geo-fms.git
```

2. **Install on site**

```bash
bench --site your-site install-app indo_geo
```

The installation will automatically import all location data from CSV files.

### Manual Data Import

If you need to reimport the data:

```bash
bench --site your-site execute indo_geo.indo_geo.utils.import_locations.import_all_locations
```

## Data Structure

### Administrative Code Format

Indonesian administrative codes follow a nested pattern:

| Level    | Code Format  | Example      | Description                  |
| -------- | ------------ | ------------ | ---------------------------- |
| Province | `XX`         | `32`         | 2-digit province code        |
| Regency  | `XXXX`       | `3201`       | 4-digit (includes province)  |
| District | `XXXXXXX`    | `3201010`    | 7-digit (includes regency)   |
| Village  | `XXXXXXXXXX` | `3201010001` | 10-digit (includes district) |

### DocType Fields

#### Province

- `province_code` - 2-digit code
- `province_name` - Province name

#### Regency

- `regency_code` - 4-digit code
- `regency_name` - Regency/City name
- `province` - Link to Province

#### District

- `district_code` - 7-digit code
- `district_name` - District name
- `regency` - Link to Regency
- `province` - Auto-populated from Regency

#### Village

- `village_code` - 10-digit code
- `village_name` - Village name
- `district` - Link to District
- `regency` - Auto-populated from District
- `province` - Auto-populated from District

## API Usage

### Python API

```python
import frappe
from indo_geo.api import get_provinces, get_regencies, get_districts, get_villages

# Get all provinces
provinces = get_provinces()

# Get regencies in a province
regencies = get_regencies(province='32')

# Get districts in a regency
districts = get_districts(regency="3201")

# Get villages in a district
villages = get_villages(district="3201010")
```

### REST API Endpoints

```javascript
// Get all provinces
GET /api/method/indo_geo.api.get_provinces

// Get regencies by province
GET /api/method/indo_geo.api.get_regencies?province=DKI%20Jakarta

// Get districts by regency
GET /api/method/indo_geo.api.get_districts?regency=Jakarta%20Selatan

// Get villages by district
GET /api/method/indo_geo.api.get_villages?district=Kebayoran%20Baru
```

## Integration Examples

### Cascading Dropdowns in Forms

```javascript
// In your form script
frappe.ui.form.on("Your DocType", {
  province: function (frm) {
    // Clear dependent fields
    frm.set_value("regency", "");
    frm.set_value("district", "");
    frm.set_value("village", "");

    // Set regency filter
    frm.set_query("regency", function () {
      return {
        filters: {
          province: frm.doc.province,
        },
      };
    });
  },

  regency: function (frm) {
    // Similar pattern for district and village
  },
});
```

### Using in Other Apps

```python
# In your app's doctype
def validate(self):
    # Get location details
    if self.village:
        village = frappe.get_doc("Village", self.village)
        self.district = village.district
        self.regency = village.regency
        self.province = village.province
```

## Development

### Running Tests

```bash
# Run all tests
bench --site your-site run-tests --app indo_geo

# Run specific test
bench --site your-site run-tests --module indo_geo.indo_geo.doctype.province.test_province
```

### Code Quality

```bash
# Format code
ruff format indo_geo/

# Lint code
ruff check indo_geo/
```

## Data Sources

Administrative division data is based on official Indonesian government sources (Kemendagri).

CSV files location: `/indo_geo/data/`

- `provinces.csv` - 33 records
- `regencies.csv` - 514 records
- `districts.csv` - 7,215 records
- `villages.csv` - 80,534 records

### Development Guidelines

- Follow Frappe coding standards
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## Acknowledgments & Credits

- Indonesian Ministry of Home Affairs (Kemendagri) for administrative division data
- Frappe Framework team for the excellent framework
- Edward S. Pasaribu for initial data
  [https://github.com/edwardsamuel/Wilayah-Administratif-Indonesia](https://github.com/edwardsamuael/Wilayah-Administratif-Indonesia)

---

**Note**: This app provides read-only reference data. The administrative divisions are imported during installation and should not be modified directly through the UI to maintain data integrity.

[] Robin Syihab
