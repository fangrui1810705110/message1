import requests


class MessageUtil:
    @staticmethod
    def get_all(url):
        '''
        用于获取acc实时客流的json
        :param url: # 'http://10.1.32.42:8080/accPortal/modbus/getModbus' 填写acc实时客流的url
        :return:
        '''
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['rows']
        return data

    @staticmethod
    def get_count_number(data, name, count):
        '''
        {'id': '0100', 'name': '一号线进站客流量', 'count': 52563}
        按照名字name，查找到对应的数据，例如name写入一号线进站客流量，就会获取到参数count的数据。后续参数可以动态添加
        :param data: acc实时客流获取到的kjson
        :param name: 要获取的名字
        :param count: 总数
        :return: 对应名字的数据值
        '''
        for dic in data:
            if dic['name'] == name:
                value = dic.get(count)
                if value is not None:
                    return value
        return None

        # 获取进站客流排名
    @staticmethod
    def get_passenger_count_number(data,line_flag, line_number_flag, count):
        # 获取进站客流排名
        '''
        {'id': '0100', 'name': '一号线进站客流量', 'count': 52563}
        按照名字name，查找到对应的数据，例如name写入一号线进站客流量，就会获取到参数count的数据。后续参数可以动态添加
        :param data: acc实时客流获取到的kjson
        :param name: 要获取的名字
        :param count: 总数
        :return:
        '''
        max_count = float('-inf')
        sec_max_count = float('-inf')
        third_max_count = float('-inf')
        max_name = ''
        sec_max_name = ''
        third_max_name = ''
        result_list = []

        for dic in data:
            if dic['id'].startswith(line_flag) and int(dic['id']) > line_number_flag and 'count' in dic:
                if dic[count] > max_count:
                    third_max_count = sec_max_count
                    third_max_name = sec_max_name
                    sec_max_count = max_count
                    sec_max_name = max_name
                    max_count = dic[count]
                    max_name = dic['name']
                elif dic[count] > sec_max_count:
                    third_max_count = sec_max_count
                    third_max_name = sec_max_name
                    sec_max_count = dic[count]
                    sec_max_name = dic['name']
                elif dic[count] > third_max_count:
                    third_max_count = dic[count]
                    third_max_name = dic['name']

        result_list.append(max_name)
        result_list.append(max_count)
        result_list.append(sec_max_name)
        result_list.append(sec_max_count)
        result_list.append(third_max_name)
        result_list.append(third_max_count)
        return result_list
        # 获取进站客流排名
        # 报文-差异之间的差值报警

    @staticmethod
    def get_error_count_number(data,id, name, count, passengerCount, threshold):
        error_list = []
        for dic in data:
            if int(dic['id']) > 100 and dic['id'][-2:] != '00':
                diff = dic[count] - dic[passengerCount]
                if diff > threshold:
                    error_list.append((dic[id],dic[name], diff))
        return error_list


