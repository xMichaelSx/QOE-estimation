import os
import pandas as pd
from datetime import datetime, date
# data_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\check100'
data_path = "D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet"

class Statistics:

    @staticmethod
    def rebuffering():
        for dirName, subdirList, fileList in os.walk(os.path.join(data_path)):
            for fname in fileList:
                if fname == 'ocr.csv':
                    df = pd.read_csv(os.path.join(dirName, fname))
                    path = os.path.join(dirName, fname)
                    i = 0
                    while i < len(df):

                        read_ahead = float(str(df['readAhead'][i]).strip())

                        if i <= 10:
                            if read_ahead <= 0.5:
                                while float(str(df['readAhead'][i]).strip()) <= 0.5:
                                    i += 1
                                continue

                        if i + 10 < len(df):
                            if read_ahead <= 0.5:
                                j = i+1
                                while j < len(df) and float(str(df['readAhead'][j]).strip()) <= 0.5:
                                    j += 1

                                duration = Statistics.time_diff(str(df['time'][i]).strip(),
                                                            str(df['time'][j]).strip())
                                if duration != 0:
                                    print("rebuffering event occurred at video: " + path + "\nwith length: " + str(duration))

                                elif duration == 0:
                                    print("rebuffering event occurred at video: " + path + "\nwith length between 0-1 sec")

                                i += j



                            if i != len(df):
                                i += 1

                        else:
                            break

    # buckets can be = '0-1', '1-2', '2-3', '3-4', ... , '(n-1)-1'
    # example: to get '0-1' type 1
    @staticmethod
    def get_start(bucket):
        count = 0
        for dirName, subdirList, fileList in os.walk(os.path.join(data_path)):

            for fname in fileList:
                if fname == 'ocr.csv':
                    df = pd.read_csv(os.path.join(dirName, fname))
                    path = os.path.join(dirName, fname)
                    i = 0
                    while i < len(df):

                        read_ahead = float(str(df['readAhead'][i]).strip())
                        # video_id = str(df['videoId'][i]).strip()

                        if i <= 10:

                            if read_ahead <= 0.5:
                                j = i + 1
                                while float(str(df['readAhead'][j]).strip()) <= 0.5:
                                    j += 1

                                duration = Statistics.time_diff(str(df['time'][i]).strip(),
                                                                str(df['time'][j - 1]).strip())
                                if duration == 0:
                                    count += 1
                                else:
                                    count += duration
                            i += 10

                        if count == bucket:
                            print("start timed delay at video: " + path + "\nis between: " + str(
                                count - 1) + " and " + str(count))
                        count = 0

                        if i + 10 >= len(df):

                            if read_ahead <= 0.5:
                                j = i
                                while (float(str(df['readAhead'][j]).strip()) <= 0.5) and (j + 1 < len(df)):
                                    j += 1

                                duration = Statistics.time_diff(str(df['time'][i]).strip(), str(df['time'][j]).strip())
                                if duration == 0:  # got to the if at least once so delay is between 1-0 sec
                                    count += 1
                                else:
                                    count += duration  # delay duration
                                break
                        i += 1

    @staticmethod
    def time_diff(time1, time2):
        time_start = datetime.strptime(time1, '%H:%M:%S').time()
        time_end = datetime.strptime(time2.strip(), '%H:%M:%S').time()
        time = abs(datetime.combine(date.today(), time_start) -
                   datetime.combine(date.today(), time_end))
        duration = str(time)
        return int(duration[len(duration)-2:len(duration)])

    @staticmethod
    def start_times():
        count = 0
        for dirName, subdirList, fileList in os.walk(os.path.join(data_path)):

            for fname in fileList:
                if fname == 'ocr.csv':
                    df = pd.read_csv(os.path.join(dirName, fname))
                    path = os.path.join(dirName, fname)
                    i = 0
                    while i < len(df):

                        read_ahead = float(str(df['readAhead'][i]).strip())
                        # video_id = str(df['videoId'][i]).strip()

                        if i <= 10:

                            if read_ahead <= 0.5:
                                j = i+1
                                while float(str(df['readAhead'][j]).strip()) <= 0.5:
                                    j += 1

                                duration = Statistics.time_diff(str(df['time'][i]).strip(), str(df['time'][j-1]).strip())
                                if duration == 0:
                                    count += 1
                                else:
                                    count += duration
                            i += 10

                        if count != 0:
                            print("start timed delay at video: " + path + "\nis between: " + str(count-1) + " and " + str(count))
                        count = 0

                        if i+10 >= len(df):

                            if read_ahead <= 0.5:
                                j = i
                                while (float(str(df['readAhead'][j]).strip()) <= 0.5) and (j+1 < len(df)):
                                    j += 1

                                duration = Statistics.time_diff(str(df['time'][i]).strip(), str(df['time'][j]).strip())
                                if duration == 0:  # got to the if at least once so delay is between 1-0 sec
                                    count += 1
                                else:
                                    count += duration  # delay duration
                                break
                        i += 1

    @staticmethod
    def locate(quality):
        qualityList = {}
        entry = False
        for dirName, subdirList, fileList in os.walk(os.path.join(data_path)):

            for fname in fileList:
                if fname == 'ocr.csv':
                    first_time = True
                    df = pd.read_csv(os.path.join(dirName, fname))
                    path = os.path.join(dirName, fname)
                    # print(path)
                    i = 0
                    while i < len(df):
                        quality_read = str(df['videoformat'][i]).strip()
                        if quality_read == quality:
                            entry = True

                            if first_time:
                                qualityList.setdefault(quality_read, 0)
                                first_time = False
                            qualityList[quality_read] += 1
                        i += 1

                    if len(qualityList) != 0:
                        print(quality + " occurred at path: " + path + " \n" + str(qualityList[quality]) + " times")
                    qualityList.clear()
        if not entry:
            print("no entry for given quality at dataset")

    @staticmethod
    def fix_quality():  # unifies the qualities up to 10% similarity
        known_qualities = '256x144', '426x240', '640x360', '854x480', '1280x720', '1920x1080'
        for dirName, subdirList, fileList in os.walk(os.path.join(data_path)):
            df = None
            for fname in fileList:
                if fname == 'ocr.csv':
                    df = pd.read_csv(os.path.join(dirName, fname))
                    i = 0
                    while i < len(df):

                        quality_read = str(df['videoformat'][i]).strip()
                        if quality_read in known_qualities:

                            i += 1
                            continue

                        else:
                            j = 0
                            if len(quality_read) == 7:
                                while j < len(known_qualities):
                                    if int(len(known_qualities[j])) != 7:
                                        j += 1
                                        continue

                                    my_right = int(known_qualities[j][4:7])
                                    given_right = int(quality_read[4:7])
                                    diff = abs(my_right - given_right)
                                    if diff/my_right <= 0.1:
                                        # data.append(known_qualities[j].strip())  # maybe add str
                                        df.at[i, "videoformat"] = known_qualities[j].strip()  # change the quality
                                        break
                                    # if the quality is weird and above 10% diff, don`t change for now
                                    # elif j == len(known_qualities):

                                        # data.append(quality_read)
                                    j += 1

                            elif len(quality_read) == 8:
                                while j < len(known_qualities):

                                    if int(len(known_qualities[j])) != 8:
                                        j += 1
                                        continue

                                    # if quality_read == '1920X800':
                                    #     print("got here")

                                    my_right = int(known_qualities[j][5:8])
                                    given_right = int(quality_read[5:8])
                                    diff = abs(my_right - given_right)
                                    if diff/my_right <= 0.1:
                                        # data.append(known_qualities[j].strip())  # maybe add str
                                        df.at[i, "videoformat"] = known_qualities[j].strip()  # change the quality
                                        break
                                    # if the quality is weird and above 10% diff, add as is for now
                                    # elif j == len(known_qualities):
                                    #     data.append(quality_read)
                                    j += 1

                            elif len(quality_read) == 9:
                                while j < len(known_qualities):

                                    if int(len(known_qualities[j])) != 9:
                                        j += 1
                                        continue

                                    my_right = int(known_qualities[j][5:9])
                                    given_right = int(quality_read[5:9])
                                    diff = abs(my_right - given_right)
                                    if diff/my_right <= 0.1:
                                        # data.append(known_qualities[j].strip())  # maybe add str
                                        df.at[i, "videoformat"] = known_qualities[j].strip()  # change the quality
                                        break
                                    # if the quality is weird and above 10% diff, add as is for now
                                    # elif j == len(known_qualities):
                                    #     data.append(quality_read)
                                    j += 1
                        i += 1

                    df.to_csv(os.path.join(dirName, fname), index=False)
                    # df.to_csv("os.path.join(dirName, fname)", index=False, encoding='utf_8_sig')



                    # with open(os.path.join(dirName, fname), mode='w') as csv_file:
                    #     writer = csv.writer(csv_file, lineterminator='\n', dialect='excel', encoding='utf_8_sig')
                    #     writer.writerow(field_names)
                    #     for i in range(len(temp_pcap)):
                    #         writer.writerow(temp_pcap[i])

    # example: {'640x360': 1495, '1280x720': 8168, '1920x1080': 9367, '854x480': 3243, '426x240': 940, '426x238': 22, '854x478': 473, '256x144': 307, '640x358': 48, '640x284': 210, '1280x534': 108, '1920x800': 322, '854x356': 93, '1920X800': 2, '576x360': 30, '768x480': 338, '640x480': 1087, '1920x1040': 263, '640x320': 207, '1272x720': 30, '1908x1080': 264, '2560x1440': 51, '320x240': 781, '640x352': 249}
    # out:     {'640x360': 1915, '1280x720': 8198, '1920x1080': 9894, '854x480': 5141, '426x240': 1743, '256x144': 307, '640x284': 210, '1280x534': 108, '1920x800': 322, '1920X800': 2, '640x320': 207, '2560x1440': 51}

    @staticmethod
    def qualities():  # lists all the qualities and number of them from whole dataset
        qualityList = {}
        for dirName, subdirList, fileList in os.walk(os.path.join(data_path)):

            for fname in fileList:
                if fname == 'ocr.csv':
                    df = pd.read_csv(os.path.join(dirName, fname))
                    i = 0
                    while i < len(df):
                        quality_read = str(df['videoformat'][i]).strip()
                        if quality_read in qualityList:
                            qualityList[quality_read] += 1
                            i += 1
                            continue

                        else:
                            qualityList.setdefault(quality_read, 1)
                            i += 1
        return qualityList
