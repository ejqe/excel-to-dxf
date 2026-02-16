"""
Extract layers, styles, lines, and texts from DXF file
"""
from dwg_utils.dxf_extractor import DXFExtractor


def main():
    """Main extraction function"""
    
    input_file = 'input.dxf'
    
    print("\n" + "="*60)
    print("  DXF Extractor")
    print("="*60)
    
    # Load DXF
    print(f"\nLoading {input_file}...")
    extractor = DXFExtractor(input_file)
    
    try:
        extractor.load()
        print("  ✓ DXF file loaded")
        
        # Extract all entities
        print("\nExtracting entities...")
        data = extractor.extract_all()
        
        print(f"  ✓ {len(data['layers'])} layer(s)")
        print(f"  ✓ {len(data['styles'])} style(s)")
        print(f"  ✓ {len(data['lines'])} line(s)")
        print(f"  ✓ {len(data['texts'])} text(s)")
        
        # Save to JSON files
        print("\nSaving to JSON files...")
        extractor.save_to_json(data)
        
        print("  ✓ layers.json")
        print("  ✓ styles.json")
        print("  ✓ lines.json")
        print("  ✓ texts.json")
        
        print("\n" + "="*60)
        print("  ✓ SUCCESS! Extraction complete")
        print("="*60 + "\n")
        
    except FileNotFoundError:
        print(f"\n✗ ERROR: File '{input_file}' not found!")
        print("  Make sure input.dxf exists in the same directory.\n")
    except Exception as e:
        print(f"\n✗ ERROR: {e}\n")


if __name__ == "__main__":
    main()