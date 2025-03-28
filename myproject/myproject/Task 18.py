##Task 1
class Node:
    def __init__(self, data):
        self.data=data
        self.left=None
        self.right=None

def printLeafNodes(key):

    if key.left is None and key.right is None:
        result=key.data
        print(result)
        return

    if key.right:
        printLeafNodes(key.right)
    if key.left:
        printLeafNodes(key.left)

def countEdges(key):
    count=0

    if key is None:
        return 0

    if key.left:
        count=count+1+countEdges(key.left)

    if key.right:
        count=count+1+countEdges(key.right)

    return count




data = Node(10)
data.left = Node(20)
data.right = Node(35)
data.left.left = Node(54)
data.left.right = Node(5)
data.right.right = Node(9)
data.left.left.left = Node(-30)

print(printLeafNodes(data))
print(countEdges(data))