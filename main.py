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
from kivy.properties import ObjectProperty

# Set background RGBA color - should be a nice gray ???
from kivy.core.window import Window
Window.clearcolor = (192/255, 187/255, 178/255, 1)

##### Custom functions
# Matplotlib UT-plotter
def prod_plotter(LHS, RHS, arrow_idx=None, rect_idx=0, background_color=(192/255, 187/255, 178/255, 1), foreground_color=(0,0,0), step_by_step=False, info=False):
    """Plots product of LHS and RHS, possibly with arrows to indicate 
    next move / an error

    Args:
        LHS (int): The product left hand side
        RHS (int): The product right hand side
        arrow_idx (int, optional): arrow index - from left to right. Defaults to None.
            None implies no arrows
        rect_idx (int, optional): rectangle index - from right to left. Defaults to 0.
            None implies no rectangle
    """
    
    # Create figure and set axis limits
    font_size = 22
    y_carry = 0.1
    if step_by_step:
        plt.figure(figsize=(3,4), facecolor=background_color)
        font_size = 15
    elif info:
        plt.figure(figsize=(4,4), facecolor=background_color)
        font_size = 15
        y_carry = 0.05
    else:
        plt.figure(figsize=(6,8), facecolor=background_color)
    plt.xlim((0,1))
    plt.ylim((0,1))
    plt.axis("off")

    # Convert left and right terms to strings and add spaces to the LHS equal to len(RHS)
    text2 = str(RHS)
    text1 = "0" * len(text2) + str(LHS)
    times = r"\times"

    # The desired answer
    answer = str(LHS * RHS)
    answer = "0" * (len(text1) - len(answer)) + answer
    
    # Get length of whole plotted string
    length = len(text1) + 1 + len(text2)

    # Get midpoint for x-axis and for y-axis
    x_half = y_half = 0.5

    # Generate indicies for the text to plot s.t. letters/numbers are evenly spaced and centered in the image
    dist = 0.1
    
    idxes = [x_half - dist * (length/2 - (i + 0.6)) for i in range(length)]

    # Plot LHS
    for i, t in enumerate(text1):
        plt.text(idxes[i], y_half, fr"${t}$", {"size":font_size}, ha="center", va="center", color=foreground_color)
        
    # Plot 'times' symbol
    plt.text(idxes[len(text1)], y_half, fr"${times}$", {"size":font_size}, ha="center", va="center", color=foreground_color)

    # Plot RHS
    for i, t in enumerate(text2):
        plt.text(idxes[i + 1 + len(text1)], y_half, fr"${t}$", {"size": font_size}, ha="center", va="center", color=foreground_color)
        
    # Underline for LHS product
    plt.plot([idxes[0] - 0.02, idxes[len(text1) - 1] + 0.02], [y_half - 0.075, y_half- 0.075], color=foreground_color)
        
    # Function for creating helper arrows
    def plot_arrows(idx1, idx2, height=0.35):
        """
        idx1: idxes for the LHS of the \times are in [0, len(text1)]
        idx2: idxes for the RHS of the \times are in [0, len(text2)]
        height: how far up to go (0.4, 0.3 and 0.2 are good choices)
        """
        m = 0.8
        
        plt.plot([idxes[idx1], idxes[idx2+len(text1)+1]], [y_half + height, y_half + height], color=foreground_color)
        plt.arrow(idxes[idx1], y_half + height, 0, 0.95 * (0.1 - height), length_includes_head=True, head_width=0.015, color=foreground_color)
        if (idx1 + 1) < len(text1):
            plt.arrow(idxes[idx1], y_half + height, m * (idxes[idx1+1] - idxes[idx1]), 0.96 * (0.1 - height), length_includes_head=True, head_width=0.015, color=foreground_color)

        plt.plot([idxes[idx2 + len(text1)+1], idxes[idx2 + len(text1)+1]],[y_half + 0.1, y_half + height], color=foreground_color)
        

    # Identifier reactangle
    if rect_idx != None and arrow_idx == None:
        rect = Rectangle((idxes[len(text1) - 1 - rect_idx] - 0.03, y_half - 0.27), 0.06, 0.17, facecolor="none", edgecolor=foreground_color, linewidth=2)
        plt.gca().add_patch(rect)

    # Plot answer up untill arrow_idx, plot the arrow_idx digit with bold
    # Plot arrows according to the arrow indexing
    if arrow_idx != None:
        carry = 0
        for i in range(len(text1) - arrow_idx):
            digit = carry
            for j in range(len(text2)):
                idx = len(text1) - i + j - 1
                if idx >= len(text1):
                    break
                mult_1 = str(eval(text1[idx]) * eval(text2[len(text2) - j - 1]))
                mult_1 = "0" + mult_1 if len(mult_1) == 1 else mult_1
                digit += eval(mult_1[1])
                if (idx + 1) >= len(text1):
                    break
                mult_2 = str(eval(text1[idx + 1]) * eval(text2[len(text2) - j - 1]))
                mult_2 = "0" + mult_2 if len(mult_2) == 1 else mult_2
                digit += eval(mult_2[0])
                
            digit = str(digit) if digit >= 10 else "0" + str(digit)
            plt.text(idxes[len(text1) - 1 - i], y_half - 0.2, fr"${digit[1]}$", {"size": font_size}, ha="center", va="center", color=foreground_color)
            
            # Plot carry dots
            if eval(digit[0]) == 1:
                plt.text(idxes[len(text1) - (i + 1)] - 0.03, 0.5 - y_carry, ".", {"size": 30}, ha="center", va="center", zorder=1, size=25, color=foreground_color)
                carry = 1
            elif eval(digit[0]) == 2:
                plt.text(idxes[len(text1) - (i + 1)] - 0.03, 0.5 - y_carry, ".", {"size": 30}, ha="center", va="center", zorder=1, size=25, color=foreground_color)
                plt.text(idxes[len(text1) - (i + 1)] + 0.005, 0.5 - y_carry, ".", {"size": 30}, ha="center", va="center", zorder=1, size=25, color=foreground_color)
                carry = 2
            else:
                carry = 0
            
        
        # for i, digit in enumerate(reversed(answer)):
        #     plt.text(idxes[len(text1) - 1 - i], y_half - 0.2, fr"${digit}$", {"size": font_size}, ha="center", va="center", color=foreground_color)
        
        for i in range(len(text2)):
            if (arrow_idx + i) >= len(text1):
                break
            plot_arrows(arrow_idx + i, len(text2) - i - 1, height=(0.35 - 0.075*i))

    # plt.show()
    return idxes


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

# UT-multiplication info page
# UT-multiplication rule explainer
class UTInfo(Widget):
    inter_plot = ObjectProperty(None)
    arrow_idx = 0
    
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.LHS = self.ids["LHS"]
        self.RHS = self.ids["RHS"]
        
        # The widget in which to plot stuff
        self.box = self.inter_plot

        self.plotter(self.LHS.text, self.RHS.text)
        
    def plotter(self, LHS, RHS):
        if not LHS:
            LHS = "0"
        if not RHS:
            RHS = "0"
            
        LHS = eval(LHS)
        RHS = eval(RHS)
            
        while self.arrow_idx > len(self.LHS.text + self.RHS.text):
            self.arrow_idx -= 1
        while self.arrow_idx < 0:
            self.arrow_idx += 1
            
        plt.close("all")
        _ = prod_plotter(LHS, RHS, self.arrow_idx, info=True)
        self.fig_widget = FigureCanvasKivyAgg(plt.gcf()) # , size_hint = (0.6, 0.6), pos_hint={"x": 0.2, "top": 0.75}
        self.box.add_widget(self.fig_widget)
        
    def inp_check(self):
        if self.LHS.text:
            self.LHS.text = str(self.LHS.text)[:3]
            self.LHS.text = self.LHS.text.lstrip("0")
        if self.RHS.text:
            self.RHS.text = str(self.RHS.text)[:3]
            self.RHS.text = self.RHS.text.lstrip("0")
            
        self.box.clear_widgets()
        plt.close("all")
        self.plotter(self.LHS.text, self.RHS.text)
        
    def incr_arrow_idx(self):
        self.arrow_idx += 1
        self.box.clear_widgets()
        plt.close("all")
        self.plotter(self.LHS.text, self.RHS.text)
    
    def decr_arrow_idx(self):
        self.arrow_idx -= 1
        self.box.clear_widgets()
        plt.close("all")
        self.plotter(self.LHS.text, self.RHS.text)

class UTInfoScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(UTInfo())
        





class Test(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        plt.text(0.5,0.5,"HEYO!!!")
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))


# Get `kv` file
# - the kivy file has same name is app class (minus the 'app' part and is thus loaded automatically)
# kv = Builder.load_file("my.kv")


# My app
class MyApp(App):
    pass
    # def build(self):
    #     # self.cont = UT_Mult()
    #     # return self.cont  
    #     return kv
    

# Run app
if __name__ == "__main__":    
    app = MyApp()
    app.run()








