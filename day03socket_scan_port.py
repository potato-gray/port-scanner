# #引入socket
# import socket

# def scan_port(target_ip,port):
#     # 扫描目标ip和端口，返回端口状态
#     # param target_ip为目标ip
#     # param port为目标端口
#     # :return:端口状态（open/closed）
#     try:
#     #创建TCP socket对象
#         s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     #设置超时时间0.5s 避免脚本卡在不可达端口上
#         s.settimeout(0.5)
#     #创建连接
#         s.connect((target_ip,port))
#     #open即与目标端口连接成功
#         return "open"
#     except ConnectionRefusedError:
#     #拒绝连接返回closed
#         return "closed"
#     except TimeoutError:
#     #超时返回timeout
#         return "timeout"
#     except Exception as e:
#     #发生其他异常
#         return f"error:{e}"
#     finally:
#     #最后无论如何都要关闭连接，释放本地资源
#         try:
#             s.close()
#         except:
#             pass

# #主程序逻辑
# if __name__ == "__main__":
#     #1.创建用户输入ip并去掉首位空格
#     target_ip=input("请输入目标ip：").strip()
#     #2.创建用户输入port
#     try:
#         port_range=input("请输入端口范围：").strip()
#         #去掉空格
#         port_range=port_range.replace(" ","")
#         start_str,end_str=port_range.split("-")
#         start_port=int(start_str)
#         end_port=int(end_str)

#         #合法性校验
#         if not (1<=start_port<=65535)or not(1<=end_port<=65535):
#             print("[错误]端口必须在1-65535之间！")
#             exit()
#         if start_port>end_port:
#             print("[错误]起始端口不能大于结束端口")
#             exit()
#     except ValueError:
#         print("[错误]端口范围格式错误！请输入1-100的格式")
#         exit()
#     except Exception as e:
#         print(f"[错误]输入解析失败：{e}")
#         exit()

#     #3.初始化结果收集列表
#     open_ports=[]
#     print(f"[扫描开始]目标ip:{target_ip},端口范围：{start_port}-{end_port}")
#     print("="*50)

#     #4.批量扫描端口，range左闭右开
#     for port in range(start_port,end_port+1):
#         status=scan_port(target_ip,port)
#         #打印出所需端口
#         print(f"端口{port:5d}→{status}")
#         #如果能成功建立连接就放进open_ports里
#         if status =="open":
#             open_ports.append(port)
            
#     #5.汇总结果
#     print("="*50)
#     print("[扫描完成]汇总结果：")
#     if open_ports:
#         print(f"开放的端口：{open_ports}")
#         print(f"共发现{len(open_ports)}个开放端口")
#     else:
#         print("未发现开放的端口")


#导入socket模块
import socket
#定义核心扫描函数
def scan_port(target_ip,port):
    try:
        #创建一个socket对象，并把这个对象赋值给变量s
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #设置超时时间，避免脚本卡死
        s.settimeout(0.5)
        #尝试去连接目标ip和端口
        s.connect(target_ip,port)
        #连接成功返回open
        return "open"
    except ConnectionRefusedError:
        #连接被拒绝，端口关闭，返回colsed
        return "closed"
    except TimeoutError:
        #连接超时，防火墙拦截/端口不可达，返回timeout
        return "timeout"
    except Exception as e:
        #其他错误，返回错误信息
        return f"error:{e}"
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
print(f"\n[扫描开始]目标ip：{target_ip},端口范围：{start_port}--{end_port}")
#打印分隔符
print("="*50)
#注意遍历时左闭右开
for port in range(start_port,end_port+1):
    #status 1.暂存结果 2.标准化结果 3.简化代码
    status=scan_port(target_ip,port)
    #实时打印状态（5d是格式化）
    print(f"端口{port:5d}-{status}")
    #收集开放端口
    if status=="open":
        open_ports.append(port)

print("="*50)
print("[扫描完成]汇总结果：")
if open_ports:
    print(f"开放的端口：{open_ports}")
    print(f"共发现{len(open_ports)}个开放端口")
else:
    print("未发现开放的端口")


    