import tkinter as tk
import datetime
from tkinter import ttk
from component_interface import ComponentInterface
from tktooltip import ToolTip


class VideoControlFrame(ttk.Frame, ComponentInterface):
    def __init__(self, container, **args):
        super().__init__(container, **args)

        # layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        for c_idx in range(8):
            self.columnconfigure(c_idx, weight=1)

        # variables
        self.progress_value = tk.IntVar()

        # videos control panel
        self.skip_minus_30sec_button = ttk.Button(
            self, text="-30s", padding=(5), command=lambda: self.skip(-30)
        )
        self.skip_minus_10sec_button = ttk.Button(
            self, text="-10s", padding=(5), command=lambda: self.skip(-10)
        )
        self.skip_minus_5sec_button = ttk.Button(
            self, text="-5s", padding=(5), command=lambda: self.skip(-5)
        )
        self.start_time = tk.Label(
            self,
            text=str(datetime.timedelta(seconds=0)).split(".")[0],
            font=self.master.master.default_font,
        )
        # TODO: implement command=self.seek
        self.progress_slider = tk.Scale(
            self,
            variable=self.progress_value,
            from_=0,
            to=0,
            orient="horizontal",
            font=self.master.master.default_font,
        )
        self.end_time = tk.Label(
            self,
            text=str(datetime.timedelta(seconds=0)).split(".")[0],
            font=self.master.master.default_font,
        )
        self.skip_plus_5sec_button = ttk.Button(
            self, text="+5s", padding=(5), command=lambda: self.skip(5)
        )
        self.skip_plus_10sec_button = ttk.Button(
            self, text="+10s", padding=(5), command=lambda: self.skip(10)
        )
        self.skip_plus_30sec_button = ttk.Button(
            self, text="+30s", padding=(5), command=lambda: self.skip(30)
        )
        self.copy_timestamp_button = ttk.Button(
            self,
            text="Copy timestamp",
            padding=(5),
            command=lambda: self.copy_current_timestamp_to_clipboard(),
        )
        ToolTip(
            self.copy_timestamp_button,
            msg="Copy current timestamp to clipboard (in h:mm:ss format)",
            delay=0,
        )

        self.start_time.grid(row=0, column=0, sticky="EW")
        self.progress_slider.grid(
            row=0, column=1, columnspan=6, sticky="EW", pady=(0, 20)
        )
        self.end_time.grid(row=0, column=7, sticky="EW")
        self.copy_timestamp_button.grid(row=0, column=8, sticky="EW")

        self.skip_minus_30sec_button.grid(row=1, column=0, sticky="EW")
        self.skip_minus_10sec_button.grid(row=1, column=1, sticky="EW")
        self.skip_minus_5sec_button.grid(row=1, column=2, sticky="EW")
        self.skip_plus_5sec_button.grid(row=1, column=6, sticky="EW")
        self.skip_plus_10sec_button.grid(row=1, column=7, sticky="EW")
        self.skip_plus_30sec_button.grid(row=1, column=8, sticky="EW")

    def refresh(self):
        if len(self.master.video_renderer_component.videoplayers) > 0:
            self.video_players = self.master.video_renderer_component.videoplayers
            self.video_player = self.video_players[0]
            self.video_player.bind("<<Duration>>", self.update_duration)
            self.video_player.bind("<<SecondChanged>>", self.update_scale)
            self.video_player.bind("<<Ended>>", self.video_ended)
        else:
            self.video_player = None

    def seek(self, value):
        if self.video_player != None:
            for video_player in self.video_players:
                video_player.seek(value)

    def skip(self, value: int):
        if self.video_player != None:
            for video_player in self.video_players:
                video_player.seek(int(self.progress_slider.get()) + value)
            self.progress_value.set(self.progress_slider.get() + value)

        # audio
        self.master.video_renderer_component.seek(self.progress_value.get())

    def update_duration(self, event):
        if self.video_player != None:
            duration = self.video_player.video_info()["duration"]
            self.end_time["text"] = str(datetime.timedelta(seconds=duration)).split(
                "."
            )[0]
            self.progress_slider["to"] = duration

    def update_scale(self, event):
        if self.video_player != None:
            self.progress_value.set(self.video_player.current_duration())

    def video_ended(self, event):
        self.progress_slider.set(self.progress_slider["to"])
        self.progress_slider.set(0)

    def copy_current_timestamp_to_clipboard(self):
        if self.video_player != None:
            self.clipboard_clear()
            self.clipboard_append(
                str(
                    datetime.timedelta(
                        seconds=round(self.video_player.current_duration())
                    )
                )
            )
            self.update()
