import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_one_prop_to_html(self):
    node = HTMLNode('div', 'hello world', props={'class': 'a-class-name'})
    self.assertEqual(node.props_to_html(), 'class="a-class-name"')
  
  def test_two_props_to_html(self):
    child_node = HTMLNode('li', 'item')
    node = HTMLNode('ul', children=[child_node], props={'class': 'a-list', 'id': 'an-id'})
    self.assertEqual(node.props_to_html(), 'class="a-list" id="an-id"')

if __name__ == 'main':
  unittest.main()