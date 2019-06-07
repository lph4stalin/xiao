一、提问的智慧
提问之前要把思路整理好，并给出问题的必要条件。
目标：提出一个帮你解决问题的问题。


二、代码解析
1.服务器运行的主程序：监听 → 接收请求 → 解析请求 → 生成响应报文 → 发送响应报文 → 关闭连接
2.解析请求：把请求拆分成 method、route、query 和 body 4 部分
3.生成响应报文：
① 根据 route 返回对应的页面
② 根据 method、query 个性化返回报文

如果请求是 POST，那么请求的 Body 里就会包含 query
所以需要解析 query

三、MVC 设计模式
将一个程序分为三个部分
Model       数据
View        显示
Controller  控制器
V 是前端显示的内容
M 是后端存储的数据
C 沟通 M 和 V

四、代码重写
功能：①能够根据地址返回 html_basic、index、login、register四个网页
