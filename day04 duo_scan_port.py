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
        s.settimeout(0.5)
        #尝试去连接目标ip和端口
        s.commect(target_ip,port)
        
        print(f"端口{port:5d}-open")
        open_ports.append(port)

    except ConnectionRefusedError:
        #连接被拒绝，端口关闭，返回colsed
        #print(f"端口{port:5d}-closed")
        pass
    except TimeoutError:
        #连接超时，防火墙拦截/端口不可达，返回timeout
        #print(f"端口{port:5d}-timeout")
        pass
    except Exception as e:
        #其他错误，打印错误，返回错误信息
        #print(f"端口{port:5d}-error:{e}")
        pass
    finally:
        #无论成败都关闭socket释放资源
        try:
            s.close()
        except:
            pass
#将当前文件身份赋值为主程序，便于后续复用这个函数
if __name__=="__main__":
    #用户输入目标ip并去掉首尾空格
    target_ip=input("请输入目标ip：").strip()
    try:
        #用户输入目标端口范围并去掉空格
        port_range=input("请输入端口范围：").strip()
        #去掉空格，防止格式错误
        port_range=port_range.replace(" ","")
        #用-连接首尾端口范围
        start_str,end_str=port_range.split("-")
        #将范围都变为int类型
        start_port=int(start_str)
        end_port=int(end_str)
        #限制端口范围在1-65535
        if not (1<=start_port<=65535)  or not (1<=end_port<=65535):
            print("【错误】端口范围应该在1-65535之间")
            exit()#当程序发生错误时及时中断
        #限制起始端口不该大于结束端口
        if start_port > end_port:
            print("【错误】起始端口应该小于结束端口")
            exit()
    #防止格式错误
    except ValueError:
        print("【错误】端口格式错误，请输入1-100之类的地址")
        exit()
    #防止其他错误
    except Exception as e:
        print(f"【错误】输入解析失败：{e}")
        exit()
#创建一个空列表，将后续符合要求的值放入
open_ports=[]
threads=[]#用来存放所有创建的线程，方便后续等待
print(f"\n[扫描开始]目标ip：{target_ip},端口范围：{start_port}--{end_port}")
#打印分隔符
print("="*50)
#注意遍历时左闭右开
for port in range(start_port,end_port+1):
    #拆昂见线程对象
    t=threading.Thread(
        target=scan_port,#制定线程要执行的函数
        args=(target_ip,port,open_ports)#传给函数的参数
    )
    threads.append(t)#把线程加入列表
    t.start()#启动另一个线程，不必等前一个线程结束
for t in threads:
    t.join()#主线程等待线程执行完毕

print("="*50)
print("[扫描完成]汇总结果：")
if open_ports:
    open_ports.sort()#对开放的端口排序
    print(f"开放的端口：{open_ports}")
    print(f"共发现{len(open_ports)}个开放端口")
else:
    print("未发现开放的端口")



