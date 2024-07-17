import sys


class PrintLogCapture:
    # To capture print statements and write them to both the terminal and a log file.
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
    """Flushes the buffers of both the terminal and the log file. """

    def isatty(self):
        return False

    """ Returns False as this is not an interactive terminal."""