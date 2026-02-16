"""
Line extraction from DXF files
"""
from typing import List, Dict, Any


class LineExtractor:
    """Handles extraction of AutoCAD LINE entities"""
    
    def __init__(self, doc):
        """
        Initialize line extractor
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
        self.msp = doc.modelspace()
    
    def extract_lines(self) -> List[Dict[str, Any]]:
        """Extract all LINE entities"""
        lines = []
        
        for entity in self.msp.query('LINE'):
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
