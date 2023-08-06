class Module:
    def __init__(self, aliases : dict, canClose: bool, id: str, name : str, numDrives: int, source: str, state: str, targetName: str, type: str):
        self.aliases = aliases
        self.canClose = canClose
        self.id = id
        self.name = name
        self.source = source
        self.state = state
        self.targetName = targetName
        self.type = type

    def __str__(self):
        return f'Module(id={self.id}, name={self.name}, state={self.state}, type={self.type})'
    
    def __repr__(self):
        return self.__str__()