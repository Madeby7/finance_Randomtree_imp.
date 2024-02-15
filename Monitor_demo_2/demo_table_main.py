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
        # the estimate values:: /-/ we take from lines that phrase
        self.zaman = 300
        self.ema_zaman = 200
        # datas of thee page here:
        self.data_bs = []
        
        # the row of table:
        self.dt_page.tableWidget.setRowCount(len(hisse_senetleri))
        print(":::functions activated:::")
        self.dt_page.pushButton.clicked.connect(self.creating_data)
        # self.creating_data()
    def creating_data(self):
        self.data_bs = []
        for stock_pr in hisse_senetleri:
            self.data_bs.append(main_yfinance(stock_pr,self.zaman,self.ema_zaman))
        
        row = 0
        for data in self.data_bs:
            self.dt_page.tableWidget.setItem(row,1,QTableWidgetItem(str(data["Name"])))
            self.dt_page.tableWidget.setItem(row,2,QTableWidgetItem(str(data["Ask"])))
            self.dt_page.tableWidget.setItem(row,3,QTableWidgetItem(str(data["State time"])))
            self.dt_page.tableWidget.setItem(row,4,QTableWidgetItem(str(data["Status"])))
            row +=1
            
    
          
    def filling(self):
        row = 0
        for data in self.table_3:
            #tablo içine objeler string oalrak girmelidir. Buna dikkat etmek lazım. ID stirng değildir. stringe dönüştürülmeli.
            
            self.dt_page.tableWidget.setItem(row,1,QTableWidgetItem(str(data["Name"])))
            self.dt_page.tableWidget.setItem(row,2,QTableWidgetItem(str(data["Ask"])))
            self.dt_page.tableWidget.setItem(row,3,QTableWidgetItem(str(data["State time"])))
            self.dt_page.tableWidget.setItem(row,4,QTableWidgetItem(str(data["Status"])))
            
            row +=1
        # print("\n\n\n\n",self.table_3)
        print(self.zaman,self.ema_zaman)
        
        







if __name__ == "__main__":
    app = QApplication([])
    window = main()
    window.show()
    app.exec_()