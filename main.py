import os
import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PICTURE_DIR = os.path.join(BASE_DIR, 'picture')
SOUND_DIR = os.path.join(BASE_DIR, 'assets', 'sounds')

# --- ИСПРАВЛЕННЫЕ СВЯЗИ ЗВУКОВ ---
CATEGORIES = {
    'shapes': {'name': 'Фигуры', 'folder': 'shapes', 'items': [
        {'file': 'circle.png', 'name': 'Круг', 'sound': 's0'},
        {'file': 'square.png', 'name': 'Квадрат', 'sound': 's1'},
        {'file': 'triangle.png', 'name': 'Треугольник', 'sound': 's2'},
        {'file': 'rectangle.png', 'name': 'Прямоугольник', 'sound': 's3'},
        {'file': 'oval.png', 'name': 'Овал', 'sound': 's4'},
        {'file': 'rhombus.png', 'name': 'Ромб', 'sound': 's5'},
        {'file': 'star.png', 'name': 'Звезда', 'sound': 's6'},
        {'file': 'heart.png', 'name': 'Сердце', 'sound': 's7'},
        {'file': 'hexagon.png', 'name': 'Шестиугольник', 'sound': 's8'},
        {'file': 'semicircle.png', 'name': 'Полукруг', 'sound': 's9'}, # Теперь s9
        {'file': 'pentagon.png', 'name': 'Пятиугольник', 'sound': 's10'}, # Теперь s10
    ]},
    'numbers': {'name': 'Цифры', 'folder': 'numbers', 'items': [
        {'file': f'{i}.png', 'name': ['Ноль','Один','Два','Три','Четыре','Пять','Шесть','Семь','Восемь','Девять'][i], 'sound': f'n{i}'} for i in range(10)
    ]},
    'colors': {'name': 'Цвета', 'folder': 'colors', 'items': [
        {'file': 'red.png', 'name': 'Красный', 'sound': 'c0'},
        {'file': 'orange.png', 'name': 'Оранжевый', 'sound': 'c1'},
        {'file': 'yellow.png', 'name': 'Желтый', 'sound': 'c2'},
        {'file': 'green.png', 'name': 'Зеленый', 'sound': 'c3'},
        {'file': 'cyan.png', 'name': 'Голубой', 'sound': 'c4'},
        {'file': 'blue.png', 'name': 'Синий', 'sound': 'c5'},
        {'file': 'purple.png', 'name': 'Фиолетовый', 'sound': 'c6'},
        {'file': 'pink.png', 'name': 'Розовый', 'sound': 'c7'},
        {'file': 'gray.png', 'name': 'Серый', 'sound': 'c8'},
        {'file': 'black.png', 'name': 'Черный', 'sound': 'c9'},
        {'file': 'white.png', 'name': 'Белый', 'sound': 'c10'},
        {'file': 'brown.png', 'name': 'Коричневый', 'sound': 'c11'},
    ]}
}

def make_btn(text, bg, fn):
    b = Button(text=text, size_hint_y=None, height=70, font_size=22, bold=True, color=get_color_from_hex('#FFFFFF'), background_normal='', background_down='', border=[0,0,0,0], background_color=get_color_from_hex(bg))
    b.bind(on_press=fn)
    return b

class Menu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        lay = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lay.add_widget(Label(text="Обучалка", font_size=35, color=get_color_from_hex('#FF6B6B'), size_hint_y=None, height=60))
        for k, c in [('shapes','#A29BFE'),('numbers','#74B9FF'),('colors','#55EFC4')]:
            lay.add_widget(make_btn(CATEGORIES[k]['name'], c, lambda x, key=k: setattr(self.manager, 'current', f'diff_{key}')))
        self.add_widget(lay)

class Diff(Screen):
    def __init__(self, cat, **kw):
        super().__init__(**kw)
        self.cat = cat
        lay = BoxLayout(orientation='vertical', padding=15, spacing=10)
        lay.add_widget(Label(text=CATEGORIES[cat]['name'], font_size=35, color=get_color_from_hex('#FF6B6B'), size_hint_y=None, height=60))
        for d, t, c in [(4,'Легко','#27AE60'),(6,'Средне','#F39C12'),(9,'Сложно','#E74C3C')]:
            lay.add_widget(make_btn(t, c, lambda x, diff=d: self.start(diff)))
        lay.add_widget(make_btn("< Назад", "#95A5A6", lambda x: setattr(self.manager, 'current', 'menu')))
        self.add_widget(lay)
    def start(self, d):
        gs = self.manager.get_screen(f'game_{self.cat}')
        gs.setup(self.cat, d)
        self.manager.current = f'game_{self.cat}'

class ClickableImage(ButtonBehavior, Image):
    pass

class Game(Screen):
    def __init__(self, cat, **kw):
        super().__init__(**kw)
        self.cat = cat
        self.d = 4
        self.active = False
        self.err = 0
        self.locked = False
        
        root = BoxLayout(orientation='vertical', padding=5, spacing=5)
        
        hdr = BoxLayout(size_hint_y=None, height=45, orientation='horizontal')
        hdr.add_widget(make_btn("< Меню", "#EEEEEE", lambda x: setattr(self.manager, 'current', 'menu')))
        self.lbl_task = Label(text="", font_size=18, color=get_color_from_hex('#333333'))
        hdr.add_widget(self.lbl_task)
        root.add_widget(hdr)
        
        self.lbl_stat = Label(text="", font_size=16, size_hint_y=None, height=25, color=get_color_from_hex('#333333'))
        root.add_widget(self.lbl_stat)
        
        self.gl = GridLayout(cols=3, spacing=15, padding=10, size_hint=(1,1))
        root.add_widget(self.gl)
        
        self.add_widget(root)
        self.bind(on_enter=self.enter, on_leave=self.leave)

    def setup(self, cat, d):
        self.cat = cat
        self.d = d

    def enter(self, *a):
        self.active = True
        self.round()

    def leave(self, *a):
        self.active = False

    def round(self):
        if not self.active: return
        items = CATEGORIES[self.cat]['items']
        avail = [i for i in items if os.path.exists(os.path.join(PICTURE_DIR, CATEGORIES[self.cat]['folder'], i['file']))]
        if not avail:
            self.lbl_task.text = "Нет файлов!"
            return
        
        cnt = min(self.d, len(avail))
        sel = random.sample(avail, cnt)
        tgt = random.choice(sel)
        self.tgt = tgt
        self.err = 0
        self.locked = False
        
        self.draw_grid(sel, tgt)
        Clock.schedule_once(lambda dt: self.play(tgt['sound']), 0.3)

    def draw_grid(self, items, target):
        self.gl.clear_widgets()
        self.lbl_stat.text = ""
        cols = 2 if self.d == 4 else 3
        self.gl.cols = cols
        
        folder = os.path.join(PICTURE_DIR, CATEGORIES[self.cat]['folder'])
        self.lbl_task.text = f"Найди: {target['name']}"
        
        for it in items:
            p = os.path.join(folder, it['file'])
            
            if os.path.exists(p):
                img_btn = ClickableImage(
                    source=p,
                    allow_stretch=True,      
                    keep_ratio=True,         # Сохраняем пропорции
                    size_hint=(1, 1),        
                    pos_hint={'center_x': .5, 'center_y': .5} 
                )
                img_btn.item = it
                img_btn.bind(on_press=self.click)
                
                from kivy.graphics import Color, Rectangle
                with img_btn.canvas.before:
                    Color(1, 1, 1, 1) 
                    rect_bg = Rectangle(pos=img_btn.pos, size=img_btn.size)
                    
                img_btn.bind(pos=lambda w, v: setattr(rect_bg, 'pos', v),
                             size=lambda w, v: setattr(rect_bg, 'size', v))
                             
                self.gl.add_widget(img_btn)
            else:
                print(f"Файл не найден: {p}")

    def play(self, sn):
        if not self.active: return
        p = os.path.join(SOUND_DIR, f"{sn}.mp3")
        if os.path.exists(p):
            s = SoundLoader.load(p)
            if s: s.play()
        else:
            print(f"Звук отсутствует: {p}")

    def click(self, inst):
        if self.locked or not self.active: return
        it = inst.item
        
        if it['file'] == self.tgt['file']:
            self.play('success')
            self.lbl_stat.text = "МОЛОДЕЦ!"
            self.lbl_stat.color = get_color_from_hex('#27AE60')
            inst.background_color = get_color_from_hex('#27AE60') 
            Clock.schedule_once(lambda dt: self.round(), 1.0)
        else:
            self.err += 1
            self.play('error_retry')
            self.lbl_stat.text = "Попробуй еще"
            self.lbl_stat.color = get_color_from_hex('#E74C3C')
            inst.background_color = get_color_from_hex('#E74C3C')
            
            if self.err >= 3:
                self.locked = True
                self.lbl_stat.text = f"Ответ: {self.tgt['name']}"
                self.lbl_stat.color = get_color_from_hex('#F39C12')
                self.play('reveal_answer')
                for child in self.gl.children:
                    if hasattr(child, 'item') and child.item['file'] == self.tgt['file']:
                        child.background_color = get_color_from_hex('#27AE60')
                        break
                Clock.schedule_once(lambda dt: self.round(), 2.0)
            else:
                Clock.schedule_once(lambda dt: self.reset_btn(inst), 0.5)

    def reset_btn(self, b):
        b.background_color = get_color_from_hex('#FFFFFF')

class MyApp(App):
    def build(self):
        Window.size = (400, 700)
        Window.clearcolor = get_color_from_hex('#FFFFFF')
        
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        for k in CATEGORIES:
            sm.add_widget(Diff(k, name=f'diff_{k}'))
            sm.add_widget(Game(k, name=f'game_{k}'))
        return sm

if __name__ == '__main__':
    MyApp().run()
