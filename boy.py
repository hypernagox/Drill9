class Boy:
    event = None
    def __init__(self):
        self.x, self.y = 400, 90
        self.state_machine = None
        self.speed = 300
        self.sizeX,self.sizeY = 100,100
    def update(self):
        self.state_machine.update(Boy.event)
    def draw(self):
        self.state_machine.render()

