import math
import random

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

        self.build_sound = base.loader.loadSfx("sounds/blockadd.mp3")
        self.destroy_sound = base.loader.loadSfx("sounds/blockremove.mp3")
        self.changeMode_sound = base.loader.loadSfx("sounds/change_mode.mp3")

        self.footstep_sound = base.loader.loadSfx("sounds/footstep_1.wav")
        self.footstep_sound2 = base.loader.loadSfx("sounds/footstep_2.wav")

    def play_footstep_sound(self):
        n = random.randint(1,2)
        if n == 1:
            self.footstep_sound.play()
        self.footstep_sound2.play()


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
        self.Pick()
        return task.cont

    def clamp(value, min_value, max_value):
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
        angle = self.hero.getH() % 360  # Угол камеры
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360  # Угол камеры + 180° (обратное направление)
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360  # Угол камеры + 90° (влево)
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() - 90) % 360  # Угол камеры - 90° (вправо)
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
            new_x = self.hero.getX() + dx * 0.2  # Шаг движения (умножение на коэффициент)
            new_y = self.hero.getY() + dy * 0.2
            self.hero.setPos(new_x, new_y, self.hero.getZ())  # Перемещаем персонажа


    def calculate_direction(self, angle):
        # Нормализуем угол (0–360)
        angle %= 360

        # Заранее определённые направления для основных углов
        directions = {
            0: (0, 1),    # Вверх
            90: (1, 0),   # Вправо
            180: (0, -1), # Вниз
            270: (-1, 0)  # Влево
        }

        # Определяем соседние ключевые углы
        lower_angle = (angle // 90) * 90  # Нижняя граница
        upper_angle = (lower_angle + 90) % 360  # Верхняя граница

        # Берём векторы для соседних углов
        x1, y1 = directions[lower_angle]
        x2, y2 = directions[upper_angle]

        # Находим вес интерполяции (0–1)
        t = (angle - lower_angle) / 90

        # Линейная интерполяция между двумя векторами
        dx = x1 + t * (x2 - x1)
        dy = y1 + t * (y2 - y1)

        return dx, dy


    def look_at(self, angle):
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
        angle %= 360  # Нормализация угла
        if 0 <= angle < 45 or 315 <= angle < 360:
            return (0, -1)
        elif 45 <= angle < 135:
            return (1, 0)
        elif 135 <= angle < 225:
            return (0, 1)
        elif 225 <= angle < 315:
            return (-1, 0)
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