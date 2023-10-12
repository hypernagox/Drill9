from pico2d import get_time
from sdl2 import SDL_KEYDOWN, SDLK_a, SDLK_LEFT, SDLK_RIGHT, SDL_KEYUP
from boy import Boy

WIDTH,HEIGHT = 800,600

class State:
    def __init__(self,state_machine):
        self.state_machine = state_machine
        self.event_for_check = None
        self.frame = 0
    def enter_state(self):
        pass
    def exit_state(self):
        pass
    def update(self):
        pass
    def render(self):
        pass
    def change_state(self,event):
        pass

class Idle(State):
    def __init__(self,state_machine):
        super().__init__(state_machine)
    def enter_state(self):
        self.frame = 0
    def exit_state(self):
        pass
    def update(self):
        pass
    def render(self):
        dir = '' if self.state_machine.boy_dir == 1 else 'h'
        boy = self.state_machine.boy
        self.state_machine.boy_anim.clip_composite_draw(self.frame * 100, 300, 100, 100,
                            0, dir, boy.x, boy.y,
                            boy.sizeX, boy.sizeY)
        self.frame = (self.frame + 1) % 8
    def change_state(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                return 'AutoRun'
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                return 'Run'
        return ''
class Run(State):
    def __init__(self,state_machine):
        super().__init__(state_machine)
    def enter_state(self):
        pass
    def exit_state(self):
        pass
    def update(self):
        self.state_machine.boy.x += self.state_machine.boy_dir * self.state_machine.boy.speed * 0.01
    def render(self):
        dir = '' if self.state_machine.boy_dir == 1 else 'h'
        boy = self.state_machine.boy
        self.state_machine.boy_anim.clip_composite_draw(self.frame * 100, 100, 100, 100,
                                                        0, dir, boy.x, boy.y,
                                                        boy.sizeX, boy.sizeY)
        self.frame = (self.frame + 1) % 8
    def change_state(self,event):
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT and self.state_machine.boy_dir == 1:
                return 'Idle'
            if event.key == SDLK_LEFT and self.state_machine.boy_dir == -1:
                return 'Idle'
        return ''

class AutoRun(State):
    def __init__(self,state_machine):
        super().__init__(state_machine)
        self.startTime = get_time()
    def enter_state(self):
        self.frame = 0
        self.state_machine.boy.speed *= 4
        self.state_machine.boy.sizeX *= 2
        prevSize = self.state_machine.boy.sizeY
        self.state_machine.boy.sizeY *= 2
        self.state_machine.boy.y += (self.state_machine.boy.sizeY - prevSize)/4
        self.startTime = get_time()

    def exit_state(self):
        self.state_machine.boy.speed /= 4
        self.state_machine.boy.sizeX /= 2
        prevSize = self.state_machine.boy.sizeY
        self.state_machine.boy.sizeY /= 2
        self.state_machine.boy.y += (self.state_machine.boy.sizeY - prevSize) / 4
    def update(self):
        boy = self.state_machine.boy
        if boy.x + boy.sizeX / 4 >= WIDTH:
            self.state_machine.boy_dir = -1
        elif boy.x - boy.sizeX / 4 <= 0 :
            self.state_machine.boy_dir = 1
        self.state_machine.boy.x += self.state_machine.boy_dir * self.state_machine.boy.speed * 0.01
    def render(self):
        dir = '' if self.state_machine.boy_dir == 1 else 'h'
        boy = self.state_machine.boy
        self.state_machine.boy_anim.clip_composite_draw(self.frame * 100, 100, 100, 100,
                                                        0, dir, boy.x, boy.y,
                                                        boy.sizeX, boy.sizeY)
        self.frame = (self.frame + 1) % 8
    def change_state(self,event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT or event.key == SDLK_LEFT:
                return 'Run'
        if get_time() - self.startTime >= 5:
            return 'Idle'
        return ''

class StateMachine:
    def __init__(self,boy):
        self.cur_state = Idle(self)
        self.boy = boy
        self.boy_dir = 1
        from pico2d import load_image
        self.boy_anim = load_image('animation_sheet.png')
        self.anim_map = {
            "Idle" : Idle(self),
            "Run" : Run(self),
            "AutoRun" : AutoRun(self)
        }
    def init(self):
        self.cur_state.enter_state()
    def update(self,event):
        if event == None:
            return
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.boy_dir = -1
            elif event.key == SDLK_RIGHT:
                self.boy_dir = 1
        self.cur_state.update()
        self.cur_state.event_for_check = event
    def render(self):
        self.cur_state.render()
        if None != Boy.event:
            self.change_state(Boy.event)
    def change_state(self,event):
        state = self.cur_state.change_state(event)
        if '' != state:
            self.cur_state.exit_state()
            self.cur_state = self.anim_map[state]
            self.cur_state .enter_state()
