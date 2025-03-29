import time
import threading
import keyboard
import mouse


class ScriptRunner:

    def __init__(self, startkey, pausekey, stopkey='esc', run: callable = None, loop=False, on_state_change=None):
        self.paused = True
        self.running = True
        self.stopped = False
        self.run = run
        self.loop = loop
        self.on_state_change = on_state_change

        if startkey:
            self.hook_hotkey(startkey, self.start)
        if pausekey:
            self.hook_hotkey(pausekey, self.pause)
        if stopkey:
            self.hook_hotkey(stopkey, self.stop)

        print(f'start: {startkey}, pause: {pausekey}, stop: {stopkey}')

        self._thread = threading.Thread(target=self.update, daemon=True)
        self._thread.start()

    def mouse_hook(self, button, callback):

        def _callback(event):
            if type(event) == mouse.ButtonEvent and event.event_type == 'up' and event.button == button:
                callback()

        mouse.hook(_callback)

    def hook_hotkey(self, key, callback):
        if key.startswith('mouse.'):
            self.mouse_hook(key.replace('mouse.', ''), callback)
        else:
            keyboard.add_hotkey(key, callback)

    def start(self):
        # print('start')
        self.paused = False
        if self.on_state_change:
            self.on_state_change(self.paused, self.stopped)

    def pause(self):
        # print('pause')
        self.paused = True
        if self.on_state_change:
            self.on_state_change(self.paused, self.stopped)

    def stop(self):
        # print('stop')
        self.running = False
        self.stopped = True
        mouse.unhook_all()
        keyboard.unhook_all()
        if self.on_state_change:
            self.on_state_change(self.paused, self.stopped)

    def update(self):
        while self.running:
            time.sleep(0.01)
            if self.paused or self.stopped:
                continue
            if self.run:
                try:
                    self.run()
                except Exception as e:
                    print(f"Error in script: {e}")
                    self.stop()
            if not self.loop:
                self.pause()

    def wait(self):
        try:
            while self.running:
                time.sleep(0.01)
        except KeyboardInterrupt:
            self.stop()
        self._thread.join()
