"""
Combined DXF extract + create pipeline
"""

from extractor import ExtractionBuilder
from creator import DrawingBuilder, ConfigLoader


def main():
    input_file = "input.dxf"
    output_file = "output.dxf"

    try:
        # =========================
        # EXTRACT
        # =========================
        print("Loading input.dxf...")
        builder = ExtractionBuilder(input_file)
        builder.load()

        print("Extracting dxf...\n")
        data = builder.extract()
        builder.save()

        layer_count = len(data["layers"])
        style_count = len(data["styles"])
        line_count = len(data["lines"])
        text_count = len(data["texts"])

        print("✓ SUCCESS! Extraction complete\n")

        print("Extracted entities:")
        print(f"  {layer_count} layer(s)")
        print(f"  {style_count} style(s)")
        print(f"  {line_count} line(s)")
        print(f"  {text_count} text(s)\n")

        # =========================
        # CREATE
        # =========================
        print("Creating dxf...\n")

        config_loader = ConfigLoader(
            "layers.json",
            "styles.json",
            "lines.json",
            "texts.json"
        )
        config_loader.load()

        drawing_builder = DrawingBuilder(
            "layers.json",
            "styles.json",
            "lines.json",
            "texts.json",
            dwg_version="R2018"
        )
        drawing_builder.build()
        drawing_builder.save(output_file)

        print(f"✓ SUCCESS! Created {output_file}\n")

    except FileNotFoundError:
        print(f"✗ ERROR: File '{input_file}' not found")
    except Exception as e:
        print(f"✗ ERROR: {e}")


if __name__ == "__main__":
    main()