from nicegui import ui

# Tạo một cái hộp (Card) có bo góc, đổ bóng xịn sò
with ui.card().classes('w-80 mx-auto my-10 p-6 shadow-xl rounded-2xl bg-slate-50'):
    ui.label('Bảng điều khiển nhỏ').classes('text-xl font-extrabold text-slate-700 mx-auto')

    # Xếp 2 cái nút nằm ngang
    with ui.row().classes('justify-center w-full gap-4 mt-4'):
        ui.button('Bật', color='green').classes('px-6 rounded-lg')
        ui.button('Tắt', color='red').classes('px-6 rounded-lg')

ui.run()
