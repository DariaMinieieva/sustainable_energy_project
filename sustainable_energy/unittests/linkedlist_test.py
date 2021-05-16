from unittest import TestCase
from map_creator.linkedlist import LinkedList, Node


class test_linkedlist(TestCase):
    def setUp(self):
        self.lst = LinkedList(1)
        self.lst.add(Node(2))
        self.lst.add(Node(3))

    def test_add(self):
        self.assertTrue(self.lst[1].data == 2)
        self.assertTrue(self.lst[2].data == 3)

    def test_pop(self):
        self.assertTrue(len(self.lst) == 2)
        self.assertTrue(len(self.lst) == 1)

    def test_remove(self):
        self.lst.remove(1)
        self.assertTrue(self.lst[1].data == 3)
