from pathlib import Path

# AutoCAD Color Index (ACI) mapping
COLOR_MAP = {
    "Red": 1,
    "Yellow": 2,
    "Green": 3,
    "Cyan": 4,
    "Blue": 5,
    "Magenta": 6,
    "White": 7,
    "Gray": 8,
    "Black": 7
}

# Default DWG format version
DEFAULT_DWG_VERSION = 'R2018'

# Common AutoCAD fonts
COMMON_FONTS = [
    'romans.shx',
    'txt.shx',
    'simplex.shx',
    'standard.shx'
]


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

LAYERS_JSON = DATA_DIR / "layers.json"
STYLES_JSON = DATA_DIR / "styles.json"
LINES_JSON = DATA_DIR / "lines.json"
TEXTS_JSON = DATA_DIR / "texts.json"

INPUT_DXF = BASE_DIR / "input.dxf"
OUTPUT_DXF = BASE_DIR / "output.dxf"
