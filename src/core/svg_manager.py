from lxml import etree
import copy

class SvgManager:
    def __init__(self):
        self.tree = None
        self.root = None
        self.ns = {'svg': 'http://www.w3.org/2000/svg'}
        
        # Undo/Redo stacks containing SVG strings
        self.undo_stack = []
        self.redo_stack = []
        self.max_history = 50

    def load_content(self, content):
        """Parses SVG content string."""
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            if isinstance(content, str):
                content = content.encode('utf-8')
            self.tree = etree.fromstring(content, parser=parser).getroottree()
            self.root = self.tree.getroot()
            self._ensure_ids()
            
            # Clear history on new load
            self.undo_stack.clear()
            self.redo_stack.clear()
        except Exception as e:
            print(f"Error parsing SVG: {e}")
            raise

    def _save_state(self):
        """Saves current state to undo stack."""
        if self.tree:
            state = etree.tostring(self.tree, encoding='unicode')
            self.undo_stack.append(state)
            if len(self.undo_stack) > self.max_history:
                self.undo_stack.pop(0)
            self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return False
        
        # Push current to redo
        current_state = etree.tostring(self.tree, encoding='unicode')
        self.redo_stack.append(current_state)
        
        # Pop from undo
        prev_state = self.undo_stack.pop()
        self.load_content_no_reset(prev_state)
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        
        # Push current to undo (without clearing redo)
        current_state = etree.tostring(self.tree, encoding='unicode')
        self.undo_stack.append(current_state)
        
        # Pop from redo
        next_state = self.redo_stack.pop()
        self.load_content_no_reset(next_state)
        return True

    def load_content_no_reset(self, content):
        """Loads content without clearing history."""
        parser = etree.XMLParser(remove_blank_text=True)
        if isinstance(content, str):
            content = content.encode('utf-8')
        self.tree = etree.fromstring(content, parser=parser).getroottree()
        self.root = self.tree.getroot()
        # IDs should already be there from history

    def get_string(self):
        """Returns the current SVG as a string."""
        if self.tree:
            return etree.tostring(self.tree, pretty_print=True, encoding='unicode')
        return ""

    def _ensure_ids(self):
        """Ensures all visual elements have an ID."""
        if self.root is None:
            return
        
        count = 1
        for elem in self.root.iter():
            tag = etree.QName(elem).localname
            if tag in ['path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'text', 'g']:
                if 'id' not in elem.attrib:
                    elem.attrib['id'] = f"gen_{tag}_{count}"
                    count += 1

    def change_color(self, element_id, new_color):
        """Changes the fill/stroke of an element by ID."""
        if self.root is None:
            return False

        elements = self.root.xpath(f"//*[@id='{element_id}']")
        if not elements:
            return False
        
        self._save_state() # Save before modify
        
        el = elements[0]
        if 'style' in el.attrib:
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
        
        self._save_state()
        
        group = etree.Element("g", id=group_id)
        elements_to_move = []
        
        for eid in element_ids:
            els = self.root.xpath(f"//*[@id='{eid}']")
            if els:
                elements_to_move.append(els[0])
        
        if not elements_to_move:
            return False

        parent = elements_to_move[0].getparent()
        parent.insert(parent.index(elements_to_move[0]), group)
        
        for el in elements_to_move:
            group.append(el)
            
        return True

    def ungroup_elements(self, element_ids):
        """Ungroups selected group elements."""
        if self.root is None or not element_ids:
            return False

        self._save_state()
        changed = False

        for eid in element_ids:
            els = self.root.xpath(f"//*[@id='{eid}']")
            if els:
                group = els[0]
                # Check if it is a group
                if etree.QName(group).localname == 'g':
                    parent = group.getparent()
                    index = parent.index(group)
                    
                    # Move children up
                    for child in list(group):
                        parent.insert(index, child)
                        index += 1
                    
                    # Remove empty group
                    parent.remove(group)
                    changed = True
        
        return changed

    def delete_elements(self, element_ids):
        """Deletes multiple elements by ID."""
        if self.root is None or not element_ids:
            return False
            
        self._save_state()
        changed = False
        
        for eid in element_ids:
            elements = self.root.xpath(f"//*[@id='{eid}']")
            if elements:
                el = elements[0]
                parent = el.getparent()
                if parent is not None:
                    parent.remove(el)
                    changed = True
        
        return changed
