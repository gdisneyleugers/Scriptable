__author__ = 'gregorydisney'
import gtk
import os
import pango
import gtksourceview2
import gtk_osxapplication
import time
import uuid


class MyGUI:
    def __init__(self, title):
        self.window = gtk.Window()
        self.title = title
        self.window.set_title(title)
        self.window.set_size_request(410, 450)
        self.window.set_resize_mode(True)
        a = self.window.set_icon_from_file("icon.png")
        self.window.set_icon(a)
        self.window.connect("destroy", self.destroy)
        self.create_interior()
        self.buttons()
        self.window.show_all()

    def create_interior(self):
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
        textbuffer.connect("changed", self.text_changed) #@+
        # label for counts
        self.count_label = gtk.Label()
        self.count_label.show()
        self.mainbox.pack_start(self.count_label, expand=False)
        self.count_label.set_alignment(0, 0)
        # we set text here because we want the signal to be triggered
        # and need the count_label for display of result
        clear = textbuffer.set_text("#########################Scriptable##########################")

    def buttons(self):
        # button
        a = self.notebook.current_page()
        table = gtk.Table(1, 1, False)
        self.combobox = gtk.combo_box_new_text()
        combobox = self.combobox
        shell = combobox.insert_text(0, "Shell")
        tree = combobox.get_model()
        active = combobox.get_active_text()
        combobox.connect('changed', self.exec_engine)
        python = combobox.insert_text(1, "Python")
        perl = combobox.insert_text(2, "Perl")
        ruby = combobox.insert_text(3, "Ruby")
        clang = combobox.insert_text(4, "C")
        php = combobox.insert_text(5, "Php")
        lua = combobox.insert_text(6, "Lua")
        combobox.set_active(0)
        e = gtk.Button("Terminal")
        b = gtk.Button("Run Script")
        c = gtk.Button("Save Script")
        d = gtk.Button("Open Script")
        table.attach(e, 1, 2, 1, 2)
        table.attach(b, 2, 3, 1, 2)
        table.attach(c, 3, 4, 1, 2)
        table.attach(d, 4, 5, 1, 2)
        table.attach(combobox, 5, 6, 1, 2)
        self.mainbox.pack_start(table, expand=False)
        table.show_all()
        b.connect("clicked", self.check_text)
        c.connect("clicked", self.clear)
        e.connect("clicked", self.terminal)
        d.connect("clicked", self.open)
        e.show()
        c.show()
        b.show()
        # show the box
        self.mainbox.show()

    def main(self):
        gtk.main()

    def open(self, w):
        dialog = gtk.FileChooserDialog("Open Script",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            a = dialog.get_filename()
            b = file(a, "r")
            c = b.read()
            if ".sh" in a:
                self.combobox.set_active(0)
            if ".py" in a:
                self.combobox.set_active(1)
            if ".pl" in a:
                self.combobox.set_active(2)
            if ".rb" in a:
                self.combobox.set_active(3)
            if ".c" in a:
                self.combobox.set_active(4)
            if ".php" in a:
                self.combobox.set_active(5)
            if ".lua" in a:
                self.combobox.set_active(6)
            textbuffer = self.textview.get_buffer()
            textbuffer.set_text(c)
        elif response == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        dialog.destroy()

    def destroy(self, w):
        gtk.main_quit()

    def terminal(self, w):
        os.system("xterm")

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

    def clear(self, w):
        textbuffer = self.textview.get_buffer()
        startiter, enditer = textbuffer.get_bounds()
        text = textbuffer.get_text(startiter, enditer)
        import uuid

        active = self.combobox.get_active_text()
        if active == "Shell":
            o = "scriptable-{0}.sh".format(uuid.uuid4())
            a = file(o, "w")
            a.write(text)
            a.close()
            os.system("chmod +x {0}".format(o))
            b = os.popen("gist {0}".format(o)).read()
            parent = None
            md = gtk.MessageDialog(parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE,
                                   "Shell Script saved @ {0}".format(b) + "Local save @ {0}".format(o))
            md.run()
            if gtk.BUTTONS_CLOSE:
                gtk.MessageDialog.destroy(md)
        if active == "Python":
            o = "scriptable-{0}.py".format(uuid.uuid4())
            a = file(o, "w")
            a.write(text)
            a.close()
            os.system("chmod +x {0}".format(o))
            b = os.popen("gist {0}".format(o)).read()
            parent = None
            md = gtk.MessageDialog(parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE,
                                   "Python Script saved @ {0}".format(b) + "Local save @ {0}".format(o))
            md.run()
            if gtk.BUTTONS_CLOSE:
                gtk.MessageDialog.destroy(md)
        if active == "Perl":
            o = "scriptable-{0}.pl".format(uuid.uuid4())
            a = file(o, "w")
            a.write(text)
            a.close()
            os.system("chmod +x {0}".format(o))
            b = os.popen("gist {0}".format(o)).read()
            parent = None
            md = gtk.MessageDialog(parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE,
                                   "Perl Script saved @ {0}".format(b) + "Local save @ {0}".format(o))
            md.run()
            if gtk.BUTTONS_CLOSE:
                gtk.MessageDialog.destroy(md)
        if active == "Ruby":
            o = "scriptable-{0}.rb".format(uuid.uuid4())
            a = file(o, "w")
            a.write(text)
            a.close()
            os.system("chmod +x {0}".format(o))
            b = os.popen("gist {0}".format(o)).read()
            parent = None
            md = gtk.MessageDialog(parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE,
                                   "Ruby Script saved @ {0}".format(b) + "Local save @ {0}".format(o))
            md.run()
            if gtk.BUTTONS_CLOSE:
                gtk.MessageDialog.destroy(md)
        if active == "C":
            o = "scriptable-{0}.c".format(uuid.uuid4())
            a = file(o, "w")
            a.write(text)
            a.close()
            os.system("chmod +x {0}".format(o))
            b = os.popen("gist {0}".format(o)).read()
            parent = None
            md = gtk.MessageDialog(parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE, "C Script saved @ {0}".format(b) + "Local save @ {0}".format(o))
            md.run()
            if gtk.BUTTONS_CLOSE:
                gtk.MessageDialog.destroy(md)
        if active == "Php":
            o = "scriptable-{0}.php".format(uuid.uuid4())
            a = file(o, "w")
            a.write(text)
            a.close()
            os.system("chmod +x {0}".format(o))
            b = os.popen("gist {0}".format(o)).read()
            parent = None
            md = gtk.MessageDialog(parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE, "PHP Script saved @ {0}".format(b) + "Local save @ {0}".format(o))
            md.run()
            if gtk.BUTTONS_CLOSE:
                gtk.MessageDialog.destroy(md)
        if active == "Lua":
            o = "scriptable-{0}.lua".format(uuid.uuid4())
            a = file(o, "w")
            a.write(text)
            a.close()
            os.system("chmod +x {0}".format(o))
            b = os.popen("gist {0}".format(o)).read()
            parent = None
            md = gtk.MessageDialog(parent,
                                   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                                   gtk.BUTTONS_CLOSE,
                                   "Ruby Script saved @ {0}".format(b) + "Local save @ {0}".format(o))
            md.run()
            if gtk.BUTTONS_CLOSE:
                gtk.MessageDialog.destroy(md)
        t = gtk.Notebook()

    def exec_engine(self, w):
        active = self.combobox.get_active_text()
        textbuffer = self.textview.get_buffer()
        if active == "Shell":
            textbuffer.set_text("#########################Scriptable##########################\n#!/bin/bash")
        if active == "Python":
            textbuffer.set_text("#########################Scriptable##########################\n#!/bin/env python")
        if active == "Perl":
            textbuffer.set_text("#########################Scriptable##########################\n#!/bin/perl")
        if active == "Ruby":
            textbuffer.set_text("#########################Scriptable##########################\n#!/bin/ruby")
        if active == "C":
            textbuffer.set_text(
                "/*#########################Scriptable##########################*/\nint main(void) { \n \n \n \n }")
        if active == "Php":
            textbuffer.set_text(
                "<?php\n/*#########################Scriptable##########################*/\n \n \n \n \n ?> ")
        if active == "Lua":
            textbuffer.set_text("--[[#########################Scriptable##########################]]--\n")

    def check_text(self, w, data=None):
        active = self.combobox.get_active_text()
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
        closebtn.connect("clicked", self.rm)
        closebtn.show()
        table = gtk.Table(1, 1, False)
        table.attach(label, 1, 2, 1, 2)
        table.attach(closebtn, 2, 3, 1, 2)
        table.show_all()
        self.notebook.append_page(sw, table)
        sw.show_all()
        t.show()
        #self.mainbox.pack_start(self.notebook)
        self.notebook.show()
        self.notebook.set_current_page(b)
        active = self.combobox.get_active_text()
        self.editable_toggled("")
        if active == "Shell":
            startiter, enditer = textbuffer.get_bounds()
            text = textbuffer.get_text(startiter, enditer)
            STDOUT = os.popen(text).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Shell Script Completed @ {0}############".format(
                time.time())
            textbuffer.set_text(text)
            tt.set_text(printout)
        if active == "Python":
            startiter, enditer = textbuffer.get_bounds()
            pyscript = "scriptable-{0}.py".format(uuid.uuid4())
            text = textbuffer.get_text(startiter, enditer)
            fh = file(pyscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("python {0}".format(pyscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Python Shell Script Completed @ {0}############".format(
                time.time())
            textbuffer.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(pyscript))
        if active == "Perl":
            startiter, enditer = textbuffer.get_bounds()
            plscript = "scriptable-{0}.pl".format(uuid.uuid4())
            text = textbuffer.get_text(startiter, enditer)
            fh = file(plscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("perl {0}".format(plscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Perl Script Completed @ {0}############".format(
                time.time())
            textbuffer.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(plscript))
        if active == "Ruby":
            startiter, enditer = textbuffer.get_bounds()
            rbscript = "scriptable-{0}.rb".format(uuid.uuid4())
            text = textbuffer.get_text(startiter, enditer)
            fh = file(rbscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("ruby {0}".format(rbscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Ruby Script Completed @ {0}############".format(
                time.time())
            textbuffer.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(rbscript))
        if active == "C":
            startiter, enditer = textbuffer.get_bounds()
            cscript = "scriptable-{0}.c".format(uuid.uuid4())
            text = textbuffer.get_text(startiter, enditer)
            fh = file(cscript, "w")
            fh.write(text)
            fh.close()
            compile = os.popen("gcc {0} -o {0}".format(cscript)).read()
            STDOUT = os.popen("./{0}".format(cscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable C Script Completed @ {0}############".format(
                time.time())
            textbuffer.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(cscript))
        if active == "Php":
            startiter, enditer = textbuffer.get_bounds()
            phpscript = "scriptable-{0}.php".format(uuid.uuid4())
            text = textbuffer.get_text(startiter, enditer)
            fh = file(phpscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("php {0}".format(phpscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable PHP Script Completed @ {0}###########".format(
                time.time())
            textbuffer.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(phpscript))
        if active == "Lua":
            startiter, enditer = textbuffer.get_bounds()
            luascript = "scriptable-{0}.lua".format(uuid.uuid4())
            text = textbuffer.get_text(startiter, enditer)
            fh = file(luascript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("lua {0}".format(luascript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Lua Script Completed @ {0}###########".format(
                time.time())
            textbuffer.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(luascript))
        if STDOUT in "sh:":
            self.count_label.set_markup("<b>Failed @ {0}</b>".format(time.asctime()))
        if STDOUT not in "sh:":
            self.count_label.set_markup("<b>Pass @ {0}</b>".format(time.asctime()))

    def editable_toggled(self, w, data=None):
        a = self.notebook.current_page()

    def count_label(self):
        print self

    def text_changed(self, w, data=None):
        chars = w.get_char_count() #@+
        lines = w.get_line_count() #@+
        self.count_label.set_markup("Chars: <b>%d</b>, Lines: <b>%d</b>" % (chars, lines))
        a = self.notebook.current_page()


if __name__ == "__main__":
    try:
        m = MyGUI("Scriptable")
        osx_app = gtk_osxapplication.OSXApplication()
        osx_app.set_use_quartz_accelerators(True)
        osx_app.sync_menubar()
        osx_app.set_dock_icon_pixbuf(gtk.gdk.pixbuf_new_from_file("icon.png"))
        osx_app.chain(m.main())
        m.main()
    except KeyboardInterrupt:
        print ""
    except AttributeError:
        print ""
