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
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.lang import Builder
from settingsjson import settings_json
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.clock import Clock
from datetime import date, datetime, timedelta
from math import sin
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.screenmanager import CardTransition

from kivy.core.window import Window
Window.size = (600, 600)

class WindowManager(ScreenManager):
    pass
        

class HomePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def increment_work_time(self, *args):
        # App.get_running_app().work_scheduler = Clock.schedule_interval(self.update_work_timer, 0)
        App.get_running_app().root.get_screen("work").work_total_time += self.ids["work_slider"].value * 60 + 1

    def increment_break_time(self, *args):
        # App.get_running_app().work_scheduler = Clock.schedule_interval(self.update_work_timer, 0)
        App.get_running_app().root.get_screen("break").break_total_time += self.ids["break_slider"].value * 60 + 1

class WorkPage(Screen):
    pass

class WorkDetesPage(Screen):
    # def __init__(self, **kwargs):
        # disp = SetGraph()
        # disp.update_graph()
        # self.add_widget(disp)
    pass

class SetGraph(Widget):
    graph_test = ObjectProperty(None)

    def update_graph(self):
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        self.graph_test.add_plot(plot)

class Background(FloatLayout):
    pass

# Builder.load_file("phlo.kv")
class PhloApp(App):

    # App.get_running_app().root.transition

    # Work and Break timer vars
    work_timer_seconds = 0
    work_started = BooleanProperty(False)

    break_timer_seconds = 0
    break_started = BooleanProperty(False)

    # Temporary background change
    dark_mode = "dark.zip"
    light_mode = "green_background.jpg"
    theme = light_mode
    
    
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
        if self.config.get('example', 'lightmode'):
            self.theme = self.light_mode
            print(App.get_running_app().root)
        elif self.config.get('example', 'lightmode') == 0:
            self.theme = self.dark_mode
        # print(config, section, key, value)

    def reset_work_timer(self, *args):
        App.get_running_app().root.get_screen("work").work_total_time = 0
        self.update_work_timer(self, 0)

    def reset_break_timer(self, *args):
        App.get_running_app().root.get_screen("break").break_total_time = 0
        self.update_break_timer(self, 0)
    
    def start_stop_work_timer(self, *args):
        if not self.work_started:
            self.work_scheduler = Clock.schedule_interval(self.update_work_timer, 0)
            self.work_started = True
        else:
            self.work_scheduler.cancel()
            self.work_started = False
    
    def update_work_timer(self, nap, *args):
        workpage = App.get_running_app().root.get_screen("work")
        if self.work_started:
            workpage.work_total_time -= nap

            minutes, seconds = divmod(workpage.work_total_time, 60)
            hours, minutes = divmod(minutes, 60)
            workpage.work_timer_text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
    
    def start_stop_break_timer(self, *args):
        if not self.break_started:
            print("break started")
            self.break_scheduler = Clock.schedule_interval(self.update_break_timer, 0)
            self.break_started = True
        else:
            self.break_scheduler.cancel()
            self.break_started = False
            print("break stopped")
    
    def update_break_timer(self, nap, *args):
        breakpage = App.get_running_app().root.get_screen("break")
        if self.break_started:
            breakpage.break_total_time -= nap

            minutes, seconds = divmod(breakpage.break_total_time, 60)
            hours, minutes = divmod(minutes, 60)
            breakpage.break_timer_text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

PhloApp().run()