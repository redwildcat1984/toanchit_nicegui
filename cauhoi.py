from nicegui import ui
import random

from json_connect import JsonConnect

class CauHoi:
    def __init__(self, gioi_han:range=range(0,10), phep_tinh:list=['+', '-', '*', '/'], so_phep_tinh:int=2) -> None:
        self.gioihan:range = gioi_han
        self.pheptinh: list = phep_tinh
        self.sopheptinh: int = so_phep_tinh
        self.cauhoi: str = ''
        self.traloi: str = ''
        self.ketqua:str = ''

        cauhinh = JsonConnect()
        cauhinh.load()
        if cauhinh is not None:
            dt = cauhinh.data
            if dt:
                self.gioihan = range(dt['tu'], dt['den'])
                self.socau = dt['socau']

    def tao(self):
        self.cauhoi = ''
        for i in range(self.sopheptinh):
            self.cauhoi += f'{str(random.randint(self.gioihan[0], self.gioihan[1]))}{random.choice(self.pheptinh)}'
        self.cauhoi = self.cauhoi[:-1]
