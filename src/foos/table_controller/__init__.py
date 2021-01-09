
def TableControllerFactory(sim=True):
  if sim:
    from .sim import SimTableController
    return SimTableController()
  else:
    from .live import LiveTableController
    return LiveTableController()
