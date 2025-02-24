import customtkinter as ctk
from googletrans import Translator

translator = Translator()

def translate_text():
    text = text_input.get("1.0", ctk.END).strip()
    if not text:
        ctk.CTkMessageBox.showwarning("Предупреждение", "Введите текст для перевода.")
        return

    target_language = target_lang.get()
    try:
        translated = translator.translate(text, dest=target_language)
        result_output.delete("1.0", ctk.END)
        result_output.insert(ctk.END, translated.text)
    except Exception as e:
        ctk.CTkMessageBox.showerror("Ошибка", str(e))

# ctk.set_default_color_theme("theme/theme_1/theme.json")  

app = ctk.CTk()
app.title("Переводчик")
app.geometry("400x400")

text_input = ctk.CTkTextbox(app, height=10, width=300)
text_input.pack(pady=10)

target_lang = ctk.StringVar(value='ru')  
lang_frame = ctk.CTkFrame(app)
lang_frame.pack(pady=10)

ctk.CTkRadioButton(lang_frame, text="Русский", variable=target_lang, value='ru').pack(side=ctk.LEFT)
ctk.CTkRadioButton(lang_frame, text="Английский", variable=target_lang, value='en').pack(side=ctk.LEFT)
ctk.CTkRadioButton(lang_frame, text="Французский", variable=target_lang, value='fr').pack(side=ctk.LEFT)

translate_button = ctk.CTkButton(app, text="Перевести текст", command=translate_text)
translate_button.pack(pady=10)

result_output = ctk.CTkTextbox(app, height=10, width=300)
result_output.pack(pady=10)

app.mainloop()