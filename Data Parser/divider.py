import os
import csv
from datetime import datetime
import pandas as pd
# tshark_pcap_to_csv = 'C:\\"Program Files"\\Wireshark\\tshark.exe -r [src] -T fields -e frame.number -e frame.time -e frame.len -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e tcp.window_size -e tcp.options.wscale.shift -e tcp.analysis.keep_alive -e tcp.options.mss_val -e tcp.flags.ack -e tcp.flags.syn -e tcp.ack -e tcp.flags.reset -e frame.time_epoch -e gquic.tag.sni -E header=y -E separator=, -E quote=d -E occurrence=f > [dst]'
tshark_pcap_to_csv = 'C:\\"Program Files"\\Wireshark\\tshark.exe -r [src] -T fields -e frame.number -e frame.time -e frame.len -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e ssl.handshake.session_id_length -e ssl.handshake.comp_methods_length -e ssl.handshake.extension.len -e ssl.handshake.cipher_suites_length -e tcp.window_size -e tcp.options.wscale.shift -e tcp.analysis.keep_alive -e tcp.options.mss_val -e ssl.handshake.version -e frame.time_delta -e ip.ttl -e ssl.handshake.extensions_server_name -e tcp.flags.ack -e tcp.flags.syn -e tcp.ack -e tcp.flags.reset -e frame.time_epoch -e gquic.tag.sni -E header=y -E separator=, -E quote=d -E occurrence=f > [dst]'


class Divider:

    @staticmethod
    def make_csv():
        for dirName, subdirList, fileList in os.walk('D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video8'):
            for fname in fileList:
                if fname.endswith('.pcap') and fname.replace('.pcap', '.csv') not in fileList:
                    os.system(tshark_pcap_to_csv.replace('[src]', os.path.join(dirName, fname))
                              .replace('[dst]', os.path.join(dirName, fname.replace('.pcap', '.csv'))))

    # cuts the vid-csv into n sub vid-csv's and returns an array that
    # holds the start and stop times of all videos in order.
    # Example: even index (includes 0) is start time, odd index is end time of each vid
    # so first vid start time is at time[0] and end at time[1] and so on...
    @staticmethod
    def cut_ocr_csv():
        dir_num = 8  # and file name num
        num = 1
        #D:\Qoefinalproject\MyRecordings\Note8Vid\DataSet\Video7\Attempt2
        input_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\vid'+str(dir_num)+'ocr.csv'  # ocr id`s
        # input_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\oldVersionTests\\scrTests\\test2.csv' # test
        data = pd.read_csv(input_path, encoding='UTF-8')  # reading the ocr csv file
        # print(len(data))
        # print(data)
        # return
        ids_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\vid'+str(dir_num)+'links.csv'  # youtube video ids
        # ids_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\oldVersionTests\\scrTests\\test2Links.csv'  # test

        video_ids = pd.read_csv(ids_path, encoding='UTF-8')  # DataFrame of video id`s
        idx = 0  # video id index
        temp_ocr = []
        blast = ""  # before last row
        last = ""   # last row
        vid_start_stop_time = []  # even index with 0 is start time, odd index is end time of each vid

        temp_time = ""  # remember to get first at start later TODO should be fine now

        csv_num = 1
        # count_misread_rows = 0
        with open(input_path, 'r') as f:  # TODO get rid of this later
            reader = csv.reader(f)
            field_names = next(reader)   # get the field names from the ocr file

        i = 0
        new_vid = True
        flag = True
        while i < (len(data)-2):
            # if i == 1500:
            #     print("hi")
            # print(i)
            if flag:
                check1 = Divider.remove_end(data['videoId'][i])  # the ocr files video id
                checkidx = Divider.remove_end(video_ids.iloc[idx].values[0])  # the links video id for comparison
                # checking that were not inside an advertisement
                if Divider.check_same_id(check1, checkidx) >= 7:
                    temp_time = data['time'][i]
                    if new_vid:
                        vid_start_stop_time.append(temp_time)  # append start of first video
                        new_vid = False

                else:
                    # print("Advertisement with id: ")
                    # print(data['videoId'][i])
                    i += 1
                    continue

                # for comparison see 2 ahead
                fixed_id_curr = Divider.remove_end(data['videoId'][i])
                fixed_id_plus1 = Divider.remove_end(data['videoId'][i+1])
                fixed_id_plus2 = Divider.remove_end(data['videoId'][i+2])

                # the last two values of the end of file
                blast = data.iloc[i+1].values  # (before last)
                last = data.iloc[i+2].values

                if Divider.check_same_id(fixed_id_curr, fixed_id_plus1) >= 7:

                    check = data['videoId'][i]
                    if Divider.check_same_id(check, video_ids.iloc[idx].values[0]) >= 7:
                        temp_ocr.append(data.iloc[i].values)  # add the current row
                        temp_time = data['time'][i]  # get next time

                    else:
                        # print("Advertisement with id: ")
                        # print(data['videoId'][i])
                        i += 1
                        continue

                #  should not get here first time
                elif Divider.check_same_id(fixed_id_curr, fixed_id_plus2) >= 7:

                    check_vid_id = video_ids.iloc[idx].values[0]
                    if Divider.check_same_id(fixed_id_plus2, check_vid_id) >= 7:
                        temp_ocr.append(data.iloc[i+2].values)
                        temp_time = data['time'][i+2]
                        i += 2
                        # indicator for new video
                        if Divider.check_same_id(fixed_id_plus2, Divider.remove_end(temp_ocr[len(temp_ocr)-1][3])) < 7:
                            flag = False  # TODO check if dont lose data here and dont need to take the index back
                            i -= 1
                    else:
                        # print("Advertisement with id: ")
                        # print(data['videoId'][i])  # change later maybe to whole row
                        i += 1
                        continue

                elif Divider.check_same_id(fixed_id_plus1, fixed_id_plus2) >= 7:
                    temp_ocr.append(data.iloc[i].values)
                    # -1 cause next iteration will be False and well create the new file so to not waste a good
                    # row well go -1 cause next one will be +2 (exactly next if we didn`t do anything)
                    if Divider.check_same_id(fixed_id_plus1, Divider.remove_end(video_ids.iloc[idx+1].values[0])) < 7:  # an Ad!! question is, is it at the end or middle
                        while (Divider.check_same_id(Divider.remove_end(video_ids.iloc[idx].values[0]),
                                                     Divider.remove_end(data['videoId'][i + 1])) < 7) and\
                            (Divider.check_same_id(Divider.remove_end(video_ids.iloc[idx+1].values[0]),
                                                   Divider.remove_end(data['videoId'][i + 1])) < 7):
                            i += 1

                            # if the ad is not at the middle then stop and make the cut
                            # else continue regularly
                        if (Divider.check_same_id(Divider.remove_end(video_ids.iloc[idx].values[0]),
                                                  Divider.remove_end(data['videoId'][i + 1])) < 7):
                            flag = False
                    else:
                        i -= 1
                        flag = False

            else:  # else were creating the csv file with the collected data
                print("done video num: " + str(num))
                num += 1
                vid_start_stop_time.append(temp_time)  # end time of the current video
                # temp_time = data['time'][i+1]  # start time of the next video, +1 cause we did -1 before (last elif)
                # vid_start_stop_time.append(temp_time)  # append the first time of the next video

                file_name = "ocr" + ".csv"
                dir_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num)
                output_path = os.path.join(dir_path, file_name)

                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                else:
                    while os.path.exists(dir_path):
                        csv_num += 1
                        dir_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num)

                    output_path = os.path.join(dir_path, file_name)
                    os.makedirs(dir_path)

                with open(output_path, mode='w') as csv_file:
                    writer = csv.writer(csv_file, lineterminator='\n')
                    writer.writerow(field_names)
                    for j in range(len(temp_ocr)):
                        writer.writerow(temp_ocr[j])

                temp_ocr.clear()
                csv_num += 1
                flag = True
                new_vid = True
                idx += 1  # change the good video id idx to next one
            i += 1

        # last csv (or first if only one) creation is manual

        temp_time = data['time'][len(data)-1]
        vid_start_stop_time.append(temp_time)  # end time of the last video
        file_name = "ocr" + ".csv"
        dir_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num)
        output_path = os.path.join(dir_path, file_name)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        else:
            while os.path.exists(dir_path):
                csv_num += 1
                dir_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num)

            file_name = "ocr" + ".csv"
            output_path = os.path.join(dir_path, file_name)
            os.makedirs(dir_path)

        with open(output_path, mode='w') as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerow(field_names)

            if Divider.check_same_id(blast[3], last[3]) >= 7:
                temp_ocr.append(blast)
                temp_ocr.append(last)

            for i in range(len(temp_ocr)):
                writer.writerow(temp_ocr[i])

        # if count_misread_rows != 0:
        #     print("Total misread rows: " + str(count_misread_rows))

        return vid_start_stop_time

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    @staticmethod
    def cut_pcap_csv(times):
        dir_num = 8  # change as needed
        path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\vid'+str(dir_num)+'pcap.csv'

        with open(path, 'r') as f:
            temp_pcap = []
            reader = csv.reader(f)
            field_names = next(reader)   # get the field names from the pcap file
            csv_num = 1
            index = 0  # the index for the ocr start and end times
            # print("index is: " + str(index))
            ocr_start_time_object = datetime.strptime(times[index], '%H:%M:%S').time()
            index += 1
            ocr_end_time_object = datetime.strptime(times[index], '%H:%M:%S').time()
            # print("index is: " + str(index))
            activated = False

            for row in reader:

                temp_time_holder = row[1].split(":")  # an array of 3 that holds: str:str:str (from the pcap)
                                                      # example: "23":"55":"23.502967000"
                # extracting the time (creating time str)
                # print(temp_time_holder[2][0:9])
                pcap_time = temp_time_holder[0][len(temp_time_holder[0])-2:len(temp_time_holder[0])] +\
                    ":"+temp_time_holder[1]+":"+temp_time_holder[2][0:5]
                # creating time object
                pcap_time_object = datetime.strptime(pcap_time, '%H:%M:%S.%f').time()

                # if the pcap started before the ocr then wait until the pcap csv catches up to the ocr start time
                # or if after finishing a video, if there is a commercial then skip it
                if (ocr_start_time_object > pcap_time_object) and not activated:
                    continue

                # if the day passes this happens only once
                # first step is get the end time to its max value
                if ocr_start_time_object > ocr_end_time_object:
                    ocr_end_time_object = datetime.strptime("23:59:59.9", '%H:%M:%S.%f').time()
                    activated = True

                # this means that the runner passed to the next day (pcap runner)
                # second step is letting the start pass the day also and returning the end to actual time
                # logic: the start time and runner passed the day so start new day times
                # by letting the start be the smallest value for this vid, runner is good
                # and end time is set to its original value
                elif (ocr_start_time_object > pcap_time_object) and activated:
                    ocr_start_time_object = datetime.strptime("00:00:00", '%H:%M:%S').time()
                    ocr_end_time_object = datetime.strptime(times[index], '%H:%M:%S').time()
                    activated = False

                # collect the packets of the current vid (by times)
                elif (ocr_start_time_object <= pcap_time_object) and (pcap_time_object < ocr_end_time_object):
                    temp_pcap.append(row)

                # if were done, stop. (times[len(times)-1] is the final time)
                # don`t need further traffic data
                elif times[len(times)-1] == str(ocr_end_time_object):
                    break

                else:  # pcap_time_object >= ocr_end_time_object:
                    file_name = "pcap" + ".csv"
                    dir_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num)
                    output_path = os.path.join(dir_path, file_name)

                    check_file_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num) + "\\" + file_name

                    if not os.path.exists(dir_path):
                        print("The folder at path: " + dir_path + " Does now exist, Stopping!")
                        return

                    elif os.path.exists(check_file_path):
                        while os.path.exists(check_file_path):
                            csv_num += 1
                            check_file_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num) + "\\" + file_name
                            dir_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num)
                        output_path = os.path.join(dir_path, file_name)

                    with open(output_path, mode='w') as csv_file:
                        writer = csv.writer(csv_file, lineterminator='\n')
                        writer.writerow(field_names)
                        for i in range(len(temp_pcap)):
                            writer.writerow(temp_pcap[i])

                    index += 1
                    ocr_start_time_object = datetime.strptime(times[index], '%H:%M:%S').time()
                    index += 1
                    ocr_end_time_object = datetime.strptime(times[index], '%H:%M:%S').time()

                    temp_pcap.clear()
                    csv_num += 1

            # last csv (or first if only one) creation is manual
            file_name = "pcap" + ".csv"
            dir_path = 'D:\\Qoefinalproject\\MyRecordings\\Note8Vid\\DataSet\\Video'+str(dir_num)+'\\ocr_pcap\\vid' + str(csv_num)
            output_path = os.path.join(dir_path, file_name)

            if not os.path.exists(dir_path):
                print("The folder at path: " + dir_path + "Does now exist, Stopping!")
                return

            with open(output_path, mode='w') as csv_file:
                writer = csv.writer(csv_file, lineterminator='\n')
                writer.writerow(field_names)
                for i in range(len(temp_pcap)):
                    writer.writerow(temp_pcap[i])

#  /////////////////////////////////////////////////////////////////////////////////////

    # @staticmethod
    # def get_ids(path):
    #     ids = []
    #     with open(path, 'r') as f:
    #         reader = csv.reader(f)
    #         next(reader)  # get passed the first line
    #
    #         for row in reader:
    #             ids = row[0]
    #
    #     return ids

    @staticmethod  # adding delimiters
    def remove_end(id_name):  # by delimiters
        index = 0
        run = 0
        for c in id_name:
            # print(c)
            if c == '"':
                id_name = id_name.replace(c, "")
            if c == '\'':
                id_name = id_name.replace(c, "")

            #     print(str(id_name))

        # index = id_name.index(" ")

            if c == " ":  # and index <= run (removed this)
                index = run

            elif c == ("\\" or "|" or "/" or "[") and (len(id_name) - run >= 3):
                index = run
            run += 1

        if index != 0:
            return id_name[0:index]

        else:
            return id_name[0:len(id_name)]  #  in case the ocr found none of the above delimiters, just work with
                                            #  the original word

    # an O(n^2) lcs, there are better implementations but for now this one is sufficient.
    # @staticmethod
    # def lcs(prev, new, m, n):
    #     if m == 0 or n == 0:
    #         return 0
    #     elif prev[m - 1] == new[n - 1]:
    #         return 1 + Divider.lcs(prev, new, m - 1, n - 1)
    #     else:
    #         return max(Divider.lcs(prev, new, m, n - 1), Divider.lcs(prev, new, m - 1, n))

    # #  older version method, not used for now (lcs is better)

    #  TODO Second attempt at same id
    @staticmethod
    def check_same_id(curr, next):  # goes by probability (99% of the times it will be good enough, could be fixed a bit)

        if len(curr) >= len(next):
            smaller_word = next.upper()
            bigger_word = curr.upper()
        else:
            smaller_word = curr.upper()
            bigger_word = next.upper()
        count = 0
        for c in smaller_word:
            i = 0
            while i < len(bigger_word):
                if bigger_word[i] == c:
                    count += 1
                    break
                i += 1
        # if count < 6:
            # print("for " + smaller_word + " and " + bigger_word + " count is: " + str(count))
        return count





    # @staticmethod
    # def check_same_id(curr, next):  # goes by probability (99% of the times it will be good enough, could be fixed a bit)
    #
    #     if len(curr) >= len(next):
    #         smaller_word = next
    #     else:
    #         smaller_word = curr
    #     same = 0
    #     i = 0
    #     j = 0
    #     while i < len(smaller_word) and j < len(smaller_word):
    #         if curr[i] == " ":
    #             i += 1
    #         if next[j] == " ":
    #             j += 1
    #         if curr[i] == next[j]:
    #             same = same + 1
    #         i += 1
    #         j += 1
    #
    #     return same

    @staticmethod
    def check_diff_id(prev, new):

        if len(prev) >= len(new):
            smaller_word = new
        else:
            smaller_word = prev

        # print(smaller_word)
        diff = 0
        i = 0
        j = 0

        while i < len(smaller_word)-1 and j < len(smaller_word)-1:
            try:
                if prev[i] == " ":
                    i += 1

                if new[j] == " ":
                    j += 1

                if prev[i] != new[j]:
                    diff = diff + 1

                i += 1
                j += 1

            except:
                print(prev)
                print(new)
                print("Prev is: " + str(len(prev)))
                print("new is: " + str(len(new)))
                print("while until count : " + str(len(smaller_word)))
            #     print(i)
            #     print("An exception occurred")
                return

        if diff > len(smaller_word)/2:  # trying to be strict
            return True
        else:
            return False


