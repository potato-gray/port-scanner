import socket
import threading
import time

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
def get_banner(ip,port,timeout=1):
    try:
        s=socket.socket()
        s.settimeout(timeout)
        s.connect((ip,port))
        if port==80 or port==8080:
            s.send(b"HEAD / HTTP/1.1\r\nHost: test\r\n\r\n")
        banner=s.recv(1024)#接受服务器返回的信息
        s.close()
        try:
            return banner.decode("utf-8").strip()
        except:
            return banner.decode("gbk","ignore").strip()
    except:
        return "No Banner"
    
def scan_port(target_ip,port,open_ports):
    global open_port_count
    try:
        s=socket.socket()
        s.settimeout(0.3)
        res=s.connect_ex((target_ip,port))
        if res==0:
            service=port_service.get(port,"Unknown")
            banner=get_banner(target_ip,port)
            if port in high_risk_ports:
                print(f"[高危]{target_ip:15}{port:5}{service:10}{banner[:50]}")
            else:
                print(f"[+]开放{target_ip:15}{port:5}{service:10}{banner:50}")
            with lock:
                open_port_count+=1
            open_ports.append((target_ip,port,service,banner))
        s.close()
    except:
        pass

def parse_ip_range(ip_range):
    start_ip_str,end_ip_str=ip_range.split("-")
    start_ip=list(map(int,start_ip_str.split(".")))
    end_ip=list(map(int,end_ip_str.split(".")))

    ip_list=[]
    for i in range(start_ip[3],end_ip[3]+1):
        ip=f"{start_ip[0]}.{start_ip[1]}.{start_ip[2]}.{i}"
        ip_list.append(ip)
    return ip_list

def main():
    start_time=time.time()

    print("IP段端口扫描器")
    ip_range=input("请输入ip段：").strip()
    port_range=input("端口范围：").strip()
    thread_max=int(input("最大线程数："))

    start_port,end_port=map(int,port_range.split("-"))
    ip_list=parse_ip_range(ip_range)
    open_ports=[]
    thread_pool=[]
    print("\n开始扫描...\n")

    #双层循环
    for ip in ip_list:
        for port in range(start_port,end_port+1):
            while len(thread_pool)>=thread_max:
                thread_pool=[t for t in thread_pool if t.is_alive()]
            t=threading.Thread(target=scan_port,args=(ip,port,open_ports))
            thread_pool.append(t)
            t.start()

    for t in thread_pool:
        t.join()

    print("\n扫描完成")
    print(f"总耗时：{round(time.time()-start_time,2)}s")
    print(f"共开放端口：{open_port_count}")

    ts=time.strftime("%Y%m%d_%H%M%S")
    with open(f"scan_c段_{ts}.txt","w",encoding="utf-8") as f:
        for ip,port,service,banner in open_ports:
            f.write(f"{ip}|{port}|{service}|{banner}\n")
    print("\n结果已保存！")
if __name__=="__main__":
    main()