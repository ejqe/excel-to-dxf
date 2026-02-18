
import sys
from constants import OUTPUT_DXF, DATA_DIR
from extractor import DxfExtractor
from creator import Dxf_Creator, ConfigLoader
from modifier.text_value_replacer import TextValueReplacer


def main():

    if len(sys.argv) != 3:
        print("Usage: py main.py <input.dxf> <input.xlsx>")
        sys.exit(1)
        
    INPUT_DXF = sys.argv[1]
    INPUT_XLSX = sys.argv[2]
    
    try:
        # =========================
        # EXTRACT
        # =========================
        print("\nLoading input.dxf...")
        dxf_extractor = DxfExtractor(dxf_file=INPUT_DXF)
        dxf_extractor.load()

        print("Extracting dxf...\n")
        data = dxf_extractor.extract()
        dxf_extractor.save()

        print("✓ SUCCESS! Extraction complete")
        print(f"Saved at {DATA_DIR}\n")

        layer_count = len(data["layers"])
        style_count = len(data["styles"])
        line_count = len(data["lines"])
        text_count = len(data["texts"])

        print("Extracted entities:")
        print(f"  {layer_count} layer(s)")
        print(f"  {style_count} style(s)")
        print(f"  {line_count} line(s)")
        print(f"  {text_count} text(s)\n")

        # =========================
        # MODIFY
        # =========================
        print("Modifying text values...\n")

        replacer = TextValueReplacer(excel_path=INPUT_XLSX)
        replacer.run()

        # =========================
        # CREATE
        # =========================
        print("Creating dxf...\n")

        config_loader = ConfigLoader()
        config_loader.load()

        dxf_creator = Dxf_Creator()
        dxf_creator.build()
        dxf_creator.save(OUTPUT_DXF)

        print("✓ SUCCESS! Creation complete")
        print(f"Saved at {OUTPUT_DXF}\n")

    except FileNotFoundError:
        print(f"✗ ERROR: File '{INPUT_DXF}' not found")
    except Exception as e:
        print(f"✗ ERROR: {e}")


if __name__ == "__main__":
    main()