from nicegui import ui
from cauhinh import CauHinh

cauhinh = CauHinh()
cauhinh.nap_cau_hinh()
cauhinh.build_ui()

def row_evenly():
    """Tạo một hàng dàn đều tuyệt đối mà không cần nhớ class"""
    return ui.row().classes('w-full justify-evenly items-center')

def vecauhoi():
    if not vungcauhoi:
        return
    vungcauhoi.clear()
    with vungcauhoi:
        for i in range(cauhinh._socau):
            ui.button(f'Button_{i+1}', on_click=click)

def click(e):
    ui.notify(f'Dang click nut {e.sender.text}')



with ui.header():
    with ui.row(align_items='center').classes('w-full justify-evenly'):
        ui.linear_progress(value= 0.5, size= '15px', show_value=True, color='red').classes('w-3/5 rounded-full')
        ui.button('Cấu hình', on_click=cauhinh.open)
        ui.button('Tạo mới', on_click=vecauhoi)

vungcauhoi = ui.grid().classes('grid grid-cols-4 gap-5 w-full justify-evenly items-center w-full grow bg-gray-100 mt-3')


with ui.footer():
     with ui.row(align_items='center').classes('w-full justify-evenly'):
        ui.label('Danh cho chi Chit hoc toan')
        ui.label('v 0.1')
        ui.label('Trinh Quang Tuan')




ui.run(language='vi')
