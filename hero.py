import math

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.hero = loader.loadModel("smiley")
        self.hero.setColor(0.1, 0.1, 0.3, 1)
        self.hero.setScale(0.5)
        self.hero.setPos(pos)
        self.hero.setH(180)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
        self.mode = True
        self.lastMouseX = base.win.getXSize() // 2
        self.lastMouseY = base.win.getYSize() // 2
        base.win.movePointer(0, self.lastMouseX, self.lastMouseY)
        base.taskMgr.add(self.mouseTask, "mouseTask")

    def Pick(self):   
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        
        if base.win.movePointer(0, base.win.getXSize() // 2, base.win.getYSize() // 2):
            deltaX = x - base.win.getXSize() // 2
            deltaY = y - base.win.getYSize() // 2
            
            base.camera.setH(base.camera.getH() - deltaX * 0.1)  # Horizontal rotation
            base.camera.setP(clamp(base.camera.getP() - deltaY * 0.1, -90, 90))  # Vertical rotation

            # Синхронизация героя с направлением камеры
            self.sync_hero_with_camera()

    def mouseTask(self, task):
        """Task to process mouse movements."""
        self.Pick()
        return task.cont

    def clamp(value, min_value, max_value):
        """Clamp a value between min_value and max_value."""
        return max(min(value, max_value), min_value)

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        camCenter = render.attachNewNode('camCenter')      
        base.camera.reparentTo(camCenter)   

        base.camera.setPos(0,20,8)   
        base.camera.lookAt(camCenter)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def accept_events(self):
        base.accept("1", self.changeView)
        base.accept("2", self.changeMode)

        base.accept("w", self.forward)
        base.accept("a", self.left)
        base.accept("s", self.back)
        base.accept("d", self.right)

        base.accept("q", self.camLeft)
        base.accept("e", self.camRight)

        base.accept("space", self.up)
        base.accept("lshift", self.down)
        base.accept("mouse1", self.build)
        base.accept("mouse3", self.destroy)

        base.accept("w" + '-repeat', self.forward)
        base.accept("a" + '-repeat', self.left)
        base.accept("s" + '-repeat', self.back)
        base.accept("d" + '-repeat', self.right)

        base.accept("q" + '-repeat', self.camLeft)
        base.accept("e" + '-repeat', self.camRight)

        base.accept("space" + '-repeat', self.up)
        base.accept("lshift" + '-repeat', self.down)

        base.accept("o", self.land.saveMap)
        base.accept("l", self.land.loadMap)

        base.accept('mouse1',self.Pick)

    def sync_hero_with_camera(self):
        self.hero.setH(base.camera.getH())

    def forward(self):
        angle = base.camera.getH() % 360  # Угол камеры
        self.move_to(angle)

    def back(self):
        angle = (base.camera.getH() + 180) % 360  # Угол камеры + 180° (обратное направление)
        self.move_to(angle)

    def left(self):
        angle = (base.camera.getH() + 90) % 360  # Угол камеры + 90° (влево)
        self.move_to(angle)

    def right(self):
        angle = (base.camera.getH() - 90) % 360  # Угол камеры - 90° (вправо)
        self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def camLeft(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def camRight(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def move_to(self, angle):
        if self.mode:
            dx, dy = self.calculate_direction(angle)
            new_x = self.hero.getX() + dx
            new_y = self.hero.getY() + dy
            self.hero.setPos(new_x, new_y, self.hero.getZ())  # Перемещаем персонажа


    def calculate_direction(self, angle):
        # Перевод угла в радианы
        rad_angle = math.radians(angle)
        # Вычисление направления
        dx = -math.sin(rad_angle)  # Смещение по X (с отрицанием, чтобы соответствовать координатной системе Panda3D)
        dy = math.cos(rad_angle)   # Смещение по Y
        return dx, dy


        pos_x = round(self.hero.getX())
        pos_y = round(self.hero.getY())
        pos_z = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        
        resultx = pos_x + dx
        resulty = pos_y + dy


        return resultx, resulty, pos_z
        


    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)

        elif angle >= 21 and angle <= 65:
            return (1, -1)

        elif angle >= 66 and angle <= 110:
            return (1, 0)

        elif angle >= 111 and angle <= 155:
            return (1, 1)

        elif angle >= 156 and angle <= 200:
            return (0, 1)

        elif angle >= 201 and angle <= 245:
            return (-1, 1)

        elif angle >= 246 and angle <= 290:
            return (-1, 0)

        elif angle >= 291 and angle <= 335:
            return (-1, -1)

        else:
            return (0, -1)


    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighetsEmpty(pos)
            self.hero.setPos(pos)

        else:
            pos = pos[0], pos[1], pos[2] + 1 
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
        
    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)

        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)