from config import *


class Camera:
    
    def __init__(self, game): self.game = game
    
    def set_ground_camera(self):
        """
        Set camera for rooms on the ground floor
        """

        match self.game.saved_room_data:

            # Changing room
            case "017":
                for sprite in self.game.all_sprites: sprite.rect.x -= 158 * TILE_SIZE

            # Lit 3
            case "023": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 14 * TILE_SIZE
                    sprite.rect.x += 34 * TILE_SIZE
                self.game.player.rect.y += 15 * TILE_SIZE
                self.game.player.rect.x -= 35 * TILE_SIZE
            
            # Lcuj 4
            case "025": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 15 * TILE_SIZE
                    sprite.rect.x += 71 * TILE_SIZE
                self.game.player.rect.y += 15 * TILE_SIZE
                self.game.player.rect.x -= 72 * TILE_SIZE

            # II.SA
            case "016": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 8 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 9 * TILE_SIZE

            # II.C
            case "015": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 32 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 33 * TILE_SIZE

            # LAELE
            case "014": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 53 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 54 * TILE_SIZE

            # II.B
            case "013": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 79 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 80 * TILE_SIZE

            # II.A
            case "012": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 88 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 89 * TILE_SIZE

            # DPXA 1
            case "002": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 132 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 133 * TILE_SIZE

            # DPXA 3
            case "003": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 143 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 144 * TILE_SIZE

            # Lit 8
            case "004": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 7 * TILE_SIZE
                    sprite.rect.x += 147 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 148 * TILE_SIZE

            # Lit 9
            case "006": 
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= 7 * TILE_SIZE
                self.game.player.rect.y += 7 * TILE_SIZE
                self.game.player.rect.x -= 159 * TILE_SIZE

            # Lit 10
            case "007": 
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= 11 * TILE_SIZE
                self.game.player.rect.y += 11 * TILE_SIZE
                self.game.player.rect.x -= 158 * TILE_SIZE

            # DPXA 3
            case "008": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 15 * TILE_SIZE
                    sprite.rect.x += 148 * TILE_SIZE
                self.game.player.rect.y += 15 * TILE_SIZE
                self.game.player.rect.x -= 149 * TILE_SIZE

            # Toilet
            case "010": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 158 * TILE_SIZE
                    sprite.rect.y -= 15 * TILE_SIZE
                    sprite.rect.x += 134 * TILE_SIZE
                self.game.player.rect.y += 15 * TILE_SIZE
                self.game.player.rect.x -= 135 * TILE_SIZE
        
    def set_first_camera(self):
        """
        Set camera for rooms on the first floor
        """

        match self.game.saved_room_data:

            # Lit 1
            case "122/1": 
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= 6 * TILE_SIZE
                    sprite.rect.x -= 166 * TILE_SIZE
                self.game.player.rect.y -= 10 * TILE_SIZE
                self.game.player.rect.x -= 6 * TILE_SIZE

            # Lit 2
            case "122/2": 
                for sprite in self.game.all_sprites:
                    sprite.rect.y += 5 * TILE_SIZE
                    sprite.rect.x -= 167 * TILE_SIZE
                self.game.player.rect.y -= 16 * TILE_SIZE
                self.game.player.rect.x -= 3 * TILE_SIZE
            
            # OUC
            case "117": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 147 * TILE_SIZE
                    sprite.rect.y -= 16 * TILE_SIZE
                self.game.player.rect.x -= 23 * TILE_SIZE     

            # OUB          
            case "115": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 119 * TILE_SIZE
                    sprite.rect.y -= 16 * TILE_SIZE
                self.game.player.rect.x -= 52 * TILE_SIZE

            # OUA
            case "113": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 84 * TILE_SIZE
                    sprite.rect.y -= 16 * TILE_SIZE
                self.game.player.rect.x -= 87 * TILE_SIZE

            # LELM 1
            case "112": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 67 * TILE_SIZE
                    sprite.rect.y -= 16 * TILE_SIZE
                self.game.player.rect.x -= 104 * TILE_SIZE
 
            # LELM 2
            case "124": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 151 * TILE_SIZE
                    sprite.rect.y -= 24 * TILE_SIZE
                self.game.player.rect.x -= 20 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE

            # LSIE 2
            case "126": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 132 * TILE_SIZE
                    sprite.rect.y -= 24 * TILE_SIZE
                self.game.player.rect.x -= 39 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE

            # LIOT 2
            case "127": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 117 * TILE_SIZE
                    sprite.rect.y -= 24 * TILE_SIZE
                self.game.player.rect.x -= 54 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE

            # CZV
            case "130": 
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 95 * TILE_SIZE
                    sprite.rect.y -= 24 * TILE_SIZE
                self.game.player.rect.x -= 76 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE
            

    
    def set_second_camera(self):
        """
        Set camera for rooms on the second floor
        """

        match self.game.saved_room_data:

            # Cabinet Haramgozo
            case "Cabinet HAR":
                for sprite in self.game.all_sprites:
                    sprite.rect.x += 1 * TILE_SIZE
                    sprite.rect.y -= 14 * TILE_SIZE
                self.game.player.rect.x -= 172 * TILE_SIZE
                self.game.player.rect.y -= 3 * TILE_SIZE

            # OUG
            case "203":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 1 * TILE_SIZE
                    sprite.rect.y -= 21 * TILE_SIZE
                self.game.player.rect.x -= 170 * TILE_SIZE
                self.game.player.rect.y += 4 * TILE_SIZE

            # LELN
            case "205":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 7 * TILE_SIZE
                    sprite.rect.y -= 25 * TILE_SIZE
                self.game.player.rect.x -= 164 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE

            # I.SC
            case "202":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 14 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.game.player.rect.x -= 157 * TILE_SIZE

            # II.SB Goated place
            case "201":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 32 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.game.player.rect.x -= 139 * TILE_SIZE

            # Left toilets
            case "Toilets_1":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 31 * TILE_SIZE
                    sprite.rect.y -= 25 * TILE_SIZE
                self.game.player.rect.x -= 140 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE

            # I.A
            case "208":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 67 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.game.player.rect.x -= 104 * TILE_SIZE

            # I.B
            case "209":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 84 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.game.player.rect.x -= 87 * TILE_SIZE

            # I.SA
            case "219":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 108 * TILE_SIZE
                    sprite.rect.y -= 25 * TILE_SIZE
                self.game.player.rect.x -= 63 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE

            # III.SB
            case "210":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 119 * TILE_SIZE
                    sprite.rect.y -= 17 * TILE_SIZE
                self.game.player.rect.x -= 52 * TILE_SIZE

            # OUF
            case "216":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 160 * TILE_SIZE
                    sprite.rect.y -= 6 * TILE_SIZE
                self.game.player.rect.x -= 11 * TILE_SIZE
                self.game.player.rect.y -= 11 * TILE_SIZE
            
            # Cabinet
            case "217":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 165 * TILE_SIZE
                    sprite.rect.y -= 12 * TILE_SIZE
                self.game.player.rect.x -= 6 * TILE_SIZE
                self.game.player.rect.y -= 5 * TILE_SIZE

            # I.C
            case "220":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 108 * TILE_SIZE
                    sprite.rect.y -= 25 * TILE_SIZE
                self.game.player.rect.x -= 63 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE                
    
    def set_third_camera(self):
        """
        Set camera for rooms on the third floor
        """

        match self.game.saved_room_data:

            # Gym - changing room
            case "Gym - chr":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 52 * TILE_SIZE
                    sprite.rect.y -= 1 * TILE_SIZE
                self.game.player.rect.x -= 9 * TILE_SIZE
                self.game.player.rect.y -= 3 * TILE_SIZE

            # Toilet
            case "Toilets":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 46 * TILE_SIZE
                    sprite.rect.y -= 1 * TILE_SIZE
                self.game.player.rect.x -= 15 * TILE_SIZE
                self.game.player.rect.y -= 3 * TILE_SIZE

            # Gym
            case "302":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 43 * TILE_SIZE
                    sprite.rect.y += 2 * TILE_SIZE
                self.game.player.rect.x -= 18 * TILE_SIZE
                self.game.player.rect.y -= 5 * TILE_SIZE

            # Gymnasium
            case "304":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 43 * TILE_SIZE
                    sprite.rect.y -= 5 * TILE_SIZE
                self.game.player.rect.x -= 18 * TILE_SIZE
                self.game.player.rect.y += 2 * TILE_SIZE

            # Gymnasium - changing room
            case "Gymnasium - chr":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 57 * TILE_SIZE
                    sprite.rect.y -= 12 * TILE_SIZE
                self.game.player.rect.x -= 4 * TILE_SIZE
                self.game.player.rect.y += 9 * TILE_SIZE

            # Showers
            case "Showers":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 63 * TILE_SIZE
                    sprite.rect.y -= 18 * TILE_SIZE
                self.game.player.rect.x += 2 * TILE_SIZE
                self.game.player.rect.y += 15 * TILE_SIZE
    
    def set_fourth_camera(self):
        """
        Set camera for rooms on the fourth floor
        """

        match self.game.saved_room_data:

            # LSIE
            case "403":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 52 * TILE_SIZE
                    sprite.rect.y -= 12 * TILE_SIZE
                self.game.player.rect.x -= 9 * TILE_SIZE
                self.game.player.rect.y += 8 * TILE_SIZE

            # LROB - hallway
            case "402 - hallway":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 52 * TILE_SIZE
                    sprite.rect.y -= 1 * TILE_SIZE
                self.game.player.rect.x -= 9 * TILE_SIZE
                self.game.player.rect.y -= 3 * TILE_SIZE

            # LROB
            case "402":
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= 43 * TILE_SIZE
                    sprite.rect.y += 1 * TILE_SIZE
                self.game.player.rect.x -= 18 * TILE_SIZE
                self.game.player.rect.y -= 5 * TILE_SIZE
                
                
    def set_ending_camera(self):
        """
        Set camera for ending sequence
        """
        for sprite in self.game.all_sprites:
            sprite.rect.x += 3 * TILE_SIZE
            sprite.rect.y -= 165 * TILE_SIZE