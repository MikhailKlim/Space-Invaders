class Level:
    def __init__(self, filename="Levels.txt"):
        self.maps = []
        current_map = []
        content = open(filename, "r")

        for line in content:
            if line[0] == "{":
                current_map = []
            if line[0] == "}":
                self.maps.append(current_map)
            if line[0] not in (";", "{", "}"):
                current_map.append(line.strip())
        content.close()

    def load_level(self, num):
        self.map_width = len(self.maps[num][0]) * 40
        self.map_height = len(self.maps[num]) * 40
        self.invader_coords = []
        self.bl_invader_coords = []
        self.red_invader_coords = []
        self.volt_coords = []
        startX = 0
        startY = 0
        line_num = 0
        for line in self.maps[num]:
            sym_num = 0
            for symbol in line:
                if symbol == "G":
                    self.invader_coords.append([sym_num * 40, line_num * 40, sym_num * 40 + 240])
                if symbol == "B":
                    self.bl_invader_coords.append([sym_num * 40, line_num * 40, sym_num * 40 + 370])
                if symbol == "R":
                    self.red_invader_coords.append([sym_num * 40, line_num * 40, sym_num * 40 + 710])
                if symbol == "V":
                    self.volt_coords.append([sym_num * 40, line_num * 40, sym_num * 40 + 700])
                if symbol == "P":
                    startX = sym_num * 40
                    startY = line_num * 40
                sym_num += 1
            line_num += 1
        return startX, startY
