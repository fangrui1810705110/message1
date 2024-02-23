import os

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./data/UI/keliuduanxin.ui')
        # self.ui.nowLineEdit.setText(DateUtil.get_date_time('%Y%m%d'))
        # self.ui.thisContrastLineEdit.setText(DateUtil.get_before_day(DateUtil.get_date_time('%Y%m%d')))
        # self.ui.lastContrastLineEdit.setText(DateUtil.last_week_date(DateUtil.get_before_day(DateUtil.get_date_time('%Y%m%d'))))
        #
        # self.ui.oriTablePushButton.clicked.connect(self.open_ori_table)
        # self.ui.paoPiDoPushButton.clicked.connect(self.work_do)
        self.ui.pushButton.clicked.connect(self.extract_text_from_web)
        # self.ui.sqlPushButton.clicked.connect(self.sql_insert)
        #
        # self.ui.fenleiBushButton.clicked.connect(self.fenleibiaoge)
        # self.ui.oaPushButton.clicked.connect(self.oabiaoge)
        # self.ui.paoPiPushButton.clicked.connect(self.paopibiaoge)
        # self.ui.ccmPushButton.clicked.connect(self.ccmbiaoge)
        # self.ui.tiaokongPushButton.clicked.connect(self.tiaokongbiaoge)
        # self.ui.keliuContrastPushButton.clicked.connect(self.keliu_contrast)



app = QApplication([])
# app.setWindowIcon(QIcon('ui/icon.png'))
stats = Stats()
stats.ui.show()
app.exec_()



