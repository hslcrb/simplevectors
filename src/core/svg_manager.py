from lxml import etree

class SvgManager:
    def __init__(self):
        self.tree = None
        self.root = None
        self.ns = {'svg': 'http://www.w3.org/2000/svg'}

    def load_content(self, content):
        """Parses SVG content string."""
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            # Handle potential encoding declaration issues by passing bytes
            if isinstance(content, str):
                content = content.encode('utf-8')
            self.tree = etree.fromstring(content, parser=parser).getroottree()
            self.root = self.tree.getroot()
        except Exception as e:
            print(f"Error parsing SVG: {e}")
            raise

    def get_string(self):
        """Returns the current SVG as a string."""
        if self.tree:
            return etree.tostring(self.tree, pretty_print=True, encoding='unicode')
        return ""

    def change_color(self, element_id, new_color):
        """Changes the fill/stroke of an element by ID."""
        # This assumes we can find the element by ID. 
        # In a real editor, we'd need a robust selection mechanism.
        # For this prototype, we'll traverse or use xpath.
        if self.root is None:
            return False

        # Find element. Using .//* to search recursively
        elements = self.root.xpath(f"//*[@id='{element_id}']")
        if not elements:
            return False
        
        el = elements[0]
        # Check if it has a style attribute or fill attribute
        if 'style' in el.attrib:
            # Very basic style parsing
            styles = el.attrib['style'].split(';')
            new_styles = []
            replaced = False
            for s in styles:
                if s.strip().startswith('fill:'):
                    new_styles.append(f"fill:{new_color}")
                    replaced = True
                else:
                    new_styles.append(s)
            if not replaced:
                new_styles.append(f"fill:{new_color}")
            el.attrib['style'] = ";".join(new_styles)
        else:
            el.attrib['fill'] = new_color
        return True

    def group_elements(self, element_ids, group_id):
        """Groups elements with given IDs under a new <g> tag."""
        if self.root is None or not element_ids:
            return False
        
        group = etree.Element("g", id=group_id)
        found_any = False
        
        # We need to collect elements to move them.
        # Note: Moving elements in XML tree changes structure.
        elements_to_move = []
        
        for eid in element_ids:
            els = self.root.xpath(f"//*[@id='{eid}']")
            if els:
                elements_to_move.append(els[0])
        
        if not elements_to_move:
            return False

        # Insert group at the position of the first element to maintain roughly z-order
        parent = elements_to_move[0].getparent()
        parent.insert(parent.index(elements_to_move[0]), group)
        
        for el in elements_to_move:
            group.append(el)
            found_any = True
            
        return found_any
