"""
Layer creation and management for AutoCAD drawings
"""
import ezdxf
from typing import Dict, Any
from constants import COLOR_MAP


class LayerCreator:
    """Handles creation of AutoCAD layers"""
    
    def __init__(self, doc: ezdxf.document.Drawing):
        """
        Initialize layer creator
        
        Args:
            doc: ezdxf Drawing document
        """
        self.doc = doc
    
    def create_layer(self, layer_data: Dict[str, Any]) -> None:
        """
        Create a single layer from configuration data
        
        Args:
            layer_data: Dictionary containing layer configuration
        """
        layer_name = layer_data['name']
        
        # Add layer or get existing
        if layer_name in self.doc.layers:
            layer = self.doc.layers.get(layer_name)
        else:
            layer = self.doc.layers.add(layer_name)
        
        # Set color
        color = layer_data.get('color', 7)
        if color in COLOR_MAP:
            layer.color = COLOR_MAP[color]
        else:
            layer.color = int(color) if str(color).isdigit() else 7
        
        # Set plottable flag
        layer.plot = layer_data.get('plottable', True)
        
        # Set linetype
        layer.dxf.linetype = layer_data.get('linetype', 'Continuous')
        
        # Set lineweight (if not Default/ByLayer)
        lineweight = layer_data.get('lineweight', 'Default')
        if lineweight not in ['Default', 'ByLayer', 'ByBlock']:
            try:
                layer.dxf.lineweight = int(float(lineweight) * 100)
            except (ValueError, TypeError):
                pass  # Skip if invalid
        
        # Set transparency
        if 'transparency' in layer_data:
            layer.transparency = layer_data['transparency']
        
        # Set description
        if 'description' in layer_data and layer_data['description']:
            layer.description = layer_data['description']
        
        # Set locked
        if layer_data.get('locked', False):
            layer.lock()
        
        # Set frozen
        if layer_data.get('frozen', False):
            layer.freeze()
        
        # Set off
        layer.is_off = layer_data.get('off', False)
    
    def create_layers(self, layers_data: list) -> None:
        """
        Create multiple layers from configuration
        
        Args:
            layers_data: List of layer configuration dictionaries
        """
        for layer_data in layers_data:
            self.create_layer(layer_data)
