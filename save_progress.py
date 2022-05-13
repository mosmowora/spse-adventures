from dataclasses import dataclass
from typing import List
import json

@dataclass
class SaveProgress():
    name: str
    inventory: dict[str]
    endings: List[str] 
    quests: List[str]
    level: List[str]
    room_number: str
    grades: dict[str, int]
    settings: dict[str, bool | int] = None
    file_dest: str = "Database/progress.json"
    
    #   ↑     ↑       ↑        ↑          ↑
    # def __init__(self, name: str, inventory: List[str], quests: List[str], file_dest: str = "Database/progress.json"):
    #     self.name = name
    #     self.inventory = inventory
    #     self.quests = quests
    #     self.file_dest = file_dest
    
    @staticmethod
    def load_data(name: str):
        """
        Loads data for player if he has profile
        """
    
        # Data from file
        loaded_data: List = json.load(open(SaveProgress.file_dest))

        for i in range(len(loaded_data)):
            if loaded_data[i]["name"] == name: return loaded_data[i]
              
    def save(self):
        """
        Saves/rewrites data to file
        """

        # Data from file
        loaded_data: List = json.load(open(SaveProgress.file_dest))

        # New data
        write_data = {"name": self.name, "inventory": self.inventory, "endings": self.endings, "quests": self.quests, "level": self.level, "room_number": self.room_number, "grades": self.grades, "settings": self.settings}

        has_profile = False

        # User already has profile
        for i in range(len(loaded_data)):
            
            # Check whether user already has profile, if so then overwrite his currect data
            if write_data["name"] == loaded_data[i]["name"]: 
                loaded_data[i] = write_data
                has_profile = True

        # No profile for u big man
        if not has_profile: loaded_data.append(write_data)

        # Writing to file 
        with open(self.file_dest, "w") as destination_file: json.dump(loaded_data, destination_file, indent=4)
    
    @staticmethod
    def print_database(): return json.dumps(json.loads(open(SaveProgress.file_dest).read()), indent=4)