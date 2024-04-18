class HTMLNode:
  def __init__(self, tag: str=None, value: str=None, children: 'list[HTMLNode]'=None, props: dict=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
    