from foos.table_controller import TableControllerFactory

if __name__ == "__main__":
  table = TableControllerFactory()
  while table.run():
    pass