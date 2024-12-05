import sys
import time
import itertools
from colorama import Fore, Style, init

init(autoreset=True)

class LoadingBar:
    def __init__(self, total, prefix="", length=30, fill="█", color=Fore.CYAN):
        """
        Initialize the loading bar.

        :param total: Total steps for completion.
        :param prefix: Text to display before the loading bar.
        :param length: Length of the loading bar (number of characters).
        :param fill: Character used to fill the bar.
        :param color: Color of the bar (using colorama Fore.*).
        """
        self.total = total
        self.prefix = prefix
        self.length = length
        self.fill = fill
        self.color = color
        self.current = 0
        self.spinner = itertools.cycle(["-", "\\", "|", "/"])
    
    def setTotal(self, total):
        self.total = total

    def update(self, progress):
        """
        Update the progress of the bar.

        :param progress: Current progress (integer).
        """
        self.current = progress
        percent = self.current / self.total
        filled_length = int(self.length * percent)
        bar = self.fill * filled_length + "-" * (self.length - filled_length)
        spinner_char = next(self.spinner)
        sys.stdout.write(
            f"\r{self.color}{self.prefix} [{bar}] {percent * 100:6.2f}% {spinner_char} - ({progress}/{self.total})"
        )
        sys.stdout.flush()

    def finish(self):
        """
        Mark the loading bar as complete.
        """
        self.update(self.total)
        print(f"\n{Fore.GREEN}Completed!")

def demo_loading_bar():
    total_steps = 100
    bar = LoadingBar(total_steps, prefix="Processing", length=40, color=Fore.MAGENTA)
    for i in range(total_steps + 1):
        bar.update(i)
        time.sleep(0.05)  
    bar.finish()
