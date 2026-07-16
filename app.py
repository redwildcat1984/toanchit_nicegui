from turtle import onclick

from nicegui import ui
from cauhinh import CauHinh
from cauhoi import BaiTap

cauhinh = CauHinh()
cauhinh.nap_cau_hinh()
cauhinh.build_ui()

# Trạng thái các nút
nut_tao_moi: ui.button|None = None
nut_nop_bai: ui.button|None = None

# Trạng thái bài tập
bai_tap_hien_tai: BaiTap|None = None

# Bộ đếm thời gian làm bài (đơn vị: giây)
TONG_THOI_GIAN = 600
thoi_gian_con_lai = TONG_THOI_GIAN
timer_dem_nguoc: ui.timer|None = None

# Thanh tiến trình
thanh_thoi_gian: ui.linear_progress|None = None
nhan_thoi_gian: ui.label|None = None

def row_evenly():
    """Tạo một hàng dàn đều tuyệt đối mà không cần nhớ class"""
    return ui.row().classes('w-full justify-evenly items-center')

def vecauhoi():
    global bai_tap_hien_tai, nut_nop_bai, nut_tao_moi, timer_dem_nguoc, thoi_gian_con_lai

    if not vungcauhoi:
        return
    vungcauhoi.clear()

    # Reset thời gian về ban đầu khi bấm nút tạo mới
    thoi_gian_con_lai = TONG_THOI_GIAN
    if thanh_thoi_gian:
        thanh_thoi_gian.set_value(1.0)
    if nhan_thoi_gian:
        nhan_thoi_gian.set_text(f'{thoi_gian_con_lai}')

    # Tắt timer cũ nếu có trước khi chạy cái mới
    if timer_dem_nguoc:
        timer_dem_nguoc.deactivate()

    with vungcauhoi:
        bai_tap_hien_tai = BaiTap()
        bai_tap_hien_tai.hienthi()

    if nut_tao_moi:
        nut_tao_moi.set_visibility(False)
    if nut_nop_bai:
        nut_nop_bai.set_visibility(True)

    timer_dem_nguoc = ui.timer(1.0, giam_thoi_gian)

def giam_thoi_gian():
    global thoi_gian_con_lai, timer_dem_nguoc

    if thoi_gian_con_lai > 0:
        thoi_gian_con_lai -= 1
        # Cập nhật nhãn hiển thị chữ
        if nhan_thoi_gian:
            nhan_thoi_gian.set_text(f"Còn lại: {thoi_gian_con_lai}s")

        # Cập nhật thanh progress chạy lùi về 0
        if thanh_thoi_gian:
            ty_le = thoi_gian_con_lai / TONG_THOI_GIAN
            thanh_thoi_gian.set_value(ty_le)

            # Đổi màu thanh sang đỏ dần khi sắp hết giờ dưới 15 giây
            if thoi_gian_con_lai <= 15:
                thanh_thoi_gian.props('color="red"')
            else:
                thanh_thoi_gian.props('color="primary"') # Màu xanh mặc định
    else:
        # KHI HẾT GIỜ (Thời gian về 0)
        if timer_dem_nguoc:
            timer_dem_nguoc.deactivate() # Dừng bộ đếm

        ui.notify('⌛ Đã hết thời gian làm bài!', type='warning')
        nopbai()

def nopbai():
    global timer_dem_nguoc
    # Nếu bấm nộp bài thủ công trước khi hết giờ, hãy dừng bộ đếm thời gian lại
    if timer_dem_nguoc:
        timer_dem_nguoc.deactivate()

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
        thanh_thoi_gian = ui.linear_progress(value=1.0, size='10px', color='red', show_value=False).classes('w-1/2 md:w-3/5 lg:w-3/4 rounded-full')
        nhan_thoi_gian = ui.label(f"{thoi_gian_con_lai} s").classes('font-bold text-base text-lg min-w-[120px]')
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
