from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

topics = { 
    {1: {'id':1, 'title':'html', 'body':'html is ..'}},
    {2: {'id':2, 'title':'css', 'body':'css is ..'}},
}

def nextId():
    return len(topics) + 1
    #혹은 삭제될것을 감안한다면( 이경우 아이디가ㅏ 중복될 수 있으므로 )
    return max(topic.keys()) + 1

def htmlTemplate(article, updateDelete=''):
    nav = ''
    for topic in topics:
        nav += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return f'''
        <html>
            <h2><a href="/">web</a></h2>
            <ol>
                {nav}
            </ol>
            {article}
            <ul>
                <li><a href="/create">create</a></li>
                {updateDelete}
            </ul>
        </html>
    '''
def updateDeleteTempalte(id):
    return f'''
        <li><a href="/update/{id}">update</a></li>
        <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
    '''
def index(request):
    article = '''
        <h2>welcome</h2>
        Hello, WEB
    '''
    return HttpResponse(htmlTemplate(article))

def getTopicById(id):
    return topic[id]

def read(request, id):
    topic = getTopicById(id)
    article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(htmlTemplate(article, updateDeleteTempalte(id)))

@csrf_exempt
def create(request):
    if request.method == 'GET':
        article = f'''
            <h2>Create</h2>
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(htmlTemplate(article, updateDeleteTempalte(id)))
    else :
        global topics
        title = request.POST['title']
        body = request.POST['body']
        nid = nextId()
        topics[nid] = {
            'id':nid,
            'title':title,
            'body':body
        }
        newURL = f'/read/{nid}'
        return redirect(newURL)

@csrf_exempt
def update(request, id):
    if request.method == 'GET':
        topic = getTopicById(id)
        article = f'''
            <h2>Update</h2>
            <form action="/update/{id}" method="post">
                <p><input type="text" name="title" placeholder="title" value="{topic['title']}"></p>
                <p><textarea name="body" placeholder="body">{topic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(htmlTemplate(article, updateDeleteTempalte(id)))
    else :
        global topics, nextId
        topics[id]['title'] = request.POST['title']
        topics[id]['body'] = request.POST['body']
        newURL = f'/read/{id}'
        return redirect(newURL)

@csrf_exempt
def delete(request, id):
    if request.method == 'POST':
        global topics
        del topics[id]
        return redirect('/')