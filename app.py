from turtle import onclick

from nicegui import ui
from cauhinh import CauHinh
from cauhoi import BaiTap

cauhinh = CauHinh()
cauhinh.nap_cau_hinh()
cauhinh.build_ui()

nut_tao_moi: ui.button|None = None
nut_nop_bai: ui.button|None = None
bai_tap_hien_tai: BaiTap|None = None

def row_evenly():
    """Tạo một hàng dàn đều tuyệt đối mà không cần nhớ class"""
    return ui.row().classes('w-full justify-evenly items-center')

def vecauhoi():
    global bai_tap_hien_tai, nut_nop_bai, nut_tao_moi
    if not vungcauhoi:
        return
    vungcauhoi.clear()
    with vungcauhoi:
        bai_tap_hien_tai = BaiTap()
        bai_tap_hien_tai.hienthi()

    if nut_tao_moi:
        nut_tao_moi.set_visibility(False)
    if nut_nop_bai:
        nut_nop_bai.set_visibility(True)

def nopbai():
    if bai_tap_hien_tai is None:
        ui.notify('Vui lòng bấm "Tạo mới" để làm bài trước nhé!', type='warning')
        return

    # Tiến hành chấm điểm toàn bộ
    bai_tap_hien_tai.cham_diem_toan_bo()

    # # Tính điểm hệ số 10 hoặc hiển thị lời khen cho bé Chit
    # diem_so = round((dung / tong) * 10, 1) if tong > 0 else 0

    # if dung == tong:
    #     ui.notify(f'🎉 Xuất sắc quá Chit ơi! Đúng {dung}/{tong} câu. Đạt điểm 10 tuyệt đối!', type='positive', duration=5)
    # elif dung >= tong / 2:
    #     ui.notify(f'👍 Khá lắm Chit! Đúng {dung}/{tong} câu. Đạt {diem_so} điểm. Cố gắng lên nhé!', type='info', duration=5)
    # else:
    #     ui.notify(f'💪 Chit đúng {dung}/{tong} câu ({diem_so} điểm). Lần sau mình làm cẩn thận hơn nhé!', type='warning', duration=5)

    if nut_tao_moi:
        nut_tao_moi.set_visibility(True)
    if nut_nop_bai:
        nut_nop_bai.set_visibility(False)

with ui.header():
    with ui.row(align_items='center').classes('w-full justify-evenly'):
        ui.linear_progress(value= 0.5, size= '15px', show_value=True, color='red').classes('w-3/5 rounded-full')
        ui.button('Cấu hình', on_click=cauhinh.open)
        nut_tao_moi = ui.button('Tạo mới', on_click=vecauhoi)
        nut_nop_bai = ui.button('Nộp bài', on_click=nopbai, color='green')
        nut_nop_bai.set_visibility(False)

vungcauhoi = ui.element().classes('w-full mt-3 p-4')

with ui.footer():
     with ui.row(align_items='center').classes('w-full justify-evenly'):
        ui.label('Danh cho chi Chit hoc toan')
        ui.label('v 0.1')
        ui.label('Trinh Quang Tuan')

ui.run()
