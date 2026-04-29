from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

# Full Screen حقيقي
Window.clearcolor = (0.08, 0.08, 0.08, 1)

KV = '''
MDScreen:
    md_bg_color: 0.08, 0.08, 0.08, 1

    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(10)
        padding: 0

        MDLabel:
            id: status_label
            text: "Turn: X"
            halign: "center"
            font_style: "H5"
            size_hint_y: 0.1

        GridLayout:
            id: grid
            cols: 3
            spacing: dp(8)
            size_hint_y: 0.8

        MDRaisedButton:
            text: "Restart"
            size_hint_y: 0.1
            on_release: app.restart_game()
'''

class TicTacToe(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.current = "X"
        self.buttons = []

        for i in range(9):
            btn = MDRaisedButton(
                text="",
                font_size="36sp",
                size_hint=(1, 1),
                on_release=self.on_click
            )
            self.buttons.append(btn)
            self.add_widget(btn)

    def on_click(self, instance):
        if instance.text == "":
            instance.text = self.current

            if self.check_winner():
                App.get_running_app().root.ids.status_label.text = f"{self.current} wins!"
                self.disable_all()
            elif all(btn.text != "" for btn in self.buttons):
                App.get_running_app().root.ids.status_label.text = "Draw!"
            else:
                self.current = "O" if self.current == "X" else "X"
                App.get_running_app().root.ids.status_label.text = f"Turn: {self.current}"

    def check_winner(self):
        combos = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for c in combos:
            if self.buttons[c[0]].text == self.buttons[c[1]].text == self.buttons[c[2]].text != "":
                return True
        return False

    def disable_all(self):
        for btn in self.buttons:
            btn.disabled = True

    def reset(self):
        self.current = "X"
        for btn in self.buttons:
            btn.text = ""
            btn.disabled = False

class XOApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # يمنع الخلفية البيضاء
        screen = Builder.load_string(KV)
        self.game = TicTacToe()
        screen.ids.grid.add_widget(self.game)
        return screen

    def restart_game(self):
        self.game.reset()
        self.root.ids.status_label.text = "Turn: X"

if __name__ == "__main__":
    XOApp().run()