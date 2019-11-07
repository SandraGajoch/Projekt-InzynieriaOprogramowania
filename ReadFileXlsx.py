import math
import xlrd

# Czyta plik z trscią zadania
file = open("task.txt")
# wypisuje tresc zadania do terminala
print(file.read())
print("==========================")

# Szuka pliku exela w danej sciezce
locationFileWithData = ('numberPython5.xlsx')

# Tworzy plik z wynikiem
newFile = open("result.txt", "w")

# Otwiera plik exel z danymi
wb = xlrd.open_workbook(locationFileWithData)

# ustawia wskaznik w pliku exel
sheet = wb.sheet_by_index(0)

# Wylicza i wypisuje a = (b + c)^2
for row in range(sheet.nrows) :
    valueB = sheet.cell_value(row, 0)
    print("b = " + str(valueB))

    valueC = sheet.cell_value(row, 1)
    print("c = " + str(valueC))

    result = math.pow((valueB + valueC), 2)
    print("a = " + str(result))
    print("==============================")

    # Zapisz wynik do pliku result.txt
    newFile.write(str(result))
    newFile.write("\n")

# Zamyka strumien do pliku z wybikiem
newFile.close()
