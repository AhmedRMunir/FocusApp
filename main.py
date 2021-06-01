from kivy.app import App
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.lang import Builder
from settingsjson import settings_json
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock
from time import strftime

break_timer_seconds = 0
break_started = False


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def start_work_timer(self):
        self.app.root.get_screen("work").work_started = True

class WorkPage(Screen):

    work_timer_seconds = StringProperty("0")
    work_started = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_details(self, widget):
        print(widget)
    
    def start(self):
        print(self.parent)
    
    def update_work_timer(self, nap):
        if self.work_started:
            self.sw_seconds += nap
        minutes, seconds = divmod(self.sw_seconds, 60)
        # self.root.get_screen("work").ids["work_timer"].text = strftime("[b]%H[/b]:%M:%S")
        self.root.get_screen("work").ids["work_timer"].text = f'{int(minutes):02}:{int(seconds):02}'
    
    def on_start(self):
        Clock.schedule_interval(self.update_work_timer, 0)

class WindowManager(ScreenManager):
    pass

# Builder.load_file("phlo.kv")
class PhloApp(App):

    # Work and Break timer vars

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        # setting = self.config.get('example', 'boolexample')
        return WindowManager()
    
    def build_config(self, config):
        config.setdefaults("example", {
            "lightmode": False,
            "numericexample": 10,
            "optionsexample": "option2",
            "stringexample": "string",
            "pathexample": "/path"
        })
    
    def build_settings(self, settings):
        settings.add_json_panel("Panel Name", 
                                 self.config,
                                 data=settings_json)
    
    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)

PhloApp().run()