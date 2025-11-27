class StationNode:
    def __init__(self, name, data):
        self.name = name
        self.data = data   # liste de mesures météo (Station)
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, name, data):
        new_node = StationNode(name, data)

        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def get_names(self):
        names = []
        current = self.head
        while current:
            names.append(current.name)
            current = current.next
        return names
