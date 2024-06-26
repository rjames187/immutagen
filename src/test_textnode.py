import unittest

from textnode import TextNode, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from textnode import text_type_bold, text_type_code, text_type_italic, text_type_text, text_type_image, text_type_link

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

class TestExtractLinksAndImages(unittest.TestCase):
  def test_extract_images(self):
    text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    res = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
    self.assertEqual(extract_markdown_images(text), res)
  
  def test_extract_links(self):
    text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    res = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
    self.assertEqual(extract_markdown_links(text), res)

  def test_extract_links_ignore_images(self):
    text = "This is text with a ![image](https://www.example.com) and [another](https://www.example.com/another)"
    res = [("another", "https://www.example.com/another")]
    self.assertEqual(extract_markdown_links(text), res)

  def test_extract_no_results(self):
    text = "here is some text [ fsdafsadf ) ( ] fdasf"
    self.assertEqual(extract_markdown_images(text), [])
    self.assertEqual(extract_markdown_links(text), [])

class TestSplitNodesLinksAndImages(unittest.TestCase):
  def test_split_image(self):
    node = TextNode(
      "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      text_type_text,
    )
    res = [
      TextNode("This is text with an ", text_type_text),
      TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and another ", text_type_text),
      TextNode(
          "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
    ]
    self.assertEqual(split_nodes_image([node]), res)
  
  def test_split_link(self):
    node = TextNode(
      "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      text_type_text,
    )
    res = [
      TextNode("This is text with an ", text_type_text),
      TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and another ", text_type_text),
      TextNode(
          "second link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      ),
    ]
    self.assertEqual(split_nodes_link([node]), res)
  
  def test_split_link_no_results(self):
    node = TextNode("here is some text [ fsdafsadf ) ( ] fdasf", text_type_text)
    self.assertEqual(split_nodes_link([node]), [node])
  
  def test_split_image_no_results(self):
    node = TextNode("here is some text ![ fsdafsadf ) ( ] fdasf", text_type_text)
    self.assertEqual(split_nodes_image([node]), [node])
  
  def test_split_dup_images(self):
    node = TextNode("![howdy](https://funny.com/howdy.png) cool ![howdy](https://funny.com/howdy.png)", text_type_text)
    res = [
      TextNode("howdy", text_type_image, "https://funny.com/howdy.png"),
      TextNode(" cool ", text_type_text),
      TextNode("howdy", text_type_image, "https://funny.com/howdy.png")
    ]
    self.assertEqual(split_nodes_image([node]), res)
  
  def test_split_dup_links(self):
    node = TextNode("[howdy](https://funny.com/howdy.png) cool [howdy](https://funny.com/howdy.png)", text_type_text)
    res = [
      TextNode("howdy", text_type_link, "https://funny.com/howdy.png"),
      TextNode(" cool ", text_type_text),
      TextNode("howdy", text_type_link, "https://funny.com/howdy.png")
    ]
    self.assertEqual(split_nodes_link([node]), res)
  
  def test_split_multiple_nodes(self):
    node1 = TextNode("[howdy](https://funny.com/howdy.png) cool [howdy](https://funny.com/howdy.png)", text_type_text)
    node2 = TextNode("here is some text [ fsdafsadf ) ( ] fdasf", text_type_text)
    node3 = TextNode(
      "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
      text_type_text,
    )
    res = [
      TextNode("howdy", text_type_link, "https://funny.com/howdy.png"),
      TextNode(" cool ", text_type_text),
      TextNode("howdy", text_type_link, "https://funny.com/howdy.png"),
      TextNode("here is some text [ fsdafsadf ) ( ] fdasf", text_type_text),
      TextNode("This is text with an ", text_type_text),
      TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and another ", text_type_text),
      TextNode(
          "second link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
      )
    ]
    self.assertEqual(split_nodes_link([node1, node2, node3]), res)

  def test_split_link_igore_image(self):
    node = TextNode("[howdy](https://funny.com/howdy.png) cool ![howdy](https://funny.com/howdy.png)", text_type_text)
    res = [
      TextNode("howdy", text_type_link, "https://funny.com/howdy.png"),
      TextNode(" cool ![howdy](https://funny.com/howdy.png)", text_type_text)
    ]
    self.assertEqual(split_nodes_link([node]), res)
  
class TestTextToTextnode(unittest.TestCase):
  def test_all_text_types(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
    res = [
      TextNode("This is ", text_type_text),
      TextNode("text", text_type_bold),
      TextNode(" with an ", text_type_text),
      TextNode("italic", text_type_italic),
      TextNode(" word and a ", text_type_text),
      TextNode("code block", text_type_code),
      TextNode(" and an ", text_type_text),
      TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
      TextNode(" and a ", text_type_text),
      TextNode("link", text_type_link, "https://boot.dev"),
    ]
    self.assertEqual(text_to_textnodes(text), res)
  
  def test_no_special_types(self):
    text = "here is some text [ fsdafsadf )! ( ] fdasf"
    res = [TextNode("here is some text [ fsdafsadf )! ( ] fdasf", text_type_text)]
    self.assertEqual(text_to_textnodes(text), res)

class TestSplitBlocks(unittest.TestCase):
  def test_all_blocks(self):
    text = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
    res = [
          "This is **bolded** paragraph",
          "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
          "* This is a list\n* with items"
    ]
    self.assertEqual(markdown_to_blocks(text), res)
  
  def test_many_newlines(self):
    text = "hello this is a block\n\n\n\nhere is a\n second block\n\nhere is a third block"
    res = [
      "hello this is a block",
      "here is a\n second block",
      "here is a third block"
    ]
    self.assertEqual(markdown_to_blocks(text), res)
  
  def test_leading_trailing_whitespaces(self):
    text = "   hello\n\n    hi     \n\nsdfsgd  "
    res = [
      "hello",
      "hi",
      "sdfsgd"
    ]
    self.assertEqual(markdown_to_blocks(text), res)


if __name__ == "__main__":
  unittest.main()