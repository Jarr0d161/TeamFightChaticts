import tkinter as tk
import tkinter.font as tkFont

from .twitch_script import TwitchBot

class TwitchBotGUI(tk.Frame):
    def __init__(self, parent, width=518, height=180, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.pool = tk.IntVar()

        self.poolvari = tk.IntVar()
        self.user_input = tk.StringVar()

        self.someBot = None

        self.screenwidth = self.parent.winfo_screenwidth()
        self.screenheight = self.parent.winfo_screenheight()

        alignstr = '%dx%d+%d+%d' % (width, height, (self.screenwidth - width) / 2, (self.screenheight - height) / 2)

        self.parent.geometry(alignstr)
        self.parent.resizable(width=False, height=False)

        self.PoolEntry = tk.Entry(self.parent)
        self.PoolEntry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        self.PoolEntry["font"] = ft
        self.PoolEntry["fg"] = "#333333"
        self.PoolEntry["justify"] = "center"
        self.PoolEntry.insert(0, "10")
        self.PoolEntry.place(x=220,y=110,width=82,height=30)

        self.GLabel_256 = tk.Label(self.parent)
        self.GLabel_256["bg"] = "#878787"
        ft = tkFont.Font(family='arial',size=9)
        self.GLabel_256["font"] = ft
        self.GLabel_256["fg"] = "#ffffff"
        self.GLabel_256["justify"] = "center"
        self.GLabel_256["text"] = "Mit dem Start Button beginnt der Twitchbot seine Arbeit."
        self.GLabel_256.place(x=20,y=30,width=476,height=30)

        self.GLabel_253 = tk.Label(self.parent)
        self.GLabel_253["bg"] = "#878787"
        ft = tkFont.Font(family='arial',size=9)
        self.GLabel_253["font"] = ft
        self.GLabel_253["fg"] = "#ffffff"
        self.GLabel_253["justify"] = "center"
        self.GLabel_253["text"] = "Auth für Twich in config eintragen im Stil auth=oauth:... und channel=channelname"
        self.GLabel_253.place(x=20,y=50,width=476,height=30)

        self.GLabel_459 = tk.Label(self.parent)
        ft = tkFont.Font(family='arial',size=12)
        self.GLabel_459["font"] = ft
        self.GLabel_459["fg"] = "#333333"
        self.GLabel_459["justify"] = "center"
        self.GLabel_459["text"] = "Nachrichten Pool (Anzahl):"
        self.GLabel_459.place(x=10,y=110,width=210,height=30)

        self.someButton = tk.Button(self.parent, text="Start", bg="#efefef",justify="center", font=('arial', 12, 'normal'), command=self.runBot)
        self.someButton.place(x=330,y=110,width=70,height=30)

        tk.Button(self.parent, text="Exit", bg="#efefef",justify="center", font=('arial', 12, 'normal'), command=self.exitButton).place(x=420,y=110,width=70,height=30)
        self.state = False

    def runBot(self):
        self.pool = self.PoolEntry.get()

        if self.pool.isdigit():
            self.pool = int(self.pool)
        else:
            self.pool = 10

        if not self.state:
            self.startButton()
        else:
            self.stopButton()

    def startButton(self):
        self.someBot = TwitchBot(False, self.pool)
        self.someBot.start_bot()
        print("Gestartet")
        self.state = True
        self.someButton.config(text="Stop")

    def stopButton(self):
        if self.someBot is not None:
            self.someBot.stop()
        print("Bot beendet.")
        self.state  = False
        self.someBot = None
        self.someButton.config(text="Start")

    def exitButton(self):
        print('Closing.')
        if self.someBot is not None:
            self.someBot.stop()
        self.parent.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TeamFightChaticts by Flanivia & Jarr0d")
    TwitchBotGUI(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
