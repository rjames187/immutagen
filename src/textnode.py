class TextNode:
  def __init__(self, text:str, text_type: str, url: str=None) -> None:
    self.text = text
    self.text_type = text_type
    self.url = url
  
  def __eq__(self, node1: "TextNode", node2: "TextNode") -> bool:
    if node1.text != node2.text:
      return False
    if node1.text_type != node2.text_type:
      return False
    if node1.url != node1.url:
      return False
    return True