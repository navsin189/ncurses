import curses
import psutil
import json
import time
def get_process_detail(key):
    cpu_usage_for_pid = {}
    memory_usage_for_pid = {}
    process_detail_list = []
    for process in psutil.process_iter():
        try:
            pinfo = process.as_dict(attrs=['cmdline', 'pid', 'ppid', 'memory_info', 'create_time', 'name', 'username', 'cpu_percent'])
            if pinfo['cmdline'] == []:
                continue
            cpu_usage_for_pid[pinfo['pid']] = pinfo['cpu_percent']
            memory_usage_for_pid[pinfo['pid']] = pinfo['memory_info'].data/1024**3
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("not allowed")
            continue
    memory_usage_for_pid = dict(sorted(memory_usage_for_pid.items(), key=lambda item: item[1],reverse=True))
    cpu_usage_for_pid = dict(sorted(cpu_usage_for_pid.items(), key=lambda item: item[1],reverse=True))
    with open('cpu_usage.txt','w') as fd:
        fd.write(json.dumps(cpu_usage_for_pid,indent=4))

    for pid in cpu_usage_for_pid.keys():
        process = psutil.Process(pid)
        memory = round(process.memory_info().data/1024**2,2)
        cmdline = " ".join(process.cmdline())
        process_detail_list.append(f"{pid :<6} {process.cpu_percent() :<5} {memory :<10} {process.name() :<30} {cmdline}")
    if key == ord('m'):
        for pid in memory_usage_for_pid.keys():
            process = psutil.Process(pid)
            memory = round(process.memory_info().data/1024**3,2)
            cmdline = " ".join(process.cmdline())
            process_detail_list.append(f"{pid :<6} {process.cpu_percent() :<5} {memory :<10} {process.name() :<30} {cmdline}")
    return process_detail_list

def get_cpu_memory_detail():
    memory_info = psutil.virtual_memory()
    cpu_usage = psutil.cpu_percent(interval=1)
    total_memory = f"{'Total memory:':<20} {memory_info.total / (1024 ** 3):.2f} GB"
    available_memory = f"{'Available memory:':<20} {memory_info.available / (1024 ** 3):.2f} GB"
    used_memory = f"{'Used memory:':<20} {memory_info.used / (1024 ** 3):.2f} GB"
    memory_usage = f"{'% Used Memory:':<20} {memory_info.percent}%"
    cpu_usage = f"{'CPU Usage:':<20} {cpu_usage}%"
    memory_info = [total_memory,available_memory,used_memory,memory_usage]
    return memory_info,cpu_usage

def print_system_info(screen,key):
    curses.start_color() #to use colored text
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    screen.clear()
    
    height,width = screen.getmaxyx()
    memory_info,cpu_usage = get_cpu_memory_detail()
    pos_y = 0
    for info in memory_info:
        screen.addstr(pos_y,0,info)
        pos_y += 1
    screen.addstr(pos_y,0,cpu_usage)
    pos_y += 1
    screen.addstr(pos_y,0,"")
    pos_y += 1
    screen.addstr(pos_y,0,f"{'PID' :<6} {'CPU%' :<5} {'MEMORY%' :<10} {'NAME' :<30} {'COMMAND'}",curses.color_pair(1))

    process_list = get_process_detail(key)
    for process in process_list[:height-10]:
        pos_y += 1
        screen.addstr(pos_y,0,process)
    # screen.addstr(pos_y+3,0,f"{height}")
    # screen.addstr(pos_y+6,0,f"{width}")

    screen.refresh()

def main(screen):
    curses.curs_set(0)
    
    screen.nodelay(True)
    
    while True:
        key = screen.getch()
        print_system_info(screen,key)

        if key == ord('q') or key == 27:  # 27 is the ASCII value for 'ESC'
            break

        # time.sleep(1)

if __name__ == "__main__":
    start_x = 0;start_y = 0
    curses.wrapper(main)
