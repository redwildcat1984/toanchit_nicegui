
from nicegui import ui
from cauhinh import CauHinh
from cauhoi import BaiTap

# Đổi màu nền toàn bộ app
ui.query('.q-page').style('background-color: #4f1e08;')

cauhinh = CauHinh()
cauhinh.nap_cau_hinh()
cauhinh.build_ui()

# Trạng thái các nút
nut_tao_moi: ui.button|None = None
nut_nop_bai: ui.button|None = None

# Trạng thái bài tập
bai_tap_hien_tai: BaiTap|None = None

# Bộ đếm thời gian làm bài (đơn vị: giây)
TONG_THOI_GIAN = 0
thoi_gian_con_lai = TONG_THOI_GIAN
timer_dem_nguoc: ui.timer|None = None

# Thanh tiến trình
thanh_thoi_gian: ui.linear_progress|None = None
nhan_thoi_gian: ui.label|None = None

def row_evenly():
    """Tạo một hàng dàn đều tuyệt đối mà không cần nhớ class"""
    return ui.row().classes('w-full justify-evenly items-center')

def vecauhoi():
    global bai_tap_hien_tai, nut_nop_bai, nut_tao_moi, timer_dem_nguoc, thoi_gian_con_lai, TONG_THOI_GIAN

    if not vungcauhoi:
        return
    vungcauhoi.clear()

    # Hiển thị thanh thời gian và reset về ban đầu
    the_thoi_gian.set_visibility(True)

    TONG_THOI_GIAN = cauhinh._thoigian
    thoi_gian_con_lai = TONG_THOI_GIAN
    if thanh_thoi_gian:
        thanh_thoi_gian.set_value(1.0)
    if nhan_thoi_gian:
        nhan_thoi_gian.set_text(f'{int(thoi_gian_con_lai)}')

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
        if thanh_thoi_gian and nhan_thoi_gian:
            nhan_thoi_gian.set_text(f"⌛ {thoi_gian_con_lai} s")
            ty_le = thoi_gian_con_lai / TONG_THOI_GIAN
            thanh_thoi_gian.set_value(ty_le)

            # Đổi màu thanh sang đỏ dần khi sắp hết giờ dưới 15 giây
            if thoi_gian_con_lai == 0:
                the_thoi_gian.set_visibility(False)
            elif thoi_gian_con_lai <= TONG_THOI_GIAN/5:
                thanh_thoi_gian.props('color="red" size="30px"').classes(replace='w-3/4 md:w-4/5 lg:w-6/7 rounded-full outline-3 outline-offset-1 outline-gray-700 grow')
                nhan_thoi_gian.classes(replace='font-bold text-2xl text-red-500 text-center min-w-[120px]')
            elif thoi_gian_con_lai <= TONG_THOI_GIAN/2 and thoi_gian_con_lai > TONG_THOI_GIAN/5:
                thanh_thoi_gian.props('color="orange" size="20px"').classes(replace='w-3/4 md:w-4/5 lg:w-6/7 rounded-full outline-3 outline-offset-1 outline-cyan-300 grow')
                nhan_thoi_gian.classes(replace='font-bold text-xl text-orange-500 text-center min-w-[120px]')
            else:
                thanh_thoi_gian.props('color="green" size="10px"').classes(replace='w-3/4 md:w-4/5 lg:w-6/7 rounded-full outline-3 outline-offset-1 outline-pink-300 grow')
                nhan_thoi_gian.classes(replace='font-bold text-center text-lg text-yellow-500 min-w-[120px]')
    else:
        # KHI HẾT GIỜ (Thời gian về 0)
        ui.notify('⌛ Đã hết thời gian làm bài!', type='warning')

        if timer_dem_nguoc:
            timer_dem_nguoc.deactivate() # Dừng bộ đếm

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
        nut_tao_moi = ui.button(icon='add', on_click=vecauhoi, color='orange').props('size="lg"')
        nut_nop_bai = ui.button(icon='done_all', on_click=nopbai, color='green').props('size="lg"')
        nut_nop_bai.set_visibility(False)

        ui.button(icon='settings', on_click=cauhinh.open, color='gray').props('size="lg"')

with ui.row(align_items='center').classes('w-full p-4 rounded-xl') as the_thoi_gian:
    thanh_thoi_gian = ui.linear_progress(value=1.0, show_value=False)
    nhan_thoi_gian = ui.label()

    the_thoi_gian.set_visibility(False)

with ui.element().classes('bg-brown-700 w-full grow'):
    vungcauhoi = ui.element().classes('w-full mt-3 p-4')

with ui.footer():
     with ui.row(align_items='center').classes('w-full justify-evenly'):
        ui.label('Danh cho chi Chit hoc toan')
        ui.label('v 0.1')
        ui.label('Trinh Quang Tuan')

ui.run()
