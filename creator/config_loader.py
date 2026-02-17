"""
Configuration loader for reading separate JSON config files
"""
import json
from typing import Dict, List, Any
from constants import LAYERS_JSON, STYLES_JSON, LINES_JSON, TEXTS_JSON


class ConfigLoader:
    """Handles loading and validation of separate JSON configuration files"""
    
    def __init__(self, layers_path: str = LAYERS_JSON, 
                 styles_path: str = STYLES_JSON,
                 lines_path: str = LINES_JSON,
                 texts_path: str = TEXTS_JSON
                 ):
       
        self.layers_path = layers_path
        self.styles_path = styles_path
        self.lines_path = lines_path
        self.texts_path = texts_path
        
        self.layers = None
        self.styles = None
        self.lines = None
        self.texts = None
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from all JSON files
        
        Returns:
            Dictionary containing all configuration data
        """
        with open(self.layers_path, 'r') as f:
            self.layers = json.load(f)
        
        with open(self.styles_path, 'r') as f:
            self.styles = json.load(f)
        
        with open(self.lines_path, 'r') as f:
            self.lines = json.load(f)
        
        with open(self.texts_path, 'r') as f:
            self.texts = json.load(f)
        
        return {
            'layers': self.layers,
            'styles': self.styles,
            'lines': self.lines,
            'texts': self.texts
        }
    
    def get_layers(self) -> List[Dict[str, Any]]:
        """Get layers configuration"""
        if self.layers is None:
            self.load()
        return self.layers
    
    def get_text_styles(self) -> List[Dict[str, Any]]:
        """Get text styles configuration"""
        if self.styles is None:
            self.load()
        return self.styles
    
    def get_texts(self) -> List[Dict[str, Any]]:
        """Get text entities configuration"""
        if self.texts is None:
            self.load()
        return self.texts
    
    def get_lines(self) -> List[Dict[str, Any]]:
        """Get line entities configuration"""
        if self.lines is None:
            self.load()
        return self.lines
    
    def validate(self) -> bool:
        """
        Validate configuration structure
        
        Returns:
            True if valid, False otherwise
        """
        if self.layers is None or self.styles is None or self.texts is None or self.lines is None:
            self.load()
        
        # Check if all data is loaded
        if not isinstance(self.layers, list):
            print("ERROR: layers must be a list")
            return False
        
        if not isinstance(self.styles, list):
            print("ERROR: styles must be a list")
            return False
        
        if not isinstance(self.texts, list):
            print("ERROR: texts must be a list")
            return False
        
        if not isinstance(self.lines, list):
            print("ERROR: lines must be a list")
            return False
        
        return True
