"""
Extraction builder that orchestrates the extraction of all entities from DXF
"""
import ezdxf
import json
from typing import Dict, List
from .layer_extractor import LayerExtractor
from .text_style_extractor import TextStyleExtractor
from .line_extractor import LineExtractor
from .text_extractor import TextExtractor


class ExtractionBuilder:
    """Main class for extracting entities from DXF files"""
    
    def __init__(self, dxf_file: str):
        """
        Initialize extraction builder
        
        Args:
            dxf_file: Path to input DXF file
        """
        self.dxf_file = dxf_file
        self.doc = None
        self.data = None
    
    def load(self):
        """Load the DXF file"""
        self.doc = ezdxf.readfile(self.dxf_file)
    
    def extract(self) -> Dict[str, List]:
        """
        Extract all entities from DXF
        
        Returns:
            Dictionary containing all extracted data
        """
        if self.doc is None:
            self.load()
        
        # Extract layers
        layer_extractor = LayerExtractor(self.doc)
        layers = layer_extractor.extract_layers()
        
        # Extract text styles
        style_extractor = TextStyleExtractor(self.doc)
        styles = style_extractor.extract_text_styles()
        
        # Extract lines
        line_extractor = LineExtractor(self.doc)
        lines = line_extractor.extract_lines()
        
        # Extract texts
        text_extractor = TextExtractor(self.doc)
        texts = text_extractor.extract_texts()
        
        self.data = {
            'layers': layers,
            'styles': styles,
            'lines': lines,
            'texts': texts
        }
        
        return self.data
    
    def save(self):
        """Save extracted data to JSON files"""
        if self.data is None:
            raise ValueError("No data to save. Call extract() first.")
        
        # Save layers
        with open('layers.json', 'w') as f:
            json.dump(self.data['layers'], f, indent=2)
        
        # Save styles
        with open('styles.json', 'w') as f:
            json.dump(self.data['styles'], f, indent=2)
        
        # Save lines
        with open('lines.json', 'w') as f:
            json.dump(self.data['lines'], f, indent=2)
        
        # Save texts
        with open('texts.json', 'w') as f:
            json.dump(self.data['texts'], f, indent=2)
    
    def extract_and_save(self):
        """Extract and save in one step"""
        self.extract()
        self.save()
