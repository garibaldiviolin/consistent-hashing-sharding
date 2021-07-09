class StorageNode:
    def __init__(self, name=None, host=None):
        self.name = name
        self.host = host


servers = [
    StorageNode(name='A', host='localhost:3000'),
    StorageNode(name='B', host='localhost:3001'),
    StorageNode(name='C', host='localhost:3002'),
    StorageNode(name='D', host='localhost:3003'),
    StorageNode(name='E', host='localhost:3004'),
]
