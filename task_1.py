from __future__ import annotations

from abc import ABC, abstractmethod


class Command(ABC):
    """Абстрпктная команда"""

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class LightOnCommand(Command):
    """Конкретная команда для включения света"""

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_on()

    def undo(self):
        self.light.turn_off()


class LightOffCommand(Command):
    """Конкретная команда для выключения света"""

    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.turn_off()

    def undo(self):
        self.light.turn_on()


class Light:
    """Класс света"""

    def turn_on(self):
        print("Свет включен")

    def turn_off(self):
        print("Свет выключен")


class Invoker:
    """Класс выключателя света"""

    def __init__(self):
        self.command = None
        self.history = []

    def set_command(self, command):
        self.command = command

    def press_button(self):
        if self.command:
            self.command.execute()
            self.history.append(self.command)

    def press_undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()


if __name__ == '__main__':
    light = Light()
    light_on = LightOnCommand(light)
    light_off = LightOffCommand(light)

    invoker = Invoker()

    # Включаем свет
    invoker.set_command(light_on)
    invoker.press_button()

    # Выключаем свет
    invoker.set_command(light_off)
    invoker.press_button()

    # Отменяем последнее действие
    invoker.press_undo()
