# reports/report_generator.py
import sqlite3
import json
from datetime import datetime
from reportlab.pdfgen import canvas
from openpyxl import Workbook

def generate_pdf_report():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    rows = cursor.fetchall()

    c = canvas.Canvas("reports/bookshelf_analysis_report.pdf")
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, "Отчёт по анализу заполняемости книжного шкафа")
    c.drawString(50, 780, f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.drawString(50, 760, "-" * 60)

    y = 740
    for row in rows:
        data = json.loads(row[2])
        line = f"{row[1]} | Найдено книг: {data['count']}"
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = 800

    c.save()
    print("PDF-отчёт сохранён: reports/bookshelf_analysis_report.pdf")

def generate_excel_report():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    rows = cursor.fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "Анализ книжного шкафа"
    ws.append(["ID", "Время", "Количество книг"])

    for row in rows:
        data = json.loads(row[2])
        ws.append([row[0], row[1], data['count']])

    wb.save("reports/bookshelf_analysis_report.xlsx")
    print("Excel-отчёт сохранён: reports/bookshelf_analysis_report.xlsx")

if __name__ == "__main__":
    generate_pdf_report()
    generate_excel_report()