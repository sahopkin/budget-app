class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []


  def __repr__(self):
    self.title = self.name.center(30, "*")
    self.report = [self.title]
    self.total = 0

    for obj in self.ledger:
      self.desc = obj["description"]
      self.amt = obj["amount"]
      self.total += self.amt
      if len(self.desc) > 23:
        self.desc = self.desc[0:23]

      self.amt_str = "%.2f" % self.amt
      
      self.report_entry = f'{self.desc}{self.amt_str.rjust(30 - len(self.desc))}'

      self.report.append(self.report_entry)

    self.total_str = "%.2f" % self.total
    self.report.append(f'Total: {self.total_str}')
    self.full_report = '\n'.join(self.report)
    
    return self.full_report

  
  def deposit(self, amount, desc=None):
    self.amount = amount
    if desc == None:
      self.desc = ""
    else:
      self.desc = desc
    self.deposit_obj = {
      "amount": self.amount,
      "description": self.desc
    }
    self.ledger.append(self.deposit_obj)
  

  def withdraw(self, amount, desc=None):
    self.amount = amount
    if desc == None:
      self.desc = ""
    else:
      self.desc = desc

    self.withdrawal_obj = {
      "amount": self.amount * -1,
      "description": self.desc
    }

    if self.check_funds(self.amount) == True:
      self.ledger.append(self.withdrawal_obj)
      return True
    else:
      return False
      

  def get_balance(self):
    balance = 0
    for object in self.ledger:
      balance += object["amount"]
    return balance


  def transfer(self, amount, category):
    self.amount = amount
    self.category = category
    self.w_desc = f'Transfer to {self.category.name}'
    self.d_desc = f'Transfer from {self.name}'
    
    if self.check_funds(self.amount) == True:
      self.withdraw(self.amount, self.w_desc)
      self.category.deposit(self.amount, self.d_desc)
      return True
    else:
      return False


  def check_funds(self, amount):
    self.amount = amount
    if self.amount > self.get_balance():
      return False
    else:
      return True



def create_spend_chart(categories):
    #build the structure for the graph and rows for category titles
  cat_len = len(categories)
  graph_list = ["Percentage spent by category"]
  for num in range(100, -10, -10):
    empty_space_list = [" " for x in range(cat_len * 3 + 3)]
    empty_space_list[0] = str(num).rjust(3)
    empty_space_list[1] = "|"
    graph_list.append(empty_space_list)

  #create base_line for graph
  base_line = [" " if x < 2 else "-" for x in range(cat_len * 3 + 3)]
  base_line[0] = " ".rjust(3)
  graph_list.append(base_line)

  #create rows of empty lists with enough rows to match the length of the longest category name and append them to graph_list below the base_line
  cat_name_lens = [len(x.name) for x in categories]
  max_cat_len = max(cat_name_lens)
  for i in range(max_cat_len):
    empty_title_row = [" " for x in range(cat_len * 3 + 3)]
    empty_title_row[0] = " ".rjust(3)
    graph_list.append(empty_title_row)
  
  #calculate total withdrawals across all categories
  total_wds = 0
  
  for cat in categories:
    for entry in cat.ledger:
      if entry["amount"] < 0:
        total_wds += abs(entry["amount"])

  #use this index variable for placing "o"s on the graph by category.  The first bar occurs at index 3.  Each additional bar is a multiple of 3, so for loop will end with x_idx += 3
  x_idx = 3
  for cat in categories:
    cat_wd = 0
    for entry in cat.ledger:
      if entry["amount"] < 0:
        cat_wd += abs(entry["amount"])
    
    #calculate category withdrawal percentage and convert to a string
    cat_wd_per = (cat_wd / total_wds) * 100
    cat_wd_per = str(int(cat_wd_per // 10 * 10))

    #plot "o" for every number <= percentage withdrawn by category
    for row in graph_list[1:12]:
      if row[0] <= cat_wd_per.rjust(3):
        row[x_idx] = "o"
    
    #Label columns with the category name spelled out vertically downards below the base_line
    row = 13
    for letter in cat.name:
      graph_list[row][x_idx] = letter
      row += 1

    #update the x position by 3 for the next column and category title
    x_idx += 3

  #convert list of lists to list of strings
  string_graph = []
  for row in graph_list:
    string_graph.append("".join(row))
  
  #join list of strings as one large string
  budget_graph = '\n'.join(string_graph)
  return budget_graph