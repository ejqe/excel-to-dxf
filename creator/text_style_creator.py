"""
Text style creation and management for AutoCAD drawings
"""
import ezdxf
from typing import Dict, Any


class TextStyleCreator:
    """Handles creation of AutoCAD text styles"""
    
    def __init__(self, doc: ezdxf.document.Drawing):
        """
        Initialize text style creator
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
    
    def create_style(self, style_data: Dict[str, Any]) -> None:
        """
        Create a single text style from configuration data
        
        Args:
            style_data: Dictionary containing text style configuration
        """
        style_name = style_data['name']
        
        if style_name not in self.doc.styles:
            # Prepare dxfattribs
            dxfattribs = {}
            
            # Width factor
            if 'width_factor' in style_data:
                dxfattribs['width'] = style_data['width_factor']
            
            # Oblique angle
            if 'oblique_angle' in style_data:
                dxfattribs['oblique'] = style_data['oblique_angle']
            
            # Generation flags
            if 'generation_flags' in style_data:
                dxfattribs['flags'] = style_data['generation_flags']
            
            # Last height
            if 'last_height' in style_data:
                dxfattribs['last_height'] = style_data['last_height']
            
            # Create the style
            style = self.doc.styles.add(
                style_name,
                font=style_data.get('font', 'txt.shx'),
                dxfattribs=dxfattribs
            )
            
            # Set height (fixed or variable)
            if 'height' in style_data:
                style.dxf.height = style_data['height']
            
            # Set big font (for Asian languages)
            if 'big_font' in style_data and style_data['big_font']:
                style.dxf.bigfont = style_data['big_font']
            
            # Set text generation flags manually if needed
            if style_data.get('is_backwards', False):
                style.dxf.flags |= 2
            
            if style_data.get('is_upside_down', False):
                style.dxf.flags |= 4
            
            if style_data.get('is_vertical', False):
                style.dxf.flags |= 4
    
    def create_styles(self, styles_data: list) -> None:
        """
        Create multiple text styles from configuration
        
        Args:
            styles_data: List of text style configuration dictionaries
        """
        for style_data in styles_data:
            self.create_style(style_data)
