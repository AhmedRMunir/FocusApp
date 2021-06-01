from time import strftime
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
from datetime import date, datetime, timedelta

break_timer_seconds = 0
break_started = False


class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def start_scheduler(self, *args):
        Clock.schedule_interval(self.update_work_timer, 0)
        App.get_running_app().root.get_screen("work").work_total_time += self.ids["work_slider"].value * 60
        # App.get_running_app().root.get_screen("work").work_total_time += 
    
    def update_work_timer(self, nap, *args):

        workpage = App.get_running_app().root.get_screen("work")
        workpage.work_total_time -= nap

        minutes, seconds = divmod(workpage.work_total_time, 60)
        hours, minutes = divmod(minutes, 60)
        workpage.work_timer_text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

class WorkPage(Screen):
    pass
    
class WindowManager(ScreenManager):
    pass

# Builder.load_file("phlo.kv")
class PhloApp(App):

    work_timer_seconds = 0
    work_started = BooleanProperty(False)
    
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