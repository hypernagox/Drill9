# 이것은 각 상태들을 객체로 구현한 것임.


from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT
from math import pi

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def time_out(e):
    return e[0] == 'TIME_OUT'
def right_down(e):
 return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
 return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
 return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
 return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
            boy.dir, boy.action = 1,1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action = -1,0

    @staticmethod
    def exit(boy,e):
       pass

    @staticmethod
    def do(boy):
       boy.frame = (boy.frame + 1) % 8
       boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
       boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Idle:

    @staticmethod
    def enter(boy,e):
        boy.frame = 0
        boy.start_time = get_time()
        print('Idle Enter')

    @staticmethod
    def exit(boy,e):
        print('Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3.0 :
            boy.state_machine.handle_event(('TIME_OUT',0))
        print('Idle Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100,100,100,
                            boy.x,boy.y)

class Sleep:

    @staticmethod
    def enter(boy,e):
        boy.frame = 0
        print('고개 숙이기')

    @staticmethod
    def exit(boy,e):
        print('고개 들기')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('드르렁')

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100,100,100,
                            pi/2,'',boy.x - 25,boy.y - 25,
                            100,100)

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.table = {
            Sleep : {space_down : Idle,right_down : Run,left_down : Run,left_up:Run,right_up:Run} ,
            Run : {right_down : Run,left_down : Run,left_up:Run, right_up : Run,time_out:Sleep},
            Idle : {time_out : Sleep,right_down : Run,left_down : Run,left_up:Run,right_up:Run}
        }
    def start(self):
        self.cur_state.enter(self.boy,('START',0))

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)

    def handle_event(self,e): # state hadling
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy,e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy,e)
                return True # 성공적으로 이벤트 변환
        return False # 이벤트를 소모하지 못했다
        pass




class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.boy_state = 0
        self.start_time = 0
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # convert pico2d event to state event
        self.state_machine.handle_event(('INPUT',event))
        pass



    def draw(self):
        self.state_machine.draw()
