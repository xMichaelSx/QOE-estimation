import divider
import Statistics
from datetime import datetime, date
import pandas as pd

if __name__ == '__main__':

    # Statistics.Statistics.rebuffering()


    # Statistics.Statistics.start_times()  # get all start time delays and paths
    Statistics.Statistics.get_start(1)     # get particular start time delay and path


    # time1str = '18:59:46'
    # time2str = '18:59:48'

    # time1 = datetime.strptime(time1str, '%H:%M:%S').time()
    # time2 = datetime.strptime(time2str, '%H:%M:%S').time()
    # time = abs(datetime.combine(date.today(), time1) - datetime.combine(date.today(), time2))
    # duration = str(time)
    # duration = float(duration[len(duration)-2:len(duration)])
    # print(duration)

    # Statistics.Statistics.fix_quality()  #  merge the strange qualities (up to 10%) with known once.
    # qualities = Statistics.Statistics.qualities()  # get all qualities and path
    # print(qualities)

    # Statistics.Statistics.locate('1920X1080')  # find specific quality, occurrences and path

    # {'640x360': 1915, '1280x720': 8198, '1920x1080': 9894, '854x480': 5141, '426x240': 1743, '256x144': 307,
    # '640x284': 210, '1280x534': 108, '1920x800': 324, '640x320': 207, '2560x1440': 51}

    # check = []
    # check.append('1920X800')
    # if '1920x800' in check:
    #     print("in")
    # else:
    #     print("thats the problem")




    # str = "1920X800"
    # print(str[4])
    # print(str.strip().lower())







    # data = pd.read_csv("D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\ocr_pcap\\vid1\\ocr.csv", encoding='utf-8')
    # data = pd.read_csv('D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\oldVersionTests\\scrTests\\links.csv')
    # i = 0
    # while i < len(data):
    #     print(data.iloc[i].values[0])
    #     i += 1
    # temp = []
    # print(len(data))
    # for i in range(len(data)):
    # print(data['videoId'][0])
    # temp.append(data.iloc[0].values)
    # print(temp[len(temp)-1][3])



    # divider.Divider.make_csv()

    # times = divider.Divider.cut_ocr_csv()  # get times + ocr csv cuts
    # print(times)
    # divider.Divider.cut_pcap_csv(times)  # get pcap csv cuts using the times

    # str1 = "HHOTtoNHYOO [vod]"

    # str2 = "xhXXVMOPRrQ [vod]"


    # str1 = 'NlpxjBgG-7E [vod]'
    # print(divider.Divider.remove_end(str1).upper())
    # print(divider.Divider.remove_end(str2).upper())
    # same = divider.Divider.check_same_id(divider.Divider.remove_end(str1).upper(),
    #                                      divider.Divider.remove_end(str2).upper())
    # print(same)

    # TODO check this later
    # times = ['23:55:25', '23:59:27', '23:59:38', '0:03:14', '0:03:14', '0:06:16', '0:06:17', '0:09:27', '0:09:28',
    #          '0:12:37', '0:12:48', '0:16:16', '0:16:25', '0:19:41', '0:19:42', '0:22:54', '0:23:01', '0:25:55',
    #          '0:25:56', '0:28:49', '0:28:50', '0:32:37', '0:32:51', '0:35:09', '0:35:30', '0:38:09', '0:38:37',
    #          '0:41:45', '0:41:54', '0:44:59', '0:44:59', '0:47:56', '0:47:57', '0:51:12', '0:51:14', '0:54:04',
    #          '0:54:05', '0:57:21', '0:57:24', '1:00:48']
    # times = ['11:48:01.123415', '11:49:02.326214', '11:49:02.672532', '11:50:00.152326']
    # times = ['17:25:54', '17:29:19', '17:29:20', '17:29:26', '17:29:27', '17:32:56', '17:32:57', '17:33:57',
    #          '17:33:57', '17:34:55', '17:34:56', '17:35:08', '17:35:08', '17:41:12', '17:41:13', '17:41:23',
    #          '17:41:24', '17:41:33', '17:41:33', '17:42:44']
    # for i in range(len(times)):
    #     print(times[i])

    # divider.Divider.cut_pcap_csv(times)  # get pcap csv cuts using the times

    # checking the remove end function
    # str = "o9aaoilecM [dash-otf]"
    # str = "09tX391Cn?U‘lvodl'"
    # str = "09a aoivJ lc'M'IIda‘stkot?"
    # str = divider.Divider.remove_end(str) # if the delimiter is not present, it returns an empty string!!!!
    # print(str)


    # pcaptime = "May 15, 2020 11:48:02.264677000 Jerusalem Daylight Time"

    # pcaptime = pcaptime.split(":")
    # time = pcaptime[0][len(pcaptime[0])-2:len(pcaptime[0])]+":"+pcaptime[1]+":"+pcaptime[2][0:2]
    # print(time)

    # time_str = 'bla bla 13:55:26.12153151 bla bla'
    # temp_time_holder = time_str.split(":")
    # time_str = temp_time_holder[0][len(temp_time_holder[0])-2:len(temp_time_holder[0])] + ":" + temp_time_holder[1] + ":" + temp_time_holder[2][0:9]
    # time_str2 = '13:55:27.231222'
    #
    # time_object1 = datetime.strptime(time_str, '%H:%M:%S.%f').time()
    # time_object2 = datetime.strptime(time_str2, '%H:%M:%S.%f').time()
    #
    # if time_object1 > time_object2:
    #     print("at if")
    #     print(time_object1)
    # else:
    #     print("at else")
    #     print(time_object2)

    # print(type(time_object))
    # print(time_object)


    # check = datetime.datetime("11:48:02")
    # print(check)

    # start = datetime.strptime("23:59:38", '%H:%M:%S')
    # end = datetime.strptime("0:03:14", '%H:%M:%S')
    # duration = end - start
    # duration_in_s = duration.total_seconds()  # Total number of seconds between dates
    # hours = abs(divmod(duration_in_s, 3600)[0])  # Seconds in an hour = 3600
    # print(hours)

    # s1 = '10:04:00'
    # s2 = '11:03:11'  # for example
    # format = '%H:%M:%S'
    # time = datetime.strptime(s2, format) - datetime.strptime(s1, format)
    # print
    # time




    # check1 = "a"+""+"b"
    # check2 = "a"+" "+"b"
    # print(check1)
    # print(check2)

    # str = 'a?aaaivJ ch [dash-otf]'
    # str = str.replace(" ","")
    # print(str)

     # Dynamic Programming implementation of LCS problem




     # # Driver program to test the lcs func
     # x = "AGGTAB"
     # y = "GXTXAYB"
    # x = "09a aoivJ"
    # y = "o9aaoilecM"
    # x = "o9aaoilecM"
    # y = "T99e041quE"
    # x = "o9aaoilecM [dash—otf]"
    # y = "T99e041quE [dash-otf]" ???
    # x = "o9aaoilecM [dash—otf]" ???
    # y = "T99e041quE [dash-otf]"
    # x = "ad"
    # y = "sd"

    # x = divider.Divider.remove_end(x)
    # y = divider.Divider.remove_end(y)
    # print(x)
    # print(y)
    # ans = divider.Divider.lcs(x, y, len(x), len(y))
    # print("Length of LCS is: " + str(ans))

    # str1 = "abcd"

    # ans = str1[0:(len(str1))]
    # print(ans)