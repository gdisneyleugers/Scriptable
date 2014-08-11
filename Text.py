__author__ = 'gregorydisney'
import gtk
import os
import pango
import gtksourceview2
import vte
import gobject

class MyGUI:

  def __init__( self, title):
    self.window = gtk.Window()
    self.title = title
    self.window.set_title( title)
    self.window.set_size_request(600, 450)
    self.window.set_resize_mode(True)
    a = self.window.set_icon_from_file("icon.png")
    self.window.set_icon(a)
    self.window.connect( "destroy", self.destroy)
    self.create_interior()
    self.buttons()
    self.window.show_all()

  def create_interior( self):
    self.mainbox = gtk.VBox()
    self.window.add(self.mainbox)
    # the textview
    self.notebook = gtk.Notebook()
    self.notebook.set_scrollable(True)
    self.notebook.set_current_page(1)
    self.textview = gtk.TextView()
    sw = gtk.ScrolledWindow()
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.notebook.add(sw)
    self.mainbox.pack_start(self.notebook)
    self.notebook.show()
    textbuffer = self.textview.get_buffer()
    textpack = gtksourceview2.View(textbuffer)
    sw.add(textpack)
    sw.show()
    self.textview.set_cursor_visible(True)
    self.textview.drag_highlight()
    self.textview.show()
    textbuffer.connect( "changed", self.text_changed) #@+
    # label for counts
    self.count_label = gtk.Label()
    self.count_label.show()
    self.mainbox.pack_start( self.count_label, expand=False)
    self.count_label.set_alignment(0, 0)
    # we set text here because we want the signal to be triggered
    # and need the count_label for display of result
    clear = textbuffer.set_text("#########################Scriptable##########################")
  def buttons(self):
    # button
    a = self.notebook.current_page()
    table = gtk.Table( 1, 1, False)
    e = gtk.Button(label="Open Terminal")
    b = gtk.Button("Run Script")
    c = gtk.Button("Save Script")
    d = gtk.Button("Open Script")
    table.attach(e, 1, 2, 1, 2)
    table.attach(b, 2, 3, 1, 2)
    table.attach(c, 3, 4, 1, 2)
    table.attach(d, 4, 5, 1, 2)
    self.mainbox.pack_start(table, expand=False)
    table.show_all()
    b.connect( "clicked", self.check_text)
    c.connect( "clicked", self.clear)
    e.connect( "clicked", self.terminal)
    d.connect( "clicked", self.open)
    e.show()
    c.show()
    b.show()
    # show the box
    self.mainbox.show()

  def main( self):
    gtk.main()
  def open( self, w):
    dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    response = dialog.run()
    filter = gtk.FileFilter()

    filter.add_pattern("scriptable*")
    dialog.add_filter(filter)
    if response == gtk.RESPONSE_OK:
    	a = dialog.get_filename()
	b = file(a, "r")
	c = b.read()
	textbuffer = self.textview.get_buffer()
    	textbuffer.set_text(c)
    elif response == gtk.RESPONSE_CANCEL:
    	print 'Closed, no files selected'
    dialog.destroy()
  def destroy( self, w):
    gtk.main_quit()
  def terminal(self, w):
      import vte
      self.terminal = vte.Terminal()
      self.terminal.connect ("child-exited", lambda term: gtk.main_quit())
      self.terminal.fork_command()      
      sw = gtk.ScrolledWindow()
      sw.add(self.terminal)
      sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      closebtn = gtk.Button("x")
      label = gtk.Label()
      label.set_label("Terminal  ")
      table = gtk.Table( 1, 1, False)
      table.attach(label, 1, 2, 1, 2)
      table.attach(closebtn, 2, 3, 1, 2)
      table.show_all()
      closebtn.connect( "clicked", self.rm)
      e = os.popen("tty").read()
      self.count_label.set_markup("Connected: {0}".format(e))
      self.notebook.append_page(sw, table)
      sw.show_all()
      a = self.notebook.current_page()
      b = a + 1
      self.notebook.set_current_page(b) 
  def rm(self, w):
    a = self.notebook.current_page()
    self.notebook.remove_page(a)
    if a == 0:
	md = gtk.MessageDialog(None,
    	gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING,
    	gtk.BUTTONS_CLOSE, "Warning about to close Scriptable Engine")
    	md.run()
	if gtk.BUTTONS_CLOSE:
        	gtk.MessageDialog.destroy(md)
		quit()
    
  def clear( self, w ):
    textbuffer = self.textview.get_buffer()
    startiter, enditer = textbuffer.get_bounds()
    text = textbuffer.get_text( startiter, enditer)
    import uuid
    o = "scriptable-{0}".format(uuid.uuid4())
    a = file(o, "w")
    a.write(text)
    a.close()
    os.system("chmod +x {0}".format(o))
    b = os.popen("gist {0}".format(o)).read()
    parent = None
    md = gtk.MessageDialog(parent,
    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
    gtk.BUTTONS_CLOSE, "Scripted saved @ {0}".format(b) + "Local save @ {0}".format(o))
    md.run()
    if gtk.BUTTONS_CLOSE:
        gtk.MessageDialog.destroy(md)
    t = gtk.Notebook()
  def check_text( self, w, data=None):
    t = gtk.TextView()
    sw = gtk.ScrolledWindow()
    sw.add(t)
    textbuffer = self.textview.get_buffer()
    tt = t.get_buffer()
    label = gtk.Label()
    a = self.notebook.current_page()
    b = a + 1
    self.notebook.set_current_page(b)
    if a is 0:
	b = a + 1
	self.notebook.set_current_page(b) 
    self.notebook.set_current_page(b)
    label.set_label("Output {0} ".format(a))
    closebtn = gtk.Button("x")
    closebtn.connect( "clicked", self.rm)
    closebtn.show()
    table = gtk.Table( 1, 1, False)
    table.attach(label, 1, 2, 1, 2)
    table.attach(closebtn, 2, 3, 1, 2)
    table.show_all()
    self.notebook.append_page(sw, table)
    sw.show_all()
    t.show()
    #self.mainbox.pack_start(self.notebook)
    self.notebook.show()
    self.notebook.set_current_page(b) 
    self.editable_toggled("")
    startiter, enditer = textbuffer.get_bounds()
    text = textbuffer.get_text( startiter, enditer)
    STDOUT = os.popen(text).read()
    if STDOUT in "sh:":
	self.count_label.set_markup("Failed")
    if STDOUT not in "sh:":
	self.count_label.set_markup("Success")
    import time
    printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Script Completed @ {0}############".format(time.time())
    textbuffer.set_text(text)
    tt.set_text(printout)
  def editable_toggled( self, w, data=None):
   a = self.notebook.current_page()

  def count_label(self):
      print self
  def text_changed( self, w, data=None):
    chars = w.get_char_count() #@+
    lines = w.get_line_count() #@+
    self.count_label.set_markup( "Chars: <b>%d</b>, Lines: <b>%d</b>" % (chars, lines))
    a = self.notebook.current_page()


if __name__ == "__main__":
  try:
    m = MyGUI("Scriptable")
    m.main()
  except Exception:
      print ""
  except gtk.GtkWarning:
      print ""
  except pango.PangoWarning:
      print ""
  except AttributeError:
      print ""
