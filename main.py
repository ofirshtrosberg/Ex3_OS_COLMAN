# אופיר שטרוסברג 207828641
# לידור דנון 211823240
import sys


def compute_FCFS(list, num):
    turnaround = 0
    finish_time = []
    arrival_time = []
    need_time = []
    num_of_processes_need_to_run = num
    for i in range(num):
        arrival_time.append(int(list[i][0]))
    for i in range(num):
        finish_time.append(-1)
    for i in range(num):
        need_time.append(int(list[i][1]))
        if need_time[i] == 0:
            finish_time[i] = arrival_time[i]
            num_of_processes_need_to_run -= 1
    curr_time = arrival_time[0]
    while True:
        if num_of_processes_need_to_run == 0:
            break
        for i in range(num):
            if arrival_time[i] <= curr_time:
                while need_time[i] > 0 and finish_time[i] == -1:
                    need_time[i] -= 1
                    curr_time += 1
                if need_time[i] == 0 and finish_time[i] == -1:
                    num_of_processes_need_to_run -= 1
                    finish_time[i] = curr_time
            else:
                break
        curr_time += 1
    for i in range(num):
        turnaround += finish_time[i] - arrival_time[i]
    turnaround = turnaround / num
    print("FCFS: mean turnaround =", turnaround)


def compute_LCFS_NP(list, num):
    turnaround = 0
    curr_time = int(list[0][0])
    finish_time = []
    arrival_time = []
    need_time = []
    num_of_processes_need_to_run = num
    for i in range(num):
        finish_time.append(-1)
    for i in range(num):
        arrival_time.append(int(list[i][0]))
    for i in range(num):
        need_time.append(int(list[i][1]))
        if need_time[i] == 0:
            finish_time[i] = arrival_time[i]
            num_of_processes_need_to_run -= 1
    while True:
        last_process_arrived_index = -1
        if num_of_processes_need_to_run == 0:
            break
        for i in range(num):
            if need_time[i] > 0 and finish_time[i] == -1:
                if arrival_time[i] <= curr_time:
                    last_process_arrived_index = i
        if last_process_arrived_index == -1:
            curr_time += 1
            continue
        curr_time += need_time[last_process_arrived_index]
        need_time[last_process_arrived_index] = 0
        num_of_processes_need_to_run -= 1
        finish_time[last_process_arrived_index] = curr_time
    for i in range(num):
        turnaround += finish_time[i] - arrival_time[i]
    turnaround = turnaround / num
    print("LCFS (NP): mean turnaround =", turnaround)


def compute_LCFS_P(list, num):
    curr_time = int(list[0][0])
    turnaround = 0
    run_now_index = 0
    finish_time = []
    arrival_time = []
    need_time = []
    num_of_processes_need_to_run = num
    for i in range(num):
        finish_time.append(-1)
    for i in range(num):
        arrival_time.append(int(list[i][0]))
    for i in range(num):
        need_time.append(int(list[i][1]))
        if need_time[i] == 0:
            finish_time[i] = arrival_time[i]
            num_of_processes_need_to_run -= 1
    while True:
        if num_of_processes_need_to_run == 0:
            break
        curr_time += 1
        if need_time[run_now_index] > 0:
            need_time[run_now_index] -= 1
            if need_time[run_now_index] == 0:
                finish_time[run_now_index] = curr_time
                num_of_processes_need_to_run -= 1
                if num_of_processes_need_to_run == 0:
                    break
        # new process arrived
        if run_now_index + 1 < num and arrival_time[run_now_index + 1] == curr_time:
            run_now_index = run_now_index + 1
        else:
            if need_time[run_now_index] == 0:
                for i in range(run_now_index, -1, -1):
                    if need_time[i] > 0:
                        run_now_index = i
                        break
    for i in range(num):
        turnaround += finish_time[i] - arrival_time[i]
    turnaround = turnaround / num
    print("LCFS (P): mean turnaround =", turnaround)


def compute_RR(list, num):
    num_copy = num
    rr_list = []
    last_process_arrived_yet = 0
    curr_time = int(list[0][0])
    turnaround = 0
    finish_time = []
    arrival_time = []
    need_time = []
    num_of_processes_need_to_run = num
    for i in range(num):
        arrival_time.append(int(list[i][0]))
    for i in range(num):
        finish_time.append(-1)
    for i in range(num):
        need_time.append(int(list[i][1]))
        if need_time[i] == 0:
            finish_time[i] == arrival_time[i]
            num_of_processes_need_to_run -= 1
    # initialize with the processes index
    for i in range(num):
        rr_list.append(i)
    while True:
        # print("!!!!!!!!!!")
        if num_of_processes_need_to_run == 0:
            break
        last_process_finished = False
        #########?????
        while need_time[rr_list[0]] != 0:
            # give time quantum
            if need_time[rr_list[0]] >= 2:
                need_time[rr_list[0]] -= 2
                curr_time += 2
            elif need_time[rr_list[0]] == 1:
                need_time[rr_list[0]] -= 1
                curr_time += 1
            if need_time[rr_list[0]] == 0:
                finish_time[rr_list[0]] = curr_time
                num_of_processes_need_to_run -= 1
                last_process_finished = True
                del rr_list[0]
                num_copy -= 1
                if num_of_processes_need_to_run == 0:
                    break
            if last_process_finished is True:
                if arrival_time[rr_list[0]] <= curr_time:
                    last_process_arrived_yet = rr_list[0]
            if last_process_finished is False:
                for i in range(num_copy):
                    if arrival_time[rr_list[i]] <= curr_time:
                        last_process_arrived_yet = max(rr_list[i], last_process_arrived_yet)
                rr_list.insert(last_process_arrived_yet + 1, rr_list[0])
                del rr_list[0]
    for i in range(num):
        turnaround += finish_time[i] - arrival_time[i]
    turnaround = turnaround / num
    print("RR: mean turnaround =", turnaround)


def compute_SJF(list, num):
    curr_time = int(list[0][0])
    turnaround = 0
    run_now_index = 0
    finish_time = []
    arrival_time = []
    need_time = []
    burst_time = []
    num_of_processes_need_to_run = num
    for i in range(num):
        finish_time.append(-1)
    for i in range(num):
        arrival_time.append(int(list[i][0]))
    for i in range(num):
        need_time.append(int(list[i][1]))
        burst_time.append(int(list[i][1]))
        if need_time[i] == 0:
            finish_time[i] = arrival_time[i]
            num_of_processes_need_to_run -= 1
    index_min_burst = 0
    for i in range(num):
        if need_time[i] > 0 and arrival_time[i] <= curr_time:
            if burst_time[i] <= burst_time[index_min_burst] and finish_time[i] == -1:
                run_now_index = i
                index_min_burst = i
    while True:
        if num_of_processes_need_to_run == 0:
            break
        if need_time[run_now_index] > 0:
            need_time[run_now_index] -= 1
            if need_time[run_now_index] == 0:
                finish_time[run_now_index] = curr_time
                num_of_processes_need_to_run -= 1
                if num_of_processes_need_to_run == 0:
                    break
        for i in range(num):
            if finish_time[i] == -1 and need_time[i] > 0 and arrival_time[i] <= curr_time:
                index_min_burst = i
                break
        for i in range(num):
            if need_time[i] > 0 and arrival_time[i] <= curr_time:
                if burst_time[i] <= burst_time[index_min_burst] and finish_time[i] == -1:
                    run_now_index = i
                    index_min_burst = i
        curr_time += 1
    for i in range(num):
        turnaround += finish_time[i] - arrival_time[i]
    turnaround = turnaround / num
    print("SJF: mean turnaround =", turnaround)


def main():
    with open(sys.argv[1]) as file:
        numOfProcesses = file.readline()
        num = int(numOfProcesses)
        list = []
        process_list = []
        for i in range(num):
            list.append(file.readline().split('\n')[0])
        for i in range(num):
            list[i] = list[i].split(",")
        for i in range(num):
            process_list.append([0, 0, 0])
            process_list[i][0] = list[i][0]
            process_list[i][1] = list[i][1]
            # line num in the file
            process_list[i][2] = i
        process_list.sort()
        prev_arrival = process_list[0][2]
        prev_arrival_index = 0
        # for the swap, just initialization here
        for i in range(num):
            if process_list[i][0] == prev_arrival:
                if process_list[i][2] < process_list[prev_arrival_index][2]:
                    # swap
                    curr_process = process_list[i]
                    prev_process = process_list[prev_arrival_index]
                    process_list[i] = prev_process
                    process_list[prev_arrival_index] = curr_process
            prev_arrival = process_list[i][0]
            prev_arrival_index = i
        print(process_list)
        compute_FCFS(process_list, num)
        compute_LCFS_NP(process_list, num)
        compute_LCFS_P(process_list, num)
        compute_RR(process_list, num)
        compute_SJF(process_list, num)


if __name__ == "__main__":
    main()
