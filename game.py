from direct.showbase.ShowBase import ShowBase
# import direct.directbase.DirectStart
from pandac.PandaModules import *
from mapmanager import Mapmanager
from panda3d.core import WindowProperties
from hero import Hero
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        x,y = self.land.loadLand("lands/land.txt")
        self.hero = Hero((x//2, y//2, 2),self.land)
        base.camLens.setFov(110)
        

game = Game()
game.run()