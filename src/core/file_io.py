import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM, renderPS
import lxml.etree as ET

class FileIO:
    @staticmethod
    def open_svg(path):
        """Reads SVG content."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def save_svg(path, content):
        """Saves content to SVG."""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def convert(input_path, output_path, format):
        """Converts vector files."""
        # This is a basic implementation using svglib.
        # svglib mainly supports SVG -> PDF/PS/PNG context via ReportLab.
        
        drawing = svg2rlg(input_path)
        
        if format.lower() == 'pdf':
            renderPDF.drawToFile(drawing, output_path)
        elif format.lower() == 'eps' or format.lower() == 'ps':
            renderPS.drawToFile(drawing, output_path)
        elif format.lower() == 'png':
            renderPM.drawToFile(drawing, output_path, fmt="PNG")
        else:
            raise ValueError(f"Unsupported format: {format}")

    @staticmethod
    def export_element(element_xml, output_path):
        """Exports a single SVG element (XML string) to a file."""
        # Wrap the element in a basic SVG tag for validity
        root = ET.Element('svg', nsmap={None: "http://www.w3.org/2000/svg"})
        root.append(ET.fromstring(element_xml))
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
