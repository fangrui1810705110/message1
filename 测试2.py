import os

class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('./data/UI/keliuduanxin.ui')

        self.plainTextEdit_3 = self.ui.findChild(QPlainTextEdit, "plainTextEdit_3")
        self.plainTextEdit_4 = self.ui.findChild(QPlainTextEdit, "plainTextEdit_4")

        self.ui.pushButton.clicked.connect(self.main111)
        # self.ui.nowLineEdit.setText(DateUtil.get_date_time('%Y%m%d'))
        # self.ui.thisContrastLineEdit.setText(DateUtil.get_before_day(DateUtil.get_date_time('%Y%m%d')))
        # self.ui.lastContrastLineEdit.setText(DateUtil.last_week_date(DateUtil.get_before_day(DateUtil.get_date_time('%Y%m%d'))))
        # self.ui.oriTablePushButton.clicked.connect(self.open_ori_table)
        # self.ui.paoPiDoPushButton.clicked.connect(self.work_do)
        # self.ui.sqlPushButton.clicked.connect(self.sql_insert)
        # self.ui.fenleiBushButton.clicked.connect(self.fenleibiaoge)
        # self.ui.oaPushButton.clicked.connect(self.oabiaoge)
        # self.ui.paoPiPushButton.clicked.connect(self.paopibiaoge)
        # self.ui.ccmPushButton.clicked.connect(self.ccmbiaoge)
        # self.ui.tiaokongPushButton.clicked.connect(self.tiaokongbiaoge)
        # self.ui.keliuContrastPushButton.clicked.connect(self.keliu_contrast)

    def Clear_SMS(self):
        # 清除"日常客流短信"框文本内容
        self.plainTextEdit.clear()


    def extract_text_from_web(self, url, filepath):

        # 清除流程框文本内容
        self.plainTextEdit_3.clear()

        # 发送HTTP请求，获取网页内容
        self.plainTextEdit_3.appendPlainText("1.正在发送HTTP请求；")
        # print("正在发送HTTP请求...")
        response = requests.get(url)

        if response.status_code == 200:
            # 使用BeautifulSoup解析网页内容
            self.plainTextEdit_3.appendPlainText("2.正在解析网页内容；")
            # print("正在解析网页内容...")
            soup = BeautifulSoup(response.content, 'html.parser')

            # 提取文本内容，并将多个连续空白字符替换为单个换行符
            self.plainTextEdit_3.appendPlainText("3.提取文本内容；")
            # print("提取文本内容...")
            text = soup.get_text()

            import re
            text = re.sub(r'\s+', '\n', text)

            # 将文本内容拆分成行，并创建DataFrame对象
            self.plainTextEdit_3.appendPlainText("4.拆分文本内容并创建DataFrame对象；")
            # print("拆分文本内容并创建DataFrame对象...")
            lines = text.strip().split('\n')

            # 生成文件夹
            folder_path = os.path.join('E:/桌面/客流短信调试/原始数据表格', datetime.now().strftime('%Y-%m-%d'))
            self.create_folder_if_not_exist(folder_path)

            # 将DataFrame对象写入Excel文件的指定工作表
            file_path = os.path.join(folder_path, '初始数据.xlsx')
            self.plainTextEdit_3.appendPlainText("5.将文本内容写入Excel文件；")
            # print("将文本内容写入Excel文件...")
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df = pd.DataFrame(lines, columns=['Text'])
                df.to_excel(writer, sheet_name='初始数据', index=False)
                # writer.save()
                self.plainTextEdit_3.appendPlainText("6.网页文本内容已成功复制到表格；")


            # print("网页文本内容已成功复制到表格！")
        else:
            self.plainTextEdit_3.appendPlainText("!!!!!无法获取网页内容!!!!!")
            self.plainTextEdit_4.appendPlainText("!!!!!无法获取网页内容!!!!!")
            # print("无法获取网页内容")

    def main111(self):
        # 要提取文本内容的网址
        url = "https://www.xmdjej.gov.cn/"

        # 表格保存的完整路径和文件名
        filepath = 'E:/桌面/客流短信调试/' + DateUtil.get_date_time("%Y%m%d-%H") + '.xlsx'
        print(DateUtil.get_date_time("%Y%m%d-%H"))
        self.extract_text_from_web(url, filepath)

        read_workbook = openpyxl.load_workbook(filepath, data_only=True)

        # 生成文件夹
        folder_path = os.path.join('E:/桌面/客流短信调试/原始数据表格', datetime.now().strftime('%Y-%m-%d'))
        self.create_folder_if_not_exist(folder_path)

        write_workbook = openpyxl.load_workbook(os.path.join(folder_path, '客流表格神器.xlsx'), data_only=True)
        write_sheet = write_workbook['初始数据']
        read_sheet = read_workbook['初始数据']

        for i in range(1, 200):
            for j in range(1, 5):
                write_sheet.cell(i, j).value = read_sheet.cell(i, j).value

        write_workbook.save(os.path.join(folder_path, '客流表格神器.xlsx'))

        now = datetime.now()
        now_date = now.strftime("%Y%m%d-%H")  # 格式化当前日期和时间

        # 读取Excel文件，并指定表格名称和不使用列名
        df = pd.read_excel(os.path.join(folder_path, '客流表格神器.XLSX'), sheet_name='客流模板', header=None)
        self.plainTextEdit_3.appendPlainText("7.读取Excel文件完成；")
        # print("读取Excel文件完成：")
        print(df)

        # 选择指定区域（B3到N20）
        selected_data = df.iloc[2:21, 1:14]
        self.plainTextEdit_3.appendPlainText("8.选择区域完成；")
        # print("选择区域完成：")
        print(selected_data)

        # 去除空格
        selected_data = selected_data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # 将选定区域保存为文本文件
        selected_data.to_csv(os.path.join(folder_path, '信息调度客流短信_' + now_date + '.txt'), sep='\t', index=False, header=None, quoting=3,
                             quotechar='"')
        self.plainTextEdit_3.appendPlainText("9.保存为文本文件完成；")
        # print("9.保存为文本文件完成")
        with open(os.path.join(folder_path, '信息调度客流短信_' + now_date + '.txt'), 'rb') as file:
            content = file.read()
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                text = content.decode('gbk', errors='ignore')

        text = text.strip()  # 去掉字符串两端的空白字符
        text = text.replace('\t', ' ')  # 将制表符替换为空格
        self.ui.plainTextEdit.setPlainText(text)
        self.plainTextEdit_3.appendPlainText("10.已输出至“日常客流短信”。")

    def create_folder_if_not_exist(self, path):
        """
        如果指定路径下文件夹不存在，则创建该文件夹
        :param path: 文件夹路径
        """
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"已创建文件夹：{path}")
        else:
            print(f"文件夹已存在：{path}")


app = QApplication([])
