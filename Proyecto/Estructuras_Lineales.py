from collections import deque


class Pila:
    def __init__(self):
        self.elementos = []

    def push(self, item):
        self.elementos.append(item)

    def pop(self):
        if self.esta_vacia():
            return None
        return self.elementos.pop()

    def esta_vacia(self):
        return len(self.elementos) == 0


class Cola:
    def __init__(self):
        self.elementos = deque()

    def enqueue(self, item):
        self.elementos.append(item)

    def dequeue(self):
        if self.esta_vacia():
            return None
        return self.elementos.popleft()

    def esta_vacia(self):
        return len(self.elementos) == 0
