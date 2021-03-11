import xlsxwriter
import datetime

message = "0-12-13-0-0-6"
edit_message = message.split("-")
print(edit_message[0])
print(edit_message[1])
print(edit_message[2])
print(edit_message[3])
print(edit_message[4])
print(edit_message[5])

workbook = xlsxwriter.Workbook(f'{datetime.date.today()}.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('B1', f'{datetime.date.today()}')

worksheet.write('A2', 'ОРЗ')
worksheet.write('A3', 'Ковид')
worksheet.write('A4', 'Пневмония')
worksheet.write('A5', 'По не ув. пр.')
worksheet.write('A6', 'По ув. пр.')
worksheet.write('A7', 'По приказу')

worksheet.write('B2', f'{edit_message[0]}')
worksheet.write('B3', f'{edit_message[1]}')
worksheet.write('B4', f'{edit_message[2]}')
worksheet.write('B5', f'{edit_message[3]}')
worksheet.write('B6', f'{edit_message[4]}')
worksheet.write('B7', f'{edit_message[5]}')

workbook.close()