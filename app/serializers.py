
from rest_framework import serializers,exceptions

from app.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    #出版社的序列化器
    class Meta:
        model=Press
        fields=("press_name","adress","pic")
class BookModelSerializer(serializers.ModelSerializer):
    # TODO 自定义连表查询  查询图书时将图书对应的出版的信息完整的查询出来
    # 可以在序列化器中嵌套另一个序列化器来完成多表查询
    # 需要与图书表的中外键名保持一致  在连表查询较多字段时推荐使用
    pushlish = PressModelSerializer()

    class Meta:
        model=Book
        #指定要序列化的字段

        fields = ("book_name","price","pic","pushlish","author_list")
        # #查询全部字段
        # fields="__all__"
        #
        # #可以不指定查询有关的字段
        # exclude=("is_delete","create_time","status")
        #
        # #查询深度为一的所有字段
        # depth=1

class BookDeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=("book_name","price","pushlish","author")

        #添加DRF所提供的校验规则
        extra_kwargs={
            "book_name":{
                "required":True,  #设置为必填项
                "min_length":3,
                "error_messages":{
                    "required":"图书名字是必填的",
                    "min_length":"图书名长度不够，太短了~"
                }
            },
            "price":{
                "max_digits":5,
                "decimal_places":2,
            }
        }
        #局部校验钩子：可以对反序列化中某个字段进行校验
        def vaildate_book_name(self,value):
            print(1)
            #自定义用户名校验规则
            if "1" in value:
                raise exceptions.ValidationError("图书名字包含有敏感字")
            return value


        #全局校验钩子  可以通过attrs获取到前台发送的所有的参数
            # 全局校验钩子  可以通过attrs获取到前台发送的所有的参数
        def validate(self, attrs):
            print(1)
            # 可以对前端发送的所有数据进行自定义校验
            # print(self, "当前实例所使用的反序列化器")
            pwd = attrs.get("password")
            re_pwd = attrs.pop("re_pwd")
            # 自定义规则  两次密码如果不一致  则无法保存
            if pwd != re_pwd:
                raise exceptions.ValidationError("两次密码不一致")
            return attrs

# 序列化和反序列化的整合
class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model=Book
        #fields里面填序列化和反序列化的并集
        fields=("book_name","price","pushlish","author","pic")

        #添加DRF所提供的校验规则
        #通过此参数指定那些字段是参与序列化的，那些是参与反序列化的
        extra_kwargs={
            "book_name":{
                "required":True,
                "min_length":3,
                "error_messages":{
                    "required":"图书名字是必填的",
                    "min_length":"长度不够，太短了~"
                }
            },
            #指定此字段只参与反序列化
            "pushlish":{
                "write_only":True
            },
            "author":{
                "write_only":True
            },
            #此字段只参与序列化
            "pic":{
                "read_only":True
            }
        }


        def validate_book_name(self,value):
            #自定义用户名校验规则
            if "1" in value:
                raise exceptions.ValidationError("图书名含有敏感字")
            return value

        def validate(self,attrs):
            price=attrs.get("price",0)
            if price > 90:
                raise exceptions.ValidationError("超过制定价格的最高价格")
            return attrs

