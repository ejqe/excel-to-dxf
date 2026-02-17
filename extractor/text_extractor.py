"""
Text extraction from DXF files
"""
from typing import List, Dict, Any


class TextExtractor:
    """Handles extraction of AutoCAD TEXT entities"""
    
    def __init__(self, doc):
        """
        Initialize text extractor
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
        self.msp = doc.modelspace()
    
    def extract_texts(self) -> List[Dict[str, Any]]:
        """Extract all TEXT entities"""
        texts = []
        
        for entity in self.msp.query('TEXT'):
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
                
                text_value = str(entity.dxf.text).strip()
                if not text_value:
                    continue

                text_data = {
                    "value": text_value,
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
                if color == 256:
                    return "ByLayer"
                elif color == 0:
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
                if lw == -1:
                    return "ByLayer"
                elif lw == -2:
                    return "ByBlock"
                elif lw == -3:
                    return "Default"
                else:
                    return lw / 100.0
            except (ValueError, TypeError):
                return "ByLayer"
        return "ByLayer"