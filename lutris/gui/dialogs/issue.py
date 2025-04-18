"""GUI dialog for reporting issues"""

import json
import os
from gettext import gettext as _
from gi.repository import Gtk

from lutris.gui.dialogs import NoticeDialog
from lutris.gui.widgets.window import BaseApplicationWindow
from lutris.util.linux import gather_system_info


class IssueReportWindow(BaseApplicationWindow):
    """Window for collecting and sending issue reports"""

    def __init__(self, application):
        super().__init__(application)

        self.title_label = Gtk.Label(visible=True)
        self.vbox.add(self.title_label)

        title_label = Gtk.Label()
        title_label.set_markup(_("<b>Submit an issue</b>"))
        self.vbox.add(title_label)
        self.vbox.add(Gtk.HSeparator())

        issue_entry_label = Gtk.Label(
            _(
                "Describe the problem you're having in the text box below. "
                "This information will be sent the Lutris team along with your system information. "
                "You can also save this information locally if you are offline."
            )
        )
        issue_entry_label.set_max_width_chars(80)
        issue_entry_label.set_property("wrap", True)
        self.vbox.add(issue_entry_label)

        self.textview = Gtk.TextView()
        self.textview.set_pixels_above_lines(12)
        self.textview.set_pixels_below_lines(12)
        self.textview.set_left_margin(12)
        self.textview.set_right_margin(12)
        self.vbox.pack_start(self.textview, True, True, 0)

        self.action_buttons = Gtk.Box(spacing=6)
        action_buttons_alignment = Gtk.Alignment.new(1, 0, 0, 0)
        action_buttons_alignment.add(self.action_buttons)
        self.vbox.pack_start(action_buttons_alignment, False, True, 0)

        cancel_button = self.get_action_button(_("C_ancel"), handler=lambda *x: self.destroy())
        self.action_buttons.add(cancel_button)

        save_button = self.get_action_button(_("_Save"), handler=self.on_save)
        self.action_buttons.add(save_button)

        self.show_all()

    def get_issue_info(self):
        buffer = self.textview.get_buffer()
        return {
            "comment": buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True),
            "system": gather_system_info(),
        }

    def on_save(self, _button):
        """Signal handler for the save button"""

        save_dialog = Gtk.FileChooserNative.new(
            _("Select a location to save the issue"),
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            _("_OK"),
            _("_Cancel"),
        )
        save_dialog.connect("response", self.on_folder_selected, save_dialog)
        save_dialog.show()

    def on_folder_selected(self, dialog, response, _dialog):
        if response != Gtk.ResponseType.ACCEPT:
            return
        target_path = dialog.get_filename()
        if not target_path:
            return
        issue_path = os.path.join(target_path, "lutris-issue-report.json")
        issue_info = self.get_issue_info()
        with open(issue_path, "w", encoding="utf-8") as issue_file:
            json.dump(issue_info, issue_file, indent=2)
        dialog.destroy()
        NoticeDialog(_("Issue saved in %s") % issue_path)
        self.destroy()
