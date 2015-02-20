import nuke

def alignVertically():
  xresult = None
  for n in nuke.selectedNodes():
    if xresult is None:
      xresult = n.xpos()
    else:
      n.setXpos(xresult)

#alignVertically()
