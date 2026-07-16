import random
from nicegui import ui
from json_connect import JsonConnect


class CauHoi:
    def __init__(
        self, tu: int, den: int, phep_tinh: list, so_phep_tinh: int, ket_qua_am: bool
    ) -> None:
        self._tu = tu
        self._den = den
        self._pheptinh = phep_tinh
        self._sopheptinh = so_phep_tinh
        self._ketquaam = ket_qua_am
        self._cauhoi: str = ""
        self._traloi: float | None = None
        self._ketqua: float | None = None
        self._kiemtra: str = "!"

        if len(phep_tinh) == 0:
            self._pheptinh = ['+']
            ui.notify("Chưa chỉ định phép tính. Mặc định dùng phép cộng (+)", type='warning')

    def tao(self):
        # ui.notify('Đang tạo câu hỏi...', type='info')
        self._cauhoi = ""
        for i in range(int(self._sopheptinh) + 1):
            self._cauhoi += str(random.randint(self._tu, self._den))
            if i < self._sopheptinh:
                self._cauhoi += f' {random.choice(self._pheptinh)} '
        self._cauhoi = self._cauhoi.strip()
        try:
            self._ketqua = eval(self._cauhoi)
        except ZeroDivisionError:
            # Nếu gặp lỗi chia cho 0 thì tạo câu khác
            self.tao()

    def hienthi(self):
        self.tao()

        if not self._ketquaam:
            # ui.notify('Chế độ kết quả không âm', type='info')
            gioihan_lap = 0
            while self._ketqua is None or self._ketqua < 0:
                # ui.notify('Kết quả âm, đang tạo mới', type='warning')
                self.tao()
                gioihan_lap += 1
                if gioihan_lap>100:
                    break

            # Sử dụng flex row, không cho co cụm (whitespace-nowrap) để đề bài luôn nằm ngang
            with ui.row().classes('w-full items-center justify-between no-wrap'):

                # Cột 1: Đề bài (Phép tính) - Thêm 'whitespace-nowrap' để ép nằm trên 1 dòng
                ui.label(f"{self._cauhoi} =").classes("text-base font-bold text-gray-700 whitespace-nowrap grow text-right pr-2")

                # Cột 2: Ô nhập số - Giữ kích thước nhỏ gọn
                ui.number(on_change=lambda e: self.kiemtranhap(e)).bind_value(self, "_traloi").classes("w-20").props("outlined dense input-class='text-center text-lg font-semibold'")

                # Cột 3: Icon đúng/sai (❓, ✅, ❌)
                ui.label().bind_text(self, '_kiemtra').classes("text-xl font-bold w-8 text-center text-red-500")

    def kiemtranhap(self, e):
        if e.value is None and e.value == '':
            self._kiemtra = '!'
        else:
            self._kiemtra = ''

    def chamdiem(self):
        if self._traloi is None or self._ketqua is None:
            self._kiemtra = '!'
            return

        if self._traloi == self._ketqua:
            self._kiemtra = "✅"
        else:
            self._kiemtra = "❌"

        try:
            # Làm tròn 2 chữ số để xử lý các phép chia có số thập phân lẻ
            if round(float(self._traloi), 2) == round(float(self._ketqua), 2):
                self._kiemtra = '✅'
            else:
                self._kiemtra = '❌'
        except (ValueError, TypeError):
            self._kiemtra = '!'


class BaiTap:
    def __init__(self) -> None:
        self._socauhoi: int = 10
        self._tu: int = 0
        self._den: int = 10
        self._pheptinh: list = []
        self._sopheptinh: int = 1
        self._ketquaam: bool = False
        self._diem: float = 0.0
        self._socaudung:int = 0

        self.danh_sach_cau_hoi:list[CauHoi] = []

        cauhinh = JsonConnect("cauhinh.json")
        cauhinh.load()

        if cauhinh is not None:
            dt = cauhinh.data
            if dt:
                self._tu = int(dt.get("tu", 0))
                self._den = int(dt.get("den", 10))
                self._socauhoi = int(dt.get("socauhoi", 5))
                self._pheptinh = dt.get("pheptinh", ['+'])
                self._sopheptinh = int(dt.get("sopheptinh", 1))
                self._ketquaam = dt.get("ketquaam", False)

    def hienthi(self):
        with ui.card().classes('w-full max-w-5xl mx-auto p-6 bg-white shadow-md rounded-xl'):
            with ui.row().classes('w-full justify-center gap-4 mb-6'):
                with ui.card().classes('p-3 px-5 items-center border border-emerald-100 bg-emerald-50/30 min-w-[120px]'):
                    ui.label('Số câu đúng').classes('text-xs text-emerald-600 font-medium')
                    self.lbl_socaudung = ui.label('0').classes('text-2xl font-black text-emerald-700 mt-1').bind_text(self, '_socaudung')

                with ui.card().classes('p-3 px-5 items-center border border-amber-100 bg-amber-50/30 min-w-[120px]'):
                    ui.label('Điểm').classes('text-xs text-amber-600 font-medium')
                    self.lbl_diem = ui.label('0').classes('text-2xl font-black text-amber-700 mt-1').bind_text(self, '_diem')

            self.danh_sach_cau_hoi.clear()
            with ui.grid().classes('w-full grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 p-2'):
                for i in range(self._socauhoi):
                    cauhoi = CauHoi(
                        tu=self._tu,
                        den=self._den,
                        phep_tinh=self._pheptinh,
                        so_phep_tinh=self._sopheptinh,
                        ket_qua_am=self._ketquaam,
                    )
                    cauhoi.hienthi()
                    self.danh_sach_cau_hoi.append(cauhoi)

    def cham_diem_toan_bo(self):
        self._socaudung = 0
        for cauhoi in self.danh_sach_cau_hoi:
            cauhoi.chamdiem()
            if cauhoi._kiemtra == '✅':
                self._socaudung += 1
        # self._diem = round((self._socaudung / self._socauhoi) * 10, 0) if self._socauhoi > 0 else 0
        self._diem = int(round((self._socaudung / self._socauhoi) * 10, 0)) if self._socauhoi > 0 else 0

        # CẬP NHẬT GIAO DIỆN TRỰC TIẾP TẠI ĐÂY:
        if hasattr(self, 'lbl_socaudung'):
            self.lbl_socaudung.text = f'{self._socaudung}/{self._socauhoi}'
        if hasattr(self, 'lbl_diem'):
            self.lbl_diem.text = str(self._diem)
