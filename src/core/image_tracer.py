import cv2
import numpy as np
import lxml.etree as ET

class ImageTracer:
    """
    Provides functionality to convert bitmap images to vector SVG formats.
    """
    
    PRESETS = {
        "Default": {"threshold": 127, "mode": cv2.RETR_TREE, "approx": 0.01},
        "Detailed": {"threshold": 100, "mode": cv2.RETR_TREE, "approx": 0.001},
        "Simplified": {"threshold": 150, "mode": cv2.RETR_EXTERNAL, "approx": 0.02},
        "Sketch": {"canny": True, "low_t": 50, "high_t": 150, "approx": 0.005}
    }

    @staticmethod
    def trace_image(image_path, preset_name="Default"):
        """
        Traces an image and returns SVG content as string.
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Could not read image: {image_path}")
        
        settings = ImageTracer.PRESETS.get(preset_name, ImageTracer.PRESETS["Default"])
        
        # Preprocessing
        if settings.get("canny"):
            edges = cv2.Canny(img, settings["low_t"], settings["high_t"])
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, thresh = cv2.threshold(img, settings["threshold"], 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, settings["mode"], cv2.CHAIN_APPROX_SIMPLE)
        
        # SVG Generation
        svg_root = ET.Element('svg', nsmap={None: "http://www.w3.org/2000/svg"})
        height, width = img.shape
        svg_root.attrib['width'] = str(width)
        svg_root.attrib['height'] = str(height)
        svg_root.attrib['viewBox'] = f"0 0 {width} {height}"
        
        # Group for paths
        g = ET.SubElement(svg_root, 'g')
        g.attrib['id'] = "traced_layer"
        
        for i, cnt in enumerate(contours):
            # Approx Poly
            epsilon = settings["approx"] * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            if len(approx) < 3:
                continue
            
            # Build Path Data
            pts = approx.reshape(-1, 2)
            path_data = f"M {pts[0][0]},{pts[0][1]} "
            for pt in pts[1:]:
                path_data += f"L {pt[0]},{pt[1]} "
            path_data += "Z"
            
            path_elem = ET.SubElement(g, 'path')
            path_elem.attrib['d'] = path_data
            path_elem.attrib['fill'] = "black" if not settings.get("canny") else "none"
            path_elem.attrib['stroke'] = "none" if not settings.get("canny") else "black"
            path_elem.attrib['stroke-width'] = "1"
            path_elem.attrib['id'] = f"trace_{i}"
            
        return ET.tostring(svg_root, encoding='unicode', pretty_print=True)
