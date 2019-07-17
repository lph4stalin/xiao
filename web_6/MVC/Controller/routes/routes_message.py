from Model import *

def route_messages(request):
    messages_list = Message.all()
    if request.method == 'POST':
        form = request.form()
        msg = Message(form)
        messages_list.append(msg)
        msg.save()
        # 应该在这里保存 messages_list
    r = page(request).decode(encoding='utf-8')
    # '#'.join(['a', 'b', 'c']) 的结果是 'a#b#c'
    msgs = '<br>'.join([str(m) for m in messages_list])
    r = r.replace('{{messagess}}', msgs)
    return r.encode(encoding='utf-8')
