import pickle

class Mapmanager():
    def __init__(self):
        self.model = "block.egg"
        self.texture = "block.png"

        self.colors = [(0.2, 0.2 ,0.4, 1),
                      (0.1, 0.5 ,0.3, 1),
                      (0.4, 0.7 ,0.1, 1),
                      (0.5, 0.1 ,0.9, 1)]

        self.startNew()
        self.addBlock((0,10,0))
    def startNew(self):
        self.land = render.attachNewNode("Land")


    def addBlock(self, pos):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(pos)
        self.color=self.getColor(int(pos[2]))
        self.block.setColor(self.color)
        self.block.setTag("at", str(pos))
        self.block.reparentTo(self.land)
        
        

    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def buildBlock(self, pos):
        x, y,z = pos
        new = self.findHighetsEmpty(pos)
        if new[2] <= z+1:
            self.addBlock(new)
            


    def delBlockFrom(self, position):
        x, y, z = findHighetsEmpty(position)
        pos = x, y, z-1
        for block in self.findBlocks(pos):
            block.removeNode()

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename, "r") as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(" ")
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x,y, z0))

                    x += 1
                y += 1

        return x, y

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:

            return False
        else:

            return True

    def findHighetsEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z = z + 1

        return (x, y, z)

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def saveMap(self):
        blocks = self.land.getChildren()
        with open("my_map.dat", "wb") as map:
            pickle.dump(len(blocks), map)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, map)




    def loadMap(self):
        self.clear()
        with open("my_map.dat", "rb") as map:
            length = pickle.load(map)
            for i in range(length):
                pos = pickle.load(map)
                self.addBlock(pos)