# excel-to-dxf

A Python tool that populates a DXF table drawing with data from an Excel spreadsheet — using a reference DXF file as a layout template.

---

## How to Use

Place both input files in the project root, then run:

```bash
python main.py
```

### `input.xlsx` — Your Data

A standard Excel file containing the data you want to populate into the drawing. The table layout (rows and columns) must match the reference DXF.

| A   | B        | C     |
|-----|----------|-------|
| 1   | John Doe | 42.5  |
| 2   | Jane Doe | 38.0  |

### `input.dxf` — Your Reference Drawing

A DXF file where every table cell contains an Excel-style cell ID as its text instead of actual data. The structure (rows and columns) must match `input.xlsx` exactly.

```
┌──────┬──────────┬───────┐
│  A1  │    B1    │  C1   │
├──────┼──────────┼───────┤
│  A2  │    B2    │  C2   │
└──────┴──────────┴───────┘
```

The output `output.dxf` will be generated in the project root with all placeholders replaced by your Excel values, preserving the original geometry and styling from the reference drawing.

---

## How It Works

The tool works in four stages:

**1. Extract** — Reads `input.dxf` and extracts all entities (text, lines, layers, styles) along with their positions and styling. The data is stored across JSON files in the `data/` folder (`texts.json`, `lines.json`, `layers.json`, `styles.json`).

**2. Map** — Opens `input.xlsx` and reads the actual data values from `texts.json`. Each value is matched to its corresponding cell ID (e.g. `A1`, `B3`) found in the extracted JSON data.

**3. Update** — Writes the mapped values back into the JSON data, replacing the placeholder cell IDs with real content while preserving all geometry and styling.

**4. Draw** — Generates `output.dxf` by re-drawing the table using the updated JSON data.

```
input.xlsx  ──┐
               ├──► Extract ──► data/ (JSON) ──► Map ──► Update ──► Draw ──► output.dxf
input.dxf  ──┘
```

---

## Requirements

- Python 3.x
- [`openpyxl`](https://openpyxl.readthedocs.io/) — reading Excel files
- [`ezdxf`](https://ezdxf.readthedocs.io/) — reading and writing DXF files
- `json` — built into Python, no install needed

```bash
pip install openpyxl ezdxf
```