from Node import Node
from hashlib import sha256
from copy import deepcopy


class MerkleTree:

    def __init__(self, size):
        self.root = None
        self.size = size
        self.file_list = None

    # create a merkle tree from the bottom to the top
    def create_tree(self, file_list):
        self.file_list = file_list
        count = len(file_list)  # nodes count for current layer
        leaves = []
        for i in range(0, count):
            data = sha256(file_list[i]).digest()
            leaf = Node(data)
            leaf.children.append(i)
            leaves.append(leaf)
        last_layer = deepcopy(leaves)
        while count > 1:
            current_layer = []
            for i in range(0, count // 2):
                data = sha256(last_layer[2 * i].data + last_layer[2 * i + 1].data).digest()
                node = Node(data)
                node.children = last_layer[2 * i].children + last_layer[2 * i + 1].children
                node.left = last_layer[2 * i]
                last_layer[2 * i].parent = node
                node.right = last_layer[2 * i + 1]
                last_layer[2 * i + 1].parent = node
                current_layer.append(node)
            if count % 2 == 1:  # there will be a node without sibling
                data = sha256(last_layer[-1].data).digest()
                node = Node(data)
                node.children = last_layer[-1].children
                node.left = last_layer[-1]
                last_layer[-1].parent = node
                current_layer.append(node)
            last_layer = current_layer
            count = count // 2 + count % 2
        self.root = last_layer[0]
        return self.root

    def read_file(self, i):
        assert i in self.root.children
        sibling_list = []
        current_node = self.root
        while len(current_node.children) > 1:  # before reaching the end
            if i in current_node.left.children:
                sibling_list.append(current_node.right.data)
                current_node = current_node.left
            else:
                sibling_list.append(current_node.left.data)
                current_node = current_node.right
        return self.file_list[i], sibling_list

    def check_integrity(self, i, file, sibling_list):
        current = sha256(file).digest()
        for h in reversed(sibling_list):  # h is the abbreviation of hash
            if i % 2 == 1:  # right child
                current = sha256(h + current).digest()
            else:  # left child
                current = sha256(current + h).digest()
            i //= 2
        return current == self.root.data

    def write_file(self, file, i):
        assert i in self.root.children
        self.file_list[i] = file
        current_node = self.root
        while len(current_node.children) > 1:
            if i in current_node.left.children:
                current_node = current_node.left
            else:
                current_node = current_node.right
        current_node.data = sha256(file).digest()
        while len(current_node.children) < self.size:  # before reaching the root
            if i % 2 == 1:  # right child
                current_node.parent.data = sha256(current_node.parent.left.data + current_node.data).digest()
            else:  # left child
                current_node.parent.data = sha256(current_node.data + current_node.parent.right.data).digest()
            i //= 2
            current_node = current_node.parent


if __name__ == '__main__':
    from os import urandom
    from random import randint

    max_length = 1024  # max file length

    def generate_file_list(list_size):
        file_list = []
        for i in range(0, list_size):
            file_list.append(urandom(randint(0, max_length)))
        return file_list


    # problem 2
    def test_merkle_tree():
        n = 32
        times = 10
        # create tree
        file_list = generate_file_list(n)
        tree = MerkleTree(n)
        tree.create_tree(file_list)

        for t in range(0, times):
            # check integrity
            pos = randint(0, n - 1)
            file, sibling_list = tree.read_file(pos)
            integrity = tree.check_integrity(pos, file_list[pos], sibling_list)
            assert file_list[pos] == file and integrity
            pos = randint(0, n - 1)
            while file == file[pos]:
                file = urandom(randint(0, max_length))
            read_file, sibling_list = tree.read_file(pos)
            integrity = tree.check_integrity(pos, file, sibling_list)
            assert not integrity

            # write file
            pos = randint(0, n - 1)
            new_file = urandom(randint(0, max_length))
            tree.write_file(new_file, pos)
            read_file, sibling_list = tree.read_file(pos)
            integrity = tree.check_integrity(pos, new_file, sibling_list)
            assert new_file == read_file and integrity


    test_merkle_tree()
