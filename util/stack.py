class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def __len__(self):
        return self.length

    def add_to_head(self, value):
        if self.head:
            self.head = Node(value, self.head)
        else:
            self.head = Node(value)
        self.length += 1

    def remove_from_head(self, value):
        if self.head:
            return_value = self.head.value
            self.head = self.head.next_node
            self.length -= 1
            return return_value
        else:
            return None


class Stack:
    def __init__(self):
        self.storage = LinkedList()

    def __len__(self):
        return len(self.storage)

    def check(self):
        return self.storage.head.value

    def push(self, value):
        self.storage.add_to_head(value)

    def pop(self):
        return self.storage.remove_from_head()
