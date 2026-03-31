#print("hyh我永远爱你")
# ip="192.168.31.123"
# port=8080
# is_open=True
# password="123456"

#print("目标ip：",ip)
#print("开放端口：",port)
#print("端口是否开放：",is_open)
      
#print(type(ip))
#print(type(port))
#print(type(is_open))


# target=ip+":"+str(port)
# #print("目标地址：",target)
# new_port=port+10
# #print("新端口：",new_port)

# username="admin"
# password="123qwe"
#print("用户名：",username,",","密码：",password)

#target_ip=input("请输入目标ip：")
#target_port=int(input("请输入目标端口："))
#print("你要扫描的目标是：",target_ip,":",target_port)

#user=input("请输入用户名：")
#pwd=input("请输入密码：")
#print("你输入的用户名:",user,"密码：",pwd)

# wcom=input("请输入目标域名：")
# sum=int(input("请输入扫描线程数:"))
# #print("目标域名为：",wcom,"扫描线程数为：",sum)
# print(f"目标域名为：{wcom},扫描线程数为：{sum}")

common_ports=[80,443,8080,21,3389]
try:
    user_port=int(input("请输入端口："))
    if (1 <= user_port <= 65535):
        
        if user_port in common_ports:
            print(f"[检测结果]端口{user_port}是常见端口")
        else:
            print(f"[检测结果]端口{user_port}不是常见端口")
    else:
        print(f"【检测结果】{user_port}超出合法范围（1-65525)")
except ValueError:
    print("输入错误，输入格式不正确，请输入数字格式的端口")
except Exception as e:
    print(f"[检测结果]发生未知错误：{e}")



    

    



