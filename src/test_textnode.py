import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("textnode", "italic")
    node2 = TextNode("textnode", "italic")
    self.assertEqual(node, node2)
  
  def test_eq2(self):
    node = TextNode("a text node", "bold", "http://awesome.net")
    node2 = TextNode("a text node", "bold", "http://awesome.net")
    self.assertEqual(node, node2)

  def test_eq_false_url(self):
    node = TextNode("a text node", "bold", "http://awesome.net")
    node2 = TextNode("a text node", "bold", "http://awesome.ne")
    self.assertNotEqual(node, node2)

  def test_eq_false_tt(self):
    node = TextNode("a text node", "bolds")
    node2 = TextNode("a text node", "bold")
    self.assertNotEqual(node, node2)
  
  def test_eq_false_t(self):
    node = TextNode("a text nodes", "bold")
    node2 = TextNode("a text node", "bold")
    self.assertNotEqual(node, node2)
  
  def test_repr(self):
    node = TextNode("textnode", "bold", "https://cool.com")
    self.assertEqual(str(node), "TextNode(textnode, bold, https://cool.com)")

  def test_repor_no_url(self):
    node = TextNode("textnode", "bold")
    self.assertEqual(str(node), "TextNode(textnode, bold, None)")

if __name__ == "__main__":
  unittest.main()