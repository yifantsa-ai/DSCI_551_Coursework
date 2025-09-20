from filesystem import Session

class HW2Session(Session):
  def __init__(self, fs):
    super().__init__(fs)

  # you can add any helper function here, if needed
  def remove_node(self, node_name):
    #set index counter
    index_count = 0
    #traverse the children list
    for child in self.curr_dir.children:
      if (child.name == node_name.name):
        break
      else:
        index_count = index_count + 1
    #pop out the node by index
    self.curr_dir.children.pop(index_count)
    #clearup all info to delete Node
    node_name.parent = None
    node_name.node_type = None
    node_name.name = None
    return None
  
  #recursive printing function
  def print_fs(self, node):
    #print current directory + node type
    print(self.pwd() + ',' + self.curr_dir.node_type)
    #traverse current directory
    for child in node.children:
      #if children is a file, print it
      if child.node_type == 'file':
        print(self.pwd() + '/' + child.name + ',' + child.node_type)
      else:
        #if directory, go into it and call the method recursively
        self.curr_dir = child
        self.print_fs(self.curr_dir)
    #set current directory to parent for traversing
    if self.curr_dir != self.root:
      self.curr_dir = self.curr_dir.parent

  # This removes the directory dir_name from the current working directory
  # It should report errors when
  #   * dir_name does not exist
  #   * dir_name is not empty
  #   * dir_name is not a directory
  def rmdir(self, dir_name):
    # first check if directory exists
    if not any(dir_name == child.name for child in self.curr_dir.children):
      print(f'{dir_name} does not exist!')
      return None
    else:
      #get the node of the dir_name
      node = next(child for child in self.curr_dir.children if child.name == dir_name)
      #check if dir_name is a directory
      if (node.node_type != 'directory'):
        print(f'{dir_name} is not a directory!')
        return None
      elif (node.children):
        #if the directory is not empty, print err msg
        print(f'{dir_name} is not empty!')
        return None
      else:
        #call remove node method
        self.remove_node(node)
        return None
      
  # this removes a file "file_name" from the current working directory
  # it should report errors when:
  #   * file_name does not exist
  #   * file_name is a directory
  def rm(self, file_name):
    # first check if file exists
    if not any(file_name == child.name for child in self.curr_dir.children):
      print(f'{file_name} does not exist!')
      return None
    else:
      #get the node of the file_name
      node = next(child for child in self.curr_dir.children if child.name == file_name)
      #check if file_name is a file
      if (node.node_type != 'file'):
        print(f'{file_name} is not a file!')
        return None
      else:
        #call remove node method
        self.remove_node(node)
        return None

  # This emulates the hdfs oiv (offline image viewer) command to print the
  # entire namespace of file system. In other words, it lists all file system
  # objects (file or directory), one line at a time. For each object,
  # it shows the path to the object and the type of object, seperated by comma.
  # For example,
  #           /,directory
  #           /home,directory
  #           /home/john,directory
  #           /home/john/hw1.py,file
  #           ...
  #
  def dump_fsimage(self):
    #set current directory to root
    self.curr_dir = self.root
    return self.print_fs(self.curr_dir)
    
      