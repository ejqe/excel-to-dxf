"""
Line creation for AutoCAD drawings
"""
import ezdxf
from typing import Dict, Any
from constants import COLOR_MAP


class LineCreator:
    """Handles creation of AutoCAD line entities"""
    
    def __init__(self, doc: ezdxf.document.Drawing):
        """
        Initialize line creator
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
        self.msp = doc.modelspace()
    
    def create_line(self, line_data: Dict[str, Any], index: int = None) -> None:
        """
        Create a single line entity from configuration data
        
        Args:
            line_data: Dictionary containing line configuration
            index: Optional index for display purposes
        """
        # Prepare linetype (handle ByLayer)
        linetype = line_data.get('linetype', 'ByLayer')
        if linetype == 'ByLayer':
            linetype = 'Continuous'
        
        # Prepare dxfattribs
        dxfattribs = {
            'layer': line_data['layer'],
            'linetype': linetype
        }
        
        # Add thickness if specified
        if 'thickness' in line_data and line_data['thickness'] != 0:
            dxfattribs['thickness'] = line_data['thickness']
        
        # Add extrusion if specified and not default
        if 'extrusion' in line_data:
            extrusion = line_data['extrusion']
            if extrusion != [0, 0, 1]:
                dxfattribs['extrusion'] = tuple(extrusion)
        
        # Create line entity
        line = self.msp.add_line(
            tuple(line_data['start']),
            tuple(line_data['end']),
            dxfattribs=dxfattribs
        )
        
        # Set color if specified and not ByLayer
        if 'color' in line_data:
            color = line_data['color']
            if color != 'ByLayer' and color != 'ByBlock':
                if color in COLOR_MAP:
                    line.dxf.color = COLOR_MAP[color]
                else:
                    line.dxf.color = int(color) if str(color).isdigit() else 7
        
        # Set lineweight if specified and not ByLayer
        if 'lineweight' in line_data:
            lineweight = line_data['lineweight']
            if lineweight not in ['ByLayer', 'ByBlock', 'Default']:
                try:
                    line.dxf.lineweight = int(float(lineweight) * 100)
                except (ValueError, TypeError):
                    pass
        
        # Set linetype scale
        if 'ltscale' in line_data and line_data['ltscale'] != 1.0:
            line.dxf.ltscale = line_data['ltscale']
        
        # Set invisible flag
        if 'invisible' in line_data and line_data['invisible']:
            line.dxf.invisible = 1
        
        # Set transparency
        if 'transparency' in line_data and line_data['transparency'] != 0:
            line.transparency = line_data['transparency']
    
    def create_lines(self, lines_data: list) -> None:
        """
        Create multiple line entities from configuration
        
        Args:
            lines_data: List of line configuration dictionaries
        """
        for idx, line_data in enumerate(lines_data, 1):
            self.create_line(line_data, idx)
