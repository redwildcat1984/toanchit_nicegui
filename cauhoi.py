import random
from nicegui import ui

MANG_PHEP_TINH = {'cong': '+', 'tru': '-', 'nhan': '*', 'chia': '/'}

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
        self._kiemtra:bool|None = None
        self.label_kiem_tra:ui.label|None = None
        self._traloi:int|None = None
        self.nhap_tra_loi:ui.number|None = None

        self.mang_so:list = []
        self.mang_phep_tinh:list = []

    def hien_thi(self):
        """Hàm trừu tượng, các class con bắt buộc phải tự định nghĩa cách vẽ"""
        raise NotImplementedError("Class con phải tự triển khai hàm hien_thi")

    def kiem_tra_ket_qua(self):
        """Hàm trừu tượng, các class con bắt buộc phải tự định nghĩa cách vẽ"""
        raise NotImplementedError("Class con phải tự triển khai hàm kiem_tra_ket_qua")

    def doi_chu_thanh_ky_hieu_phep_tinh(self, ten_phep_tinh:str):
        return MANG_PHEP_TINH[ten_phep_tinh]

    def hien_thi_ket_qua(self):
        if not self.label_kiem_tra or self._kiemtra is None:
            return
        if self._kiemtra:
            self.label_kiem_tra.set_text("✅")
        else:
            self.label_kiem_tra.set_text("❌")
        # Đặt class hiện dần cho icon kiểm tra
        self.label_kiem_tra.classes('fade-in-3s')

    def hetgio(self):
        if self.nhap_tra_loi:
            self.nhap_tra_loi.disable()

    def tao_cau_hoi(self):
        # ui.notify('Đang tạo câu hỏi...', type='info')
        self._cauhoi = ""
        self.mang_so = []
        self.mang_phep_tinh = []

        for i in range(int(self._sopheptinh) + 1):
            so = random.randint(self._tu, self._den)
            self._cauhoi += str(so)
            self.mang_so.append(so)
            if i < self._sopheptinh:
                pt = self.doi_chu_thanh_ky_hieu_phep_tinh(random.choice(self._pheptinh))
                self._cauhoi += f' {pt} '
                self.mang_phep_tinh.append(pt)
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
