import sys
from abc import ABC, abstractmethod

class SystemsManager():
    instance = None
    
    def __init__(self):        
        self._systemses = {}
        SystemsManager.instance = self
        
        # Получаем все загруженные модули
        all_modules = sys.modules.values()

        # Собираем все классы из всех модулей
        all_classes = []
        for module in all_modules:
            if hasattr(module, "__dict__"):
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type):
                        all_classes.append(obj)

        # Фильтруем классы, которые наследуются от BaseClass
        subclasses = [cls for cls in all_classes if issubclass(cls, SystemBase) and cls != SystemBase]
        
        for system_class in subclasses:
            self._systemses[system_class.__class__.__name__] = system_class()
        
        
    def reg_system(self, system):
        self._systemses[system.__class__.__name__] = system
        
    async def execute_systems(self):
        for system_name, system in self._systemses.items():
            if system.enbled:
               await system.execute()



class SystemBase(ABC):
    def __init__(self):
        super().__init__()
        
        self.enbled = True

    @abstractmethod
    async def create(self):
        pass
    
    @abstractmethod
    def execute(self):
        pass

class SimplePrintSystem(SystemBase):
    
    async def create(self):
        pass
    
    async def execute(self):
        print(f"simple print")
        self.enbled = False