from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework import generics
from rest_framework import viewsets

from app.models import Book
from utils.response import APIResponse
from .serializers import BookModelSerializer


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False)
        data_ser = BookModelSerializer(book_list, many=True).data

        return APIResponse(status.HTTP_200_OK,"SUCCESS",results=data_ser)


# GenericAPIView继承了APIView, 两者完全兼容
# 重点分析GenericAPIView 在APIView的基础上完成了哪些事情
class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    # 获取当前视图所操作的模型 与序列化器类
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    # 指定获取单条信息的主键的名称
    lookup_field = "id"

    # 通过继承ListModelMixin 提供self.list完成了查询所有
    # 通过继承RetrieveModelMixin 提供了self.retrieve 完成了查询单个
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    """
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # 获取book模型的所有的数据
        # book_list = Book.objects.filter(is_delete=False)
        book_list = self.get_queryset()
        # 获取要使用序列化器
        # data_ser = BookModelSerializer(book_obj).data
        data_ser = self.get_serializer(book_list, many=True)
        data = data_ser.data

        return APIResponse(results=data)

    def get(self, request, *args, **kwargs):
        # user_id = kwargs.get("id")
        # book_obj = Book.objects.get(pk=user_id, is_delete=False)
        book_obj = self.get_object()
        # data_ser = BookModelSerializer(book_obj).data
        data_ser = self.get_serializer(book_obj)
        data = data_ser.data

        return APIResponse(results=data)
    """

    # 新增图书  通过继承CreateModelMixin 来获得self.create方法  内部完成了新增
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return APIResponse(status.HTTP_200_OK,"SUCCESS",results=response.data)

    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(status.HTTP_200_OK,"SUCCESS",results=response.data)

    # 单局部改
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(status.HTTP_200_OK,"SUCCESS",results=response.data)

    # 通过继承DestroyModelMixin 获取self
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return APIResponse(status.HTTP_200_OK,"SUCCESS")


class BookListAPIVIew(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"


class BookGenericViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    # 如何确定post请求是需要登录
    def user_login(self, request, *args, **kwargs):
        # 可以在此方法中完成用户登录的逻辑
        return self.retrieve(request, *args, **kwargs)

    def get_user_count(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


"""
所有的操作都是以Http方法来进行匹配的
发送登录请求：post   登录请求不需要新增对象，而GenericAPIView与mixins中提供的post方法是为了将数据保存到数据库
但是登录请求不需要数据入库  GenericViewSet可以自定义方法处理
"""