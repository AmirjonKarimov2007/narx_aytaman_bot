import win32com.client

# Hujjat manzili
file_path = r"C:\Users\user\Documents\narx_chiqarbot-main\bot\aaa.docx"

# Word dasturini ishga tushiramiz
word = win32com.client.Dispatch("Word.Application")

# Hujjatni ochamiz
doc = word.Documents.Open(file_path)

for _ in range(3):
    doc.PrintOut()

# Hujjatni yopamiz va Word dasturini o‘chiramiz
doc.Close(False)
word.Quit()

print("Hujjat 3 nusxada chop etildi!")
