from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from python.MessageUtil import MessageUtil
import datetime
import os
import pandas as pd
import requests


class Stats(QMainWindow):
    def __init__(self):
        super(Stats, self).__init__()

        # 加载UI文件
        uic.loadUi('./data/UI/message.ui', self)
        # 设置当前路径为 current_path
        self.current_path = os.getcwd()

        settings = QSettings("MyApp", "MyProgram")
        last_url = settings.value("last_url")
        if last_url is not None:
            self.lineEdit.setText(last_url)

        last_threshold = settings.value("last_threshold")
        if last_threshold is not None:
            self.lineEdit_2.setText(last_threshold)

        # 连接按钮点击事件到槽函数
        self.pushButton.clicked.connect(self.run_script)
        self.pushButton_2.clicked.connect(self.clear_text)

    def run_script(self):
        try:
            new_url = self.lineEdit.text()
            data = MessageUtil.get_all(new_url)

            # 保存新的URL
            settings = QSettings("MyApp", "MyProgram")
            settings.setValue("last_url", new_url)

            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")

            # 客流短信编辑
            message_str = ''  # 初始化 message_str 变量
            message_str += '截至' + current_time + '，地铁线网进站' + str(
                MessageUtil.get_count_number(data, '地铁线网总进站量', 'count')) + '，较上周？XXX增长/减少XX%，其中1号线进站' + str(
                MessageUtil.get_count_number(data, '一号线进站客流量', 'count')) + '，较上周？XXX增长/减少XX%，2号线进站' + str(
                MessageUtil.get_count_number(data, '二号线进站客流量', 'count')) + '，较上周？XXX增长/减少XX%，3号线进站' + str(
                MessageUtil.get_count_number(data, '三号线进站客流量', 'count')) +'，较上周？XXX增长/减少XX%。' + '\n'
            message_str += '主要车站：' + '\n'
            message_str += '一号线:' + str(MessageUtil.get_passenger_count_number(data, '01', 100, 'count')[0]) + str(
                MessageUtil.get_passenger_count_number(data, '01', 100, 'count')[1]) + ',' + str(
                MessageUtil.get_passenger_count_number(data, '01', 100, 'count')[2]) + str(
                MessageUtil.get_passenger_count_number(data, '01', 100, 'count')[3]) + ';' + '\n'
            message_str += '二号线:' + str(MessageUtil.get_passenger_count_number(data, '02', 200, 'count')[0]) + str(
                MessageUtil.get_passenger_count_number(data, '02', 200, 'count')[1]) + ',' + str(
                MessageUtil.get_passenger_count_number(data, '02', 200, 'count')[2]) + str(
                MessageUtil.get_passenger_count_number(data, '02', 200, 'count')[3]) + ';' + '\n'
            message_str += '三号线:' + str(MessageUtil.get_passenger_count_number(data, '03', 300, 'count')[0]) + str(
                MessageUtil.get_passenger_count_number(data, '03', 300, 'count')[1]) + ',' + str(
                MessageUtil.get_passenger_count_number(data, '03', 300, 'count')[2]) + str(
                MessageUtil.get_passenger_count_number(data, '03', 300, 'count')[3]) + ';' + '\n'
            # 客流短信编辑

            # 报文-差异之间的差值报警
            try:
                threshold = int(self.lineEdit_2.text())
                result_list = MessageUtil.get_error_count_number(data, 'id','name', 'count', 'passengerCount', threshold)
                if not result_list:
                    output_text = "当前报文与交易差额无异常。"
                else:
                    sorted_result_list = sorted(result_list, key=lambda x: x[2], reverse=True)

                    output_text = ""
                    output_text += f"注意：交易数据自动刷新/小时，点击“实时客流界面”刷新按钮后重新查询交易数据。”\n"
                    for item in sorted_result_list:
                        output_text += f" 异常车站：{item[0]}-{item[1]}【报文与交易差额: {item[2]}】\n"
            except ValueError:
                output_text = "请输入有效整数作为阈值。"

            self.plainTextEdit_2.setPlainText(output_text)

            # 报文-差异之间的差值报警

            # 创建文件夹
            now = datetime.datetime.now()
            year_month = now.strftime("%Y%m")
            folder_path = os.path.join(self.current_path, 'data', '原始数据表格', year_month)
            folder_path_2 = os.path.join(self.current_path, 'data', '日常客流短信', year_month)
            folder_path_3 = os.path.join(self.current_path, 'data', '阶段客流短信', year_month)

            os.makedirs(folder_path, exist_ok=True)
            os.makedirs(folder_path_2, exist_ok=True)
            os.makedirs(folder_path_3, exist_ok=True)
            # 创建文件夹

            # 保存客流短信为“.txt”格式
            file_name = now.strftime("%Y%m%d%H%M_") + "客流短信" + ".txt"
            file_path = os.path.join(folder_path_2, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(message_str)
            # 保存客流短信为“.txt”格式

            # 将结果显示在文本编辑控件中
            self.plainTextEdit.setPlainText(message_str)
            # 将结果显示在文本编辑控件中

            # 保存阈值
            new_threshold = self.lineEdit_2.text()
            settings.setValue("last_threshold", new_threshold)
            # 保存阈值

        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            # self.plainTextEdit.setPlainText(error_msg)
            self.plainTextEdit_2.setPlainText(error_msg)

        try:
            new_url = self.lineEdit.text()
            response = requests.get(new_url)
            response.raise_for_status()

            data = response.json()
            msg = data.get('msg')
            total = data.get('total')
            rows = data.get('rows')
            success = data.get('success')

            df = pd.DataFrame(rows)

            # 创建文件夹和完整文件路径
            now = datetime.datetime.now()
            year_month = now.strftime("%Y%m")
            folder_path_2 = os.path.join(self.current_path, 'data', '日常客流短信', year_month)
            file_name = now.strftime("%Y%m%d%H%M_") + "客流数据.xlsx"
            file_path = os.path.join(folder_path_2, file_name)

            # 将数据保存到 Excel 文件
            df.to_excel(file_path, index=False)


        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            self.plainTextEdit_2.setPlainText(error_msg)

    def clear_text(self):
        self.plainTextEdit.clear()
        self.plainTextEdit_2.clear()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    stats = Stats()
    stats.show()
    sys.exit(app.exec_())
