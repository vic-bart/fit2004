"""
"""

from typing import TypeVar

SuffixTrieNode = TypeVar("SuffixTrieNode")

class SuffixTrieNode():

  def __init__(self) -> None:
    self.character = None
    self.children = []

  def set_character(self, character:str) -> None:
    self.character = character

  def get_character(self) -> str:
    return self.character

  def set_child(self, character:str) -> None:
    node:SuffixTrieNode = SuffixTrieNode()
    node.set_character(character)
    self.children.append(node)

  def get_child(self, character:str) -> SuffixTrieNode:
    for child in self.children:
      if child.get_character() == character:
        return child
    raise ValueError
  
  def has_child(self, character:str) -> bool:
    for child in self.children:
      if child.get_character() == character:
        return True
    return False
  
  def has_children(self) -> bool:
    return (len(self.children) > 0)
  
  def insert(self, suffix:str):
    if not self.has_child(suffix[0]):
      self.set_child(suffix[0])
    if len(suffix) > 1:
      node = self.get_child(suffix[0])
      node.insert(suffix[1:])

class SuffixTrie():

  def __init__(self):
    self.terminal_character:str = "$"

  def insert(self, string:str) -> None:
    self.string = string
    self.root = SuffixTrieNode()

    for i in range(len(string)):
      self.root.insert(string[i:] + self.terminal_character)

    self.root.insert(self.terminal_character)

  def __str__(self) -> str:
    array:list[list[str]] = [[] for _ in range((2 * (len(self.string)+1)) + 1)]
    array[0].append("root")
    stack:list[SuffixTrieNode] = [self.root]
    depth:int = 2
    column:list[int] = [0]
    self._str_aux(array, stack, depth, column)
    string:str = ""
    for sub_array in array:
      for character in sub_array:
        string += character + " "
      string += "\n"
    return string
  
  def _str_aux(self, array:list[list[str]], stack:list[SuffixTrieNode], depth:int, column:list[int]):
    for i in range(len(stack[-1].children)):
      if i > 0:
        column[0] += 1
      child = stack[-1].children[i]
      while (len(array[depth-1])) < column[0]:
        array[depth-1].append(" ")
      while (len(array[depth])) < column[0]:
        array[depth].append(" ")
      if i == 0:
        array[depth-1].append("|")
      else:
        array[depth-1].append("\\")
      array[depth].append(child.get_character())
      stack.append(child)
      self._str_aux(array, stack, depth+2, column)
      stack.pop()


if __name__ == "__main__":
  suffix_trie:SuffixTrie = SuffixTrie()
  string:str = "ABCABCABCABC"
  suffix_trie.insert(string)
  print(suffix_trie)