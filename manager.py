import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

# Tạo hoặc kết nối với database SQLite
conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute('''
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_name TEXT,
    fingerprints TEXT,
    acc_fb TEXT,
    proxy TEXT
)
''')

conn.commit()

# Hàm thêm profile mới
def add_profile():
    profile_name = entry_profile.get()
    fingerprints = entry_fingerprints.get()
    acc_fb = entry_acc_fb.get()
    proxy = entry_proxy.get()

    if profile_name and fingerprints and acc_fb and proxy:
        cursor.execute("INSERT INTO profiles (profile_name, fingerprints, acc_fb, proxy) VALUES (?, ?, ?, ?)", 
                       (profile_name, fingerprints, acc_fb, proxy))
        conn.commit()
        load_profiles()
        clear_entries()
    else:
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng điền đầy đủ thông tin")

# Hàm xóa profile theo id
def delete_profile():
    selected_item = tree.selection()
    if selected_item:
        profile_id = tree.item(selected_item)['values'][0]
        cursor.execute("DELETE FROM profiles WHERE id=?", (profile_id,))
        conn.commit()
        load_profiles()

# Hàm tải danh sách profile
def load_profiles():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM profiles")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

# Hàm xóa các trường input sau khi thêm
def clear_entries():
    entry_profile.delete(0, 'end')
    entry_fingerprints.delete(0, 'end')
    entry_acc_fb.delete(0, 'end')
    entry_proxy.delete(0, 'end')

# Tạo giao diện người dùng với ttkbootstrap
root = ttk.Window(themename="superhero")
root.title("Trình quản lý Profile")
root.geometry("800x600")

# Các label và entry cho profile, fingerprints, acc_fb, proxy
label_profile = ttk.Label(root, text="Profile:")
label_profile.grid(row=0, column=0, padx=10, pady=10)

entry_profile = ttk.Entry(root)
entry_profile.grid(row=0, column=1, padx=10, pady=10)

label_fingerprints = ttk.Label(root, text="Fingerprints:")
label_fingerprints.grid(row=1, column=0, padx=10, pady=10)

entry_fingerprints = ttk.Entry(root)
entry_fingerprints.grid(row=1, column=1, padx=10, pady=10)

label_acc_fb = ttk.Label(root, text="Acc FB:")
label_acc_fb.grid(row=2, column=0, padx=10, pady=10)

entry_acc_fb = ttk.Entry(root)
entry_acc_fb.grid(row=2, column=1, padx=10, pady=10)

label_proxy = ttk.Label(root, text="Proxy:")
label_proxy.grid(row=3, column=0, padx=10, pady=10)

entry_proxy = ttk.Entry(root)
entry_proxy.grid(row=3, column=1, padx=10, pady=10)

# Button thêm và xóa profile
btn_add = ttk.Button(root, text="Thêm Profile", command=add_profile, bootstyle=SUCCESS)
btn_add.grid(row=4, column=0, padx=10, pady=10)

btn_delete = ttk.Button(root, text="Xóa Profile", command=delete_profile, bootstyle=DANGER)
btn_delete.grid(row=4, column=1, padx=10, pady=10)

# Bảng hiển thị danh sách profile
columns = ("ID", "Profile", "Fingerprints", "Acc FB", "Proxy")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Profile", text="Profile")
tree.heading("Fingerprints", text="Fingerprints")
tree.heading("Acc FB", text="Acc FB")
tree.heading("Proxy", text="Proxy")

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Tải dữ liệu ban đầu
load_profiles()

root.mainloop()
