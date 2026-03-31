import socket
import threading
import time
import ipaddress

port_service={
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy"
}

high_risk_ports=[21,22,445,3389]

open_port_count=0
lock=threading.Lock()

def get_banner(target_ip,port,timeout=1):
    try:
        socket_object=socket.socket()
        socket_object.settimeout(timeout)
        socket_object.connect((target_ip,port))
        if port==80 or port ==8080:
            socket_object.send(b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n")
        receive_data=socket_object.recv(1024)
        socket_object.close()
        try:
            return receive_data.decode("utf-8").strip()
        except:
            return receive_data.decode("gbk",errors="ignore").strip()
    except:
        return "No Banner"
    
def scan_port(target_ip,port,open_ports_list):
    global open_port_count
    try:
        socket_object=socket.socket()
        socket_object.settimeout(0.3)
        connect_result=socket_object.connect_ex((target_ip,port))
        if connect_result==0:
            service=port_service.get(port,"Unknown")
            banner=get_banner(target_ip,port)
            if port in high_risk_ports:
                print(f"[高危]{target_ip:15}{port:5}{service:10}{banner[:50]}")
            else:
                print(f"[+]开放{target_ip:15}{port:5}{service:10}{banner[:50]}")
            with lock:
                open_port_count=open_port_count+1
            open_ports_list.append((target_ip,port,service,banner))
        socket_object.close()
    except:
        pass

def parse_ip_address(input_string):
    ip_list=[]
    try:
        network=ipaddress.ip_network(input_string,strict=False)
        for ip in network.hosts():
            ip_list.append(str(ip))
    except:
        if "-" in input_string:
            start_ip_string,end_ip_string=input_string.split("-")
            start_ip=list(map(int,start_ip_string.split(".")))
            end_ip=list(map(int,end_ip_string.aplit(".")))
            for last_number in range(start_ip[3],end_ip[3]+1):
                current_ip=f"{start_ip[0]}.{start_ip[1]}.{start_ip[2]}.{last_number}"
                ip_list.append(current_ip)
    return ip_list

def main():
    start_time=time.time()
    print("day10")
    input_target = input("请输入目标(192.168.1.0/24 或 192.168.1.1-10)：").strip()
    port_range = input("请输入端口范围(例如 1-1000)：").strip()
    max_thread_number = int(input("请输入最大线程数(推荐50)："))

    start_port, end_port = map(int, port_range.split("-"))
    ip_list = parse_ip_address(input_target)

    open_ports_list = []
    thread_pool = []

    print("\n开始扫描...\n")

    for ip in ip_list:
        for port in range(start_port, end_port + 1):
            while len(thread_pool) >= max_thread_number:
                thread_pool = [t for t in thread_pool if t.is_alive()]
            thread_object = threading.Thread(target=scan_port, args=(ip, port, open_ports_list))
            thread_pool.append(thread_object)
            thread_object.start()

    for thread_object in thread_pool:
        thread_object.join()

    print("\n========== 扫描完成 ==========")
    total_use_time = round(time.time() - start_time, 2)
    print(f"总耗时：{total_use_time} 秒")
    print(f"总共发现开放端口数量：{open_port_count}")

    time_string = time.strftime("%Y%m%d_%H%M%S")
    with open(f"scan_result_{time_string}.txt", "w", encoding="utf-8") as file_object:
        for ip, port, service, banner in open_ports_list:
            file_object.write(f"{ip} | {port} | {service} | {banner}\n")
    print("\n扫描结果已经保存到文件中！")

if __name__ == "__main__":
    main()
