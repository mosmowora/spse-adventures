# Imports
from dataclasses import dataclass
from typing import List
import firedatabase

@dataclass
class SaveProgress():
    name: str
    credentials: str
    inventory: dict[str]
    endings: List[str] 
    quests: List[str]
    number_bananok: int
    bananky_in_trash: dict[str, dict[str, int]]
    bananky_on_ground: dict[str, dict[str, bool]]
    amper_stuff: dict[str, tuple]
    level: List[str]
    room_number: str
    lyz_dlc_number: str
    lyz_dlc_level: int
    dlc_bought: bool
    grades: dict[str, int]
    controls: dict[str, int]
    played_for: float
    settings: dict[str, bool | int] = None
    
    @staticmethod
    def load_data(name: str):
        """
        Loads data for player if he has profile on OUR server
        """
    
        # Data from file
        loaded_data = firedatabase.retrieve_data(name)
        return None if len(loaded_data) == 0 else loaded_data 
              
    def save(self):
        """
        Saves/rewrites data to server
        """

        # Data from file
        loaded_data: list = firedatabase.retrieve_data()

        # New data
        write_data = {"name": self.name, 'credentials': self.credentials, "inventory": self.inventory, "endings": self.endings, "quests": self.quests, "number_bananok": self.number_bananok, "bananky_in_trash": self.bananky_in_trash, "bananky_on_ground": self.bananky_on_ground, "amper_stuff": self.amper_stuff, "level": self.level, "room_number": self.room_number, "lyz_room_level": self.lyz_dlc_level, "lyz_room_number": self.lyz_dlc_number, "DLC bought": self.dlc_bought, "grades": self.grades, "controls": self.controls, "played": self.played_for, "settings": self.settings}

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
            firedatabase.push_data(loaded_data, write_data["name"])
