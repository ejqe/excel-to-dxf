"""
DXF Extractor class for extracting entities from DXF files
"""
import ezdxf
import json
from typing import List, Dict, Any


class DXFExtractor:
    """Extract entities from DXF file and convert to JSON format"""
    
    def __init__(self, dxf_file: str):
        """
        Initialize extractor
        
        Args:
            dxf_file: Path to input DXF file
        """
        self.dxf_file = dxf_file
        self.doc = None
        
    def load(self):
        """Load the DXF file"""
        self.doc = ezdxf.readfile(self.dxf_file)
        
    def extract_layers(self) -> List[Dict[str, Any]]:
        """Extract all layers with their properties"""
        layers = []
        
        for layer in self.doc.layers:
            # Skip layer 0 and Defpoints (standard layers)
            if layer.dxf.name in ['0', 'Defpoints']:
                continue
            
            try:
                # Get locked state from flags
                locked = bool(layer.dxf.flags & 4) if hasattr(layer.dxf, 'flags') else False
                
                # Get frozen state from flags
                frozen = bool(layer.dxf.flags & 1) if hasattr(layer.dxf, 'flags') else False
                
                layer_data = {
                    "name": layer.dxf.name,
                    "color": layer.dxf.color if hasattr(layer.dxf, 'color') else 7,
                    "plottable": layer.dxf.plot if hasattr(layer.dxf, 'plot') else True,
                    "linetype": layer.dxf.linetype if hasattr(layer.dxf, 'linetype') else "Continuous",
                    "lineweight": layer.dxf.lineweight if hasattr(layer.dxf, 'lineweight') else "Default",
                    "transparency": 0,
                    "description": "",
                    "locked": locked,
                    "frozen": frozen,
                    "off": bool(layer.dxf.flags & 2) if hasattr(layer.dxf, 'flags') else False
                }
                layers.append(layer_data)
            except Exception:
                continue
        
        return layers
    
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
    
    def extract_lines(self) -> List[Dict[str, Any]]:
        """Extract all LINE entities"""
        lines = []
        msp = self.doc.modelspace()
        
        for entity in msp.query('LINE'):
            try:
                # Get start and end points
                start = entity.dxf.start
                end = entity.dxf.end
                
                # Get extrusion (with default)
                extrusion = [0, 0, 1]
                if hasattr(entity.dxf, 'extrusion') and entity.dxf.extrusion is not None:
                    extrusion = [float(entity.dxf.extrusion.x), float(entity.dxf.extrusion.y), float(entity.dxf.extrusion.z)]
                
                # Get ltscale
                ltscale = 1.0
                if hasattr(entity.dxf, 'ltscale'):
                    try:
                        ltscale = float(entity.dxf.ltscale)
                    except (ValueError, TypeError):
                        ltscale = 1.0
                
                # Get thickness
                thickness = 0
                if hasattr(entity.dxf, 'thickness'):
                    try:
                        thickness = float(entity.dxf.thickness)
                    except (ValueError, TypeError):
                        thickness = 0
                
                line_data = {
                    "start": [float(start.x), float(start.y), float(start.z)],
                    "end": [float(end.x), float(end.y), float(end.z)],
                    "layer": str(entity.dxf.layer),
                    "color": self._get_color(entity),
                    "lineweight": self._get_lineweight(entity),
                    "linetype": str(entity.dxf.linetype) if hasattr(entity.dxf, 'linetype') else "ByLayer",
                    "ltscale": ltscale,
                    "invisible": bool(entity.dxf.invisible) if hasattr(entity.dxf, 'invisible') else False,
                    "thickness": thickness,
                    "extrusion": extrusion,
                    "transparency": 0
                }
                lines.append(line_data)
            except Exception:
                continue
        
        return lines
    
    def extract_texts(self) -> List[Dict[str, Any]]:
        """Extract all TEXT entities"""
        texts = []
        msp = self.doc.modelspace()
        
        for entity in msp.query('TEXT'):
            try:
                # Get position
                insert = entity.dxf.insert
                
                # Get align point (may be None)
                align_point = None
                if hasattr(entity.dxf, 'align_point') and entity.dxf.align_point is not None:
                    align_point = [float(entity.dxf.align_point.x), float(entity.dxf.align_point.y), float(entity.dxf.align_point.z)]
                
                # Get extrusion (with default)
                extrusion = [0, 0, 1]
                if hasattr(entity.dxf, 'extrusion') and entity.dxf.extrusion is not None:
                    extrusion = [float(entity.dxf.extrusion.x), float(entity.dxf.extrusion.y), float(entity.dxf.extrusion.z)]
                
                # Get width factor
                width_factor = 1.0
                if hasattr(entity.dxf, 'width'):
                    try:
                        width_factor = float(entity.dxf.width)
                    except (ValueError, TypeError):
                        width_factor = 1.0
                
                # Get rotation
                rotation = 0
                if hasattr(entity.dxf, 'rotation'):
                    try:
                        rotation = float(entity.dxf.rotation)
                    except (ValueError, TypeError):
                        rotation = 0
                
                # Get thickness
                thickness = 0
                if hasattr(entity.dxf, 'thickness'):
                    try:
                        thickness = float(entity.dxf.thickness)
                    except (ValueError, TypeError):
                        thickness = 0
                
                # Get oblique
                oblique_angle = 0
                if hasattr(entity.dxf, 'oblique'):
                    try:
                        oblique_angle = float(entity.dxf.oblique)
                    except (ValueError, TypeError):
                        oblique_angle = 0
                
                # Get ltscale
                ltscale = 1.0
                if hasattr(entity.dxf, 'ltscale'):
                    try:
                        ltscale = float(entity.dxf.ltscale)
                    except (ValueError, TypeError):
                        ltscale = 1.0
                
                text_data = {
                    "value": str(entity.dxf.text),
                    "layer": str(entity.dxf.layer),
                    "style": str(entity.dxf.style) if hasattr(entity.dxf, 'style') else "Standard",
                    "height": float(entity.dxf.height),
                    "position": [float(insert.x), float(insert.y), float(insert.z)],
                    "width_factor": width_factor,
                    "rotation": rotation,
                    "thickness": thickness,
                    "oblique_angle": oblique_angle,
                    "align_point": align_point,
                    "horizontal_align": int(entity.dxf.halign) if hasattr(entity.dxf, 'halign') else 0,
                    "vertical_align": int(entity.dxf.valign) if hasattr(entity.dxf, 'valign') else 0,
                    "color": self._get_color(entity),
                    "linetype": str(entity.dxf.linetype) if hasattr(entity.dxf, 'linetype') else "ByLayer",
                    "lineweight": self._get_lineweight(entity),
                    "ltscale": ltscale,
                    "invisible": bool(entity.dxf.invisible) if hasattr(entity.dxf, 'invisible') else False,
                    "extrusion": extrusion,
                    "transparency": 0
                }
                texts.append(text_data)
            except Exception:
                continue
        
        return texts
    
    def _get_color(self, entity) -> str:
        """Get color as string (ByLayer or color number)"""
        if hasattr(entity.dxf, 'color'):
            try:
                color = int(entity.dxf.color)
                if color == 256:  # ByLayer
                    return "ByLayer"
                elif color == 0:  # ByBlock
                    return "ByBlock"
                else:
                    return color
            except (ValueError, TypeError):
                return "ByLayer"
        return "ByLayer"
    
    def _get_lineweight(self, entity) -> str:
        """Get lineweight as string or number"""
        if hasattr(entity.dxf, 'lineweight'):
            try:
                lw = int(entity.dxf.lineweight)
                if lw == -1:  # ByLayer
                    return "ByLayer"
                elif lw == -2:  # ByBlock
                    return "ByBlock"
                elif lw == -3:  # Default
                    return "Default"
                else:
                    return lw / 100.0  # Convert from 1/100mm to mm
            except (ValueError, TypeError):
                return "ByLayer"
        return "ByLayer"
    
    def extract_all(self) -> Dict[str, List]:
        """Extract all entities"""
        if self.doc is None:
            self.load()
        
        layers = self.extract_layers()
        styles = self.extract_text_styles()
        lines = self.extract_lines()
        texts = self.extract_texts()
        
        return {
            'layers': layers,
            'styles': styles,
            'lines': lines,
            'texts': texts
        }
    
    def save_to_json(self, data: Dict[str, List]):
        """Save extracted data to 4 separate JSON files"""
        # Save layers
        with open('layers.json', 'w') as f:
            json.dump(data['layers'], f, indent=2)
        
        # Save styles
        with open('styles.json', 'w') as f:
            json.dump(data['styles'], f, indent=2)
        
        # Save lines
        with open('lines.json', 'w') as f:
            json.dump(data['lines'], f, indent=2)
        
        # Save texts
        with open('texts.json', 'w') as f:
            json.dump(data['texts'], f, indent=2)