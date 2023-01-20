import gspread
import csv

sa = gspread.service_account()
sh = sa.open("STOCK")
wks = sh.worksheet("Sheet1")

def main():
    is_stock("[['Iphone X 64gb']]")


def is_stock(phone):
    iphone = f"[['{phone}']]"
    for i in range(1,18):
        if str(wks.get(f'A{str(i)}')) == iphone:
            if str(wks.get(f'D{str(i)}')) == 0:
                return False
            else:
                return True
def is_color(color,phone):
    colors = f"[['{color}']]"
    for i in range(1,18):
        print(phone," ",str(wks.get(f'A{str(i)}')))
        if str(phone) in str(wks.get(f'A{str(i)}')):
            if colors in str(wks.get(f'E{str(i)}')):
                return True
            else:
                return False
def is_battery(battery,phone):
    batteries = f"[['{battery}']]"
    for i in range(1,18):
        print(phone)
        if str(phone) in str(wks.get(f'A{str(i)}')):
            if batteries in str(wks.get(f'F{str(i)}')):
                return str(wks.get(f'F{str(i)}'))
            else:
                return "80%"
def is_pesos(phone,gb):
    for i in range(1,18):
        if str(phone) in str(wks.get(f'A{str(i)}')):
            if gb in str(wks.get(f'B{str(i)}')):
                pesos = str(wks.acell(f'G{str(i)}').value)
                return pesos
            else:
                pass
    return "no"

def gb_get(phone,gb):
    for i in range(1,18):
        if str(phone) in str(wks.get(f'A{str(i)}')):
            if gb in str(wks.get(f'B{str(i)}')):
                price = str(wks.acell(f'C{str(i)}').value)
                return price
            else:
                pass
    return "no"


if "__main__" == __name__:
    main()