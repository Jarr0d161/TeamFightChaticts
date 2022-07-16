from typing import Dict, Any, Protocol

import tkinter as tk
import tkinter.font as tkFont


class TwitchChatbot(Protocol):
    def start_bot(self, pool_size: int):
        raise NotImplementedError()

    def stop_bot(self):
        raise NotImplementedError()


class TwitchChatbotLauncherUI(tk.Frame):
    # pylint: disable=too-many-ancestors, too-many-instance-attributes
    # pylint: disable=keyword-arg-before-vararg, too-many-arguments
    def __init__(self, chatbot: TwitchChatbot, ui_settings: Dict[str, Any],
                 parent: tk.Tk=tk.Tk(), width=518, height=180, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.chatbot = chatbot
        self.ui_settings = ui_settings
        self.pool = 10
        self.is_running = False

        self.parent = TwitchChatbotLauncherUI._init_parent(
            parent, self.ui_settings['ui_title'], width, height)
        self.poolsize_input = self._load_poolsize_input()
        self._load_auth_usage_label()
        self._load_poolsize_label()
        self.start_stop_button = self._load_start_stop_button()
        self._load_exit_button()

    def display_as_daemon(self):
        self.pack(side="top", fill="both", expand=True)
        self.parent.mainloop()

    @staticmethod
    def _init_parent(parent: tk.Tk, title: str, width, height) -> tk.Tk:
        parent.title(title)
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        align_width, align_height = (screen_width - width) // 2, (screen_height - height) // 2
        alignstr = '%dx%d+%d+%d' % (width, height, align_width, align_height)
        parent.geometry(alignstr)
        parent.resizable(width=False, height=False)
        return parent

    def _load_poolsize_input(self) -> tk.Entry:
        poolsize_input = tk.Entry(self.parent)
        poolsize_input["borderwidth"] = "1px"
        poolsize_input["font"] = tkFont.Font(family='Times',size=12)
        poolsize_input["fg"] = "#333333"
        poolsize_input["justify"] = "center"
        poolsize_input.insert(0, str(self.pool))
        poolsize_input.place(x=220, y=110, width=82, height=30)
        return poolsize_input

    def _load_auth_usage_label(self):
        auth_usage_label = tk.Label(self.parent)
        auth_usage_label["bg"] = "#878787"
        auth_usage_label["font"] = tkFont.Font(family='arial',size=9)
        auth_usage_label["fg"] = "#ffffff"
        auth_usage_label["justify"] = "center"
        auth_usage_label["text"] = self.ui_settings["auth_usage"]
        auth_usage_label.place(x=20, y=50, width=476, height=30)

    def _load_poolsize_label(self):
        msg_pool_label = tk.Label(self.parent)
        msg_pool_label["font"] = tkFont.Font(family='arial', size=12)
        msg_pool_label["fg"] = "#333333"
        msg_pool_label["justify"] = "center"
        msg_pool_label["text"] = self.ui_settings["msg_pool_count"]
        msg_pool_label.place(x=10, y=110, width=210, height=30)

    def _load_start_stop_button(self) -> tk.Button:
        start_stop_button = tk.Button(
            self.parent, text="Start", bg="#efefef", justify="center",
             font=('arial', 12, 'normal'), command=self._start_or_stop_button_pressed)
        start_stop_button.place(x=330, y=110, width=70, height=30)
        return start_stop_button

    def _load_exit_button(self):
        exit_button = tk.Button(
            self.parent, text="Exit", bg="#efefef",justify="center",
            font=('arial', 12, 'normal'), command=self._exit_button)
        exit_button.place(x=420, y=110, width=70, height=30)

    def _start_or_stop_button_pressed(self):
        pool: str = self.poolsize_input.get()
        self.pool = int(pool) if pool.isdigit() else 10

        if self.is_running:
            self._stop_button_pressed()
        else:
            self._start_button_pressed()

    def _start_button_pressed(self):
        self.chatbot.start_bot(self.pool)
        self.is_running = True
        self.start_stop_button.config(text=self.ui_settings['stop_button_text'])

    def _stop_button_pressed(self):
        self.chatbot.stop_bot()
        self.is_running  = False
        self.start_stop_button.config(text=self.ui_settings['start_button_text'])

    def _exit_button(self):
        self.chatbot.stop_bot()
        self.parent.destroy()
