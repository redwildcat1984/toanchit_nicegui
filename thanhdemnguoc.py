from typing import Callable

from nicegui import ui

class ThanhDemNguoc:
    def __init__(self, ham_het_gio:Callable|None = None) -> None:
        self.tong_thoi_gian:int
        self.thoi_gian_con_lai:int
        self.bo_dem_nguoc: ui.timer|None = None

        self.thanh_thoi_gian: ui.linear_progress|None = None
        self.nhan_thoi_gian: ui.label|None = None

        self.ham_het_gio = ham_het_gio

    def hienthi(self):
        with ui.row(align_items='center').classes('w-full rounded-xl p-4') as self.container_dem_nguoc:
            self.thanh_thoi_gian = ui.linear_progress(value=1, color='green', size='10px', show_value=False).classes('w-3/4 md:w-4/5 lg:w-6/7 rounded-full outline-3 outline-offset-1 outline-pink-300 grow')
            self.nhan_thoi_gian = ui.label('300s').classes('font-bold text-center text-lg text-yellow-500 min-w-[120px]')

    def batdau(self):
        ui.notify('Bat dau dem nguoc')
        self.thoi_gian_con_lai = self.tong_thoi_gian
        self.bo_dem_nguoc = ui.timer(1.0, self.giam_thoi_gian)
        self.bo_dem_nguoc.activate()

    def dung(self):
        if self.bo_dem_nguoc:
            self.bo_dem_nguoc.deactivate()

    def doi_kieu_thanh_thoi_gian(self):
        # Đổi màu thanh sang đỏ dần khi sắp hết giờ dưới 15 giây
        if not self.thanh_thoi_gian or not self.nhan_thoi_gian:
            return

        if self.thoi_gian_con_lai == 0:
            # self.container_dem_nguoc.set_visibility(False)
            self.container_dem_nguoc.clear()
            self.container_dem_nguoc = ui.label('HẾT GIỜ').classes('text-4xl text-yellow-300 font-bold text-center bg-orange-500/30 py-4')
        elif self.thoi_gian_con_lai <= self.tong_thoi_gian/5:
            self.thanh_thoi_gian.props('color="red" size="30px"').classes(replace='w-3/4 md:w-4/5 lg:w-6/7 rounded-full outline-3 outline-offset-1 outline-yellow-500 grow')
            self.nhan_thoi_gian.classes(replace='font-bold text-2xl text-red-500 text-center min-w-[120px]')
        elif self.thoi_gian_con_lai <= self.tong_thoi_gian/2 and self.thoi_gian_con_lai > self.tong_thoi_gian/5:
            self.thanh_thoi_gian.props('color="orange" size="20px"').classes(replace='w-3/4 md:w-4/5 lg:w-6/7 rounded-full outline-3 outline-offset-1 outline-cyan-300 grow')
            self.nhan_thoi_gian.classes(replace='font-bold text-xl text-orange-500 text-center min-w-[120px]')
        else:
            self.thanh_thoi_gian.props('color="green" size="10px"').classes(replace='w-3/4 md:w-4/5 lg:w-6/7 rounded-full outline-3 outline-offset-1 outline-pink-300 grow')
            self.nhan_thoi_gian.classes(replace='font-bold text-center text-lg text-yellow-500 min-w-[120px]')

    def giam_thoi_gian(self):
        if self.thoi_gian_con_lai > 0:
            self.thoi_gian_con_lai -= 1

            # Cập nhật thanh thời gian và nhãn thời gian
            if self.thanh_thoi_gian and self.nhan_thoi_gian:
                self.nhan_thoi_gian.set_text(f'{self.thoi_gian_con_lai} s')

                tyle = self.thoi_gian_con_lai/self.tong_thoi_gian
                self.thanh_thoi_gian.set_value(tyle)

            # Gọi hàm đổi kiểu thanh thời gian theo thời gian còn lại
            self.doi_kieu_thanh_thoi_gian()
        else:
            if self.ham_het_gio:
                self.ham_het_gio()
            self.dung()
