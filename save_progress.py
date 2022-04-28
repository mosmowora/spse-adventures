from dataclasses import dataclass
from typing import Any, List
import json

@dataclass
class SaveProgress:
    name: str
    inventory: List[str]
    quests: List[str]
    file_dest: str = "Database/progress.json"
    data: List[dict[str, Any]] = []
    
    #   ↑     ↑       ↑        ↑          ↑
    # def __init__(self, name: str, inventory: List[str], quests: List[str], file_dest: str = "Database/progress.json"):
    #     self.name = name
    #     self.inventory = inventory
    #     self.quests = quests
    #     self.file_dest = file_dest
    
    
    @staticmethod
    def load_data():
        """
        Isn't finished
        """
        if len(SaveProgress.data) != 1:
            with open(SaveProgress.file_dest) as file:
                content = file.read()
                print(content)
            
    def save(self):
        _file = open(self.file_dest).read()
        with open(self.file_dest) as destination_file:
            destination_file.write(json.dumps(_file))
    
    
    @staticmethod
    def print_database(): return json.load(open(SaveProgress.file_dest).read())