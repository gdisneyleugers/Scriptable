__author__ = 'gregorydisney'
import gtk
import os
import pango
import gtksourceview2

class MyGUI:

  def __init__( self, title):
    self.window = gtk.Window()
    self.title = title
    self.window.set_title( title)
    self.window.set_size_request(405, 450)
    self.window.set_resize_mode(True)
    a = self.window.set_icon_from_file("icon.png")
    self.window.connect( "destroy", self.destroy)
    self.create_interior()
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
    sw.add(self.textview)
    self.notebook.add(sw)
    sw.show()
    self.mainbox.pack_start(self.notebook)
    self.notebook.show()
    textbuffer = self.textview.get_buffer()
    gtksourceview2.Buffer()
    gtksourceview2.View(textbuffer)
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

    # button
    a = self.notebook.current_page()
    b = gtk.Button("Run Script")
    c = gtk.Button("Save Script")
    if a == -1:
        d = gtk.Button("Close tab")
        self.mainbox.pack_start(b, expand=False)
        self.mainbox.pack_start(c, expand=False)
        self.mainbox.pack_start(d, expand=False)
        b.connect( "clicked", self.check_text)
        c.connect( "clicked", self.clear)
        d.connect( "clicked", self.rm)
        c.show()
        b.show()
        d.show()
    if a == 0:
        d = gtk.Button("Close tab")
        self.mainbox.pack_start(b, expand=False)
        self.mainbox.pack_start(c, expand=False)
        self.mainbox.pack_start(d, expand=False)
        b.connect( "clicked", self.check_text)
        c.connect( "clicked", self.clear)
        d.connect( "clicked", self.rm)
        d.show()
    # show the box
    self.mainbox.show()

  def main( self):
    gtk.main()

  def destroy( self, w):
    gtk.main_quit()
  def rm(self, w):
    a = self.notebook.current_page()
    self.notebook.remove_page(a)
    if a == 0:
        self.window.destroy()
        m = MyGUI("Scriptable")
        m.main()
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
    textbuffer = self.textview.get_buffer()
    tt = t.get_buffer()
    self.notebook.append_page(t, None)
    t.show()
    self.mainbox.pack_start(self.notebook)
    self.notebook.show()
    self.editable_toggled("")
    startiter, enditer = textbuffer.get_bounds()
    text = textbuffer.get_text( startiter, enditer)
    STDOUT = os.popen(text).read()
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
  except pango.PangoWarning:
      print ""
