
from extractor import DxfExtractor
from creator import Dxf_Creator, ConfigLoader
from constants import INPUT_DXF, OUTPUT_DXF, LAYERS_JSON, STYLES_JSON, LINES_JSON, TEXTS_JSON, DEFAULT_DWG_VERSION, DATA_DIR


def main():
    
    try:
        # =========================
        # EXTRACT
        # =========================
        print("\nLoading input.dxf...")
        dxf_extractor = DxfExtractor(
            INPUT_DXF,
            LAYERS_JSON,
            STYLES_JSON, 
            LINES_JSON,
            TEXTS_JSON
            )
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

        # WIP - Excel to JSON modification logic would go here (not implemented yet)



        # =========================
        # CREATE
        # =========================
        print("Creating dxf...\n")

        config_loader = ConfigLoader(
            LAYERS_JSON,
            STYLES_JSON,
            LINES_JSON,
            TEXTS_JSON
            )
        config_loader.load()

        dxf_creator = Dxf_Creator(
            LAYERS_JSON,
            STYLES_JSON,
            LINES_JSON,
            TEXTS_JSON,
            DEFAULT_DWG_VERSION
            )
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