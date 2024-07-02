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
    array:list[list[str]] = [[] for _ in range((2 * (len(self.string)+1)) + 1)]
    array[0].append("root")
    stack:list[SuffixTrieNode] = [self.root]
    depth:int = 2
    column:list[int] = [0]
    self._str_aux(array, stack, depth, column)
    string:str = ""
    for i in range(len(array)):
      try:
        j = array[i].index("\\")
        if array[i+1][j] == "$":
          while array[i][j-1] == " ":
            value = array[i][j-1]
            array[i][j-1] = array[i][j]
            array[i][j] = value
            value = array[i+1][j-1]
            array[i+1][j-1] = array[i+1][j]
            array[i+1][j] = value
            j -= 1
      except ValueError:
        pass

    empty_column = True
    while empty_column:
      for j in range(len(array[1])):
        empty_column = True
        for i in range(1, len(array)):
          try:
            if array[i][j] != " ":
              empty_column = False
              break
          except IndexError:
            break
        if empty_column:
          for i in range(1, len(array)):
            try:
              del array[i][j]
            except IndexError:
              break

    for i in range(len(array)):
      for j in range(len(array[i])):
        string += array[i][j] + " "
      string += "\n"
    return string
  
  def _str_aux(self, array:list[list[str]], stack:list[SuffixTrieNode], depth:int, column:list[int]):
    for i in range(len(stack[-1].children)):
      child = stack[-1].children[i]
      if (i > 0):
        column[0] += 1
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

  def temp1(self, stack, current_depth, previous_depth, array, spacing):
    for i in range(len(stack[-1].children)):
      child = stack[-1].children[i]
      stack.append(child)
      previous_depth = self.temp1(stack, current_depth+1, previous_depth, array, spacing)
    node = stack.pop()
    print(node.get_character(), previous_depth - current_depth)
    previous_depth = current_depth
    array[current_depth*2].append(node.get_character())
    return previous_depth

  def temp2(self, array, depth=0):
    print('')
    for value in array:
      if type(value) == str:
        print(f"{' ' * depth}{value}")
      else:
        self.temp2(value, depth+1)

  def temp3(self):   

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
  print(suffix_trie.temp3())
  exit(0)
  stack = [suffix_trie.root]
  current_depth = 0
  previous_depth = len(suffix_trie.string)+1
  array = [[] for _ in range((len(suffix_trie.string)*2)+1)]
  spacing = ' ' * 1
  suffix_trie.temp1(stack, current_depth, previous_depth, array, spacing)
  for subarray in array:
    print(subarray)
  # print(suffix_trie)