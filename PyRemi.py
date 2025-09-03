import remi.gui as gui
from remi import start, App

class MyApp(App):

    def main(self):
        container = gui.VBox(width=320, height=200)
        gui.grid()
        # Create a button, with the label "Hello, World!"

        self.lab = gui.Label("Welcome")
        # self.txt = gui.Input
        self.txt = gui.TextInput("Number")
        self.bt = gui.Button('Hello')
        self.bt.onclick.do(self.on_button_pressed)
        # Add the button to the container, and return it.
        container.append(self.lab)
        container.append(self.txt)
        container.append(self.bt)

        return container

    def on_button_pressed(self, widget):

        no = self.txt.get_value()
        self.bt.set_text('Hello, World!' + no)



start(MyApp)