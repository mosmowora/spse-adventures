# Imports
from dataclasses import dataclass
from typing import List
import json, firedatabase

@dataclass
class SaveProgress():
    name: str
    inventory: dict[str]
    endings: List[str] 
    quests: List[str]
    number_bananok: int
    bananky_in_trash: dict[str, dict[str, int]]
    bananky_on_ground: dict[str, dict[str, bool]]
    amper_stuff: dict[str, tuple]
    level: List[str]
    room_number: str
    grades: dict[str, int]
    settings: dict[str, bool | int] = None
    file_dest: str = "Database/progress.json"
    
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
        write_data = {"name": self.name, "inventory": self.inventory, "endings": self.endings, "quests": self.quests, "number_bananok": self.number_bananok, "bananky_in_trash": self.bananky_in_trash, "bananky_on_ground": self.bananky_on_ground, "amper_stuff": self.amper_stuff, "level": self.level, "room_number": self.room_number, "grades": self.grades, "settings": self.settings}

        has_profile = False

        # User already has profile
        for i in range(len(loaded_data)):
            
            # Check whether user already has profile, if so then overwrite his currect data
            if write_data["name"] == loaded_data[i]["name"]: 
                loaded_data[i] = write_data
                has_profile = True
                firedatabase.update_data(write_data, write_data["name"])

        # No profile for u big man
        if not has_profile: 
            loaded_data.append(write_data)
            firedatabase.push_data(loaded_data, loaded_data[loaded_data.index(write_data)]['name'])

        # Writing to file 
        with open(self.file_dest, "w") as destination_file: json.dump(loaded_data, destination_file, indent=4)
    
    @staticmethod
    def print_database(): return json.dumps(json.loads(open(SaveProgress.file_dest).read()), indent=4)

