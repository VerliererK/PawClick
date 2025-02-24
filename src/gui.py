import os
import importlib
import logging

import customtkinter
from PIL import Image
from .runner import ScriptRunner

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
customtkinter.set_widget_scaling(2)

ICON_PATH = 'assets/icon.ico'
if not os.path.exists(ICON_PATH):
    ICON_PATH = os.path.join('app', ICON_PATH)


class Button(customtkinter.CTkButton):

    def __init__(self, master=None, **kwargs):
        self.origin_fg_color = None
        self.disabled_fg_color = '#808080'
        super().__init__(master=master, **kwargs)

    def _draw(self, no_color_updates=False):
        if self.origin_fg_color is None:
            self.origin_fg_color = self._fg_color
        self._fg_color = self.disabled_fg_color if self._state == 'disabled' else self.origin_fg_color
        super()._draw(no_color_updates=no_color_updates)

    def configure(self, require_redraw=False, **kwargs):
        if 'fg_color' in kwargs:
            self.origin_fg_color = kwargs['fg_color']
        super().configure(require_redraw, **kwargs)


class App(customtkinter.CTk):

    def __init__(self):
        self.runner = None
        self.hotkeys = {'start': 'F1', 'pause': 'F2', 'stop': 'Esc'}

        super().__init__()
        self.title("PawClick")
        self.minsize(600, 800)
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)

        self.font = customtkinter.CTkFont(size=16, family='Noto Sans CJK TC')
        self.create_widgets()

    def create_widgets(self):
        image = Image.open(ICON_PATH) if os.path.exists(ICON_PATH) else Image.new('RGBA', (10, 10), (255, 0, 0, 0))
        icon = customtkinter.CTkImage(light_image=image, size=(60, 60))
        label = customtkinter.CTkLabel(self, image=icon, text='')
        label.pack(side='top', pady=10)

        # --- Script Selection ---
        frame = customtkinter.CTkFrame(self, fg_color='transparent')
        frame.pack(expand=True, ipadx=10, pady=10)

        scripts = self.find_scripts()
        self.menu_scripts = customtkinter.CTkOptionMenu(frame, width=160, font=self.font, values=scripts)
        self.menu_scripts.configure(button_color=self.menu_scripts.cget('fg_color'), button_hover_color=self.menu_scripts.cget('fg_color'))
        self.menu_scripts.set("Select Script" if not scripts else scripts[0])
        self.menu_scripts.pack(side='left')

        self.btn_load = Button(frame, width=80, font=self.font, text="Load", command=self.load_script)
        self.btn_load.pack(side='right')

        # --- Hotkey Configuration ---
        hotkey_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        hotkey_frame.pack(expand=True, pady=10)

        self.entry_hotkeys = {}
        row = 0
        for hotkey in ['start', 'pause', 'stop']:
            label = customtkinter.CTkLabel(hotkey_frame, font=self.font, text=f"{hotkey.capitalize()}:")
            label.grid(row=row, column=0, padx=10, ipady=10)
            entry = customtkinter.CTkEntry(hotkey_frame, font=self.font, width=50, height=28)
            entry.grid(row=row, column=1)
            entry.insert(0, self.hotkeys[hotkey])
            row = row + 1
            self.entry_hotkeys[hotkey] = entry

        label = customtkinter.CTkLabel(hotkey_frame, font=self.font, text="Loop:")
        label.grid(row=row, column=0, padx=10, ipady=10)
        self.checkbox_loop = customtkinter.CTkCheckBox(
            hotkey_frame,
            text='',
            width=50,
            height=28,
            checkbox_height=22,
            checkbox_width=22,
            border_color=entry._border_color,
            border_width=entry._border_width,
        )
        self.checkbox_loop.grid(row=row, column=1)
        self.entry_hotkeys['loop'] = self.checkbox_loop

        # --- Button Frame ---
        btn_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        btn_frame.pack(expand=True, pady=10, ipadx=10)

        self.btn_pause = Button(btn_frame, width=100, font=self.font, text="Start", command=self.pause_script)
        self.btn_pause.pack(side='left')
        self.btn_stop = Button(btn_frame, width=100, font=self.font, text="Stop", command=self.stop_script)
        self.btn_stop.configure(fg_color='#B00020', hover_color='#800018')
        self.btn_stop.pack(side='right')

        self.btn_pause.configure(state='disabled')
        self.btn_stop.configure(state='disabled')

    def find_scripts(self):
        scripts_dir = os.path.join(os.getcwd(), 'scripts')
        if os.path.exists(scripts_dir):
            scripts = [f[:-3] for f in os.listdir(scripts_dir) if f.endswith('.py') and f != '__init__.py']
            return scripts
        return []

    def on_script_state_change(self, paused, stopped):
        self.btn_load.configure(state='normal' if stopped else 'disabled')
        self.menu_scripts.configure(state='normal' if stopped else 'disabled')
        self.btn_pause.configure(state='disabled' if stopped else 'normal')
        self.btn_stop.configure(state='disabled' if stopped else 'normal')
        self.btn_pause.configure(text='Start' if paused else 'Pause')

        for key in self.entry_hotkeys:
            self.entry_hotkeys[key].configure(state='normal' if stopped else 'disabled')

    def load_script(self):
        script_name = self.menu_scripts.get()
        try:
            module = importlib.import_module(f'scripts.{script_name}')
            importlib.reload(module)
            logging.info(f"Load {script_name} successfully.")

            self.runner = ScriptRunner(startkey=self.entry_hotkeys['start'].get(),
                                       pausekey=self.entry_hotkeys['pause'].get(),
                                       stopkey=self.entry_hotkeys['stop'].get(),
                                       run=module.run,
                                       loop=self.checkbox_loop.get() == 1,
                                       on_state_change=self.on_script_state_change)

            self.on_script_state_change(True, False)
        except Exception as e:
            logging.error(f"Error executing script {script_name}: {e}")

    def pause_script(self):
        if not self.runner:
            return
        if self.runner.paused:
            self.runner.start()
        else:
            self.runner.pause()

    def stop_script(self):
        if self.runner:
            self.runner.stop()
            self.runner = None

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
