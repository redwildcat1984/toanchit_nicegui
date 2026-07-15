from nicegui import ui

from json_connect import JsonConnect

class CauHinh:
    def __init__(self) -> None:
        self._tu: int = 0
        self._den: int = 10
        self._socauhoi: int = 10
        self._mangpheptinh = ['+', '-', '*', '/']
        self._pheptinh:list = []
        self._sopheptinh:int = 2
        self._ketquaam:bool = False
        self.mangsocau: list = [10, 20, 30]
        self.thongtin: str|None = None
        self.dialog: ui.dialog|None = None
        self.json: JsonConnect = JsonConnect(path='cauhinh.json')

    def nap_cau_hinh(self):
        kq = self.json.load()
        if kq and self.json.data is not None:
            self._tu = self.json.data.get('tu', 0)
            self._den = self.json.data.get('den', 0)
            self._socauhoi = self.json.data.get('socauhoi', 0)
            self._pheptinh = self.json.data.get('pheptinh', ['+', '-'])
            self._sopheptinh = self.json.data.get('sopheptinh', 2)
            self._ketquaam = self.json.data.get('ketquaam', False)
            # ui.notify('Đã nạp dữ liệu cấu hình', color='green', type='positive')
        # else:
            # ui.notify('Nạp cấu hình không thành công. Có thể là sai đường dẫn hoặc file không tồn tại', color='orange', type='info')

    def luu_cau_hinh(self):
        self.json.data = {'tu': self._tu, 'den': self._den, 'socauhoi': self._socauhoi, 'sopheptinh': self._sopheptinh, 'pheptinh': self._pheptinh, 'ketquaam': self._ketquaam}
        kq = self.json.save()
        if kq:
            ui.notify('Lưu cấu hình thành công', color='green', type='positive')
        else:
            ui.notify('Lưu cấu hình không thành công', color='red', type='negative')

    def cap_nhat_phep_tinh(self, phep_tinh:str, duoc_chon:bool|None):
        if len(self._pheptinh) < 1:
            ui.notify('Bắt buộc phải chọn một phép tính. Không thể loại bỏ phép tính này', type='negative', color='red')
            duoc_chon = True
            return
        else:
            if duoc_chon:
                if phep_tinh not in self._pheptinh:
                    self._pheptinh.append(phep_tinh)
                    ui.notify(f'Đã thêm phép tính {phep_tinh} vào danh sách', type='positive', color='green')
            else:
                if phep_tinh in self._pheptinh:
                    self._pheptinh.remove(phep_tinh)
                    ui.notify(f'Đã loại bỏ phép tính {phep_tinh} khỏi danh sách', type='warning', color='orange')

    def build_ui(self):
        if self.dialog:
            return self.dialog
        with ui.dialog().on_value_change(self.close) as self.dialog, ui.card(align_items='start'):
            with ui.row(align_items='center'):
                ui.label('Nhập khoảng số')
                ui.number('Từ', on_change=self.hien_thong_tin).bind_value(self,'_tu')
                ui.number('đến', on_change=self.hien_thong_tin).bind_value(self, '_den')
            with ui.row(align_items='center'):
                ui.label('Số câu hỏi mỗi bài')
                ui.radio(self.mangsocau, on_change=self.hien_thong_tin).bind_value(self, '_socauhoi').props('inline')
            ui.number('Số phép tính').bind_value(self, '_sopheptinh')
            ui.checkbox('Kết quả âm').bind_value(self,'_ketquaam')

            # Danh sách các checkbox cho phép chọn phép tính, tích chọn nếu có trong danh sách self._pheptinh
            with ui.row(align_items='center').classes('gap-4'):
                for i in self._mangpheptinh:
                    dangchon = i in self._pheptinh
                    ui.checkbox(f'Phép "{i}"', value=dangchon, on_change=lambda e, p=i:self.cap_nhat_phep_tinh(p, e.value))

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
