"""
Main script to create AutoCAD DXF files from separate JSON configuration files
"""
from dwg_utils import DrawingBuilder, ConfigLoader


def main():
    """Main function"""
    
    # Separate JSON file paths (shorter names!)
    layers_file = 'layers.json'
    styles_file = 'styles.json'
    lines_file = 'lines.json'
    texts_file = 'texts.json'
    
    print("\n" + "="*60)
    print("  AutoCAD DXF Generator")
    print("="*60)
    
    # Load configuration
    print("\nLoading configuration...")
    config_loader = ConfigLoader(layers_file, styles_file, lines_file, texts_file)
    config_loader.load()
    
    layers = config_loader.get_layers()
    styles = config_loader.get_text_styles()
    lines = config_loader.get_lines()
    texts = config_loader.get_texts()
    
    print(f"  ✓ {len(layers)} layer(s) from {layers_file}")
    print(f"  ✓ {len(styles)} text style(s) from {styles_file}")
    print(f"  ✓ {len(lines)} line(s) from {lines_file}")
    print(f"  ✓ {len(texts)} text(s) from {texts_file}")
    
    # Build drawing
    print("\nBuilding drawing...")
    builder = DrawingBuilder(layers_file, styles_file, lines_file, texts_file, dwg_version='R2018')
    builder.build()
    
    # Save
    output_file = 'output.dxf'
    print(f"Saving to {output_file}...")
    builder.save(output_file)
    
    print("\n" + "="*60)
    print(f"  ✓ SUCCESS! Created {output_file}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
