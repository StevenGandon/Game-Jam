from CNEngine import *
import os
import sdl2
import sdl2.ext
import sdl2.sdlmixer as sdlmixer
import time

class OlivierDeChezCarglass(Object):
    def __init__(self, interface, maininterface):
        super().__init__(0, 0)

        self.interface = interface
        self.nb_images = len(os.listdir(f"{RESSOURCES}/videos/ad"))
        self.image = 0
        self.frame_time = 1 / 24
        self.start_time = None
        self.maininterface = maininterface
        self.is_paused = False
        self.paused_time = 0
        self.pause_start = None

        self.pause_image_path = f"{RESSOURCES}/UI/pause.png"
        if os.path.exists(self.pause_image_path):
            self.pause_texture = get_texture(self.pause_image_path)

        sdlmixer.Mix_OpenAudio(44100, sdlmixer.MIX_DEFAULT_FORMAT, 2, 2048)

        sound_path = f"{RESSOURCES}/sound/ad.mp3".encode('utf-8')
        self.sound = sdlmixer.Mix_LoadMUS(sound_path)

        button_width = 150
        button_height = 50
        button_x = self.interface.window.video_mode.size.x - button_width - 10
        button_y = self.interface.window.video_mode.size.y - button_height - 10

        self.skip_button = Button(button_x, button_y, button_width, button_height, self.skip_ad)
        self.interface.add_gui(self.skip_button)

        self.skip_button_text = Text(button_x + 10, button_y + 10, "Skip Ad ->", 24, color=(255, 255, 255))

    def start_sound(self):
        sdlmixer.Mix_PlayMusic(self.sound, 0)
        self.start_time = time.time()
        self.paused_time = 0

    def skip_ad(self, *args):
        self.start_time = time.time()
        sdlmixer.Mix_HaltMusic()
        self.start_sound()
        self.image = 0

    def update(self, delta_time):
        if self.is_paused:
            return

        if self.start_time is None:
            return

        elapsed_time = time.time() - self.start_time - self.paused_time
        expected_frame = int(elapsed_time / self.frame_time)
        self.image = expected_frame % self.nb_images

        if self.image == self.nb_images - 1:
            self.start_time = time.time()
            self.image = 0
            self.start_sound()

    def draw(self, screen):
        if not self.is_paused:
            sdlmixer.Mix_ResumeMusic()
        image_path = f"{RESSOURCES}/videos/ad/ad{self.image:04}.png"
        if os.path.exists(image_path):
            texture = get_texture(image_path)
            screen.blit(texture, Vector2(0, 0))

        for element in tuple(CACHED_IMAGE.keys()):
            if 'videos/ad' in element:
                CACHED_IMAGE[element].destroy()
                del CACHED_IMAGE[element]

        button_rect = Rectangle(self.skip_button.x, self.skip_button.y, self.skip_button.size_x, self.skip_button.size_y, (0, 0, 0))
        button_rect.draw(screen)

        self.skip_button_text.draw(screen)

        if self.is_paused:
            screen_size = self.interface.window.video_mode.size
            self.pause_image_size = self.pause_texture.size
            pause_position = Vector2((screen_size.x - self.pause_image_size.x) // 2, (screen_size.y - self.pause_image_size.y) // 2)
            screen.blit(self.pause_texture, pause_position)

    def event(self, window):
        if ((window.get_event(EVENT_CLOSE) or window.get_event(EVENT_QUIT)) and window.is_closable):
            self.maininterface.force_stopped = True
        key_press = window.get_event(EVENT_KEY_DOWN)
        if key_press:
            if 32 in key_press.key:
                self.is_paused = not self.is_paused
                if self.is_paused:
                    sdlmixer.Mix_PauseMusic()
                    self.pause_start = time.time()
                    if self.is_paused:
                        self.interface.window.set_closable(True)
                    else:
                        self.interface.window.set_closable(False)
                else:
                    sdlmixer.Mix_ResumeMusic()
                    self.paused_time += time.time() - self.pause_start
        self.skip_button.event(window)

    def destroy(self):
        sdlmixer.Mix_FreeMusic(self.sound)
        sdlmixer.Mix_CloseAudio()

def build_level3(interface: MainInterface = None):
    interfaceAd: MainInterface = Interface("Ads (1 out of 1)")
    olivier = OlivierDeChezCarglass(interfaceAd, interface)
    interfaceAd.add_element(olivier)
    olivier.start_sound()
    interface.add_interface(interfaceAd)
    interfaceAd.window.set_closable(False)
    return interface