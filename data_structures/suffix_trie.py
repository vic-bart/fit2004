"""
"""
from typing import TypeVar

SuffixTrieNode = TypeVar("SuffixTrieNode")

class SuffixTrieNode():

  def __init__(self) -> None:
    self.index = None
    self.children = []
    self.count = 0

  def set_index(self, index:int) -> None:
    self.index = index

  def get_index(self) -> str:
    return self.index

  def set_child(self, index:int) -> None:
    node:SuffixTrieNode = SuffixTrieNode()
    node.set_index(index)
    self.children.append(node)

  def get_child(self, string:str, index:int) -> SuffixTrieNode|None:
    for child in self.children:
      if string[child.get_index()] == string[index]:
        return child
    return None

  def get_children(self) -> list[SuffixTrieNode]:
    return self.children

  def has_children(self) -> bool:
    return (len(self.children) > 0)

  def set_count(self, count:int) -> None:
    self.count = count

  def get_count(self) -> int:
    return self.count

class SuffixTrie():

  def __init__(self):
    self.terminal_character:str = "$"

  def insert(self, string:str) -> None:
    """
    Populates a suffix trie.
    """
    self.string = string + self.terminal_character
    self.root = SuffixTrieNode()

    for i in range(len(self.string)):

      node:SuffixTrieNode = self.root

      for j in range(i, len(self.string)):

        if node.get_child(self.string, j) is None:

          node.set_child(j)

        node.set_count(node.get_count() + 1)
        node = node.get_child(self.string, j)

  def find(self, string:str, start:int, end:int) -> int|None:
    """
    Returns the lowest index for a substring in a given inserted string within the range {start, ..., end - 1}.
    """
    node = self.root
    length = -1

    for i in range(len(string)):

      child_found = False
      
      for child in node.get_children():
        
        if string[i] == self.string[child.get_index()]:

          node = child
          child_found = True
          length += 1
          break

      if not child_found:
        return None
  
    return (node.get_index() - length)

  def count(self, string:str) -> int:
    """
    Returns the number of occurences for a substring in a given inserted string. Note that overlapping words are included (e.g. "ABBABBA" will count "ABBA" twice).
    """
    node = self.root

    for i in range(len(string)):
      
      child_found = False

      for child in node.get_children():
        
        if string[i] == self.string[child.get_index()]:

          node = child
          child_found = True
          break

      if not child_found:
        return 0
  
    return node.get_count()

  def __str__(self) -> str:
    """
    Creates a string representation of a suffix trie.
    """
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

          new_layer.append(children[:])
          newest_target = len(new_targets)
          boundary = len(table[row])
          
          for child in children:

            for char in list(" " + self.string[child.get_index()]):

              table[row].append(char)

            if child.has_children():

              new_targets.append(len(table[row])-1)

          if len(children) == 1:

            for char in list(" |"):

              table[row-1].append(char)

            target = len(table[row-1])-1

          elif len(children) == 2:

            table[row].insert(-1, " ")
            table[row].insert(-1, " ")

            if children[-1].has_children():

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

              if (padding == "|") or ((padding == " ") and (targets[0] < len(table[i])) and (table[i][targets[0]] == "_")):

                padding = "_"

              if padding not in ["_", "|", " "]:
                padding = " "

              for _ in range(difference):

                table[i].insert(targets[0], padding)

            for i in range(len(targets)):
              targets[i] += difference

          if target < targets[0]:
            
            difference = targets[0] - target

            for i in range(row, row-2, -1):

              padding = table[i][boundary]

              for _ in range(difference):

                table[i].insert(boundary, padding)
                
            for i in range(newest_target, len(new_targets)):

              new_targets[i] += difference

          targets.pop(0)
          
      row += 2
      targets = new_targets

      if len(new_layer) > 0:

        queue.append(new_layer)

    string = (" " * (table[0].index("|")-1)) + "Root\n"

    for i in range(len(table)):

      if len(table[i]) == 0:

        break

      for j in range(len(table[i])):

        string += table[i][j]

      string += "\n"

    return string

if __name__ == "__main__":
  suffix_trie:SuffixTrie = SuffixTrie()
  string:str = "ABBBBABBB"
  suffix_trie.insert(string)
  print(suffix_trie)
  # i = suffix_trie.find("S")
  # print(i, string[i])
  print(suffix_trie.count("ABBA"))