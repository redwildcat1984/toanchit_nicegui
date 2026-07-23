from nicegui import ui
from cauhoi import CauHoi


class TinhKetQua(CauHoi):
    def __init__(self, loai_cau_hoi: str, tu: int, den: int, phep_tinh: list, so_phep_tinh: int, ket_qua_am: bool) -> None:
        super().__init__(loai_cau_hoi, tu, den, phep_tinh, so_phep_tinh, ket_qua_am)

    def hien_thi(self):
        self.tao_cau_hoi()
        # Sử dụng flex row, không cho co cụm (whitespace-nowrap) để đề bài luôn nằm ngang
        with ui.row().classes('w-full justify-center items-center no-wrap px-2 py-1'):
            # Cột 1: Đề bài - Bỏ 'grow' và 'text-right', dùng 'text-left' để phép tính nằm cố định bên lề trái
            ui.label(f"{self._cauhoi} =").classes("text-base font-bold text-black whitespace-nowrap text-left min-w-[80px]")

            # Cột 2: Ô nhập số - Giữ nguyên w-20
            self.nhap_tra_loi = ui.number(min=0, on_change=lambda e: self.kiem_tra_nhap(e)).bind_value(self, "_traloi").classes("w-20").props("outlined dense input-class='text-center text-lg font-semibold text-black'").style('font-size: 1.25rem; height: 32px; padding-bottom: 0;')

            # Cột 3: Icon đúng/sai - Giữ nguyên w-8
            self.label_kiem_tra = ui.label('!').classes("text-xl font-bold w-8 text-center")

    def kiem_tra_nhap(self, e):
        if not self.label_kiem_tra:
            return
        if e.value is None and e.value == '':
            self.label_kiem_tra.set_text('!')
        else:
            self.label_kiem_tra.set_text('')

    def kiem_tra_ket_qua(self):
        if self._traloi is None or self._ketqua is None:
            self._kiemtra = None
            return

        if self._traloi == self._ketqua:
            self._kiemtra = True
        else:
            self._kiemtra = False

        try:
            # Làm tròn 2 chữ số để xử lý các phép chia có số thập phân lẻ
            if round(float(self._traloi), 2) == round(float(self._ketqua), 2):
                self._kiemtra = True
            else:
                self._kiemtra = False
        except (ValueError, TypeError):
            self._kiemtra = None

        if self._kiemtra is not None:
            self.hien_thi_ket_qua()
