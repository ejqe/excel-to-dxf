"""
Text style extraction from DXF files
"""
from typing import List, Dict, Any


class TextStyleExtractor:
    """Handles extraction of AutoCAD text styles"""
    
    def __init__(self, doc):
        """
        Initialize text style extractor
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
    
    def extract_text_styles(self) -> List[Dict[str, Any]]:
        """Extract all text styles"""
        styles = []
        
        for style in self.doc.styles:
            # Skip standard styles
            if style.dxf.name in ['Standard', 'Annotative']:
                continue
            
            try:
                # Get flags
                flags = 0
                if hasattr(style.dxf, 'flags'):
                    try:
                        flags = int(style.dxf.flags)
                    except (ValueError, TypeError):
                        flags = 0
                
                # Get height
                height = 0
                if hasattr(style.dxf, 'height'):
                    try:
                        height = float(style.dxf.height)
                    except (ValueError, TypeError):
                        height = 0
                
                # Get width factor
                width_factor = 1.0
                if hasattr(style.dxf, 'width'):
                    try:
                        width_factor = float(style.dxf.width)
                    except (ValueError, TypeError):
                        width_factor = 1.0
                
                # Get oblique angle
                oblique_angle = 0
                if hasattr(style.dxf, 'oblique'):
                    try:
                        oblique_angle = float(style.dxf.oblique)
                    except (ValueError, TypeError):
                        oblique_angle = 0
                
                # Get last height
                last_height = 2.5
                if hasattr(style.dxf, 'last_height'):
                    try:
                        last_height = float(style.dxf.last_height)
                    except (ValueError, TypeError):
                        last_height = 2.5
                
                style_data = {
                    "name": str(style.dxf.name),
                    "font": str(style.dxf.font) if hasattr(style.dxf, 'font') else "txt.shx",
                    "height": height,
                    "width_factor": width_factor,
                    "oblique_angle": oblique_angle,
                    "generation_flags": flags,
                    "last_height": last_height,
                    "big_font": str(style.dxf.bigfont) if hasattr(style.dxf, 'bigfont') else "",
                    "is_backwards": bool(flags & 2),
                    "is_upside_down": bool(flags & 4),
                    "is_vertical": False
                }
                styles.append(style_data)
            except Exception:
                continue
        
        return styles
