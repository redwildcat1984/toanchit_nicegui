from cauhoi_tinhketqua import TinhKetQua
from cauhoi_dienchotrong import DienChoTrong

def tao_moi_cau_hoi(loai_cau_hoi:str, *args, **kwargs):
    if loai_cau_hoi == 'tinh_ket_qua':
        return TinhKetQua(loai_cau_hoi, *args, **kwargs)
    elif loai_cau_hoi == 'dien_cho_trong':
        return DienChoTrong(loai_cau_hoi, *args, **kwargs)
    raise ValueError(f'Không có loại câu hỏi {loai_cau_hoi}')
