from nicegui import ui

from giatri_codinh import CAU_HOI
from json_connect import JsonConnect
from cauhoi import CauHoi

from cauhoi_taomoi import tao_moi_cau_hoi


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
        self.loai_cau_hoi: list = []

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
                self.loai_cau_hoi = dt.get('loaicauhoi', 'tinh_ket_qua')

        print(f'Cấu hình đã load để tạo bài tập: {self._tu}, {self._den}, {self._socauhoi}, {self._pheptinh}, {self._sopheptinh}, {self._ketquaam}, {self.loai_cau_hoi}')

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
            with ui.grid().classes('w-full grid grid-flow-row-dense grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-2'):
                for index, loai in enumerate(self.loai_cau_hoi):
                    # Hiện tiêu đề câu hỏi
                    ui.label(f'Câu hỏi {index + 1}: {CAU_HOI[loai]}').classes('text-xl font-bold mt-4 underline text-red-600 md:col-span-2 lg:col-span-3')
                    for i in range(int(self._socauhoi/len(self.loai_cau_hoi))):
                    # loai_cau_hoi = random.choice(self.loai_cau_hoi)
                        cauhoi = tao_moi_cau_hoi(
                            loai_cau_hoi=loai,
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
        if cauhoi._kiemtra:
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
