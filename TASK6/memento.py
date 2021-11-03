from copy import deepcopy


class Memento:

    def __init__(self, state: int, lst: list):
        self.state = state
        self.container_memory = deepcopy(lst)


class Originator:

    def __init__(self, container: list):
        self.state = 0
        self.container = container

    def take_memento(self):
        mem = Memento(self.state, self.container)
        self.state += 1
        return mem

    def set_memento(self, memento: Memento):
        self.state = memento.state
        self.container.clear()
        self.container.extend(memento.container_memory)


class Caretaker:
    max_undo = 10

    def __init__(self, container: list):
        self.originator = Originator(container)
        self.prev = []
        self.curr = []
        self.next = []

    def memorize(self):
        mem = self.originator.take_memento()
        if len(self.curr) == 1:
            self.prev.append(self.curr.pop())
            if isinstance(self.max_undo, int) and len(self.prev) > self.max_undo:
                self.prev.pop(0)
        self.curr.append(mem)
        self.next.clear()

    def undo(self):
        if len(self.prev) == 0:
            raise IndexError
        else:
            self.next.append(self.curr.pop())
            self.curr.append(self.prev.pop())
            self.originator.set_memento(self.curr[0])

    def redo(self):
        if len(self.next) == 0:
            raise IndexError
        else:
            self.prev.append(self.curr.pop())
            self.curr.append(self.next.pop())
            self.originator.set_memento(self.curr[0])
