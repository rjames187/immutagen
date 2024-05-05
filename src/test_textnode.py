import unittest

from textnode import TextNode, split_nodes_delimiter, text_type_bold, text_type_code, text_type_italic, text_type_text

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

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_code(self):
    node = TextNode("This is text with a `code block` word", text_type_text)  
    new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    res = [
      TextNode("This is text with a ", text_type_text),
      TextNode("code block", text_type_code),
      TextNode(" word", text_type_text),
    ]
    self.assertEqual(new_nodes, res)
  
  def test_bold(self):
    node = TextNode("This is text with a **bold block** word", text_type_text)  
    new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
    res = [
      TextNode("This is text with a ", text_type_text),
      TextNode("bold block", text_type_bold),
      TextNode(" word", text_type_text),
    ]
    self.assertEqual(new_nodes, res)
  
  def test_italic(self):
    node = TextNode("This is text with a *italic block* word", text_type_text)  
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
    res = [
      TextNode("This is text with a ", text_type_text),
      TextNode("italic block", text_type_italic),
      TextNode(" word", text_type_text),
    ]
    self.assertEqual(new_nodes, res)
  
  def test_multiple_delimiters(self):
    node = TextNode("This is *text* with a *italic block* word", text_type_text)  
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
    res = [
      TextNode("This is ", text_type_text),
      TextNode("text", text_type_italic),
      TextNode(" with a ", text_type_text),
      TextNode("italic block", text_type_italic),
      TextNode(" word", text_type_text),
    ]
    self.assertEqual(new_nodes, res)
  
  def test_back_to_back_delimiters(self):
    node = TextNode("This is *text**italic block* word", text_type_text)  
    new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
    res = [
      TextNode("This is ", text_type_text),
      TextNode("text", text_type_italic),
      TextNode("italic block", text_type_italic),
      TextNode(" word", text_type_text),
    ]
    self.assertEqual(new_nodes, res)

if __name__ == "__main__":
  unittest.main()