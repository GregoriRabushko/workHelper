from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class MyApp(App):
    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        self.input_name = TextInput(
            hint_text="Введите имя",
            multiline=False
        )

        button = Button(
            text="Отправить"
        )

        self.label = Label(
            text=""
        )

        button.bind(on_press=self.show_name)

        layout.add_widget(self.input_name)
        layout.add_widget(button)
        layout.add_widget(self.label)

        return layout

    def show_name(self, instance):
        name = self.input_name.text

        self.label.text = f"Привет, {name}!"


MyApp().run()