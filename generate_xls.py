# This program generates an XML from dictionary

 
import xlwt 
from xlwt import Workbook 
  
 
def xls_generator(dict_macros):
    # Workbook is created 
    wb = Workbook() 
      
    # add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet('Sheet 1') 
    total_count = 0
    i = 0
    sheet1.write(i, 0, "MACRO Name", xlwt.easyxf("align: wrap on, horiz left")) 
    sheet1.write(i, 1, "Count", xlwt.easyxf("align: wrap on, horiz left")) 
    i += 2

    for key, value in dict_macros.items():
        sheet1.write(i, 0, key, xlwt.easyxf("align: wrap on, horiz left")) 
        sheet1.write(i, 1, value, xlwt.easyxf("align: wrap on, horiz left")) 
        total_count += value
        i += 1

    sheet1.write(i+1, 0, "Total count", xlwt.easyxf("align: wrap on, horiz left"))
    sheet1.write(i+1, 1, str(total_count), xlwt.easyxf("align: wrap on, horiz left"))
      
    wb.save('Results.xls') 


if __name__== "__main__":
    dict = { 'Obsolete' : 23, 'Delete' : 4, 'PKI' : 8 }
    xls_generator(dict)
    print("File generated succesfully")
