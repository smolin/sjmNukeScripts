import nuke

def alignHorizontally():
  yresult = None
  for n in nuke.selectedNodes():
    if yresult is None:
      yresult = n.ypos()
    else:
      n.setYpos(yresult)

#alignHorizontally()
