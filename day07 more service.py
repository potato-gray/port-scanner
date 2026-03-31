import socket
import threading

import time#统计耗时
import os#检查文件路径

port_service={
    21:"FTP",
    22:"SSH",
    445:"SMB",
    80:"HTTP",
    443:"HTTPS",
    3306:"MySQL",
    3389:"RDP",
    1433:"SQLServer",
    6379:"Redis",
    27017:"MongoDB"
}

#高危端口列表
high_risk_ports=[21,22,445,3389,6379,27017]
#创建全局变量：统计开放端口数
open_port_count=0
#线程锁，避免计数错误
lock=threading.Lock()
def scan_port(target_ip,port,open_ports):
    #声明要修改的open_port_count是全局变量
    global open_port_count
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(0.3)
        #尝试连接端口，用connect_ex避免直接报错
        result=s.connect_ex((target_ip,port))

        if result==0:  #0表示端口开放
            #查服务
            service=port_service.get(port,"Unknown Service")

            if port in high_risk_ports:
                print(f"[高危端口]端口{port:5d}开放|服务：{service}")
            else:
                print(f"端口{port:5d}开放|服务：{service}")

            #线程安全计数
            with lock:
                open_port_count += 1
            open_ports.append((port,service))

        s.close()

    #捕获所有异常，避免单个端口扫描崩溃导致脚本停止
    except socket.timeout:
        pass
    except socket.gaierror:
        print(f"[错误]ip地址{target_ip}解析失败！")
        return
    except Exception as e:
        print(f"[未知错误]扫描端口{port}时出错：{str(e)}")

def main():
    #记录扫描开始时间
    start_time=time.time()
    #获取用户输入
    target_ip=input("请输入目标ip：").strip()
    port_range=input("端口范围：").strip().replace(" ","")
    thread_max=int(input("最大线程数："))

    try:
        start_str,end_str=port_range.split("-")
        start_port=int(start_str)
        end_port=int(end_str)
        if start_port<1 or end_port>65535 or start_port>end_port:
            print("[错误]端口范围输入错误！请输入1-65535之间的有效范围")
            return
    except:
        print("[错误]端口范围格式错误！请输入如1-1000的格式")
        return
    #创建空列表
    open_ports=[]
    thread_pool=[]

    print("\n"+"="*60)
    print(f"开始扫描：{target_ip}(端口范围：{start_port}-{end_port})")
    print(f"线程数:{thread_max} | 扫描时间：{time.ctime(start_time)}")
    print("="*60+"\n")

    #开始扫描
    for port in range(start_port,end_port+1):
        #控制线程数，避免过多
        while len(thread_pool)>=thread_max:
            thread_pool=[t for t in thread_pool if t.is_alive()]
        t=threading.Thread(target=scan_port,args={target_ip,port,open_ports})
        thread_pool.append(t)
        t.start()

    #等待所有线程结束
    for t in thread_pool:
        t.join()

    #计算扫描耗时
    end_time=time.time()
    scan_duration=round(end_time-start_time,2)

    #排序开放端口
    open_ports.sort(key=lambda x: x[0])

    #打印扫描结果汇总
    print("\n"+"="*50)
    print("扫描完成！")
    print(f"总耗时:{scan_duration}秒")
    print(f"共扫描{end_port - start_port+1}个端口|开放{open_port_count}个")
    if open_ports:
        print("开放端口列表：")
        for port,service in open_ports:
            #高危端口标红
            if port in high_risk_ports:
                print(f"{port:5d}-{service}")
            else:
                print(f"{port:5d}-{service}")
    else:
        print("未发现开放端口")
    print("="*50)

    #文件保存，生成带时间戳的文件名，避免覆盖
    timestamp=time.strftime("%Y%m%d_%H%M%S")
    file_name=f"port_scan_result_{timestamp}.txt"

    try:
        with open(file_name,"w",encoding="utf-8")as f:
            f.write("="*40 + " 端口扫描报告 " + "="*40 + "\n")
            f.write(f"扫描目标：{target_ip}\n")
            f.write(f"端口范围：{start_port}-{end_port}\n")
            f.write(f"扫描时间：{time.ctime(start_time)}\n")
            f.write(f"总耗时:{scan_duration}秒\n")
            f.write(f"扫描端口总数:{end_port-start_port+1}\n")
            f.write(f"开放端口数：{open_port_count}\n\n")

            #写入开放端口
            f.write("[高危端口]\n")
            high_risk_open=[p for p in open_ports if p[0] in high_risk_ports]
            if high_risk_open:
                for port,service in high_risk_open:
                    f.write(f"{port}\t{service}\n")
            else:
                f.write("无\n")

            f.write("\n[普通开放端口]\n")
            normal_open=[p for p in open_ports if p[0] not in high_risk_ports]
            if normal_open:
                for port,service in normal_open:
                    f.write(f"{port}\t{service}\n")
            else:
                f.write("无\n")

        #打印文件保存路径
        file_path=os.path.abspath(file_name)
        print(f"\n扫描报告已保存至：{file_path}")
    except Exception as e:
        print(f"[错误]保存文件失败：{str(e)}")

if __name__=="__main__":
    main()


def main():
    start_time=time.time()
    target_ip=input("请输入目标IP：").strip()
    port_range=input("端口范围:").strip().replace(" ","")
    thread_max=int(input("最大线程数："))

    try:
        start_str,end_str=port_range.split("-")
        start_port=int(start_str)
        end_port=int(end_str)
        if start_port < 1 or end_port >65535 or start_port > end_port:
            print("端口范围输入错误！请输入1-65535之间的有效范围")
            return
    except:
        print("[错误]端口范围格式错误！请输入1-1000的格式")
        return
    
    open_ports=[]
    thread_pool=[]

    print("\n"+"="*60)
    print(f"开始扫描：{target_ip}(端口范围：{start_port}-{end_port})")
    print(f"线程数：{thread_max}|扫描时间：{time.ctime(start_time)}")
    print("="*60+"\n")

    for port in range(start_port,end_port+1):
        while len(thread_pool)>=thread_max:
            thread_pool=[t for t in thread_pool if t.is_alive()]

        t=threading.Thread(target=scan_port,args=(target_ip,port,open_ports))
        thread_pool.append(t)
        t.start()

    for t in thread_pool:
        t.join()

    end_time=time.time()
    scan_duration=round(end_time-start_time,2)

    open_ports.sort(key=lambda x:x[0])

    print("\n"+"="*50)
    print("扫描完成！")
    print(f"总耗时：{scan_duration}秒")



 