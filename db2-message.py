from datetime import datetime
import openpyxl

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def keliu_data_str(now_date):
    '''
    获取客流信息字符串
    :param now_date: 格式为 '%Y%m%d' 的日期字符串
    :return: 客流信息字符串
    '''
    read_workbook = openpyxl.load_workbook('./data/客流表格神器.xlsx', data_only=True)
    read_sheet = read_workbook['数据处理表']

    keliu_str = '截至' + datetime.strptime(now_date, '%Y%m%d').strftime('%Y年%m月%d日') + '，地铁线网进站' + str(round(float(read_sheet['C7'].value), 2)) + '，较上周？XXX增长/减少XX%，其中1号线进站' + str(round(float(read_sheet['C10'].value), 2)) + '，较上周？XXX增长/减少XX%，2号线进站' + str(round(float(read_sheet['C11'].value), 2)) + '，较上周？XXX增长/减少XX%，3号线进站' + str(round(float(read_sheet['C12'].value), 2)) + '\n'
    keliu_str += '主要车站：' + '\n'
    keliu_str += '一号线:' + str(round(float(read_sheet['E7'].value), 2)) + str(round(float(read_sheet['F7'].value), 2)) + ';' + str(round(float(read_sheet['E8'].value), 2)) + str(round(float(read_sheet['F8'].value), 2)) + '\n'
    keliu_str += '二号线:' + str(round(float(read_sheet['H7'].value), 2)) + str(round(float(read_sheet['I7'].value), 2)) + ';' + str(round(float(read_sheet['H8'].value), 2)) + str(round(float(read_sheet['I8'].value), 2)) + '\n'
    keliu_str += '三号线:' + str(round(float(read_sheet['K7'].value), 2)) + str(round(float(read_sheet['L7'].value), 2)) + ';' + str(round(float(read_sheet['K8'].value), 2)) + str(round(float(read_sheet['L8'].value), 2)) + '\n'

    return keliu_str

if __name__ == '__main__':
    now_date = '20240222'  # 替换为你想获取客流信息的日期字符串
    keliu_str = keliu_data_str(now_date)
    print(keliu_str)
