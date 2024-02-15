from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from demo_table_python import Ui_MainWindow

from sources_1 import *
from stocks import *
from Yfinance_functions_v2 import *

class main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.dt_page = Ui_MainWindow()
        self.dt_page.setupUi(self)
        # datas of thee page here:
        self.table_3 = transfer_arr
        self.list_ogr = liste_3
        # the row of table:
        self.dt_page.tableWidget.setRowCount(len(self.table_3))
        print(":::functions activated:::")
        self.filling()
        # self.creating_data()
    # def creating_data(self):
    #     st_time = int(input("Please enter the state time:: "))
    #     ema_intr = int(input("Please enter the EMA period value:: "))
    #     for stock in hisse_senetleri: # -> burada herhangi bir şey eklenebilir.
    #         main_yfinance(stock,st_time,ema_intr)
    
          
    def filling(self):
        row = 0
        for data in self.table_3:
            #tablo içine objeler string oalrak girmelidir. Buna dikkat etmek lazım. ID stirng değildir. stringe dönüştürülmeli.
            
            self.dt_page.tableWidget.setItem(row,1,QTableWidgetItem(str(data["Name"])))
            self.dt_page.tableWidget.setItem(row,2,QTableWidgetItem(str(data["Ask"])))
            self.dt_page.tableWidget.setItem(row,3,QTableWidgetItem(str(data["State time"])))
            self.dt_page.tableWidget.setItem(row,4,QTableWidgetItem(str(data["Status"])))
            
            row +=1
        print("\n\n\n\n",self.table_3)
        







if __name__ == "__main__":
    app = QApplication([])
    window = main()
    window.show()
    app.exec_()