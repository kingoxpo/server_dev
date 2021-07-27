from rest_framework.views import APIView
from .models import Task
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import render



class TaskSelect(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', None)
        page_number = request.data.get('page_number', None)

        if user_id and not "":
            # 실습3
            tasks = Task.objects.filter(user_id=user_id)
        else:
            # 실습2
            tasks = Task.objects.all()

        is_last_page = True

        if page_number is not None and page_number >=0:
            # 실습3
            if tasks.count() <= 10:
                pass
            elif tasks.count() <= (1 + page_number) * 10:
                tasks = tasks[page_number * 10:]
            else:
                is_last_page = False
                tasks = tasks[page_number * 10:(1 + page_number) * 10]

        else:
            # 실습2
            pass

        task_list = []
        for task in tasks:
            task_list.append(dict(id=task.id,
                                  name=task.name,
                                  userId=user_id,
                                  done=task.done))

        return Response(status=200, data=dict(tasks=task_list, isLastPage=is_last_page))


class TaskCreate(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', '')
        todo_id = request.data.get('todo_id', '')
        name = request.data.get('name', '')

        if todo_id:
            # 실습 2
            task = Task.objects.create(user_id=user_id, id=todo_id, name=name)
        else:
            task = Task.objects.create(user_id=user_id, name=name)

        return Response(data=dict(id=task.id))


class TaskToggle(APIView):
    def post(self, request):
        todo_id = request.data.get('todo_id', '')
        task = Task.objects.get(id=todo_id)

        if task:
            task.done = False if task.done is True else True
            task.save()

        return Response()

class TaskDelete(APIView):
    def post(self, request):
        todo_id = request.data.get('todo_id', '')
        task = Task.objects.get(id=todo_id)

        if task:
            task.delete()

        return Response()


# Create your views here.
class Todo(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        name = request.data.get('name', "")
        end_date = request.data.get('end_date', None)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        Task.objects.create(user_id=user_id, name=name, end_date=end_date)

        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(dict(name=task.name, start_date=task.start_date, end_date=task.end_date, state=task.state))
        context = dict(task_list=task_list)
        return render(request, 'todo/todo.html', context=context)

    def get(self, request):
        tasks = Task.objects.all()
        task_list = []
        for task in tasks:
            task_list.append(dict(name=task.name, start_date=task.start_date, end_date=task.end_date, state=task.state))
        context=dict(task_list=task_list)
        return render(request, 'todo/todo.html', context=context)