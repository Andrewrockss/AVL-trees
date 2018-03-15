import random

class AVLNode:

    def __init__(self):

        self.key = None
        self.item = None
        self.left = None
        self.right = None
        self.height = -1

    def _recalc_height(self):
    
        self.height = 1 + max(self.left.height, self.right.height)

    def _rotate_left(self):
    
        right = self.right
        right.left, self.right = self, right.left

        self._recalc_height() # important that this is first
        right._recalc_height()

        return right

    def _rotate_right(self):

        left = self.left
        left.right, self.left = self, left.right

        self._recalc_height() # important that this is first
        left._recalc_height()

        return left

    def _check_and_fix_imbalance(self):
    
        self._recalc_height()
        balance = self.left.height - self.right.height

        if abs(balance) <= 1:
            # no imbalance, so no rotation
            return self
        elif balance == 2:
            # left subtree is higher
            left = self.left
            if left.left.height < left.right.height:
                self.left = left._rotate_left()
            return self._rotate_right()
        else: # balance == -2, right subtree is higher
            right = self.right
            if right.right.height < right.left.height:
                self.right = right._rotate_right()
            return self._rotate_left()

class AVLDict:

    def __init__(self):

        self.root = AVLNode()
        self.len = 0

    def _find_and_fix(self, key):

        def recursive_fix(node):
            if node.key is None:
                raise KeyError(key)
            elif key < node.key:
                node.left = recursive_fix(node.left)
            elif key > node.key:
                node.right = recursive_fix(node.right)

            return node._check_and_fix_imbalance()

        self.root = recursive_fix(self.root)

    def _find(self, key):

        node, parent = self.root, None

        while node.key is not None and node.key != key:
            if key < node.key:
                node, parent = node.left, node
            else:
                node, parent = node.right, node

        return node, parent

    def update(self, key, item):
    
        node, parent = self._find(key)

        if node.key is not None:
            node.item = item
            return

        self.len += 1
        node.key = key
        node.item = item
        node.left = AVLNode()
        node.right = AVLNode()
        node.height = 0
        
        self._find_and_fix(key)

    def get(self, key):
"
        node, _ = self._find(key)
        if node.key is None:
            return None
        else:
            return node.item

    def popitem(self, key):

        # first find the key
        node, parent = self._find(key)

        if node.key is None:
            raise KeyError(key)

        self.len -= 1

        if node.left.key is None:
            if parent is None:
                self.root = node.right
            elif key < parent.key:
                parent.left = node.right
            else:
                parent.right = node.right
            if parent is not None:
                self._find_and_fix(parent.key)
        else:
            
            max_node, max_parent = node.left, node
            while max_node.right.key is not None:
                max_node, max_parent = max_node.right, max_node

          
            node.key, node.item = max_node.key, max_node.item

           
            if max_node == max_parent.left:
                max_parent.left = max_node.left
            else:
                max_parent.right = max_node.left
            self._find_and_fix(max_parent.key)

    def items(self):
      
        out = []

        def rec_build(node):
            if node.key is None:
                return
            rec_build(node.left)
            out.append((node.key, node.item))
            rec_build(node.right)

        rec_build(self.root)
        return out

    def __len__(self):
        return self.len

    def __setitem__(self, key, item):
        self.update(key, item)

    def __getitem__(self, key):
        node, _ = self._find(key)
        if node.key is None:
            raise KeyError(key)
        else:
            return node.item

    def __delitem__(self, key):
        self.popitem(key)

    def __str__(self):
        return str(self.items())

    def ith_key(self, index: int):
        pass


if __name__ == "__main__":
    tree = AVLDict()
    
    for i in range(15):
        tree[i] = i
        
    print(tree.items())
