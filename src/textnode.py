class TextNode:
  def __init__(self, text:str, text_type: str, url: str=None):
    self.text = text
    self.text_type = text_type
    self.url = url