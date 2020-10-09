from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Task, SubTask, Taken


class TaskView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            tasks = Task.objects.all()
            tasks_list = get_tasks(tasks, request)
            return Response({
                'success': True,
                'message': f'Fetched {len(tasks_list)} posts',
                'post_list': tasks_list
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user = request.user
            subtasks = data.pop('subtasks')
            task = Task(user=user, task=data['task'])
            taken = Taken(user=user, task=task)
            task.save()
            taken.save()
            for subtask in subtasks:
                sub = SubTask(task=task, title=subtask['title'])
                sub.save()
            return Response({
                'success': True,
                'message': 'Added new task'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': True,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


class UserTaskView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def get(self, request, *args, **kwargs):
        try:
            tasks = Task.objects.filter(user=request.user)
            tasks_list = get_tasks(tasks, request)
            return Response({
                'success': True,
                'message': f'Fetched {len(tasks_list)} posts',
                'post_list': tasks_list
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


class SingleTaskView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):
        try:
            task = Task.objects.filter(id=kwargs['id'])
            task_list = get_tasks(task, request)
            return Response({
                'success': True,
                'message': f"Fetched task ID {kwargs['id']} successfully",
                'task': task_list
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


class TakeTaskView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def post(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(id=kwargs['id'])
            subtasks = SubTask.objects.filter(task=task)
            new_task = Task(user=request.user, task=task.task)
            new_task.save()
            for subtask in subtasks:
                sub = SubTask(task=new_task, title=subtask.title)
                sub.save()
            taken = Taken(task=new_task, user=request.user)
            taken.save()
            return Response({
                'id': new_task.pk,
                'success': True,
                'message': 'Added task'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


class DeleteTaskView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def delete(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(id=kwargs['id'])
            if task.user == request.user:
                task.delete()
                return Response({
                    'success': True,
                    'message': 'Deleted task'
                }, status=status.HTTP_200_OK)
            return Response({
                'success': False,
                'message': "Cannot delete someone others' task"
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateProgressView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, )

    def patch(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(id=request.data['id'])
            if task.user == request.user:
                subtasks = request.data.pop('subtasks')
                for subtask in subtasks:
                    sub = SubTask.objects.get(title__contains=subtask['title'])
                    sub.is_subtask = True
                    sub.save()
                return Response({
                    'success': True,
                    'message': 'Updated data'
                }, status=status.HTTP_200_OK)
            return Response({
                'success': False,
                'message': "Cannot update someone else's data"
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'success': False,
                'message': e.__str__()
            }, status=status.HTTP_400_BAD_REQUEST)


def get_tasks(tasks, request):
    tasks_list = []
    subtask_list = []
    objects = {}
    sub_objects = {}
    for task in tasks:
        completed = 0
        total = 0
        subtasks = SubTask.objects.filter(task=task.id)
        for subtask in subtasks:
            sub_objects['title'] = subtask.title
            if subtask.is_subtask:
                completed = completed + 1
            subtask_list.append(sub_objects)
            total = total + 1
            sub_objects = {}
        try:
            Taken.objects.get(task=task, user=request.user)
            is_taken = True
        except Taken.DoesNotExist:
            is_taken = False
        objects['id'] = task.id
        objects['first_name'] = task.user.first_name
        objects['last_name'] = task.user.last_name
        objects['task'] = task.task
        objects['is_taken'] = is_taken
        if is_taken:
            objects['progress'] = (completed / total) * 100
        objects['subtasks'] = subtask_list
        tasks_list.append(objects)
        objects = {}
        subtask_list = []
    return tasks_list


