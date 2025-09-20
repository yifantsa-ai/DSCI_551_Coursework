import requests
import json

############ add codes here, if needed

class TodoClient:
  # this method simply remembers the given dburl
  def __init__(self, dburl):
    self.db_path = dburl
  
  # Remove all existing tasks from the todo list.
  # If the removal was successful, return "Success!".
  # otherwise, return the error message from the Firebase server.
  # The error message should be in a Python dictionary, e.g., 
  #        {'error': '404 Not Found'}
  # clear() method should be called first before any tasks are added to the 
  #    todo list.
  # You should assume that no other methods will be called on the todo list,
  # if the clear method failed.
  def clear(self):
    # get the info of db first
    resp = requests.get(self.db_path + ".json")
    # if error, print error msg
    if resp.ok == False:
      print(json.loads(resp.text))
    else:
      # if no task in tasks, just Success
      if json.loads(resp.text) ==  None:
        print('"Success!"')
      else:
        task_dict = json.loads(resp.text)
        # delete tasks one by one
        for key in task_dict.keys():
          resp_clear = requests.delete(self.db_path + "/" + key + ".json")
          #if there's error not affecting get method
          if resp_clear.ok == False:
            print(json.loads(resp_clear.text))
            return
        print('"Success!"')

  # if the task exists in the todo list,, 
  #    return an error message in this format:
  #       Error in add_task: task "xyz" already exists!
  #         where xyz should be replaced with the actual task name
  # else, 
  #    add the task to the todo list stored in Firebase, and
  #    return "Success!"
  def add_task(self, task):
    # check if task exists
    resp = requests.get(self.db_path + "/" + task + ".json")
    if json.loads(resp.text) ==  None:
      #if not, add task
      requests.patch(self.db_path + ".json", json = {task: "pending"})
      print('"Success!"')
    else:
      #if yes, print err msg
      print('"Error in add_task: task "' + task + '" already exists!"')
  
  # if the task does not exist in the list, 
  #    return an error message in this format:
  #        Error in delete_task: task "xyz" does not exist!
  #         where xyz should be replaced with the actual task name
  # else, 
  #    remove the task from the list, and 
  #    return "Success!"
  def delete_task(self, task):
    # check if the task exists
    resp = requests.get(self.db_path + "/" + task + ".json")
    if json.loads(resp.text) ==  None:
      # if not exists, print err msg
      print('"Error in delete_task: task "' + task + '" does not exist!"')
    else:
      # if exists, delete
      requests.delete(self.db_path + "/" + task + ".json")
      print('"Success!"')
  
  # if the task does not exist in the list, 
  #    return an error message in this format:
  #        Error in mark_completed: task "xyz" does not exist!
  #         where xyz should be replaced with the actual task name
  # else, 
  #    change the status of the task to "completed", and 
  #    return "Success!"
  def mark_completed(self, task):
    #check if the task exists
    resp = requests.get(self.db_path + "/" + task + ".json")
    if json.loads(resp.text) ==  None:
      #if not, print err msg
      print('"Error in mark_completed: task "' + task + '" does not exist!"')
    else:
      #if exists, change status
      requests.patch(self.db_path + ".json", json = {task: "completed"})
      print('"Success!"')

  # return a list of tasks in the given status, 
  # and empty list if no such tasks
  def get_task_by_status(self, status):  # status is either completed or pending
    #get all tasks
    #resp = requests.get(self.db_path + ".json")

    #get request based on status
    resp = requests.get(self.db_path + '.json?orderBy="$value"&equalTo="' + status +'"')

    #create dictionary & output empty list
    task_dict = json.loads(resp.text)
    task_arr = []
    #No tasks
    if task_dict == None:
      print(task_arr)
    else:
      #add tasks recursively
      for key in task_dict.keys():
        #if task_dict[key] == status: -> for get all tasks, unused
        #append key to output list if the same status
        task_arr.append(key)
      #will print empty list if no match
      print(task_arr)
  
  # return a dictionary of task:status pairs, 
  # and None if no tasks in the todo list.
  def get_all_tasks(self):
    #check if empty task
    resp = requests.get(self.db_path + ".json")
    if json.loads(resp.text) == None:
      #print None for empty task
      print(None)
    else:
      #print all tasks in dictionary
      print(resp.json())
  
  ############ add codes here if needed