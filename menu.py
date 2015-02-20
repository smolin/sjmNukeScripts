# steve molin
print 'in my menu.py'

nuke.pluginAddPath('Gizmos')
nuke.pluginAddPath('Scripts')

# =======================================================================
# FUNCTIONS
# =======================================================================

# per Matthieu Cadet <matthieu.cadet@gmail.com> in nuke users email conversation
#
def autoColorReadNodeType(overrideNode=None):
       if overrideNode == None:
               this = nuke.thisNode()
       else:
               this = overrideNode
       # get the Read node file name
       thisFile = this["file"].evaluate()
       # catch keyword in the filename path to set custom color
       if "/wip/" in thisFile:
               nodeColor = 862912511
       elif "/pub/" in thisFile:
               nodeColor = 4280356351
       else:
               nodeColor = 0
       # set the Read node custom color
       this["tile_color"].setValue(nodeColor)
nuke.addKnobChanged(autoColorReadNodeType, nodeClass="Read")

# align selected nodes on a horizontal line, by Steve Molin
#
def sjmAlignH():
  yresult = None
  for n in nuke.selectedNodes():
    if yresult is None:
      yresult = n.ypos()
    else:
      n.setYpos(yresult)
#
# align selected nodes on a vertical line, by Steve Molin
#
def sjmAlignV():
  xresult = None
  for n in nuke.selectedNodes():
    if xresult is None:
      xresult = n.xpos()
    else:
      n.setXpos(xresult)

# by smolin, expands on the autobackdrop function from nuke/plugins/nukescripts
#
def sjmAutoBackdrop():
  import random
  selNodes = nuke.selectedNodes()
  if not selNodes:
    return nuke.nodes.BackdropNode()
  #
  margin = 20
  minWidth = 1000
  minHeight = 200
  #
  xmin = min([node.xpos() for node in selNodes]) - margin
  xmax = max([node.xpos() + node.screenWidth() for node in selNodes]) + margin
  xmin = min([xmin,(xmin+xmax-minWidth)/2])
  xmax = max([xmax,(xmin+xmax+minWidth)/2])
  #
  ymin = min([node.ypos() for node in selNodes]) - margin
  ymax = max([node.ypos() + node.screenHeight() for node in selNodes]) + margin
  ymin = min([ymin,(ymin+ymax-minHeight)/2])
  ymax = max([ymax,(ymin+ymax+minHeight)/2])
  #
  width = xmax-xmin
  height = ymax-ymin
  n = nuke.nodes.BackdropNode(xpos = xmin, bdwidth = width, ypos = ymin, bdheight = height, tile_color = int((random.random()*(16 - 10))) + 10, note_font_size=99)
  n.showControlPanel()
  #
  # restore node selection
  #
  n['selected'].setValue(False)
  for node in selNodes:
    node['selected'].setValue(True)
  return n

# backdrop font size=99, by Steve Molin
#
def sjmBackdropFonts():
  for i in nuke.allNodes():
    if i.__class__.__name__ == 'BackdropNode':
      i.knob('note_font_size').setValue(189)
      k = i.knob('label')
      k.setText(k.getText().upper())

# Walk the heirarchy up from selected node and return a set of
# all nodes that have the 'file' attribute
#
def sjmFindAllParentReads(n=None):
  if n is None:
    n = nuke.selectedNode()
  result = []
  if n.knob('file'):
    result.append(n)
  ins = n.inputs()
  for i in range(0,n.inputs()):
    input = n.input(i)
    if input:
      if input.knob('file'):
        result.append(input)
      result.extend(sjmFindAllParentReads(input))
  return set(result)

# unhide all inputs, by Steve Molin
#
def sjmHideInputsOff():
  for i in nuke.allNodes():
    if i.knob('hide_input'):
      if i.knob('hide_input').value():
	i.knob('hide_input').setValue(False)

# open a read or write node in a viewer program (djv is the first example)
#
# by steve molin
#
def sjmOpenInViewer(nd=None):
  import subprocess
  if nd is None:
    nd = nuke.selectedNode()
  fp = nd.knobs()['file'].value() % nd.firstFrame()
  args = 'C:\Program Files (x86)\djv 0.8.3\\bin\djv_view.exe %s' % fp
  subprocess.Popen(args)

# load the targets of the writeNodes in a viewer (djv):
# TODO: deal better with %04d; deal with different viewers
#
def sjmOpenAllInViewer():
  for n in nuke.allNodes():
    if n.Class() == 'Write':
      if not n.knob('disable').value():
        sjmOpenInViewer(n)
	#filespec = n.knob('file').value()
	#fn = glob.glob(filespec.replace('%04d','*'))[0]
	#print filespec
	#subprocess.call([r'C:\Program Files (x86)\djv 0.8.3\bin\djv_view.exe',fn])

# step through 'operation' values on a merge node
def sjmMergeOpIncr():
  sn = nuke.selectedNode()
  kn = sn.knobs()['operation']
  kn.setValue(kn.values().index(kn.value())+1)
def sjmMergeOpDecr():
  sn = nuke.selectedNode()
  kn = sn.knobs()['operation']
  kn.setValue(kn.values().index(kn.value())-1)

# use $gui to disable slow nodes when working interactively
#
def sjmToggleDisableExpression():
  mynodes = nuke.selectedNodes()
  for mynode in mynodes:
    myknob = mynode['disable']
    if myknob.isAnimated():
      myknob.clearAnimated()
      myknob.setValue(0)
    else:
      myknob.setExpression('$gui')

# toggle the branch selector on all the switch nodes that are selected
#
def sjmToggleSwitch():
  for mynode in nuke.selectedNodes():
    if mynode.knobs()['which'].value():
      mynode.knobs()['which'].setValue(0)
    else:
      mynode.knobs()['which'].setValue(1)

# see http://docs.thefoundry.co.uk/nuke/63/pythondevguide/basics.html
# and http://docs.thefoundry.co.uk/nuke/63/pythondevguide/custom_panels.html
#
def testMyDialog():
	p=nuke.Panel('my custom panel')
	p.addClipnameSearch('clip path', '/tmp')
	p.addFilenameSearch('file path', '/tmp')
	p.addTextFontPulldown('font browser', '/myFonts/')
	p.addRGBColorChip('some pretty color', '')
	p.addExpressionInput('enter an expression', '4*25')
	p.addBooleanCheckBox('yes or no?', True)
	p.addEnumerationPulldown('my choices', 'over under screen mask stencil')
	p.addScriptCommand('tcl or python code', '')
	p.addSingleLineInput('just one line', 'not much space')
	p.addMultilineTextInput('multiple lines of user input text', 'lineA\nlineB')
	p.addNotepad('write something', 'some very long text could go in here. For now this is just some random default value')
	p.addPasswordInput('password', 'donttellanyone')
	p.addButton('over')
	p.addButton('under')
	p.addButton('mask')
	result=p.show()
	print result

# from http://docs.thefoundry.co.uk/nuke/63/pythondevguide/custom_panels.html
#
try:
  #
  ## example PySide panel that implements a simple web browser in Nuke
  ## JW 12/10/11
  #
  import nuke
  import nukescripts
  from nukescripts import panels
  #
  from PySide.QtGui import *
  from PySide.QtCore import *
  from PySide.QtWebKit import *
  #
  class WebBrowserWidget(QWidget):
    def changeLocation(self):
      url = self.locationEdit.text()
      if not url.startswith( 'http://' ):
        url = 'http://' + url
      self.webView.load( QUrl(url) )
    def urlChanged(self, url):
      self.locationEdit.setText( url.toString() )
    def __init__(self):
      QWidget.__init__(self)
      self.webView = QWebView()
      self.setLayout( QVBoxLayout() )  
      self.locationEdit = QLineEdit( 'http://www.google.com' )
      self.locationEdit.setSizePolicy( QSizePolicy.Expanding, self.locationEdit.sizePolicy().verticalPolicy() )
      QObject.connect( self.locationEdit, SIGNAL('returnPressed()'),  self.changeLocation )
      QObject.connect( self.webView,   SIGNAL('urlChanged(QUrl)'),     self.urlChanged )
      self.layout().addWidget( self.locationEdit )
      bar = QToolBar()
      bar.addAction( self.webView.pageAction(QWebPage.Back))
      bar.addAction( self.webView.pageAction(QWebPage.Forward))
      bar.addAction( self.webView.pageAction(QWebPage.Stop))
      bar.addAction( self.webView.pageAction(QWebPage.Reload))
      bar.addSeparator()
      self.layout().addWidget( bar )
      self.layout().addWidget( self.webView )
      url = 'http://www.thefoundry.co.uk/' 
      self.webView.load( QUrl( url ) )
      self.locationEdit.setText( url ) 
      self.setSizePolicy( QSizePolicy( QSizePolicy.Expanding,  QSizePolicy.Expanding))
  #
  ## make this work in a .py file and in 'copy and paste' into the script editor
  moduleName = __name__
  if moduleName == '__main__':
    moduleName = ''
  else:
    moduleName = moduleName + '.'
  panels.registerWidgetAsPanel( moduleName + 'WebBrowserWidget', 'Web Browser','uk.co.thefoundry.WebBrowserWidget')
except ImportError:
  pass

# =======================================================================
# TOOLBAR
# =======================================================================

# Add a menu to the left-hand-side column of icons
#
# nuke.toolbar("Nodes").addCommand("sjm/test", lambda:nuke.message('test'), "Ctrl+Meta+T")
# nuke.toolbar("Nodes").addCommand("sjm/m-over", lambda:nuke.createNode('Merge2','operation over'))
# nuke.toolbar("Nodes").addCommand("sjm/m-under", lambda:nuke.createNode('Merge2','operation under'))
# nuke.toolbar("Nodes").addCommand("sjm/m-screen", lambda:nuke.createNode('Merge2','operation screen'))
# nuke.toolbar("Nodes").addCommand("sjm/m-mask", lambda:nuke.createNode('Merge2','operation mask'))
# nuke.toolbar("Nodes").addCommand("sjm/m-stencil", lambda:nuke.createNode('Merge2','operation stencil'))
# nuke.toolbar("Nodes").addCommand("sjm/m-minus", lambda:nuke.createNode('Merge2','operation minus'))
# nuke.toolbar("Nodes").addCommand("sjm/m-from", lambda:nuke.createNode('Merge2','operation from'))


# =======================================================================
# MENUBAR
# =======================================================================

# Add a personal menu to the top menu bar
#
m_keybindings = nuke.menu('Nuke').addMenu("Smolin")
m_keybindings.addCommand('mergeStencil', 'nuke.createNode("Merge2","operation stencil")', 'Ctrl+Meta+S')
m_keybindings.addCommand('colorLookup aka curve lookup','nuke.createNode("ColorLookup")', 'Ctrl+Meta+L')
m_keybindings.addCommand('sjmToggleDisableExpression','sjmToggleDisableExpression()', 'Ctrl+Meta+G')
m_keybindings.addCommand('sjmOpenAllInViewer', 'sjmOpenAllInViewer()', 'Ctrl+Meta+V')
m_keybindings.addCommand('sjmAutoBackdrop', 'sjmAutoBackdrop()', 'Ctrl+Meta+B')
m_keybindings.addCommand('sjmMergeOpIncr', 'sjmMergeOpIncr()', 'Ctrl+Meta+Up')
m_keybindings.addCommand('sjmMergeOpDecr', 'sjmMergeOpDecr()', 'Ctrl+Meta+Down')
m_keybindings.addCommand('SliceTool', 'nuke.createNode("SliceTool")')
m_keybindings.addCommand('RefractTo', 'nuke.createNode("refract_to_the_FUTURE")')
#
try:
  DeadlineNukeClient
  m_keybindings.addCommand('sjmDeadliner','DeadlineNukeClient.main()','Ctrl+Meta+D')
except:
  pass

# =======================================================================
# NODE PARAMETER DEFAULTS
# =======================================================================

# set default values for various nodes (except Labels collected below)
#
nuke.knobDefault('BackdropNode.note_font_size','120')
nuke.knobDefault('DirBlurWrapper.BlurLayer','rgba')
nuke.knobDefault('Roto.cliptype','none')
nuke.knobDefault('Roto.premultiply','rgba')
nuke.knobDefault("Blur.size", "1")
nuke.knobDefault("RotoPaint.cliptype", "none")

nuke.knobDefault("Blur.label", "s:[value size]")
nuke.knobDefault("FilterErode.label", "s:[value size]")
nuke.knobDefault("Multiply.label", "v:[value value]")
nuke.knobDefault("Switch.label", "w:[value which]")
nuke.knobDefault("TimeOffset.label", "o:[value time_offset]")
nuke.knobDefault("Tracker.label", "t:[value transform]")
