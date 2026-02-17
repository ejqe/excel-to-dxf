"""
Main drawing builder that orchestrates the creation of AutoCAD drawings
"""
import ezdxf
from .config_loader import ConfigLoader
from .layer_creator import LayerCreator
from .style_creator import StyleCreator
from .text_creator import TextEntityCreator
from .line_creator import LineCreator
from constants import LAYERS_JSON, STYLES_JSON, LINES_JSON, TEXTS_JSON, DEFAULT_DWG_VERSION


class Dxf_Creator:
    """Main class for building AutoCAD drawings from configuration"""

    def __init__(self, 
                 layers_path: str = LAYERS_JSON,
                 styles_path: str = STYLES_JSON,
                 lines_path: str = LINES_JSON,
                 texts_path: str = TEXTS_JSON,
                 dwg_version: str = DEFAULT_DWG_VERSION
                 ):
      
        self.config_loader = ConfigLoader(layers_path, styles_path, lines_path, texts_path)
        self.dwg_version = dwg_version
        self.doc = None
    
    def build(self) -> ezdxf.document.Drawing:
        """
        Build the drawing from configuration
        
        Returns:
            ezdxf Drawing document
        """
        # Load and validate configuration
        config = self.config_loader.load()
        if not self.config_loader.validate():
            raise ValueError("Invalid configuration files")
        
        # Create new drawing
        self.doc = ezdxf.new(self.dwg_version, setup=True)
        
        # Create layers
        layer_creator = LayerCreator(self.doc)
        layer_creator.create_layers(self.config_loader.get_layers())
        
        # Create text styles
        style_creator = StyleCreator(self.doc)
        style_creator.create_styles(self.config_loader.get_text_styles())
        
        # Create text entities
        text_creator = TextEntityCreator(self.doc)
        text_creator.create_texts(self.config_loader.get_texts())
        
        # Create line entities (if any)
        lines = self.config_loader.get_lines()
        if lines:
            line_creator = LineCreator(self.doc)
            line_creator.create_lines(lines)
        
        return self.doc
    
    def save(self, output_path: str) -> None:
        """
        Save the drawing to a file
        
        Args:
            output_path: Path to save the DXF/DWG file
        """
        if self.doc is None:
            raise ValueError("No drawing to save. Call build() first.")
        
        self.doc.saveas(output_path)
    
    def build_and_save(self, output_path: str) -> ezdxf.document.Drawing:
        """
        Build and save the drawing in one step
        
        Args:
            output_path: Path to save the DXF/DWG file
            
        Returns:
            ezdxf Drawing document
        """
        self.build()
        self.save(output_path)
        return self.doc
