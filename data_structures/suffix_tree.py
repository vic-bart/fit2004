"""
"""

from typing import TypeVar

SuffixTreeNode = TypeVar("SuffixTreeNode")

class SuffixTreeNode():

  def __init__(self) -> None:
    pass

  def set_character(self, character:str) -> None:
    pass

  def get_character(self) -> str:
    pass

  def set_child(self, character:str) -> None:
    pass

  def get_child(self, character:str) -> SuffixTreeNode:
    pass
  
  def has_child(self, character:str) -> bool:
    pass
  
  def has_children(self) -> bool:
    pass
  
  def insert(self, suffix:str):
    pass

class SuffixTree():

  def __init__(self):
    pass

  def insert(self, string:str) -> None:
    pass


if __name__ == "__main__":
  suffix_trie:SuffixTree = SuffixTree()
  string:str = "ABCABCABC"
  suffix_trie.insert(string)
  print(suffix_trie)