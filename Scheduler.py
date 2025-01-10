import sys

from colorama import init
from termcolor import colored


class Scheduler:

    def __init__(self, machines, max_operations, jobs):
        init()  # Init colorama for color display
        self.__original_stdout = sys.stdout
        self.__machines = machines
        self.__jobs_to_be_done = jobs
        self.__jobs_done = []
        self.__max_operations = max_operations