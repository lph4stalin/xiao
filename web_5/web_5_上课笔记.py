"""
一、作业讲解
redirect，重定向函数
location 处如果不指定host，默认使用当前页面的host

二、todo程序
routes_todo.py 包含了项目的所有路由函数：显示所有todo，增加todo，更新todo，删除todo
todo.py 包含所有 Todo Model，用于处理数据
templates/todo_index.html 显示所有 todo 页面
templates/todo_edit.html 显示编辑 todo 页面

/todo/add --> 添加todo的页面 --> todo_index.html
/todo/

新增原理：点击 add 添加新 todo 时，程序流程如下：
    1，浏览器提交一个表单给服务器（POST请求）
    2，服务器解析出表单数据，并且添加一条数据到数据库，并返回302响应
    3，浏览器根据302中的地址，自动发送一条GET请求
    4，服务器给浏览器一个页面响应

修改原理：同样的在触发时得到需要修改的内容，在数据库修改，然后全量返回数据库里的 todo
做一个超链接来作为用户发送数据的网页

验证用户：在数据库里加入一个字段-用户id，来判断todo的归属
只有经过登录验证且id一致才能访问、修改和删除todo

"""
