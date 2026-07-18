from nicegui import ui

import os

from cauhinh import CauHinh
from cauhoi import BaiTap
from thanhdemnguoc import ThanhDemNguoc

# Tạo màu nền chung
ui.query('.q-page').style('background-color: #4f1e08;')

# Thêm hiệu ứng hiện dần
ui.add_head_html('''
<style>
@keyframes hienDanNhe {
    from { opacity: 0; }
    to { opacity: 1; }
}
.fade-in-3s {
    animation: hienDanNhe 3.0s ease-in-out forwards;
}
.fade-in-2s {
    animation: hienDanNhe 2.0s ease-in-out forwards;
}
.fade-in-1s {
    animation: hienDanNhe 1.0s ease-in-out forwards;
}
</style>
''')

# Khởi tạo các thành phần giao diện trên trang chủ
cauhinh = CauHinh()
cauhinh.nap_cau_hinh()
cauhinh.build_ui()

bai_tap_hien_tai:BaiTap|None = None
thanh_dem_nguoc:ThanhDemNguoc|None = None

# Hàm vẽ nội dung trang
def taomoi():
    global bai_tap_hien_tai, thanh_dem_nguoc

    if not vungthongbao or not vungcauhoi:
        return
    else:
        # Nạp cấu hình mới để đảm bảo lấy được cấu hình mới nhất
        cauhinh.nap_cau_hinh()

        # Tạo các thành phần giao diện cần thiết
        bai_tap_hien_tai = BaiTap()
        thanh_dem_nguoc = ThanhDemNguoc(ham_het_gio=hoanthanh)

        # Ẩn nút tạo bài mới và hiển thị nút Hoàn thành
        nut_hoan_thanh.set_visibility(True)
        nut_tao_moi.set_visibility(False)

        # Xóa các vùng thông báo và vùng câu hỏi
        vungthongbao.clear()
        vungcauhoi.clear()
        vungcauhoi.classes(replace='w-full px-4')

        # Tạo nội dung vào các vùng
        with vungthongbao:
            if cauhinh._batthoigian:
                thanh_dem_nguoc.tong_thoi_gian = cauhinh._thoigian
                thanh_dem_nguoc.hienthi()
                thanh_dem_nguoc.batdau()
        with vungcauhoi:
            bai_tap_hien_tai.hienthi()

def hoanthanh():
    global bai_tap_hien_tai, thanh_dem_nguoc

    # Khóa vùng câu hỏi để ngăn nhập thêm sau khi hết giờ
    # vungcauhoi.classes(replace='w-full px-4 pointer-events-none')

    if bai_tap_hien_tai:
        bai_tap_hien_tai.hetgio()
    # await asyncio.sleep(0.01)

    ui.notify('Đang chấm điểm...', type='positive', color='green')

    # await asyncio.sleep(0.01)

    # sleep(2)
    vungthongbao.clear()

    # Chấm điểm bài tập hiện tại
    if bai_tap_hien_tai:
        bai_tap_hien_tai.cham_diem_toan_bo()

    # Hiển thị nút tạo bài mới và ẩn nút Hoàn thành
    nut_hoan_thanh.set_visibility(False)
    nut_tao_moi.set_visibility(True)

# Giao diện chính
with ui.header().classes('justify-end'):
    nut_tao_moi = ui.button(icon='add', color='orange', on_click=taomoi).props('size="lg"').classes('rounded-xl')
    nut_hoan_thanh = ui.button(icon='done_all', color='green', on_click=hoanthanh).props('size="lg"').classes('rounded-xl')
    ui.button(icon='settings', color='brown', on_click=cauhinh.open).props('size="lg"').classes('rounded-xl')

    # Ẩn nút hoàn thành
    nut_hoan_thanh.set_visibility(False)


vungthongbao = ui.element().classes('w-full px-4 mb-2')
vungcauhoi = ui.element().classes('w-full px-4')

# Footer
with ui.footer().classes('w-full justify-evenly items-center'):
    ui.label('Tặng chị Chít').classes('text-pink-500 font-bold text-xl')
    ui.label('v 1.0')
    ui.label('Ba Tuấn yêu quái').classes('italic')

port = int(os.environ.get("PORT", 8080))
ui.run(host='0.0.0.0', port=port, reload=True, storage_secret='trinhquangtuanlabayeuquai', title='App toán cho chị Chít')
