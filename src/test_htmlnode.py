import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestParentNode(unittest.TestCase):
  def test_multiple_children(self):
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    res = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
    self.assertEqual(node.to_html(), res)
  
  def test_one_child(self):
    node = ParentNode("p", [LeafNode("b", "Bold text")])
    self.assertEqual(node.to_html(), '<p><b>Bold text</b></p>')
  
  def test_nested_parents(self):
    node = ParentNode(
      "div",
      [
        ParentNode("p", [LeafNode(None, "Normal text"), LeafNode("b", "Bold Text")]),
        ParentNode("a", [LeafNode(None, "a link")])
      ]
    )
    res = '<div><p>Normal text<b>Bold Text</b></p><a>a link</a></div>'
    self.assertEqual(node.to_html(), res)
  
  def test_deep_tree(self):
    node = ParentNode(
      "div",
      [
        ParentNode("div", [
          ParentNode("p", [LeafNode(None, "Normal text"), LeafNode("b", "Bold Text")]),
          LeafNode(None, "some text")
        ]),
        ParentNode("a", [LeafNode(None, "a link")])
      ]
    )
    res = '<div><div><p>Normal text<b>Bold Text</b></p>some text</div><a>a link</a></div>'
    self.assertEqual(node.to_html(), res)
  
  def test_deep_tree_with_props(self):
    node = ParentNode(
      "div",
      [
        ParentNode("div", [
          ParentNode("p", [LeafNode(None, "Normal text"), LeafNode("b", "Bold Text")], {'class': 'paragraph', 'id': 'top-paragraph'}),
          LeafNode(None, "some text")
        ]),
        ParentNode("a", [LeafNode(None, "a link")])
      ],
      {'id': 'root'}
    )
    res = '<div id="root"><div><p class="paragraph" id="top-paragraph">Normal text<b>Bold Text</b></p>some text</div><a>a link</a></div>'
    self.assertEqual(node.to_html(), res)

if __name__ == 'main':
  unittest.main()