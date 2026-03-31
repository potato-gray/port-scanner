#导入socket模块（网络通信）
import socket
#导入threading模块（多线程）
import threading
#定义核心扫描函数
def scan_port(target_ip,port,open_ports):
    try:
        #创建一个socket对象，并把这个对象赋值给变量s,ipv4格式
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #设置超时时间，避免脚本卡死
        s.settimeout(0.3)
        #尝试去连接目标ip和端口
        s.connect(target_ip,port)
        
        print(f"端口{port:5d}-open")
        open_ports.append(port)

    except:
        pass
    finally:
        #无论成败都关闭socket释放资源
        try:
            s.close()
        except:
            pass
def main():
    target_ip=input("请输入目标ip").strip()
    port_range=input("请输入端口范围：").strip().replace(" ","")
    thread_max=int(input("请输入最大线程数："))

    start_str,end_str=port_range.split("-")
    start_port=int(start_str)
    end_port=int(end_str)

    open_ports=[]
    thread_pool=[]

    print("\n"+"="*50)
    print(f"开始扫描：{target_ip}端口{start_port}-{end_port}")
    print(f"最大线程：{thread_max}")
    print("="*60+"\n")

    for port in range(start_port,end_port+1):
        t=threading.Thread(
            target=scan_port,
            args=(target_ip,port,open_ports)
        )

    while len(thread_pool)>=thread_max:
        thread_pool=[t for t in thread_pool if t.is_alive()]
    
    thread_pool.append(t)
    t.start()

    for t in thread_pool:
        t.join()

    open_ports.sort()

    print("\n"+"="*50)
    print("扫描完成")
    if open_ports:
        print(f"开放端口：{open_ports}")
        print(f"总数：{len(open_ports)}")
    else:
        print(f"未发现端口")
    print("="*50)

    with open("result.txt","w",encoding="utf-8") as f:
        f.write(f"扫描目标：{target_ip}\n")
        f.write(f"端口范围：{start_port}-{end_port}\n")
        f.write(f"开放端口：{open_ports}\n")
        f.write(f"总数：{len(open_ports)}\n")
    print("\n结果已保存到result.txt")

if __name__=="__main__":
    main()


