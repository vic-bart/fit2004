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
  
  def get_children(self) -> list[SuffixTrieNode]:
    return self.children
  
  def has_child(self, character:str) -> bool:
    for child in self.children:
      if child.get_character() == character:
        return True
    return False
  
  def has_children(self) -> bool:
    return (len(self.children) > 0)

class SuffixTrie():

  def __init__(self):
    self.terminal_character:str = "$"

  def insert(self, string:str) -> None:
    """
    Populates a suffix trie.
    """
    self.string = string + self.terminal_character
    self.root = SuffixTrieNode()
    self.root.set_character("Root")

    for i in range(len(self.string)):

      node:SuffixTrieNode = self.root

      for j in range(i, len(self.string)):

        if not node.has_child(self.string[j]):

          node.set_child(self.string[j])

        node = node.get_child(self.string[j])

  def __str__(self) -> str:
  
    table = [[] for _ in range(len(self.string) * 2)]
    row = 1
    targets = [3]

    queue = [[[self.root]]]

    while len(queue) > 0:
      layer = queue.pop(0)
      new_layer = []
      new_targets = []

      while len(layer) > 0:

        group = layer.pop(0)

        while len(group) > 0:

          node = group.pop(0)
          children = node.get_children()
          if len(children) == 0:
            continue
          new_layer.append(children)
          
          for child in children:
            for char in list(" " + child.get_character()):
              table[row].append(char)
            new_targets.append(len(table[row])-1)
          if len(children) == 1:
            for char in list(" |"):
              table[row-1].append(char)
            target = len(table[row-1])-1
          elif len(children) == 2:
            table[row].insert(-1, " ")
            table[row].insert(-1, " ")
            new_targets[-1] += 2
            for char in list("  _|_ "):
              table[row-1].append(char)
            target = len(table[row-1])-3
          else:
            for char in list("  " + "_" * (len(children)-2) + "|" + "_" * (len(children)-2) + " "):
              table[row-1].append(char)
            target = len(table[row-1]) - 2 - (len(children)-2)
          if target > targets[0]:
            difference = target - targets[0]
            for i in range(row-2, -1, -1):
              padding = table[i][targets[0]-1]
              if padding == "|":
                padding = "_"
              for _ in range(difference):
                table[i].insert(targets[0], padding)
            for i in range(len(targets)):
              targets[i] += difference
          if target < targets[0]:
            difference = targets[0] - target
            for i in range(row, row-2, -1):
              padding = table[i][-2]
              for _ in range(difference):
                table[i].insert(-1, padding)
            for i in range(len(new_targets)-len(children), len(new_targets)):
              new_targets[i] += difference
          targets.pop(0)

      row += 2
      targets = new_targets

      if len(new_layer) > 0:
        queue.append(new_layer)

    string = ""
    for row in range(len(table)):
      if len(table[row]) == 0:
        return string
      for col in range(len(table[row])):
        string += table[row][col]
      string += "\n"
    return string

if __name__ == "__main__":
  suffix_trie:SuffixTrie = SuffixTrie()
  string:str = "ABCDEFGHIJKLMNOPQRSTUVWXYZAABBCCDDEEFFGGSHDNWOANDOAWEFEF"
  suffix_trie.insert(string)
  print(suffix_trie)