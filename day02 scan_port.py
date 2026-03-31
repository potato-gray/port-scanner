common_ports=[80,443,22,21,3389,8080]

try:
    port_range=input("输入端口范围：")
    port_range=port_range.replace(" ","")
    parts=start_str,end_str=port_range.split("-")
    start_port=int(start_str)
    end_port=int(end_str)

    if len(parts)!=2:
        print("[错误]格式错误！请输入'start-end'格式")
        exit()
        

    if not(1<=start_port<=65535)or not(1<=end_port<=65535):
        print("[检测结果]端口必须在1-65535之间")
        exit()
    if start_port>end_port:
        print("起始端口不能大于结束端口")
        exit()

    print(f"【扫描开始】范围：{start_port}-{end_port}")
    found=[]
    for port in range(start_port,end_port+1):
        if port in common_ports:
            found.append(port)
            print(f"发现常见端口：{port}")

    print("[扫描完成]")
    if found:
        print(f"共发现{len(found)}个常见端口：{found}")
    else:
        print("该范围内没有发现常见端口")
    

except ValueError:
    print("输入格式错误！请输入'start-end'格式")
except Exception as e:
    print(f"未知异常：{e}")
