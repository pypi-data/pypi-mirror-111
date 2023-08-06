import logging
import os
from typing import Iterable

from grapejuice import background
from grapejuice.gui.yes_no_dialog import yes_no_dialog
from grapejuice.tasks import DisableMimeAssociations, InstallRoblox, SandboxWine, \
    RunRobloxStudio, ExtractFastFlags, OpenLogsDirectory, PerformUpdate
from grapejuice_common import variables, robloxctrl, uninstall, update_info_providers
from grapejuice_common import winectrl
from grapejuice_common.features import settings
from grapejuice_common.features.settings import current_settings
from grapejuice_common.gtk.gtk_stuff import WindowBase, dialog
from grapejuice_common.registry_utils import logged_into_studio
from grapejuice_common.update_info_providers import UpdateInformationProvider
from grapejuice_common.util.errors import NoWineError
from grapejuice_common.util.event import Event

LOG = logging.getLogger(__name__)

on_destroy = Event()

once_task_tracker = dict()
on_background_task_error = Event()
on_background_errors_shown = Event()
background_task_errors = []

update_provider: UpdateInformationProvider = update_info_providers.guess_relevant_provider()


def on_task_removed(task: background.BackgroundTask):
    if task in once_task_tracker.keys():
        once_task_tracker[task] = None


background.tasks.task_removed.add_listener(on_task_removed)


def run_task_once(task_class, on_already_running: callable, *args, **kwargs):
    if task_class in once_task_tracker.values():
        on_already_running()
        return

    def on_error(*args2):
        on_background_task_error(*args2)

    kwargs["on_error_callback"] = on_error

    task = task_class(*args, **kwargs)
    once_task_tracker[task] = task_class

    background.tasks.add(task)


def generic_already_running():
    dialog("This task is already being performed!")


def xdg_open(*args):
    os.spawnlp(os.P_NOWAIT, "xdg-open", "xdg-open", *args)


class MainWindowHandlers:
    _updating = False

    def on_destroy(self, *_):
        from gi.repository import Gtk
        on_destroy()
        Gtk.main_quit()

    def run_winecfg(self, *_):
        winectrl.winecfg()

    def run_regedit(self, *_):
        winectrl.regedit()

    def run_winetricks(self, *_):
        winectrl.wine_tricks()

    def disable_mime_assoc(self, *_):
        run_task_once(DisableMimeAssociations, generic_already_running)

    def sandbox(self, *_):
        run_task_once(SandboxWine, generic_already_running)

    def run_roblox_installer(self, *_):
        def no_wine_dialog() -> None:
            dialog("Grapejuice could not find a working Wine binary, please install Wine using your operating "
                   "system's package manager in order to install and use Roblox.")

        try:
            wine_bin = variables.wine_binary()
            if not os.path.exists(wine_bin):
                no_wine_dialog()
                return

        except NoWineError:
            no_wine_dialog()
            return

        run_task_once(InstallRoblox, generic_already_running)

    def run_roblox_studio(self, *_):
        studio_launcher_location = robloxctrl.locate_studio_launcher()
        if not studio_launcher_location:
            dialog("Grapejuice could not locate Roblox Studio. You might have to install it first by going to the "
                   "maintenance tab and clicking 'Install Roblox'")
            return

        if not logged_into_studio() and yes_no_dialog(
            "Log into Roblox",
            "You are currently not signed into Roblox Studio. "
            "Roblox Studio is known to require an account to use. Would you like to sign in now?"
        ):
            xdg_open(variables.roblox_return_to_studio())

        else:
            run_task_once(RunRobloxStudio, generic_already_running)

    def wine_explorer(self, *_):
        winectrl.explorer()

    def open_drive_c(self, *_):
        xdg_open(variables.wine_drive_c())

    def show_about(self, *_):
        from grapejuice.gui.about_window import AboutWindow
        wnd = AboutWindow()
        wnd.window.run()

        del wnd

    def open_roblox_return_to_studio(self, *_):
        xdg_open(variables.roblox_return_to_studio())

    def open_fast_flag_editor(self, *_):
        def open_editor(b):
            if not b:
                return

            task = ExtractFastFlags()

            def poll():
                if task.finished:
                    from grapejuice.gui.fast_flag_editor import FastFlagEditor
                    wnd = FastFlagEditor()
                    wnd.window.show()

                return not task.finished

            from gi.repository import GObject
            GObject.timeout_add(100, poll)

            background.tasks.add(task)

        if current_settings.get(settings.k_show_fast_flag_warning):
            from grapejuice.gui.fast_flag_warning import FastFlagWarning
            wnd = FastFlagWarning(open_editor)
            wnd.show()

        else:
            open_editor(True)

    def show_wiki(self, *_):
        xdg_open(variables.git_wiki())

    def open_logs_directory(self, *_):
        run_task_once(OpenLogsDirectory, generic_already_running)

    def update_grapejuice(self, *_):
        if self._updating:
            return

        self._updating = True

        dialog("If the Grapejuice upgrade breaks your installation, please redo the Grapejuice installation according "
               "to the instructions in the Grapejuice git repository. The upgrade will begin after you close this "
               "dialog.")

        background.tasks.add(PerformUpdate(update_provider, reopen=True))

    def reinstall_grapejuice(self, *_):
        if self._updating:
            return

        self._updating = True
        background.tasks.add(PerformUpdate(update_provider, reopen=True))

    def uninstall_grapejuice(self, *_):
        do_it = yes_no_dialog("Uninstall Grapejuice", "Are you sure that you want to uninstall Grapejuice?")

        if not do_it:
            return

        params = uninstall.UninstallationParameters(
            yes_no_dialog(
                title="Remove Wineprefix?",
                message="Remove the Wineprefix that contains your installation of Roblox Studio? This will cause all "
                        "configuration of Roblox Studio to be permanently deleted! "
            ),
            for_reals=True
        )

        try:
            dialog("Grapejuice will now uninstall itself, the program will close when the process is finished.")
            uninstall.go(params)

        except Exception as e:
            msg = f"{e.__class__.__name__}: {str(e)}"
            LOG.error(msg)

            dialog(f"Failed to uninstall Grapejuice.\n\n{msg}")

    def show_background_task_errors(self, *_):
        errors = [*background_task_errors]
        background_task_errors.clear()

        dialog("Some errors occurred while running. The following dialogs will show them in order. Check the logs for "
               "the full details of the errors.")

        for i, err in enumerate(errors):
            dialog("Error " + str(i + 1) + ": " + str(err))

        on_background_errors_shown()


class MainWindow(WindowBase):
    def __init__(self):
        super().__init__(
            variables.grapejuice_glade(),
            MainWindowHandlers()
        )

        self._background_task_errors = []

        background.tasks.tasks_changed.add_listener(self.on_tasks_changed)
        on_destroy.add_listener(self.before_destroy)

        self.on_tasks_changed()
        self.background_task_errors_button.hide()
        self.set_update_status_visibility(False)

        if update_provider.can_update():
            self.reinstall_grapejuice_button.show()
            self.uninstall_button.show()

        else:
            self.reinstall_grapejuice_button.hide()
            self.uninstall_button.hide()

        on_background_task_error.add_listener(self.on_background_task_error)
        on_background_errors_shown.add_listener(self.on_background_task_errors_shown)

        self.perform_update_check()

    @property
    def window(self):
        return self.builder.get_object("main_window")

    @property
    def background_task_spinner(self):
        return self.builder.get_object("background_task_spinner")

    @property
    def background_task_errors_button(self):
        return self.builder.get_object("background_task_errors_button")

    @property
    def update_status(self):
        return self.builder.get_object("update_status")

    @property
    def update_status_label(self):
        return self.builder.get_object("update_status_label")

    @property
    def update_button(self):
        return self.builder.get_object("update_button")

    @property
    def uninstall_button(self):
        return self.builder.get_object("uninstall_button")

    @property
    def reinstall_grapejuice_button(self):
        return self.builder.get_object("reinstall_grapejuice_button")

    def set_update_status_visibility(self, visible: bool, ignore_elements: Iterable = None):
        for element in (self.update_status_label, self.update_button, self.update_status):
            if ignore_elements and element in ignore_elements:
                continue

            if visible:
                element.show()

            else:
                element.hide()

    def show_update_status(self, status: str, show_button: bool):
        if show_button:
            ignore_elements = []

        else:
            ignore_elements = [self.update_button]

        self.update_status_label.set_text(status)
        self.set_update_status_visibility(True, ignore_elements)

    def on_background_task_error(self, _task, e):
        self.background_task_errors_button.show()
        background_task_errors.append(e)

    def on_background_task_errors_shown(self):
        self.background_task_errors_button.hide()

    def on_tasks_changed(self):
        if background.tasks.count > 0:
            self.background_task_spinner.start()

        else:
            self.background_task_spinner.stop()

    def show(self):
        self.window.show()

    def before_destroy(self):
        background.tasks.tasks_changed.remove_listener(self.on_tasks_changed)

    def perform_update_check(self):
        if not update_provider.can_update():
            return

        w = self

        class CheckForUpdates(background.BackgroundTask):
            def __init__(self, **kwargs):
                super().__init__("Checking for a newer version of Grapejuice", **kwargs)

            def work(self) -> None:
                show_button = False

                if update_provider.update_available():
                    s = "This version of Grapejuice is out of date.\n" \
                        f"{update_provider.local_version()} -> {update_provider.target_version()}"
                    show_button = True

                else:
                    if update_provider.local_is_newer():
                        s = f"This version of Grapejuice is from the future\n{update_provider.local_version()}"

                    else:
                        s = f" Grapejuice is up to date\n{update_provider.local_version()}"

                if s:
                    w.update_status_label.set_text(s)
                    w.show_update_status(s, show_button)

        background.tasks.add(CheckForUpdates())

    def __del__(self):
        on_background_task_error.remove_listener(self.on_background_task_error)
        on_background_errors_shown.remove_listener(self.on_background_task_errors_shown)
