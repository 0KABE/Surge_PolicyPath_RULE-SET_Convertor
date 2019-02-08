import re
import requests


def GetPolicyNode(source):  # 获取policy-path中含有的节点，并将其添加在[Proxy]中
    s = re.findall("policy-path *= *([^ ,\n]*)", source)
    # 去除重复节点
    s = list(set(s))
    a = set()
    # 下载对应的List
    for index in range(len(s)):
        temp = requests.get(s[index])
        temp = bytes.decode(temp.content).splitlines()
        for index in range(len(temp)):
            a.add(temp[index])
    # 保存已经存在的[Proxy]内节点
    exist = re.search(r"\[Proxy\]((.|\n|\r)*)\[Proxy Group\]", source)
    a.add(exist.group(1).strip(" \n"))
    a = sorted(a)
    a = ",\n".join(a)
    toinstead = "[Proxy]\n" + a + "\n[Proxy Group]\n"
    source = source.replace(exist.group(), toinstead)
    return source


def PolicyPathTransfer(data):  # 获取policy-path后面的url 并把其转化为普通的版本
    pattern = re.compile("policy-path *= *[^ ,\n]*")
    search = re.search(pattern, data)
    while search:
        url = search.group(0).split("=", 1)[1]
        r = requests.get(url)
        s = bytes.decode(r.content)
        s = s.split("\n")
        instead = ""
        for index in range(len(s)-2):
            s[index] = s[index].split("=", 1)[0]
            instead += s[index]+","
        instead += s[len(s)-2].split("=", 1)[0]
        data = data.replace(search.group(), instead)
        search = re.search(pattern, data)
    return data


def RuleSetTransfer(source):  # 将RULE-SET转化为普通的，可以在CLASH上使用的版本
    rule = re.findall("RULE-SET *, *([^,\n]*) *, *([^,\n]*)", source)
    # 获取每个RULE-SET地址
    for i in rule:
        if(i[0] in {"SYSTEM", "LAN"}):
            continue
        temp = requests.get(i[0])
        temp = bytes.decode(temp.content).splitlines()
        if(temp[0] == "404: Not Found"):
            continue
        for index in range(len(temp)):
            # 跳过注释
            if(temp[index].startswith("#") or temp[index].startswith("//") or len(temp[index]) == 0):
                continue
            comment = re.search("//.*", temp[index])
            if(comment == None):
                temp[index] += ", "+i[1]
            else:
                temp[index] = temp[index].replace(
                    comment.group(), "")+i[1]
            NoResolve = re.search(
                "IP-CIDR *(.*) *, *no-resolve *, *(.*)", temp[index])
            if(NoResolve != None):
                temp[index] = "IP-CIDR" + \
                    NoResolve.group(1)+","+NoResolve.group(2)+",no-resolve"
        r = re.search("RULE-SET.*", source)
        source = source.replace(r.group(), "\n".join(temp))

    rule = re.findall("RULE-SET.*", source)
    for i in rule:
        source = source.replace(i, "")
    return source


# 被打开的Surge文件,根据需要进行修改
f = open("C:/Users/OKAB3/iCloudDrive/iCloud~com~nssurge~inc/OKAB3-Clash.conf",
         "r", encoding='utf-8')
# 转换之后的Surge文件,根据需要进行修改
w = open("C:/Users/OKAB3/Documents/PolicyPathConvertor/OKAB3-Clash.conf",
         "w", encoding='utf-8')
source = f.read()
source = GetPolicyNode(source)
source = PolicyPathTransfer(source)
source = RuleSetTransfer(source)
w.write(source)
