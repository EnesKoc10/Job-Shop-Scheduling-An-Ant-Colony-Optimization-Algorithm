class Machine:
    def __init__(self, machine_id, max_operations):
        self.__machine_id = machine_id
        self.__is_working = False
        self.__operations_done = []
        self.__processed_operations = []
        self.__max_operations = max_operations