import nuke
import nukescripts

# The following first defines a new class called FramePanel.
class FramePanel( nukescripts.PythonPanel ):
  # The following is a function that creates the panel. The panel is given the
  # title 'Go to Frame' and the ID uk.co.thefoundry.FramePanel. The ID is used
  # for saving window layouts that contain this panel. An integer control called 'frame'
  # is also added to the panel. Its value is set to nuke.frame(), which is the
  # current frame on the timeline.
  def __init__( self ):
    nukescripts.PythonPanel.__init__( self, "Go to Frame", "uk.co.thefoundry.FramePanel" )
    self.frame = nuke.Int_Knob( "frame", "Frame:" )
    self.addKnob( self.frame )
    self.frame.setValue( nuke.frame() )
  # This function tells NUKE to change the current frame on the timeline if the user changes the value of the 'frame' control.
  def knobChanged( self, knob ):
    if knob == self.frame:
      nuke.frame( self.frame.value() )

# The next function (called testPanel) is called to create the panel when the user selects it from a content menu or restores a layout containing it. The function can either create a new panel or return a singleton if only one such panel is allowed to exist.
def testPanel():
  return FramePanel().addToPane()

def dialogNonModalSample():
  # Next, the testPanel function is added to the content menus where it will appear under Pane > Frame Panel.
  menu = nuke.menu( "Pane" )
  menu.addCommand( "Frame Panel", testPanel )
  # Finally, the panel's unique ID is registered for window layout restoration. The testPanel function is called to create the panel that should go into the pane with the unique ID.
  nukescripts.registerPanel( "uk.co.thefoundry.FramePanel", testPanel )

