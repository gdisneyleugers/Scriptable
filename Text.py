from TextBuff.TextBuff import buffer_ui_description, buffer_actions, create_view_window, update_cursor_position, button_press_cb, \
    move_cursor_cb
import gtk
import os
import pango
import gtksourceview2
import vte
import uuid

class MyGUI:
    def __init__(self, title):
        self.count_label = gtk.Label()
        self.notebook = gtk.Notebook()
        self.window = gtk.Window()
        self.title = title
        self.window.set_title(title)
        self.window.set_size_request(610, 550)
        self.window.set_resize_mode(True)
        a = self.window.set_icon_from_file("icon.png")
        self.window.set_icon(a)
        self.window.connect("destroy", self.destroy)
        self.create_interior()
        self.buttons()
        self.window.show_all()

    def create_interior(self):
        """

        :type self: object
        """
        self.mainbox = gtk.VBox()
        self.window.add(self.mainbox)
        # the textview
        self.label = gtk.Label()
        self.label.show()
        self.notebook.set_scrollable(True)
        #self.notebook.set_current_page(1)
        self.label.set_label("Scriptable")
        textview = gtksourceview2.View()
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        closebtn = gtk.Button("x")
        closebtn.connect("clicked", self.rm)
        closebtn.show()
        table = gtk.Table(1, 1, False)
        table.attach(self.label, 1, 2, 1, 2)
        table.attach(closebtn, 2, 3, 1, 2)
        table.show_all()
        sw.show_all()
        self.mainbox.pack_start(self.notebook)
        self.notebook.append_page(sw, table)
        self.notebook.show()
        self.textbuffer = gtksourceview2.Buffer()
        lm = gtksourceview2.LanguageManager()
        manager = self.textbuffer.get_data('languages-manager')
        self.textbuffer.set_data('languages-manager', lm)
        self.textbuffer.set_highlight_syntax(True)
        self.textpack = gtksourceview2.View(self.textbuffer)
        self.textbuffer.connect('mark_set', move_cursor_cb, self.textpack)
        self.textbuffer.connect('changed', update_cursor_position, self.textpack)
        self.textpack.connect('button-press-event', button_press_cb)
        sw.add(self.textpack)
        sw.show()
        textview.show()
        # label for counts
        self.count_label = gtk.Label()
        self.count_label.show()
        self.mainbox.pack_start(self.count_label, expand=False)
        self.count_label.set_alignment(0, 0)
        # we set text here because we want the signal to be triggered
        # and need the count_label for display of result
        action_group = gtk.ActionGroup('ViewActions')
        clear = self.textbuffer.set_text("#########################Scriptable##########################")

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
        window = create_view_window(buffer)
        ui_manager = window.get_data('ui_manager')

        # buffer action group
        action_group = gtk.ActionGroup('BufferActions')
        action_group.add_actions(buffer_actions, buffer)
        ui_manager.insert_action_group(action_group, 1)
        # merge buffer ui
        chars = self.textbuffer.get_char_count()  # @+
        lines = self.textbuffer.get_line_count()  # @+
        self.count_label.set_markup("Chars: <b>%d</b>, Lines: <b>%d</b>" % (chars, lines))
        ui_manager.add_ui_from_string(buffer_ui_description)
        # preselect menu checkitems
        groups = ui_manager.get_action_groups()
        # retrieve the view action group at position 0 in the list
        action_group = groups[0]
        action = action_group.get_action('ShowNumbers')
        action.set_active(True)
        action = action_group.get_action('ShowMarkers')
        action.set_active(True)
        action = action_group.get_action('ShowMargin')
        action.set_active(True)
        action = action_group.get_action('AutoIndent')
        action.set_active(True)
        action = action_group.get_action('InsertSpaces')
        action.set_active(True)
        action = action_group.get_action('TabsWidth8')
        action.set_active(True)
        ui_manager.show()

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
            filename = a
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
            self.textbuffer.set_text(c)
            self.textbuffer.set_data('filename', filename)
            self.textbuffer.place_cursor(self.textbuffer.get_start_iter())
        elif response == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        dialog.destroy()

    def destroy(self, w):
        gtk.main_quit()

    def terminal(self, w):
        self.terminal = vte.Terminal()
        self.terminal.connect("child-exited", lambda term: gtk.main_quit())
        self.terminal.fork_command()
        sw = gtk.ScrolledWindow()
        sw.add(self.terminal)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        closebtn = gtk.Button("x")
        label = gtk.Label()
        a = self.notebook.current_page()
        b = a + 1
        label.set_label("Terminal {0}".format(b))
        table = gtk.Table(1, 1, False)
        table.attach(label, 1, 2, 1, 2)
        table.attach(closebtn, 2, 3, 1, 2)
        table.show_all()
        closebtn.connect("clicked", self.rm)
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

    def clear(self, w):
        textbuffer = self.textbuffer
        startiter, enditer = textbuffer.get_bounds()
        text = textbuffer.get_text(startiter, enditer)

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
        if active == "Shell":
            lang = gtksourceview2.LanguageManager()
            lt = lang.get_language('sh')
            self.textbuffer.set_language(lt)
            self.textbuffer.set_highlight_matching_brackets(True)
            self.textbuffer.set_text("#########################Scriptable##########################\n#!/bin/bash")
        if active == "Python":
            lang = gtksourceview2.LanguageManager()
            lt = lang.get_language('python')
            self.textbuffer.set_language(lt)
            self.textbuffer.set_highlight_matching_brackets(True)
            self.textbuffer.set_text("#########################Scriptable##########################\n#!/bin/env python")
        if active == "Perl":
            lang = gtksourceview2.LanguageManager()
            lt = lang.get_language('perl')
            self.textbuffer.set_language(lt)
            self.textbuffer.set_highlight_matching_brackets(True)
            self.textbuffer.set_text("#########################Scriptable##########################\n#!/bin/perl")
        if active == "Ruby":
            lang = gtksourceview2.LanguageManager()
            lt = lang.get_language('ruby')
            self.textbuffer.set_language(lt)
            self.textbuffer.set_highlight_matching_brackets(True)
            self.textbuffer.set_text("#########################Scriptable##########################\n#!/bin/ruby")
        if active == "C":
            lang = gtksourceview2.LanguageManager()
            lt = lang.get_language('c')
            self.textbuffer.set_language(lt)
            self.textbuffer.set_highlight_matching_brackets(True)
            self.textbuffer.set_text(
                "/*#########################Scriptable##########################*/\nint main(void) { \n \n \n \n }")
        if active == "Php":
            lang = gtksourceview2.LanguageManager()
            lt = lang.get_language('php')
            self.textbuffer.set_language(lt)
            self.textbuffer.set_highlight_matching_brackets(True)
            self.textbuffer.set_text(
                "<?php\n/*#########################Scriptable##########################*/\n \n \n \n \n ?> ")
        if active == "Lua":
            lang = gtksourceview2.LanguageManager()
            lt = lang.get_language('lua')
            self.textbuffer.set_language(lt)
            self.textbuffer.set_highlight_matching_brackets(True)
            self.textbuffer.set_text("--[[#########################Scriptable##########################]]--\n")

    def check_text(self, w, data=None):
        i = True
        active = self.combobox.get_active_text()
        t = gtksourceview2.View()
        tt = gtksourceview2.Buffer()
        sw = gtk.ScrolledWindow()
        textpack = gtksourceview2.View(tt)
        sw.add(textpack)
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
        # self.mainbox.pack_start(self.notebook)
        self.notebook.show()
        self.notebook.set_current_page(b)
        active = self.combobox.get_active_text()
        self.editable_toggled("")
        if active == "Shell":

            startiter, enditer = self.textbuffer.get_bounds()
            text = self.textbuffer.get_text(startiter, enditer)
            STDOUT = os.popen(text).read()
            import time
            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Shell Script Completed @ {0}############".format(
                time.time())
            tt.set_text(text)
            tt.set_text(printout)
        if active == "Python":
            startiter, enditer = self.textbuffer.get_bounds()
            pyscript = "scriptable-{0}.py".format(uuid.uuid4())
            text = self.textbuffer.get_text(startiter, enditer)
            fh = file(pyscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("python {0}".format(pyscript)).read()
            import time
            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Python Shell Script Completed @ {0}############".format(
                time.time())
            tt.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(pyscript))
        if active == "Perl":
            startiter, enditer = self.textbuffer.get_bounds()
            plscript = "scriptable-{0}.pl".format(uuid.uuid4())
            text = self.textbuffer.get_text(startiter, enditer)
            fh = file(plscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("perl {0}".format(plscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Perl Script Completed @ {0}############".format(
                time.time())
            tt.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(plscript))
        if active == "Ruby":
            startiter, enditer = self.textbuffer.get_bounds()
            rbscript = "scriptable-{0}.rb".format(uuid.uuid4())
            text = self.textbuffer.get_text(startiter, enditer)
            fh = file(rbscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("ruby {0}".format(rbscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Ruby Script Completed @ {0}############".format(
                time.time())
            tt.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(rbscript))
        if active == "C":
            startiter, enditer = self.textbuffer.get_bounds()
            cscript = "scriptable-{0}.c".format(uuid.uuid4())
            text = self.textbuffer.get_text(startiter, enditer)
            fh = file(cscript, "w")
            fh.write(text)
            fh.close()
            compiled = os.popen("gcc {0} -o {0}".format(cscript)).read()
            print compiled
            STDOUT = os.popen("./{0}".format(cscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable C Script Completed @ {0}############".format(
                time.time())
            tt.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(cscript))
        if active == "Php":
            startiter, enditer = self.textbuffer.get_bounds()
            phpscript = "scriptable-{0}.php".format(uuid.uuid4())
            text = self.textbuffer.get_text(startiter, enditer)
            fh = file(phpscript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("php {0}".format(phpscript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable PHP Script Completed @ {0}###########".format(
                time.time())
            tt.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(phpscript))
        if active == "Lua":
            startiter, enditer = self.textbuffer.get_bounds()
            luascript = "scriptable-{0}.lua".format(uuid.uuid4())
            text = self.textbuffer.get_text(startiter, enditer)
            fh = file(luascript, "w")
            fh.write(text)
            fh.close()
            STDOUT = os.popen("lua {0}".format(luascript)).read()
            import time

            printout = "\n" + "Output:\n" + STDOUT + "############Scriptable Lua Script Completed @ {0}###########".format(
                time.time())
            tt.set_text(text)
            tt.set_text(printout)
            os.system("rm {0}".format(luascript))

        chars = self.textbuffer.get_char_count()  # @+
        lines = self.textbuffer.get_line_count()  # @+
        a = self.count_label.set_markup("Chars: <b>%d</b>, Lines: <b>%d</b>" % (chars, lines))
        self.count_label.show()
    def editable_toggled(self, w, data=None):
        a = self.notebook.current_page()

    def count_label(self):
        chars = self.textbuffer.get_char_count()  # @+
        lines = self.textbuffer.get_line_count()  # @+
        self.count_label.set_markup("Chars: <b>%d</b>, Lines: <b>%d</b>" % (chars, lines))
        self.count_label.show()
        a = self.notebook.current_page()

    def text_changed(self, w, data=None):
        chars = self.textbuffer.get_char_count()  # @+
        lines = self.textbuffer.get_line_count()  # @+
        self.count_label.set_markup("Chars: <b>%d</b>, Lines: <b>%d</b>" % (chars, lines))
        self.count_label.show()
        a = self.notebook.current_page()


if __name__ == "__main__":
    try:
        m = MyGUI("Scriptable")
        m.main()
    except Exception:
        print ""
    except pango.PangoWarning:
        print ""
    except AttributeError:
        print ""
