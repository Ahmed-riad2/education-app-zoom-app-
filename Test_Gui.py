import customtkinter as ctk

# 1. بنعمل النافذة الأساسية
app = ctk.CTk()
app.title("برنامجي الأول")
app.geometry("300x200")

# دالة بتشتغل لما ندوس على الزرار
def say_hello():
    label.configure(text="أهلاً بك في عالم البرمجة!")

# 2. بنعمل نص (Label)
label = ctk.CTkLabel(app, text="اضغط على الزرار")
label.pack(pady=20)

# 3. بنعمل زرار (Button) ونربطه بالدالة
button = ctk.CTkButton(app, text="دوس هنا", command=say_hello)
button.pack(pady=10)

# تشغيل البرنامج
app.mainloop()