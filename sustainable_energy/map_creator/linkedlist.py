"""Linked list implementation"""


class Node:
    """Linked list node"""

    def __init__(self, data) -> None:
        self.data = data
        self.next = None

    def __str__(self):
        return f"{self.data}"


class LinkedList:
    def __init__(self, head: Node = None):
        self._head = head

    def __len__(self):
        if self._head is None:
            return 0

        length = 1
        currentItem = self._head
        while currentItem.next is not None:
            length += 1
            currentItem = currentItem.next

        return length

    def __getitem__(self, index: int):
        currentItem = self._head
        for i in range(index):
            currentItem = currentItem.next

        return currentItem

    def __iter__(self):
        return LinkedIterator(self)

    def add(self, data):
        """Adds element to the end of the list"""
        if self._head is None:
            self._head = Node(data)
        else:
            head = self._head
            self._head = Node(data)
            self._head.next = head

    def pop(self):
        """Removes element from the end of the list"""
        self._head = self._head.next

    def remove(self, index):
        """Removes element with index"""
        if index == len(self) - 1:
            self.pop()
        else:
            self[index-1].next = self[index+1]


class LinkedIterator:
    def __init__(self, lst):
        self.lst = lst
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.lst):
            data = self.lst[len(self.lst) - self.index - 1]
            self.index += 1
            return data
        else:
            raise StopIteration
