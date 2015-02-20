# nicked from http://docs.thefoundry.co.uk/nuke/63/pythondevguide/basics.html#creating-modal-dialogs

import nuke
import nukescripts

# The following defines a new class called ModalFramePanel.
class ModalFramePanel( nukescripts.PythonPanel ):

  # The following function creates a dialog titled 'Go to Frame' with the optional ID uk.co.thefoundry.FramePanel. It aso adds an integer control called 'frame' to the dialog. This control is set to the value nuke.frame() which is the current frame on the timeline.
  def __init__( self ):
    nukescripts.PythonPanel.__init__( self, "Go to Frame", "uk.co.thefoundry.FramePanel" )
    self.frame = nuke.Int_Knob( "frame", "Frame:" )
    self.addKnob( self.frame )
    self.frame.setValue( nuke.frame() )

  # The next function shows the dialog as a modal dialog. Doing this automatically adds the 'OK' and 'Cancel' buttons to the dialog.
  def showModalDialog( self ):
    result = nukescripts.PythonPanel.showModalDialog( self )
    if result:
      nuke.frame( self.frame.value() )

ModalFramePanel().showModalDialog()

# If you want to add the dialog to a menu item, you can also do the following:
# menubar = nuke.menu("Nuke")
# menubar.addCommand("&File/Show My Panel", testModalPanel)

