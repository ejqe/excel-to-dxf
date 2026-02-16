"""
Layer extraction from DXF files
"""
from typing import List, Dict, Any


class LayerExtractor:
    """Handles extraction of AutoCAD layers"""
    
    def __init__(self, doc):
        """
        Initialize layer extractor
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
    
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
