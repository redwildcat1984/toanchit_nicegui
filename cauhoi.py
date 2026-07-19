import random
from nicegui import ui
from json_connect import JsonConnect

class CauHoi:
    def __init__(self, loai_cau_hoi:str, tu:int, den:int, phep_tinh: list, so_phep_tinh: int, ket_qua_am: bool ) -> None:
        self._loai_cau_hoi = loai_cau_hoi
        self._tu = tu
        self._den = den
        self._pheptinh = phep_tinh
        self._sopheptinh = so_phep_tinh
        self._ketquaam = ket_qua_am
        self._cauhoi: str = ""
        self._ketqua: float | None = None
        self._kiemtra:ui.label|None = None
        self.label_kiem_tra:ui.label|None = None
        self._traloi:int|None = None
        self.nhap_tra_loi:ui.number|None = None

    @staticmethod
    def tao_moi(loai_cau_hoi:str, *args, **kwargs):
        if loai_cau_hoi == 'tinh_ket_qua':
            return TinhKetQua(loai_cau_hoi, *args, **kwargs)
        raise ValueError(f'Không có loại câu hỏi {loai_cau_hoi}')

    def hien_thi(self):
        """Hàm trừu tượng, các class con bắt buộc phải tự định nghĩa cách vẽ"""
        raise NotImplementedError("Class con phải tự triển khai hàm hien_thi")

    def kiem_tra_ket_qua(self):
        """Hàm trừu tượng, các class con bắt buộc phải tự định nghĩa cách vẽ"""
        raise NotImplementedError("Class con phải tự triển khai hàm kiem_tra_ket_qua")

    def hetgio(self):
        if self.nhap_tra_loi:
            self.nhap_tra_loi.disable()

    def tao_cau_hoi(self):
        # ui.notify('Đang tạo câu hỏi...', type='info')
        self._cauhoi = ""
        for i in range(int(self._sopheptinh) + 1):
            self._cauhoi += str(random.randint(self._tu, self._den))
            if i < self._sopheptinh:
                self._cauhoi += f' {random.choice(self._pheptinh)} '
        self._cauhoi = self._cauhoi.strip()
        try:
            self._ketqua = eval(self._cauhoi)
            # Kiểm tra có cho phép kết quả âm không, nếu không thì tạo câu khác
            if self._ketqua:
                if self._ketqua < 0 and not self._ketquaam:
                    self.tao_cau_hoi()
        except ZeroDivisionError:
            # Nếu gặp lỗi chia cho 0 thì tạo câu khác
            self.tao_cau_hoi()


class TinhKetQua(CauHoi):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def hien_thi(self):
        self.tao_cau_hoi()
        # Sử dụng flex row, không cho co cụm (whitespace-nowrap) để đề bài luôn nằm ngang
        with ui.row().classes('w-full justify-between items-center no-wrap px-2 py-1'):
            # Cột 1: Đề bài - Bỏ 'grow' và 'text-right', dùng 'text-left' để phép tính nằm cố định bên lề trái
            ui.label(f"{self._cauhoi} =").classes("text-base font-bold text-black whitespace-nowrap text-left min-w-[80px]")

            # Cột 2: Ô nhập số - Giữ nguyên w-20
            self.nhap_tra_loi = ui.number(min=0, on_change=lambda e: self.kiem_tra_nhap(e)).bind_value(self, "_traloi").classes("w-20").props("outlined dense input-class='text-center text-lg font-semibold text-black'")

            # Cột 3: Icon đúng/sai - Giữ nguyên w-8
            self._kiemtra = ui.label('!').classes("text-xl font-bold w-8 text-center text-red-500")

    def kiem_tra_nhap(self, e):
        if not self._kiemtra:
            return
        if e.value is None and e.value == '':
            self._kiemtra.set_text('!')
        else:
            self._kiemtra.set_text('')

    def kiem_tra_ket_qua(self):
        if not self._kiemtra:
            return

        if self._traloi is None or self._ketqua is None:
            self._kiemtra.set_text('❌')
            self._kiemtra.classes('fade-in-2s')
            return

        if self._traloi == self._ketqua:
            self._kiemtra.set_text("✅")
        else:
            self._kiemtra.set_text("❌")

        try:
            # Làm tròn 2 chữ số để xử lý các phép chia có số thập phân lẻ
            if round(float(self._traloi), 2) == round(float(self._ketqua), 2):
                self._kiemtra.set_text('✅')
            else:
                self._kiemtra.set_text('❌')
        except (ValueError, TypeError):
            self._kiemtra.set_text('!')

        # Đặt class hiện dần cho icon kiểm tra
        self._kiemtra.classes('fade-in-3s')

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
        with ui.card().classes('w-full max-w-5xl mx-auto p-6 bg-white shadow-md rounded-xl fade-in-1s'):
            with ui.row().classes('w-full justify-center gap-4 mb-6 fade-in-1s') as self.khung_diem:
                with ui.card().classes('p-3 px-5 items-center border border-emerald-100 bg-emerald-50/30 min-w-[120px] bg-ember-50'):
                    ui.label('Số câu đúng').classes('text-xs text-emerald-600 font-medium')
                    self.lbl_socaudung = ui.label('0').classes('text-2xl font-black text-emerald-700 mt-1').bind_text(self, '_socaudung')

                with ui.card().classes('p-3 px-5 items-center border border-amber-100 bg-amber-50/30 min-w-[120px] bg-ember-50'):
                    ui.label('Điểm').classes('text-xs text-amber-600 font-medium')
                    self.lbl_diem = ui.label('0').classes('text-2xl font-black text-amber-700 mt-1').bind_text(self, '_diem')
            self.khung_diem.set_visibility(False)

            self.danh_sach_cau_hoi.clear()
            with ui.grid().classes('w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-2'):
                for i in range(self._socauhoi):
                    cauhoi = CauHoi.tao_moi(
                        loai_cau_hoi='tinh_ket_qua',
                        tu=self._tu,
                        den=self._den,
                        phep_tinh=self._pheptinh,
                        so_phep_tinh=self._sopheptinh,
                        ket_qua_am=self._ketquaam,
                    )
                    cauhoi.hien_thi()
                    self.danh_sach_cau_hoi.append(cauhoi)
    def hetgio(self):
        for cauhoi in self.danh_sach_cau_hoi:
            cauhoi.hetgio()

    def cong_diem(self, cauhoi):
        if cauhoi._kiemtra.text == '✅':
            self._socaudung += 1

    def hien_thi_tong_diem(self):
        # ui.notify('Hien thi tong diem')
        self._diem = int(round((self._socaudung / self._socauhoi) * 10, 0)) if self._socauhoi > 0 else 0

        # CẬP NHẬT GIAO DIỆN TRỰC TIẾP TẠI ĐÂY:
        if self.khung_diem:
            self.khung_diem.set_visibility(True)

        if hasattr(self, 'lbl_socaudung'):
            self.lbl_socaudung.text = f'{self._socaudung}/{self._socauhoi}'
        if hasattr(self, 'lbl_diem'):
            self.lbl_diem.text = str(self._diem)

    def cham_diem_toan_bo(self):
        ui.notify('Bắt đầu chấm điểm', type='info')
        do_tre_tung_cau = 1
        self._socaudung = 0
        for index, cauhoi in enumerate(self.danh_sach_cau_hoi):
            # Xác định độ trễ hiển thị theo từng câu hỏi
            do_tre = (index+1)*do_tre_tung_cau
            # Hẹn giờ chấm điểm từng câu hỏi theo độ trễ
            ui.timer(do_tre, cauhoi.kiem_tra_ket_qua, once=True)
            # Đồng thời hẹn giờ cộng điểm cho các câu hỏi đúng (đồng bộ độ trễ với việc chấm điểm)
            ui.timer(do_tre, lambda c=cauhoi: self.cong_diem(c), once=True)
        # Hiển thị tổng điểm sau khi toàn bộ câu hỏi được chấm
        tong_do_tre = (len(self.danh_sach_cau_hoi) + 2)*do_tre_tung_cau
        ui.timer(tong_do_tre, self.hien_thi_tong_diem, once=True)
        # ui.label(f'Tong do tre: {tong_do_tre}')
