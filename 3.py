from nicegui import ui

# Tạo một dictionary thuần Python để lưu dữ liệu dữ liệu tính toán
du_lieu = {'so_a': 0, 'ket_qua': 0}

def tinh_binh_phuong():
    # Chỉ tính toán trên data thuần Python, không đụng vào UI
    du_lieu['ket_qua'] = du_lieu['so_a'] ** 2

ui.label('--- Test Data Binding ---').classes('text-lg font-bold mt-4')

# Trói (bind) giá trị ô nhập với du_lieu['so_a']
# Mỗi khi người dùng nhập số, nó sẽ tự gọi hàm tính toán
ui.number('Nhập một số', value=0, on_change=tinh_binh_phuong).bind_value(du_lieu, 'so_a')

# Trói chữ hiển thị của label với du_lieu['ket_qua']
ui.label().bind_text_from(du_lieu, 'ket_qua', backward=lambda x: f'Bình phương là: {x}')

ui.run()
