import os
import sys
import threading
import time
import unicodedata
from contextlib import contextmanager
from typing import Generator


@contextmanager
def spin(message: str) -> Generator[None, None, None]:
    spin_cursor = SpinCursor(msg=message)
    spin_cursor.start()
    try:
        yield
    finally:
        spin_cursor.stop()


class SpinCursor(threading.Thread):
    """ A console spin cursor class """

    def __init__(self, msg: str = '', maxspin: int = 0, minspin: int = 10, speed: int = 5) -> None:
        # Count of a spin
        self.count: int = 0
        self.out = sys.stdout
        self.flag: bool = False
        self.max: int = maxspin
        self.min: int = minspin
        # Any message to print first ?
        self.msg: str = msg
        # Complete printed string
        self.string: str = ''
        # Speed is given as number of spins a second
        # Use it to calculate spin wait time
        self.waittime: float = 1.0 / float(speed * 4)
        if os.name == 'posix':
            self.spinchars: tuple = (unicodedata.lookup('FIGURE DASH'), '\\ ', '| ', '/ ')
        else:
            # The unicode dash character does not show
            # up properly in Windows console.
            self.spinchars = ('-', '\\ ', '| ', '/ ')
        threading.Thread.__init__(self, None, None, "Spin Thread")

    def spin(self) -> None:
        """ Perform a single spin """

        for x in self.spinchars:
            self.string = f"{self.msg}...\t{x}\r"
            self.out.write(self.string)
            self.out.flush()
            time.sleep(self.waittime)

    def run(self) -> None:

        while not self.flag:
            self.spin()
            self.count += 1

        # Clean up display...
        self.out.write(f"{' ' * (len(self.string) + 1)}")

    def stop(self) -> None:
        self.flag = True
        if self.is_alive():
            self.join()
