# IMPORTS
# Plotting
import kivy
# Specify kivy version
kivy.require("1.9.0")

# Plotting imports
from backend_kivyagg import FigureCanvasKivyAgg
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

# Kivy imports
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

# Set background RGBA color - should be a nice gray ???
from kivy.core.window import Window
Window.clearcolor = (192/255, 187/255, 178/255, 1)


# Navigation manager
class WindowManager(ScreenManager):
    pass

class MainWindowScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(MainWindow())

class MainWindow(Widget):
    pass

class InfoScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Info())

class Info(Widget):
    pass

# Trachtenberg system conventions + trachtenberg history
class TrachtSysInfo(FloatLayout):   
    def __init__(self, **kw):
        super(TrachtSysInfo, self).__init__(**kw)

class TrachtSysInfoScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(TrachtSysInfo())




# Get `kv` file
kv = Builder.load_file("my.kv")


# My app
class MyApp(App):
    def build(self):
        # self.cont = UT_Mult()
        # return self.cont  
        return kv
    

# Run app
if __name__ == "__main__":    
    app = MyApp()
    app.run()








