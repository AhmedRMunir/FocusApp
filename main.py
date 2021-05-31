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

class HomePage(Screen):
    pass

class WorkPage(Screen):
    def show_details(self, widget):
        print(widget)

class WindowManager(ScreenManager):
    pass

# Builder.load_file("phlo.kv")
class PhloApp(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        setting = self.config.get('example', 'boolexample')
        return WindowManager()
    
    def build_config(self, config):
        config.setdefaults("example", {
            "boolexample": True,
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