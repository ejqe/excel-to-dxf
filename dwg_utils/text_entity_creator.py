"""
Text entity creation for AutoCAD drawings
"""
import ezdxf
from typing import Dict, Any
from .constants import COLOR_MAP


class TextEntityCreator:
    """Handles creation of AutoCAD text entities"""
    
    def __init__(self, doc: ezdxf.document.Drawing):
        """
        Initialize text entity creator
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
        self.msp = doc.modelspace()
    
    def create_text(self, text_data: Dict[str, Any], index: int = None) -> None:
        """
        Create a single text entity from configuration data
        
        Args:
            text_data: Dictionary containing text entity configuration
            index: Optional index for display purposes
        """
        # Prepare dxfattribs
        dxfattribs = {
            'insert': tuple(text_data['position']),
            'height': text_data['height'],
            'layer': text_data['layer'],
            'style': text_data['style'],
            'rotation': text_data.get('rotation', 0),
            'thickness': text_data.get('thickness', 0)
        }
        
        # Add oblique angle if specified
        if 'oblique_angle' in text_data and text_data['oblique_angle'] != 0:
            dxfattribs['oblique'] = text_data['oblique_angle']
        
        # Add alignment if specified
        if 'horizontal_align' in text_data and text_data['horizontal_align'] != 0:
            dxfattribs['halign'] = text_data['horizontal_align']
        
        if 'vertical_align' in text_data and text_data['vertical_align'] != 0:
            dxfattribs['valign'] = text_data['vertical_align']
        
        # Add align point if specified
        if 'align_point' in text_data and text_data['align_point'] is not None:
            dxfattribs['align_point'] = tuple(text_data['align_point'])
        
        # Handle linetype
        linetype = text_data.get('linetype', 'ByLayer')
        if linetype != 'ByLayer' and linetype != 'ByBlock':
            dxfattribs['linetype'] = linetype
        
        # Add extrusion if specified and not default
        if 'extrusion' in text_data:
            extrusion = text_data['extrusion']
            if extrusion != [0, 0, 1]:
                dxfattribs['extrusion'] = tuple(extrusion)
        
        # Create text entity
        text = self.msp.add_text(
            text_data['value'],
            dxfattribs=dxfattribs
        )
        
        # Set individual width factor if different from 1.0
        if 'width_factor' in text_data and text_data['width_factor'] != 1.0:
            text.dxf.width = text_data['width_factor']
        
        # Set color if specified and not ByLayer
        if 'color' in text_data:
            color = text_data['color']
            if color != 'ByLayer' and color != 'ByBlock':
                if color in COLOR_MAP:
                    text.dxf.color = COLOR_MAP[color]
                else:
                    text.dxf.color = int(color) if str(color).isdigit() else 7
        
        # Set lineweight if specified and not ByLayer
        if 'lineweight' in text_data:
            lineweight = text_data['lineweight']
            if lineweight not in ['ByLayer', 'ByBlock', 'Default']:
                try:
                    text.dxf.lineweight = int(float(lineweight) * 100)
                except (ValueError, TypeError):
                    pass
        
        # Set linetype scale
        if 'ltscale' in text_data and text_data['ltscale'] != 1.0:
            text.dxf.ltscale = text_data['ltscale']
        
        # Set invisible flag
        if 'invisible' in text_data and text_data['invisible']:
            text.dxf.invisible = 1
        
        # Set transparency
        if 'transparency' in text_data and text_data['transparency'] != 0:
            text.transparency = text_data['transparency']
    
    def create_texts(self, texts_data: list) -> None:
        """
        Create multiple text entities from configuration
        
        Args:
            texts_data: List of text entity configuration dictionaries
        """
        for idx, text_data in enumerate(texts_data, 1):
            self.create_text(text_data, idx)
