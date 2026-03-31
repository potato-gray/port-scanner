import socket
import threading
import time

# 端口-服务对照表
port_service = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy"
}

# 高危端口
high_risk_ports = [21, 22, 445, 3389, 6379, 27017]

open_port_count = 0
lock = threading.Lock()

# ===================== Day8 新增：获取Banner =====================
def get_banner(ip, port, timeout=2):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        
        # ================= 关键改进：根据不同端口发送探测命令 =================
        banner = b""
        
        if port == 25:  # SMTP
            s.send(b"HELO test\r\n")
            banner = s.recv(1024)
        elif port in [110, 143]:  # POP3 / IMAP
            banner = s.recv(1024)  # 这两个端口通常连接即发Banner，或者需要先读
        else:
            # 其他端口直接读取
            banner = s.recv(1024)
        
        s.close()
        
        # 尝试解码
        try:
            return banner.decode("utf-8").strip()
        except:
            return banner.decode("gbk", errors="ignore").strip()
            
    except Exception as e:
        # print(f"获取Banner失败：{e}") # 调试用
        return "No Banner"

def scan_port(target_ip, port, open_ports):
    global open_port_count
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            service = port_service.get(port, "Unknown Service")
            
            # ===================== Day8：获取Banner =====================
            banner = get_banner(target_ip, port)
            
            if port in high_risk_ports:
                print(f"[⚠️ 高危] {port:5d} {service:12} | {banner[:50]}")
            else:
                print(f"[+] 开放 {port:5d} {service:12} | {banner[:50]}")
            
            with lock:
                open_port_count += 1
            open_ports.append((port, service, banner))  # 存入Banner
            
        s.close()
    except:
        pass

def main():
    start_time = time.time()
    
    target_ip = input("目标IP：").strip()
    port_range = input("端口范围（1-1000）：").strip()
    thread_max = int(input("线程数（推荐50）："))
    
    try:
        start_port, end_port = map(int, port_range.split("-"))
    except:
        print("格式错误！如 1-1000")
        return

    open_ports = []
    thread_pool = []

    print("\n" + "="*60)
    print(f"开始扫描：{target_ip}")
    print("="*60 + "\n")

    for port in range(start_port, end_port + 1):
        while len(thread_pool) >= thread_max:
            thread_pool = [t for t in thread_pool if t.is_alive()]
        
        t = threading.Thread(target=scan_port, args=(target_ip, port, open_ports))
        thread_pool.append(t)
        t.start()

    for t in thread_pool:
        t.join()

    scan_duration = round(time.time() - start_time, 2)

    print("\n" + "="*50)
    print(f"扫描完成！耗时：{scan_duration}s")
    print(f"开放端口总数：{open_port_count}")
    print("="*50)

    # 保存文件（新增Banner）
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    with open(f"scan_result_{timestamp}.txt", "w", encoding="utf-8") as f:
        f.write(f"扫描目标：{target_ip}\n")
        f.write(f"耗时：{scan_duration}s\n\n")
        for port, service, banner in open_ports:
            f.write(f"{port} | {service} | {banner}\n")

    print("\n结果已保存！")

if __name__ == "__main__":
    main()



