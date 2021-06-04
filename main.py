from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, OptionProperty
from kivymd.uix.picker import MDTimePicker
from kivy.core.window import Window
from datetime import date, datetime
from time import strftime, asctime
from kivy.clock import Clock
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

Window.size = (400, 800)

class WindowManager(ScreenManager):
    pass

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class LoginPage(Screen):
    pass

class HomePage(Screen):
    def increment_work_time(self, *args):
        # print(self.work_increment)
        App.get_running_app().root.ids["window_manager"].get_screen("work").work_total_time += self.work_increment

    def increment_break_time(self, *args):
        App.get_running_app().root.ids["window_manager"].get_screen("break").break_total_time += self.break_increment
        


class PhloApp(MDApp):

    isWork = None
    work_started = False
    break_started = False

    # data = {
    #     'Python': 'language-python',
    #     'PHP': 'language-php',
    #     'C++': 'language-cpp'
    # }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [{"text": f'Item {i}'} for i in range(5)]

        # self.menu = MDDropDownMenu(
        #     caller = self.root.ids["window_manager"].get_screen("home").ids["dropdown_item"],
        #     items = menu_items,
        #     position = "center",
        #     width_mult = 4
        # )
        # self.menu.bind(on_release=self.set_item)
        # print(self.root.ids["window_manager"].get_screen("home"))
        # self.menu = MDDropdownMenu(
        #     caller=self.root.ids["window_manager"].get_screen("home").ids["dropdown_item"],
        #     items=menu_items,
        #     position="center",
        #     width_mult=4,
        # )
    
    def set_item(self, instance_menu, instance_menu_item):
        self.root.ids["window_manager"].get_screen("home").ids["dropdown_item"].set_item(instance_menu_item.text)
        instance_menu.dismiss()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        # self.theme_cls.accent_palette = "Yellow"

        # screen = MDScreen()
        # speed_dial = MDFloatingActionButtonSpeedDial()
        # speed_dial.data = self.data
        # speed_dial.root_button_anim = True
        # screen.add_widget(speed_dial)
        # return screen
        # return Builder.load_file("phlo.kv")
        # return Builder.load_string(KV)
    
    def login(self):
        pass
        # self.root.ids["window_manager"].get_screen("login").ids["welcome_label"].text = f'Welcome {self.root.ids["window_manager"].get_screen("login").ids["user"].text}!'
    
    def clear(self):
        self.root.ids["window_manager"].get_screen("login").ids["user"].text = ""
        self.root.ids["window_manager"].get_screen("login").ids["password"].text = ""

    def show_time_picker(self, widget, time):
        previous_time = datetime.strptime(time, '%H:%M:%S').time()
        time_dialog = MDTimePicker()
        time_dialog.set_time(previous_time)
        self.isWork = widget.isWork
        time_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        time_dialog.open()
    
    def get_time(self, instance, time):
        '''
        The method returns the set time.

        :type instance: <kivymd.uix.picker.MDTimePicker object>
        :type time: <class 'datetime.time'>
        '''
        print(time)

        return time
    
    def on_save(self, instance, value):
        # self.root.ids["window_manager"].get_screen("home").ids["work_timer"].text = "4"
        total_time_increment = 0
        total_time_increment += int(value.strftime("%H")) * 60 * 60
        total_time_increment += int(value.strftime("%M")) * 60
        total_time_increment += int(value.strftime("%S"))

        if self.isWork:
            self.root.ids["window_manager"].get_screen("home").ids["work_time_picker"].text = value.strftime("%H:%M:00")
            # self.root.ids["window_manager"].get_screen("home").work_increment = value.strftime("%H:%M:00")
            self.root.ids["window_manager"].get_screen("home").work_increment = total_time_increment
        else:
            self.root.ids["window_manager"].get_screen("home").ids["break_time_picker"].text = value.strftime("%H:%M:00")
            self.root.ids["window_manager"].get_screen("home").break_increment = total_time_increment

    def on_cancel(self, instance, value):
        pass

    def start_stop_work_timer(self, *args):
        if not self.work_started:
            self.work_scheduler = Clock.schedule_interval(self.update_work_timer, 0)
            self.work_started = True
        else:
            self.work_scheduler.cancel()
            self.work_started = False
    
    def update_work_timer(self, nap, *args):
        workpage = self.root.ids["window_manager"].get_screen("work")
        if self.work_started:
            workpage.work_total_time -= nap

            minutes, seconds = divmod(workpage.work_total_time, 60)
            hours, minutes = divmod(minutes, 60)
            workpage.work_timer_text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
    
    def show_hide_work_timer(self, *args):
        opacity = self.root.ids["window_manager"].get_screen("work").ids["work_timer"].opacity
        if opacity > 0:
            self.root.ids["window_manager"].get_screen("work").ids["work_timer"].opacity = 0
        else:
            self.root.ids["window_manager"].get_screen("work").ids["work_timer"].opacity = 1.0

    def start_stop_break_timer(self, *args):
        if not self.break_started:
            self.break_scheduler = Clock.schedule_interval(self.update_break_timer, 0)
            self.break_started = True
        else:
            self.break_scheduler.cancel()
            self.break_started = False
    
    def update_break_timer(self, nap, *args):
        breakpage = self.root.ids["window_manager"].get_screen("break")
        if self.break_started:
            breakpage.break_total_time -= nap

            minutes, seconds = divmod(breakpage.break_total_time, 60)
            hours, minutes = divmod(minutes, 60)
            breakpage.break_timer_text = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
    
    def show_hide_break_timer(self, *args):
        opacity = self.root.ids["window_manager"].get_screen("break").ids["break_timer"].opacity
        if opacity > 0:
            self.root.ids["window_manager"].get_screen("break").ids["break_timer"].opacity = 0
        else:
            self.root.ids["window_manager"].get_screen("break").ids["break_timer"].opacity = 1.0

    def callback(self, instance):
        if instance.icon == "coffee":
            if (self.root.ids["window_manager"].current == "break"):
                self.root.ids["window_manager"].current = "work"
                self.root.ids["window_manager"].transition.direction = "right"
            else:
                self.root.ids["window_manager"].current = "break"
                self.root.ids["window_manager"].transition.direction = "left"
            self.start_stop_work_timer(self)
            self.start_stop_break_timer(self)
        elif instance.icon == "trending-up":
            print("Show Graph")
        elif instance.icon == "cancel":
            if (self.work_started):
                self.start_stop_work_timer(self)
            
            if (self.break_started):
                self.start_stop_break_timer(self)
            self.root.ids["window_manager"].current = "summary"

            # print(self.root.ids["window_manager"].get_screen("work").ids["work_float"].state.options)
            # self.root.ids["window_manager"].get_screen("work").ids["work_float"].state = state = OptionProperty("open", options=("close", "open"))

PhloApp().run()