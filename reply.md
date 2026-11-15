(analyzer) PS D:\Winprojects\analyzer> python src/scripts/excel_reader_feature_spike.py --benchmark-rows 20000
{
  "cached_value_view": {
    "coordinate": "D2",
    "data_type": "n",
    "number_format": "General",
    "value": 1
  },
  "date_epoch_comparison": {
    "1900": {
      "cell_value": "2024-01-01T00:00:00",
      "raw_date_serial": "45292",
      "workbook_epoch": "1899-12-30T00:00:00"
    },
    "1904": {
      "cell_value": "2024-01-01T00:00:00",
      "raw_date_serial": "43830",
      "workbook_epoch": "1904-01-01T00:00:00"
    },
    "same_calendar_value": true,
    "serials_differ": true
  },
  "dependency_inventory_note": "Reflects the interpreter running this utility; packages installed manually and absent from requirements.txt are reported when present.",
  "formula_cache_pair": {
    "cached_value": 1,
    "formula": "=B2+1",
    "same_coordinate": true
  },
  "formula_view": {
    "coordinate": "D2",
    "data_type": "f",
    "number_format": "General",
    "value": "=B2+1"
  },
  "formula_without_cache": {
    "cached_value": null,
    "formula": "=B2+2"
  },
  "hidden_column_H": true,
  "hidden_row_6": true,
  "large_sheet_benchmark": {
    "enabled": true,
    "load_and_scan_current_tracemalloc_bytes": 46269931,
    "load_and_scan_elapsed_seconds": 6.769802,
    "load_and_scan_peak_tracemalloc_bytes": 47889981,
    "load_current_tracemalloc_bytes": 46093935,
    "load_elapsed_seconds": 6.545057,
    "load_peak_tracemalloc_bytes": 47889981,
    "memory_measurement": "Python allocations tracked by tracemalloc; native allocations outside Python's allocator may not be fully represented.",
    "observed_max_column": 6,
    "observed_max_row_including_header": 20001,
    "observed_non_empty_cells": 120006,
    "reader_mode": "normal",
    "reader_version": "3.1.5",
    "requested_data_rows": 20000,
    "xlsx_file_size_bytes": 588827
  },
  "merged_ranges": [
    "A4:B4"
  ],
  "non_empty_coordinates": [
    "A1",
    "A2",
    "A4",
    "B1",
    "B2",
    "C1",
    "C2",
    "D1",
    "D2",
    "E1",
    "E2",
    "F1",
    "F2",
    "G1",
    "G2",
    "H2"
  ],
  "notes": [
    "Synthetic fixture only; no source workbook was opened.",
    "No formula was calculated; cached value was injected into synthetic XLSX XML.",
    "Raw numeric token is read from worksheet XML for comparison with the library scalar.",
    "This utility reports observations; it does not assert pass/fail or modify project data.",
    "1900/1904 comparison uses separate synthetic workbooks with the same calendar date.",
    "Repeatability compares two independent loads of the same immutable synthetic XLSX bytes."
  ],
  "numeric_library_value": 123.45,
  "openpyxl_version": "3.1.5",
  "python_calamine_installed": false,
  "raw_numeric_xml_token": "123.4500",
  "reader_package_inventory": {
    "fastexcel": {
      "distribution_installed": false,
      "import_module_available": false,
      "version": null
    },
    "odfpy": {
      "distribution_installed": false,
      "import_module_available": false,
      "version": null
    },
    "openpyxl": {
      "distribution_installed": true,
      "import_module_available": true,
      "version": "3.1.5"
    },
    "pandas": {
      "distribution_installed": false,
      "import_module_available": false,
      "version": null
    },
    "python_calamine": {
      "distribution_installed": false,
      "import_module_available": false,
      "version": null
    },
    "pyxlsb": {
      "distribution_installed": false,
      "import_module_available": false,
      "version": null
    },
    "xlrd": {
      "distribution_installed": true,
      "import_module_available": true,
      "version": "2.0.2"
    }
  },
  "repeatability": {
    "comparison_scope": "two independent loads of the same immutable synthetic XLSX bytes",
    "input_sha256": "4fd53807f15ef3c3d3fd40ebebdd9747546703f67e189f3fa945948fa2205086",
    "reader_version": "3.1.5",
    "same_input_sha256": true,
    "same_observation_projection": true
  },
  "sample_cells": {
    "A2": {
      "coordinate": "A2",
      "data_type": "s",
      "number_format": "General",
      "value": "Revenue"
    },
    "B2": {
      "coordinate": "B2",
      "data_type": "n",
      "number_format": "General",
      "value": 0
    },
    "C2": {
      "coordinate": "C2",
      "data_type": "n",
      "number_format": "General",
      "value": 123.45
    },
    "E2": {
      "coordinate": "E2",
      "data_type": "d",
      "number_format": "yyyy-mm-dd h:mm:ss",
      "value": "2024-01-01T00:00:00"
    },
    "F2": {
      "coordinate": "F2",
      "data_type": "e",
      "number_format": "General",
      "value": "#N/A"
    },
    "G2": {
      "coordinate": "G2",
      "data_type": "b",
      "number_format": "General",
      "value": true
    }
  },
  "sheet_states": [
    {
      "state": "visible",
      "title": "Main"
    },
    {
      "state": "hidden",
      "title": "HiddenSheet"
    },
    {
      "state": "veryHidden",
      "title": "VeryHiddenSheet"
    }
  ],
  "tables": {
    "SyntheticFacts": "A1:G2"
  },
  "utility": "excel_reader_feature_spike",
  "workbook_epoch": "1904-01-01T00:00:00",
  "workbook_sha256": "4fd53807f15ef3c3d3fd40ebebdd9747546703f67e189f3fa945948fa2205086"