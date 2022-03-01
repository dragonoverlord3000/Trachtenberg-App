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
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from kivy.properties import ObjectProperty

# Set background RGBA color - should be a nice gray ???
from kivy.core.window import Window
Window.clearcolor = (192/255, 187/255, 178/255, 1)

# Other imports
import random

# Global variables
LHS_global = [v for v in range(1,1000)]
random.shuffle(LHS_global)

RHS_easy = [v for v in range(1,20)]
random.shuffle(RHS_easy)

RHS_medium = [v for v in range(1,100)]
random.shuffle(RHS_medium)

RHS_hard = [v for v in range(1,1000)]
random.shuffle(RHS_hard)

RHS_global = [RHS_easy, RHS_medium, RHS_hard]

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

class UT_Mult(Widget):
    top = ObjectProperty(None)
    enter = ObjectProperty(None)
    
    # Random idx
    idx = 0
    
    def __init__(self, difficulty:int, RHS=None, **kwargs):
        super().__init__()
        plt.close()
                
        print("KWARGS", kwargs)
        self.difficulty = difficulty
        self.idx = self.idx % (1000 if self.difficulty == 2 else (100 if self.difficulty == 1 else 20))
                
        # Setting up the LHS and the RHS
        self.max_num = 1000
        if RHS:
            self.RHS = RHS
            self.input_RHS = True
            self.LHS = LHS_global[(self.idx + 80 * RHS) % self.max_num]
            
            self.float_lay = self.ids["float_lay"]
            btn = Button(text="Rule", pos_hint={"right": 0.5 + 0.175/2, "top": 0.99}, size_hint=(0.175,0.075), background_color=(0,0,1,3/4))
            btn.bind(on_press=self.show_rule)
            self.float_lay.add_widget(btn)
        else:
            self.RHS = RHS_global[difficulty][self.idx] # 0 is easy, 1 is medium, 2 is hard
            self.input_RHS = False
            self.LHS = LHS_global[(self.idx + 333 * difficulty) % self.max_num]
        # Setting up user answer + real answer
        self.number = ""
        self.answer = self.LHS * self.RHS

        # Store number of carry dots in array        
        self.carries = [0 for _ in range(len(str(self.LHS) + str(self.RHS)))]
        
        # For popup
        self.popup_idx = 0
        
        # Num btn presses
        self.num_btn_presses = 0
        
        # Initialize plot 
        self.CE()
    
    
    # [1-9] digits
    def btn(self, val):
        print(val)
        if self.num_btn_presses == 0:
            self.CE()
        self.num_btn_presses += 1
            
        if len(self.number) < len(str(self.LHS) + str(self.RHS)):
            self.number = str(val) + self.number
            self.plot_next_num(val)

    # Plots the number typed and moves identifier rectangle 
    def plot_next_num(self, val):
        self.top.clear_widgets()
        
        # Fill over rect 
        fill_rect = Rectangle((self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number)] - 0.035 - 0.01, 0.5 - 0.28), 0.07 + 0.02, 0.195, facecolor=(192/255, 187/255, 178/255, 1), edgecolor=(192/255, 187/255, 178/255, 1), linewidth=2, zorder=1)
        plt.gca().add_patch(fill_rect)
        
        # Plot 'val' 
        plt.text(self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number)] + 0.005, 0.5 - 0.2, str(val), {"size": 22}, ha="center", va="center", zorder=1)
        
        # Plot new rect 
        if len(self.number) <= len(str(self.LHS) + str(self.RHS)) - 1:
            rect = Rectangle((self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number) - 1] - 0.03, 0.5 - 0.27), 0.06, 0.17, facecolor="none", edgecolor="black", linewidth=2, zorder=1)
            plt.gca().add_patch(rect)
                
        # Plot new figure
        self.top.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    # Clear everything
    def CE(self, *args):
        print("CE")
        
        # Clear number
        self.number = ""
        # Clear carries
        self.carries = [0 for _ in range(len(str(self.LHS) + str(self.RHS)))]
        
        self.top.clear_widgets()
        self.idxes = prod_plotter(self.LHS, self.RHS)
        self.top.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    # Go back once
    def back(self): 
        # Only delete if there are any numbers to delete
        if len(self.number) > 0:
            self.top.clear_widgets()
            
            # Fill over identifier rect and former number
            fill_rect1 = Rectangle((self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number)] - 0.03 - 0.01, 0.5 - 0.28), 0.06 + 0.02, 0.195, facecolor=(192/255, 187/255, 178/255, 1), edgecolor=(192/255, 187/255, 178/255, 1), linewidth=2, zorder=1)
            fill_rect2 = Rectangle((self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number) - 1] - 0.03 - 0.01, 0.5 - 0.28), 0.06 + 0.02, 0.195, facecolor=(192/255, 187/255, 178/255, 1), edgecolor=(192/255, 187/255, 178/255, 1), linewidth=2, zorder=1)
            plt.gca().add_patch(fill_rect1)
            plt.gca().add_patch(fill_rect2)
        
            # Plot new identifier rect
            rect = Rectangle((self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number)] - 0.035, 0.5 - 0.27), 0.07, 0.17, facecolor="none", edgecolor="black", linewidth=2, zorder=1)
            plt.gca().add_patch(rect)
        
            # Reassign number
            self.number = self.number[1:]
            
            # Reassign carry
            self.carries[len(self.number)] = 0
            
            # Plot new figure
            self.top.add_widget(FigureCanvasKivyAgg(plt.gcf()))

            
    # Add dot, to symbol a carry
    def carry(self):
        if self.carries[len(self.number) - 1] < 2 and len(self.number) >= 1:
            print("Carry")
            
            # Clear current image
            self.top.clear_widgets()
            
            # Plot carry dots
            if int(self.carries[len(self.number) - 1]) == 0:
                plt.text(self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number)] - 0.02, 0.5 - 0.065, ".", {"size": 25}, ha="center", va="center", zorder=1, size=35)
            else:
                plt.text(self.idxes[len(str(self.LHS) + str(self.RHS)) - len(self.number)] + 0.005, 0.5 - 0.065, ".", {"size": 25}, ha="center", va="center", zorder=1, size=35)
            
            # Add 1 carry
            self.carries[len(self.number) - 1] += 1
            
            # Plot new figure
            self.top.add_widget(FigureCanvasKivyAgg(plt.gcf()))

            
    # Checks whether the current answer is the correct one
    def check_answer(self):
        if len(self.number) == 0:
            print(False)
            return False
                 
        non_zero_idx = 0
        for i, n in enumerate(self.number):
            if n != "0":
                non_zero_idx = i
                break
                
        print(f"The user answer is: {self.number}")
                
        # Answer by user
        check_number = eval(self.number[non_zero_idx:])    
        
        # Check if answer is correct
        if check_number == self.answer:
            print(True)            
            return True
        else:
            print(False)
            return False
         
    # Goes to next multiplication
    def next_mult(self):
        # Get current score
        # current_score = 0
        # with open("./score.txt", "r") as f:
        #     txt = f.read()
        #     if txt != "":
        #         current_score = eval(txt)
        # f.close()
        
        # # Add to score
        # with open("./score.txt", "w") as f:
        #     f.write(str(1 + current_score))
        # f.close()
        
        mod = 1000 if self.difficulty == 2 else (100 if self.difficulty == 1 else 20)
        self.idx = (self.idx + 1) % mod
        if self.input_RHS:
            self.__init__(self.difficulty, self.RHS)
        else:
            self.__init__(self.difficulty)
        
    # Function for creating explanation
    def explanation(self, arrow_idx):
        # Add label for step 1
        self.step_lab = Label(text=f"Step {self.popup_idx + 1}", size_hint = (0.6, 0.2), pos_hint={"x": 0.2, "top": 1}, font_size=30)
        self.box.add_widget(self.step_lab)
        
        # Add steps for calculating 
        answer = "0" * (len(str(self.LHS) + str(self.RHS)) - len(str(self.answer))) + str(self.answer)
        RHS_str = str(self.RHS)
        LHS_str = "0" * len(RHS_str) + str(self.LHS)
        
        # Plot steps ???
        # if self.input_RHS:
        #     if self.RHS == 2:
        #         explainer_str = explainer_func_2(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_2(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 3:
        #         explainer_str = explainer_func_3(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_3(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 4:
        #         explainer_str = explainer_func_4(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_4(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 5:
        #         explainer_str = explainer_func_5(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_5(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 6:
        #         explainer_str = explainer_func_6(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_6(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 7:
        #         explainer_str = explainer_func_7(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_7(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 8:
        #         explainer_str = explainer_func_8(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_8(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 9:
        #         explainer_str = explainer_func_9(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_9(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 11:
        #         explainer_str = explainer_func_11(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_11(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)
        #     elif self.RHS == 12:
        #         explainer_str = explainer_func_12(arrow_idx=arrow_idx, LHS_str=LHS_str, answer=answer)
        #         _ = prod_plotter_12(self.LHS, arrow_idx=arrow_idx, background_color=(40/255,40/255,40/255,1), foreground_color=(1,1,1), step_by_step=True)

        
        self.fig_widget = FigureCanvasKivyAgg(plt.gcf(), size_hint = (0.6, 0.6), pos_hint={"x": 0.2, "top": 0.75})
        self.box.add_widget(self.fig_widget)
        
        
        # Add to widget ???
        # self.lab = Label(text=explainer_str, size_hint = (0.6, 0.2), pos_hint={"x": 0.2, "top": 0.85}, markup=True)
        # self.box.add_widget(self.lab)

    # Go to next step in solution method
    def forward_popup(self, *args):
        self.popup_idx = self.popup_idx + 1
        self.main_pop.dismiss()
        plt.close()
        self.step_by_step()
        
    # Go to former step in solution method
    def backward_popup(self, *args):
        self.popup_idx = self.popup_idx - 1
        self.main_pop.dismiss()
        plt.close()
        self.step_by_step()

    # Popup index
    def set_popup_idx_to_zero(self, *args):
        self.popup_idx = 0

    #### Step by step solution ####
    def step_by_step(self):
        # Main box (should maybe be gridlayout with some number of rows -)
        self.box = FloatLayout()
        
        # Show explanation
        self.explanation(len(str(self.LHS) + str(self.RHS)) - 1 - self.popup_idx)
        
        # Button for going to next index
        if self.popup_idx < len(str(self.LHS) + str(self.RHS)) - 1:
            self.forward_btn = Button(text="F", size_hint=(0.1, 0.1), pos_hint={"x": 0.8, "top": 0.95})
            self.box.add_widget(self.forward_btn)
            
            # Forward button functionality
            self.forward_btn.bind(on_press=self.forward_popup)
            
        # Button for going to next index
        if self.popup_idx > 0:
            self.backward_btn = Button(text="B", size_hint=(0.1, 0.1), pos_hint={"x": 0.2, "top": 0.95})
            self.box.add_widget(self.backward_btn)
            
            # Forward button functionality
            self.backward_btn.bind(on_press=self.backward_popup)
            
        
        # Button for closing the popup
        self.popup_close_btn=Button(text="Close", size_hint=(0.7, 0.15), pos_hint={"x": 0.15, "y": 0.1})
        self.box.add_widget(self.popup_close_btn)
        
        # Creating the popup
        self.main_pop = Popup(title="Step-by-step solution",content=self.box,
            size_hint=(1,1),title_size=15)
        
        # Close button functionality
        self.popup_close_btn.bind(on_press=self.main_pop.dismiss)
        self.popup_close_btn.bind(on_press=self.set_popup_idx_to_zero)
        self.popup_close_btn.bind(on_press=self.CE)

        # Open popup window
        self.main_pop.open()
        
    def show_rule(self, *args, **kwargs):
        self.rule_box = FloatLayout()      
        
        # Explanation
        explanation = ""
        num = self.RHS
            
        fontsize = 18
            
        if num == 12:
            explanation = """[b]Double each number add it's neighbor[/b]\n"""
        elif num == 11:
            explanation = """[b]To each number add it's neighbor[/b]\n"""
        elif num == 9:
            explanation = """[i]First Digit[/i]: [b]subtract from 10[/b]\n\n2.)[i]Middle Digits[/i]: [b]Subtract the number from 9 and add the neighbor[/b]\n\n3.)[i]Last Digit[/i] [b]subtract 1 from the leftmost digit in the number[/b]"""
            fontsize = 15
        elif num == 8:
            explanation = """[i]First Digit[/i]: [b]subtract from 10 and double[/b]\n\n2.)[i]Middle Digits[/i]: [b]Subtract the number from 9 and double what you get, then add the neighbor[/b]\n\n3.)[i]Last Digit[/i] [b]subtract 2 from the leftmost digit in the number[/b]"""
            fontsize = 15
        elif num == 7:
            explanation = """[b]Double the number and add half the neighbor; add 5 if the number is odd. [/b]""" 
        elif num == 6:
            explanation = """[b]To each "number" add half the neighbor; plus 5 if "number" is odd.[/b]""" 
        elif num == 5:
            explanation = """[b]Half the neighbor; plus 5 if "number" is odd.[/b]""" 
        elif num == 4:
            explanation = """[i]First Digit[/i]: [b]subtract from 10[/b]\n\n2.)[i]Middle Digits[/i]: [b]Subtract the number from 9 and add half the neighbor; add 5 if the number is odd[/b]\n\n3.)[i]Last Digit[/i] [b]subtract 1 from half of the leftmost digit in the number[/b]"""
            fontsize = 15
        elif num == 3:
            explanation = """[i]First Digit[/i]: [b]subtract from 10 and double; Add 5 if the number is odd[/b]\n\n2.)[i]Middle Digits[/i]: [b]Subtract the number from 9 and double what you get, then add half the neighbor; add 5 if the number is odd[/b]\n\n3.)[i]Last Digit[/i] [b]subtract 2 from half of the leftmost digit in the number[/b]"""
            fontsize = 15
        elif num == 2:
            explanation = """[b]Double the number[/b]"""   

        # Add title
        title_lab = Label(text="Multiplication rule | " + (str(self.RHS) if self.input_RHS else "UT"), size_hint=(0.7, None), font_size=20, pos_hint={"x": 0.15, "y": 0.82})
        self.rule_box.add_widget(title_lab)
        
        # Add explanation
        if fontsize == 15:
            expl_lab = Label(text=explanation, markup=True, font_size=fontsize, size_hint=(0.8, None),  text_size=(self.width * 0.6, None), pos_hint={"x": 0.1, "y": 0.45})
        else:
            expl_lab = Label(text=explanation, markup=True, font_size=fontsize, size_hint=(0.8, None),  text_size=(self.width * 0.6, None), pos_hint={"x": 0.1, "y": 0.45}, halign="center")
        self.rule_box.add_widget(expl_lab)
        
        # Button for closing the popup
        self.popup_close_btn=Button(text="Close", size_hint=(0.65, 0.1), pos_hint={"x": 0.15, "y": 0.05})
        self.rule_box.add_widget(self.popup_close_btn)
        
        # Creating the popup
        self.main_pop = Popup(title="Multiplication rule | " + (str(self.RHS) if self.input_RHS else "UT"),content=self.rule_box,
            size_hint=(0.8,0.9),title_size=15)
        
        # Close button functionality
        self.popup_close_btn.bind(on_press=self.main_pop.dismiss)
        self.popup_close_btn.bind(on_press=self.set_popup_idx_to_zero)
        self.popup_close_btn.bind(on_press=self.CE)   
        
        # Open popup window
        self.main_pop.open()
        
        
    def clear_wid(self):
        self.idx = (self.idx + 1) % 20
        self.CE()
        self.num_btn_presses = 0
        plt.close("all")
        
    def go_back(self):
        app= App.get_running_app()
        if self.input_RHS:
            app.root.current = "OneTwelve"
        else:
            app.root.current = "mult"


class MultWindow(Screen):
    def go_to_hard(self):
        self.parent.current = "hard"
        MultHard().__init__()
        
    def go_to_med(self):
        self.parent.current = "medium"
        MultMed().__init__()
        
    def go_to_easy(self):
        self.parent.current = "easy"
        plt.close("all")
        MultEasy().__init__()


class MultHard(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(UT_Mult(2))

class MultMed(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(UT_Mult(1))

class MultEasy(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(UT_Mult(0))


# Info and rules
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








