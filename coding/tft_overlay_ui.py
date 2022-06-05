from typing import Callable

import tkinter as tk
import tkinter.font as tkFont

from .settings import ui_settings_of_selected_language


class TFTRemoteControlOverlayUI(tk.Frame):
    # TODO: get rid of inheritance if possible!!!
    def __init__(self, start_chatbot: Callable[[int], None], stop_chatbot: Callable[[], None],
                 parent: tk.Tk=tk.Tk(), width=518, height=180, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.fn_start_chatbot = start_chatbot
        self.fn_stop_chatbot = stop_chatbot

        self.ui_settings = ui_settings_of_selected_language()
        self.parent = self.init_parent(parent, self.ui_settings['ui_title'], width, height)
        self.poolsize_input = self.load_poolsize_input()
        self.load_launch_usage_label()
        self.load_auth_usage_label()
        self.load_poolsize_label()
        self.start_stop_button = self.load_start_stop_button()
        self.load_exit_button()

        self.is_running = False

    def init_parent(self, parent: tk.Tk, title: str, width, height) -> tk.Tk:
        parent.title(title)
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        align_width, align_height = (screen_width - width) // 2, (screen_height - height) // 2
        alignstr = '%dx%d+%d+%d' % (width, height, align_width, align_height)
        parent.geometry(alignstr)
        parent.resizable(width=False, height=False)

    def load_poolsize_input(self) -> tk.Entry:
        poolsize_input = tk.Entry(self.parent)
        poolsize_input["borderwidth"] = "1px"
        poolsize_input["font"] = tkFont.Font(family='Times',size=12)
        poolsize_input["fg"] = "#333333"
        poolsize_input["justify"] = "center"
        poolsize_input.insert(0, "10")
        poolsize_input.place(x=220, y=110, width=82, height=30)
        return poolsize_input

    def load_launch_usage_label(self):
        # TODO: this shouldn't be required, usage of a 'start' button is obvious
        launch_usage = tk.Label(self.parent)
        launch_usage["bg"] = "#878787"
        launch_usage["font"] = tkFont.Font(family='arial',size=9)
        launch_usage["fg"] = "#ffffff"
        launch_usage["justify"] = "center"
        launch_usage["text"] = self.ui_settings["launch_usage"]
        launch_usage.place(x=20, y=30, width=476, height=30)

    def load_auth_usage_label(self):
        auth_usage_label = tk.Label(self.parent)
        auth_usage_label["bg"] = "#878787"
        auth_usage_label["font"] = tkFont.Font(family='arial',size=9)
        auth_usage_label["fg"] = "#ffffff"
        auth_usage_label["justify"] = "center"
        auth_usage_label["text"] = self.ui_settings["auth_usage"]
        auth_usage_label.place(x=20, y=50, width=476, height=30)

    def load_poolsize_label(self):
        msg_pool_label = tk.Label(self.parent)
        msg_pool_label["font"] = tkFont.Font(family='arial', size=12)
        msg_pool_label["fg"] = "#333333"
        msg_pool_label["justify"] = "center"
        msg_pool_label["text"] = self.ui_settings["msg_pool_count"]
        msg_pool_label.place(x=10, y=110, width=210, height=30)

    def load_start_stop_button(self) -> tk.Button:
        start_stop_button = tk.Button(
            self.parent, text="Start", bg="#efefef", justify="center",
             font=('arial', 12, 'normal'), command=self.start_or_stop_button_pressed)
        start_stop_button.place(x=330, y=110, width=70, height=30)
        return start_stop_button

    def load_exit_button(self):
        exit_button = tk.Button(
            self.parent, text="Exit", bg="#efefef",justify="center",
            font=('arial', 12, 'normal'), command=self.exit_button)
        exit_button.place(x=420, y=110, width=70, height=30)

    def display_as_daemon(self):
        self.pack(side="top", fill="both", expand=True)
        self.parent.mainloop()

    def start_or_stop_button_pressed(self):
        pool: str = self.poolsize_input.get()
        self.pool = int(pool) if pool.isdigit() else 10

        if self.is_running:
            self.stop_button_pressed()
        else:
            self.start_button_pressed()

    def start_button_pressed(self):
        self.fn_start_chatbot(self.pool)
        print(self.ui_settings["start"])
        self.is_running = True
        self.start_stop_button.config(text=self.ui_settings['stop_button_text'])

    def stop_button_pressed(self):
        self.fn_stop_chatbot()
        print(self.ui_settings["stop"])
        self.is_running  = False
        self.start_stop_button.config(text=self.ui_settings['start_button_text'])

    def exit_button(self):
        self.fn_stop_chatbot()
        self.parent.destroy()
