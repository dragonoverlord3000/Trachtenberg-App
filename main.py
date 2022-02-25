# IMPORTS
# Plotting
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

# Kivy imports
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget


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








