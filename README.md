# excel-to-dxf

A Python tool that populates a DXF table drawing with data from an Excel spreadsheet — using a reference DXF file as a layout template.

---

## Overview

Native Excel-to-DXF/DWG export lacks layer support and ignores any existing drawing template. Manually editing a CAD template with spreadsheet data is tedious and prone to error.
This tool bridges the two — it reads your existing DXF template and populates it with values from Excel, preserving layers, styles, and geometry without any manual intervention.

## Usage
```bash
python main.py input.dxf input.xlsx 
```

### `input.dxf` — Your Template Drawing

A DXF file where every table cell contains an Excel-style cell ID as its text instead of actual data. The structure (rows and columns) must match Excel file exactly.
⚠️ Note: Only LINE and TEXT along with its STYLES and LAYERS entities are supported. Other entity types will be ignored.
```
┌──────────┬──────────┬───────┐
│    A1    │    B1    │  C1   │
├──────────┼──────────┼───────┤
│    A2    │    B2    │  C2   │
├──────────┼──────────┼───────┤
│    A3    │    B3    │  C3   │
└──────────┴──────────┴───────┘
```

### `input.xlsx` — Your Data

A standard Excel file containing the data you want to populate into the drawing. The table layout (rows and columns) must match the reference DXF.
```
     A          B         C
  ┌──────────┬──────────┬───────┐
1 │    #     │   NAME   │ SCORE │
  ├──────────┼──────────┼───────┤
2 │    1     │ John Doe │ 42.5  │
  ├──────────┼──────────┼───────┤
3 │    2     │ Jane Doe │  38   │
  └──────────┴──────────┴───────┘
```

The output `output.dxf` will be generated in the project root with all placeholders replaced by your Excel values, preserving the original geometry and styling from the reference drawing.

---

## Requirements

- Python 3.x
- [`openpyxl`](https://openpyxl.readthedocs.io/) — reading Excel files
- [`ezdxf`](https://ezdxf.readthedocs.io/) — reading and writing DXF files
```bash
pip install openpyxl ezdxf
```