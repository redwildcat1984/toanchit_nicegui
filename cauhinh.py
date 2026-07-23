from nicegui import ui

from json_connect import JsonConnect

from giatri_codinh import CAU_HOI, PHEP_TINH

class CauHinh:
    def __init__(self) -> None:
        self._mangpheptinh = PHEP_TINH
        self.mangsocau: list = [10, 20, 30]
        self.mangloaicauhoi:dict = CAU_HOI

        self._tu: int = 0
        self._den: int = 10

        self._socauhoi: int = 10
        self._pheptinh:list = ['cong']
        self._sopheptinh:int = 2
        self._ketquaam:bool = False
        self._batthoigian:bool = True
        self._thoigian:int = 60
        self.thongtin: str|None = None
        self.dialog: ui.dialog|None = None
        self.json: JsonConnect = JsonConnect(path='cauhinh.json')
        self._loaicauhoi:list = ['tinh_ket_qua']

        # Biến lưu các checkbox và trạng thái của nó để điều khiển
        self.cac_cau_hoi = {}
        self.cac_phep_tinh = {}

    def nap_cau_hinh(self):
        kq = self.json.load()
        if kq and self.json.data is not None:
            self._tu = int(self.json.data.get('tu', 0))
            self._den = int(self.json.data.get('den', 0))
            self._socauhoi = int(self.json.data.get('socauhoi', 0))
            self._loaicauhoi = self.json.data.get('loaicauhoi', ['tinh_ket_qua'])
            self._pheptinh = self.json.data.get('pheptinh', ['+', '-'])
            self._sopheptinh = int(self.json.data.get('sopheptinh', 2))
            self._ketquaam = self.json.data.get('ketquaam', False)
            self._batthoigian = self.json.data.get('batthoigian', True)
            self._thoigian = int(self.json.data.get('thoigian', 60))
            # ui.notify('Đã nạp dữ liệu cấu hình', color='green', type='positive')
        # else:
            # ui.notify('Nạp cấu hình không thành công. Có thể là sai đường dẫn hoặc file không tồn tại', color='orange', type='info')

    def luu_cau_hinh(self):
        self.json.data = {'tu': self._tu, 'den': self._den, 'socauhoi': self._socauhoi, 'loaicauhoi': self._loaicauhoi, 'sopheptinh': self._sopheptinh, 'pheptinh': self._pheptinh, 'ketquaam': self._ketquaam, 'batthoigian': self._batthoigian, 'thoigian': self._thoigian}
        kq = self.json.save()
        if kq:
            ui.notify('Lưu cấu hình thành công', color='green', type='positive')
        else:
            ui.notify('Lưu cấu hình không thành công', color='red', type='negative')

    def cap_nhat_phep_tinh(self, duoc_chon:bool|None, phep_tinh:str):
        if not duoc_chon:
            if len(self._pheptinh)<=1 and phep_tinh in self._pheptinh:
                self.cac_phep_tinh[phep_tinh].value = True
                ui.notify('Phải chọn ít nhất một loại phép tính!', type='warning')
                return
        if not duoc_chon and phep_tinh in self._pheptinh:
            self._pheptinh.remove(phep_tinh)
        if duoc_chon and phep_tinh not in self._pheptinh:
            self._pheptinh.append(phep_tinh)
        ui.notify(f'{self._pheptinh}', type='info')


    def cap_nhat_loai_cau_hoi(self, duoc_chon:bool|None, loai_cau_hoi:str):
        if not duoc_chon:
            if len(self._loaicauhoi)<=1 and loai_cau_hoi in self._loaicauhoi:
                self.cac_cau_hoi[loai_cau_hoi].value = True
                ui.notify('Chít phải học ít nhất 1 loại toán chứ ba!', type='warning')
                return
        if not duoc_chon and loai_cau_hoi in self._loaicauhoi:
            self._loaicauhoi.remove(loai_cau_hoi)
        if duoc_chon and loai_cau_hoi not in self._loaicauhoi:
            self._loaicauhoi.append(loai_cau_hoi)
        ui.notify(f'{self._loaicauhoi}', type='info')

    def build_ui(self):
        if self.dialog:
            return self.dialog
        with ui.dialog().on_value_change(self.close) as self.dialog, ui.card(align_items='start').classes('p-6'):
            with ui.row(align_items='center'):
                # Nhập khoảng số trong câu hỏi
                ui.label('Nhập khoảng số')
                ui.number('Từ', on_change=self.hien_thong_tin).bind_value(self,'_tu')
                ui.number('đến', on_change=self.hien_thong_tin).bind_value(self, '_den')

                # Chọn loại câu hỏi đưa vào danh sách
                with ui.row(align_items='center').classes('gap-4'):
                    for k, v in self.mangloaicauhoi.items():
                        chon = k in self._loaicauhoi
                        self.cac_cau_hoi[k] = ui.checkbox(text=v.title(), value=chon, on_change=lambda e, p=k: self.cap_nhat_loai_cau_hoi(e.value, p))

            with ui.row(align_items='center'):
                ui.label('Số câu hỏi mỗi bài')
                ui.radio(self.mangsocau, on_change=self.hien_thong_tin).bind_value(self, '_socauhoi').props('inline')
            ui.number('Số phép tính').bind_value(self, '_sopheptinh')
            ui.checkbox('Kết quả âm').bind_value(self,'_ketquaam')

            # Danh sách các checkbox cho phép chọn phép tính, tích chọn nếu có trong danh sách self._pheptinh
            with ui.row(align_items='center').classes('gap-4'):
                for k, v in self._mangpheptinh.items():
                    chon = k in self._pheptinh
                    self.cac_phep_tinh[k] = ui.checkbox(text=f'Phép " {v.title()} "', value=chon, on_change=lambda e, p=k: self.cap_nhat_phep_tinh(e.value, p))

            # Tùy chọn thời gian
            with ui.row(align_items='center'):
                ui.checkbox('Bật thời gian').bind_value(self, '_batthoigian')
                ui.number('Thời gian làm bài').bind_value(self, '_thoigian')

            # Hiển thị thông tin đã chọn
            ui.label().bind_text_from(self, 'thongtin')
            self.hien_thong_tin()
        # self.dialog.on('dismiss', self.luu_cau_hinh)
        # return self.dialog

    def hien_thong_tin(self):
        if self._tu > self._den:
            self.thongtin = 'Số trước không được lớn hơn số sau'
        else:
            self.thongtin = f'Từ {int(self._tu)} đến {int(self._den)}. Mỗi bài có {int(self._socauhoi)} câu hỏi'

    # Mở dialog thay đổi cấu hình
    def open(self):
        if self.dialog:
            self.dialog.open()

    def close(self):
        if self.dialog and self.dialog.value == 0:
            if self._pheptinh == []:
                self._pheptinh.append('+')
            self.luu_cau_hinh()
