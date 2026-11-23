"""S-Calculator Kivy Android application: responsive v1.1 interface."""
from __future__ import annotations

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from calculator import CalculatorError, calculate

BACKGROUND = (0.055, 0.075, 0.12, 1)
PANEL = (0.105, 0.135, 0.20, 1)
NUMBER = (0.16, 0.20, 0.29, 1)
ACCENT = (0.25, 0.80, 0.76, 1)
OPERATION = (0.28, 0.38, 0.57, 1)
TEXT = (0.94, 0.96, 1.0, 1)
MUTED = (0.65, 0.72, 0.82, 1)

# A conservative Android navigation-gesture inset. This keeps the last row
# accessible on devices where Kivy draws beneath system navigation controls.
BOTTOM_INSET = dp(52)

KEYS = [
    ['AC', 'DEL', '(', ')'],
    ['√', '%', '÷', '×'],
    ['7', '8', '9', '−'],
    ['4', '5', '6', '+'],
    ['1', '2', '3', '±'],
    ['0', '.', 'C', '='],
]


class CalculatorApp(App):
    title = 'S-Calculator'

    def build(self):
        Window.clearcolor = BACKGROUND
        self.expression = ''
        self.history: list[str] = []
        root = BoxLayout(
            orientation='vertical',
            padding=[dp(14), dp(8), dp(14), BOTTOM_INSET],
            spacing=dp(6),
        )
        heading = Label(
            text='S-CALCULATOR', color=ACCENT, bold=True,
            font_size=sp(16), size_hint_y=None, height=dp(32),
            halign='center', valign='middle',
        )
        heading.bind(size=lambda obj, size: setattr(obj, 'text_size', size))
        root.add_widget(heading)

        self.display = Label(
            text='0', color=TEXT, font_size=sp(38),
            halign='right', valign='middle', shorten=True,
            shorten_from='left', size_hint_y=0.23,
        )
        self.display.bind(size=lambda obj, size: setattr(
            obj, 'text_size', (max(0, size[0] - dp(12)), size[1])))
        root.add_widget(self.display)

        self.status = Label(
            text='Offline • Ready', color=MUTED, font_size=sp(12),
            halign='right', valign='middle',
            size_hint_y=None, height=dp(22),
        )
        self.status.bind(size=lambda obj, size: setattr(obj, 'text_size', size))
        root.add_widget(self.status)

        history_header = Label(
            text='HISTORY', color=MUTED, font_size=sp(12),
            size_hint_y=None, height=dp(22), halign='left',
        )
        history_header.bind(size=lambda obj, size: setattr(obj, 'text_size', size))
        root.add_widget(history_header)

        scroll = ScrollView(size_hint_y=0.13, do_scroll_x=False)
        self.history_label = Label(
            text='No calculations yet', color=MUTED, font_size=sp(13),
            halign='right', valign='top', size_hint_y=None,
            markup=False,
        )
        self.history_label.bind(
            texture_size=lambda obj, size: setattr(
                obj, 'height', max(dp(48), size[1] + dp(8))))
        self.history_label.bind(
            width=lambda obj, width: setattr(
                obj, 'text_size', (max(0, width - dp(8)), None)))
        scroll.add_widget(self.history_label)
        root.add_widget(scroll)

        grid = GridLayout(cols=4, rows=6, spacing=dp(6), size_hint_y=0.64)
        for row in KEYS:
            for key in row:
                bg = (ACCENT if key == '=' else
                      OPERATION if key in ('÷', '×', '−', '+', '√', '%') else
                      PANEL if key in ('AC', 'C', 'DEL', '±') else NUMBER)
                button = Button(
                    text=key, background_normal='', background_down='',
                    background_color=bg,
                    color=BACKGROUND if key == '=' else TEXT,
                    bold=key == '=', font_size=sp(19),
                )
                button.bind(on_release=lambda _button, value=key: self.press(value))
                grid.add_widget(button)
        root.add_widget(grid)
        return root

    def press(self, key: str):
        if key in ('AC', 'C'):
            self.expression = ''
            self.status.text = 'Cleared'
        elif key == 'DEL':
            self.expression = self.expression[:-1]
            self.status.text = 'Ready'
        elif key == '±':
            if self.expression:
                candidate = (
                    self.expression[1:] if self.expression.startswith('-')
                    and self.expression.count('(') == self.expression.count(')')
                    and self.expression[1:].replace('.', '', 1).isdigit()
                    else f'-({self.expression})'
                )
                if len(candidate) <= 512:
                    self.expression = candidate
                    self.status.text = 'Ready'
                else:
                    self.status.text = 'Expression is too long'
        elif key == '=':
            if not self.expression:
                return
            try:
                result = calculate(self.expression)
            except CalculatorError as exc:
                self.status.text = str(exc)
                return
            self.history.append(f'{self.expression} = {result}')
            self.history = self.history[-20:]
            self.history_label.text = '\n'.join(reversed(self.history))
            self.expression = result
            self.status.text = 'Calculated offline'
        else:
            char = {'÷': '/', '×': '*', '−': '-'}.get(key, key)
            if len(self.expression) + len(char) <= 512:
                self.expression += char
                self.status.text = 'Ready'
            else:
                self.status.text = 'Expression is too long'
        self.display.text = self.expression or '0'


if __name__ == '__main__':
    CalculatorApp().run()
