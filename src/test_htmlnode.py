import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
  def test_one_prop_to_html(self):
    node = HTMLNode('div', 'hello world', props={'class': 'a-class-name'})
    self.assertEqual(node.props_to_html(), 'class="a-class-name"')
  
  def test_two_props_to_html(self):
    child_node = HTMLNode('li', 'item')
    node = HTMLNode('ul', children=[child_node], props={'class': 'a-list', 'id': 'an-id'})
    self.assertEqual(node.props_to_html(), 'class="a-list" id="an-id"')
  
  def test_no_props_to_html(self):
    node = HTMLNode('div', 'hello', props={})
    self.assertEqual(node.props_to_html(), '')

class TestLeafNode(unittest.TestCase):
  def test_render_raw_text(self):
    node = LeafNode(value='some text')
    self.assertEqual(node.to_html(), 'some text')
  
  def test_render_leaf_elem(self):
    node = LeafNode("p", "This is a paragraph of text.")
    self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')
  
  def test_render_leaf_with_props(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

if __name__ == 'main':
  unittest.main()