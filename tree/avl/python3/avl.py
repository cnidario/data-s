class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = AVL()
        self.right = AVL()
        self.b = 0


class AVL:
    """Árbol AVL"""
    def __init__(self):
        self.node = None

    def empty(self):
        return self.node is None

    def height(self):
        if self.node is None:
            return 0
        else:
            return 1 + max(self.node.left.height(), self.node.right.height())

    def _simpleRotLeft(a_node, b_node):
        """Izqda a dcha"""
        a_new_node, b_new_node = b_node, a_node
        alpha = b_node.node.left
        beta = b_node.node.right
        gamma = a_node.node.right
        b_new_node.node, a_new_node.node = b_node.node, a_node.node
        b_new_node.node.left = alpha
        b_new_node.node.right = a_new_node
        a_new_node.node.left = beta
        a_new_node.node.right = gamma
        a_new_node.node.b = b_new_node.node.b = 0

    def _simpleRotRight(a_node, b_node):
        a_new_node, b_new_node = b_node, a_node
        alpha = a_node.node.left
        beta = b_node.node.left
        gamma = b_node.node.right
        b_new_node.node, a_new_node.node = b_node.node, a_node.node
        b_new_node.node.left = a_new_node
        b_new_node.node.right = gamma
        a_new_node.node.left = alpha
        a_new_node.node.right = beta
        a_new_node.node.b = b_new_node.node.b = 0

    def _doubleRotLeft(a_node, b_node, c_node):
        c_new_node, a_new_node, b_new_node = a_node, c_node, b_node
        beta = c_node.node.left
        gamma = c_node.node.right
        alpha = b_node.node.left
        delta = a_node.node.right
        izb = 0 if c_node.node.b == -1 or c_node.node.b == 0 else -1
        dcb = 0 if c_node.node.b ==  1 or c_node.node.b == 0 else  1
        a_new_node.node, b_new_node.node, c_new_node.node = a_node.node, b_node.node, c_node.node
        c_new_node.node.left = b_new_node
        c_new_node.node.right = a_new_node
        b_new_node.node.left, b_new_node.node.right = alpha, beta
        a_new_node.node.left, a_new_node.node.right = gamma, delta
        b_new_node.node.b = izb
        a_new_node.node.b = dcb
        c_new_node.node.b = 0

    def _doubleRotRight(a_node, b_node, c_node):
        c_new_node, a_new_node, b_new_node = a_node, c_node, b_node
        alpha = a_node.node.left
        delta = b_node.node.right
        beta = c_node.node.left
        gamma = c_node.node.right
        izb = 0 if c_node.node.b == -1 or c_node.node.b == 0 else -1
        dcb = 0 if c_node.node.b ==  1 or c_node.node.b == 0 else  1
        a_new_node.node, b_new_node.node, c_new_node.node = a_node.node, b_node.node, c_node.node
        c_new_node.node.left = a_new_node
        c_new_node.node.right = b_new_node
        b_new_node.node.left, b_new_node.node.right = gamma, delta
        a_new_node.node.left, a_new_node.node.right = alpha, beta
        a_new_node.node.b = izb
        b_new_node.node.b = dcb
        c_new_node.node.b = 0

    def find(self, key):
        path = []
        current = self
        
        while not current.empty():
            if key < current.node.key:
                path.append((current, -1))
                current = current.node.left
            elif key > current.node.key:
                path.append((current,  1))
                current = current.node.right
            else:
                break
        path.append((current, 0))
        return path
    
    def _chkB(self):
        if self.empty():
            return True
        else:
            res = self.node.b in {-1, 0, 1} and self.node.left._chkB() and self.node.right._chkB()
            #if not res:
            #   print("Failed with {}".format(self.node.b))
            return res

    def _updateBInsert(self, path):
        a_node_ix = None
        for i, a in reversed(list(enumerate(path))):
            n, position = a
            n.node.b += position
            if n.node.b in {-2, 2}: # desequilibrio
                a_node_ix = i
                break
            if n.node.b == 0: # asegura que no hay desequilibrio, conservación altura
                break
        return path[a_node_ix][0] if a_node_ix is not None else None

    def _updateBDelete(self, path):
        a_node_ix = None
        for i, a in reversed(list(enumerate(path))):
            n, position = a
            n.node.b -= position
            if n.node.b in {-2, 2}: # desequilibrio
                a_node_ix = i
                break
            if n.node.b in {-1, 1}: # asegura que no hay desequilibrio, conservación altura
                break
        return path[a_node_ix][0] if a_node_ix is not None else None

    def _rebalance(self, a_node):
        b_node = a_node.node.left if a_node.node.b < 0 else a_node.node.right
        if (a_node.node.b >= 0) ^ (b_node.node.b < 0): # mismo signo? -> rot simple
            if a_node.node.b < 0:
                AVL._simpleRotLeft(a_node, b_node)
            else:
                AVL._simpleRotRight(a_node, b_node)
        else:
            if a_node.node.b < 0:
                AVL._doubleRotLeft(a_node, b_node, b_node.node.right)
            else:
                AVL._doubleRotRight(a_node, b_node, b_node.node.left)

    def dump(self):
        if self.empty():
            print("* ", end='')
        else:
            print("{} [ ".format(self.node.key), end='')
            self.node.left.dump()
            print(", ", end='')
            self.node.right.dump()
            print(" ]", end='')

    def insert(self, key, data):
        ancestors = self.find(key)
        place, _ = ancestors.pop()
        if not place.empty(): # assert place.node.key == key
            place.node.data = data # se sobreescribe
            return
        place.node = AVLNode(key, data)

        a_node = self._updateBInsert(ancestors)

        if a_node is not None:
            self._rebalance(a_node)

    def max(self):
        if self.empty():
            return None
        else:
            res = self.node.right.max()
            return res if res is not None else self

    def min(self):
        if self.empty():
            return None
        else:
            res = self.node.left.min()
            return res if res is not None else self

    def maxPath(self):
        path = []
        current = self
        while not current.empty():
            path.append(current)
            current = current.node.right
        return path

    def isLeaf(self):
        return not self.empty() and self.node.left.empty() and self.node.right.empty()
    
    def isSemiLeaf(self):
        return not self.empty() and (self.node.left.empty() or self.node.right.empty())

    def delete(self, key):
        ancestors = self.find(key)
        place, _ = ancestors.pop()
        if place.empty(): # nada que borrar, no encontrado
            return
        
        if place.isLeaf():
            place.node = None
        elif place.isSemiLeaf():
            subtree = place.node.left if place.node.right.empty() else place.node.right
            place.node = subtree.node
        else:
            maxim_path = place.node.left.maxPath()
            maxim = maxim_path.pop()
            node = maxim.node
            if maxim.isLeaf():
                maxim.node = None
            else: # es semileaf
                maxim.node = maxim.node.left
            place.node.key = node.key
            place.node.data = node.data
            ancestors = maxim_path
            
        a_node = self._updateBDelete(ancestors)
        if a_node is not None:
            self._rebalance(a_node)

def check_binary_order(avl):
    if avl.node is None:
        return True
    elif avl.node.left.node is not None and avl.node.left.node.key > avl.node.key:
        return False
    elif avl.node.right.node is not None and avl.node.right.node.key < avl.node.key:
        return False
    else:
        return check_binary_order(avl.node.left) and check_binary_order(avl.node.right)

def check_avl_condition(avl):
    if avl.node is None:
        return True
    elif abs(avl.node.left.height() - avl.node.right.height()) <= 1:
        return check_avl_condition(avl.node.left) and check_avl_condition(avl.node.right)
    else:
        print("{} {} ".format(avl.node.left.height(), avl.node.right.height()))
        avl.dump()
        return False

def check_avl_balances(avl):
    if avl.node is None:
        return True
    else:
        height_left  = avl.node.left.height()
        height_right = avl.node.right.height()
        return avl.node.b == height_right - height_left and avl.node.b in {-1, 0, 1} and check_avl_balances(avl.node.left) and check_avl_balances(avl.node.right)

def avl_from_list(ls):
    avl = AVL()
    for i in ls:
        avl.insert(i, i)
    return avl

def insert(x, l):
    for i in range(0, len(l) + 1):
        yield l[:i] + [x] + l[i:]

def combinations(ls):
    """combinaciones de elementos, están todos los elementos en todos los órdenes posibles"""
    if len(ls) == 0:
        yield []
    else:
        x, xs = ls[0], ls[1:]
        for c in combinations(xs):
            for l in insert(x, list(c)):
                yield l

def selections(ls):
    """selecciones de elementos, el orden se mantiene, pero puede faltar cualquier combinacion de elementos"""
    if len(ls) == 0:
        yield []
    else:
        x, xs = ls[0], ls[1:]
        for s in selections(xs):
            yield [x] + s
            yield s

def test_inserts():
    cn = 0
    for c in combinations(list(range(0,25))):
        avl = avl_from_list(c)
        cn += 1
        tst1, tst2, tst3 = check_binary_order(avl), check_avl_condition(avl), check_avl_balances(avl)
        print("Combinación {} tests => bin {}, avl {}, bal {}".format(cn, tst1, tst2, tst3))
        if not(tst1 and tst2 and tst3):
            break

def avl_multi_delete(avl, deletes):
    for k in deletes:
        avl.delete(k)

def test_deletes():
    n = 12
    cn = 0
    for c in combinations(list(range(0,n))):
        avl = avl_from_list(c)
        cn += 1
        sn = 0
        for s in selections(list(range(0,n))):
            avl_multi_delete(avl, s)
            sn += 1
            tst1, tst2, tst3 = check_binary_order(avl), check_avl_condition(avl), check_avl_balances(avl)
            print("Combinación {} Selección {} tests => bin {}, avl {}, bal {}".format(cn, sn, tst1, tst2, tst3))
        if not(tst1 and tst2 and tst3):
            return

if __name__ == '__main__':
    test_deletes()
