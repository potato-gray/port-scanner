import socket
import threading

port_service={
    21:"FTP",
    22:"SSH",
    23:"Telnet",
    53:"DNS",
    80:"HTTP",
    110:"POP3",
    139:"NetBIOS",
    443:"HTTPS",
    445:"SMB",
    3306:"MySQL",
    3389:"RDP",
    8080:"HHTP-Proxy"
}
def scan_port(target_ip,port,open_ports):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(0.3)
        s.connect((target_ip,port))

        service=port_service.get(port,"Unknow Service")
        print(f"[+]端口{port:5d}开放|服务：{service}")
        open_ports.append((port,service))
    except:
        pass
    finally:
        try:
            s.close()
        except:
            pass

def main():
    target_ip=input("请输入目标ip：").strip()
    port_range=input("端口范围：").strip().replace(" ","")
    thread_max=int(input("最大线程数:"))

    start_str,end_str=port_range.split("-")
    start_port=int(start_str)
    end_port=int(end_str)

    open_ports=[]
    thread_pool=[]
    print("\n"+"="*60)
    print(f"开始扫描：{target_ip}")
    print(f" 线程数：{thread_max}")
    print("="*60 + "\n")

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port, open_ports))

        while len(thread_pool) >= thread_max:
            thread_pool = [t for t in thread_pool if t.is_alive()]

        thread_pool.append(t)
        t.start()

    for t in thread_pool:
        t.join()



    open_ports.sort(key=lambda x:x[0])
    print("\n"+"="*50)
    print("扫描完成！")
    if open_ports:
        for port,service in open_ports:
            print(f"{port:5d}-{service}")
        print(f"共发现{len(open_ports)}个开放端口")
    else:
        print("未发现开放端口")
    print("="*50)

    #打开result.txt文件，写入模式，用utf-8编码
    with open("result.txt","w",encoding="utf-8")as f:
        f.write(f"扫描目标：{target_ip}\n")
        f.write(f"端口范围：{start_port}-{end_port}\n")
        f.write("\n开放端口列表：\n")
        for port,service in open_ports:
            f.write(f"{port}-{service}\n")

    print("\n 结果已保存至 result.txt")

if __name__ == "__main__":
    main()