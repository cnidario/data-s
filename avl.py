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
        pass
    def _simpleRotRight(a_node, b_node):
        pass
    def _doubleRotLeft(a_node, b_node, c_node):
        pass
    def _doubleRotRight(a_node, b_node, c_node):
        pass

    def insert(self, key, data):
        ancestors = []
        current = self

        # búsqueda del punto de inserción
        while not current.empty():
            if key < current.node.key:
                ancestors.append((current, -1))
                current = current.node.left
            else:
                ancestors.append((current,  1))
                current = current.node.right

        ancestors.append((current, 0))  # caso especial doble rotación de un C insertado como hoja
        # inserción propiamente
        current.node = AVLNode(key, data)

        # actualizar factores de equilibrio b
        a_node_ix = None
        for i, a in reversed(list(enumerate(ancestors))):
            n, position = a
            if position == 0:
                continue
            if n.node.b == position:
                a_node_ix = i
                break
            n.node.b += position
            if n.node.b == 0:
                break

        # reequilibrar
        if a_node_ix is not None:
            a_node, a_position = ancestors[a_node_ix]
            b_node, b_position = ancestors[a_node_ix + 1]
            if a_position == b_position:
                # rotación simple
                a_new_node = b_node
                b_new_node = a_node
                b_new_node.node.b = a_new_node.node.b = 0
                if a_position == -1:
                    # de izqda a dcha
                    alpha = b_node.node.left
                    beta = b_node.node.right
                    gamma = a_node.node.right
                    b_new_node.node, a_new_node.node = b_node.node, a_node.node
                    b_new_node.node.left = alpha
                    b_new_node.node.right = a_new_node
                    a_new_node.node.left = beta
                    a_new_node.node.right = gamma
                else:
                    # dcha a izqda
                    alpha = a_node.node.left
                    beta = b_node.node.left
                    gamma = b_node.node.right
                    b_new_node.node, a_new_node.node = b_node.node, a_node.node
                    b_new_node.node.left = a_new_node
                    b_new_node.node.right = gamma
                    a_new_node.node.left = alpha
                    a_new_node.node.right = beta
            else:
                # rotación doble
                c_node, c_position = ancestors[a_node_ix + 2]
                c_new_node = a_node
                a_new_node = c_node
                b_new_node = b_node
                beta = c_node.node.left
                gamma = c_node.node.right
                c_node.node.b = 0
                if a_position == -1:
                    # izqda a dcha
                    alpha = b_node.node.left
                    delta = a_node.node.right
                    a_new_node.node, b_new_node.node, c_new_node.node = a_node.node, b_node.node, c_node.node
                    c_new_node.node.left = b_new_node
                    c_new_node.node.right = a_new_node
                    b_new_node.node.left, b_new_node.node.right = alpha, beta
                    a_new_node.node.left, a_new_node.node.right = gamma, delta
                    b_new_node.node.b = 0 if c_position == -1 or c_position == 0 else -1
                    a_new_node.node.b = 0 if c_position ==  1 or c_position == 0 else  1
                else:
                    # dcha a izqda
                    alpha = a_node.node.left
                    delta = b_node.node.right
                    a_new_node.node, b_new_node.node, c_new_node.node = a_node.node, b_node.node, c_node.node
                    c_new_node.node.left = a_new_node
                    c_new_node.node.right = b_new_node
                    b_new_node.node.left, b_new_node.node.right = gamma, delta
                    a_new_node.node.left, a_new_node.node.right = alpha, beta
                    a_new_node.node.b = 0 if c_position == -1 or c_position == 0 else -1
                    b_new_node.node.b = 0 if c_position ==  1 or c_position == 0 else  1


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

def check_avl_balances(avl):
    if avl.node is None:
        return True
    else:
        height_left  = avl.node.left.height()
        height_right = avl.node.right.height()
        return avl.node.b == height_right - height_left and check_avl_balances(avl.node.left) and check_avl_balances(avl.node.right)

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

if __name__ == '__main__':
    cn = 0
    for c in combinations(list(range(0,25))):
        avl = avl_from_list(c)
        cn += 1
        tst1, tst2, tst3 = check_binary_order(avl), check_avl_condition(avl), check_avl_balances(avl)
        print("Combinación {} tests => bin {}, avl {}, bal {}".format(cn, tst1, tst2, tst3))
        if not(tst1 and tst2 and tst3):
            break