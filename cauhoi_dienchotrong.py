import random

from nicegui import ui
from cauhoi import CauHoi

class DienChoTrong(CauHoi):
    def __init__(self, loai_cau_hoi: str, tu: int, den: int, phep_tinh: list, so_phep_tinh: int, ket_qua_am: bool) -> None:
        super().__init__(loai_cau_hoi, tu, den, phep_tinh, so_phep_tinh, ket_qua_am)
        self.vi_tri_dien = random.randint(0, self._sopheptinh)

    def kiem_tra_nhap(self, e):
        if not self.label_kiem_tra:
            return
        if e.value is None and e.value == '':
            self.label_kiem_tra.set_text('!')
        else:
            self.label_kiem_tra.set_text('')

    def hien_thi(self):
        self.tao_cau_hoi()
        with ui.row().classes('items-center justify-center'):
            with ui.row().classes('items-center justify-end'):
                for idx, so in enumerate(self.mang_so):
                    if idx == self.vi_tri_dien:
                        self.input_o_trong = ui.number(min=0, on_change=lambda e: self.kiem_tra_nhap(e)).bind_value(self, "_traloi").props('outlined dense input-class="text-center text-bold"').classes('w-16 bg-yellow-50 text-black').style('font-size: 1.25rem; height: 32px; padding-bottom: 0;')
                    else:
                        ui.label(str(so)).classes('text-black font-bold')

                    # Vẽ dấu phép tính nếu chưa phải số cuối cùng vế trái
                    if idx < len(self.mang_phep_tinh):
                        ui.label(self.mang_phep_tinh[idx]).classes('text-black font-bold')

            # Vẽ phần kết quả bằng
            ui.label(f"= {self._ketqua}").classes('text-base font-bold text-black whitespace-nowrap text-left w-[40px]')

            # Icon đúng/sai - Giữ nguyên w-8
            self.label_kiem_tra = ui.label('!').classes("text-xl font-bold w-8 text-center text-red-500 w-[20px]")

    def kiem_tra_ket_qua(self):
        if not self.input_o_trong:
           return
        if self.input_o_trong.value == self.mang_so[self.vi_tri_dien]:
            self._kiemtra = True
        else:
            self._kiemtra = False
        if self._kiemtra is not None:
            self.hien_thi_ket_qua()
