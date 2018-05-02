import win32com.client

excel = win32com.client.Dispatch("Excel.Application")
excel.visible = True
wb = excel.workbooks.Add()
ws = wb.Worksheets("sheet1")
ws.Cells(2, 4).value = "Hello COM"
