from nicegui import ui

nhan_thong_bao = ui.label('He thong hoat dong on dinh...').classes('text-green-500')

def bao_loi(nhan):
    nhan.set_text('He thong loi...')
    nhan.classes(replace = 'text-red-500 font-bold')

ui.button('Hien loi', on_click=lambda: bao_loi(nhan_thong_bao))

ui.run()
