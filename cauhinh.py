from nicegui import ui

from json_connect import JsonConnect

class CauHinh:
    def __init__(self) -> None:
        self._tu: int = 0
        self._den: int = 10
        self._socau: int = 10
        self.mangsocau: list = [10, 20, 30]
        self.thongtin: str|None = None
        self.dialog: ui.dialog|None = None
        self.json: JsonConnect = JsonConnect()
        self.json.path = 'cauhinh.json'

    def nap_cau_hinh(self):
        kq = self.json.load()
        if kq and self.json.data is not None:
            self._tu = self.json.data.get('tu', 0)
            self._den = self.json.data.get('den', 0)
            self._socau = self.json.data.get('socau', 0)
            ui.notify('Đã nạp dữ liệu cấu hình', color='green', type='positive')
        else:
            ui.notify('Nạp cấu hình không thành công. Có thể là sai đường dẫn hoặc file không tồn tại', color='orange', type='info')

    def luu_cau_hinh(self):
        self.json.data = {'tu': self._tu, 'den': self._den, 'socau': self._socau}
        kq = self.json.save()
        if kq:
            ui.notify('Lưu cấu hình thành công', color='green', type='positive')
        else:
            ui.notify('Lưu cấu hình không thành công', color='red', type='negative')

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
                ui.radio(self.mangsocau, on_change=self.hien_thong_tin).bind_value(self, '_socau').props('inline')
            ui.label().bind_text_from(self, 'thongtin')
            self.hien_thong_tin()
        # self.dialog.on('dismiss', self.luu_cau_hinh)
        return self.dialog

    def hien_thong_tin(self):
        if self._tu > self._den:
            self.thongtin = 'Số trước không được lớn hơn số sau'
        else:
            self.thongtin = f'Từ {int(self._tu)} đến {int(self._den)}. Mỗi bài có {int(self._socau)} câu hỏi'

    # Mở dialog thay đổi cấu hình
    def open(self):
        if self.dialog:
            self.dialog.open()

    def close(self):
        if self.dialog and self.dialog.value == 0:
            self.luu_cau_hinh()
