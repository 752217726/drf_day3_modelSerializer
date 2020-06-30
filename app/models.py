from django.db import models

# Create your models here.

#抽象表 基表
class BaseModel(models.Model):
    is_delete=models.BooleanField(default=False)
    create_time=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)

    class Meta:
        #在元数据中，一旦声明数据后 不会在数据库中创建对应的表结构
        #其他模型继承这个模型后 可以继承表中的字段 abstract 抽象的
        abstract=True

class Book(BaseModel):
    book_name=models.CharField(max_length=128)
    price=models.DecimalField(max_digits=5,decimal_places=3)
    pic=models.ImageField(upload_to="img",default="img/1.png")
    pushlish=models.ForeignKey(to="Press",on_delete=models.CASCADE,db_constraint=False,related_name="books")
    author=models.ManyToManyField(to="Author",db_constraint=False,related_name="books")

    class Meta:
        db_table="bz_book"
        verbose_name="图书"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.book_name
    @property
    def pushlish_name(self):
        return self.pushlish.press_name

    @property
    def press_adress(self):
        return self.pushlish.adress

    @property
    def author_list(self):
        return self.author.values("author_name",'age',"detail__phone")


#出版社表
class Press(BaseModel):
    press_name=models.CharField(max_length=128)
    pic=models.ImageField(upload_to="img",default="img/1.png")
    adress=models.CharField(max_length=256)

    class Meta:
        db_table="bz_press"
        verbose_name="出版社"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.press_name

#作者表
class Author(BaseModel):
    author_name=models.CharField(max_length=128)
    age=models.IntegerField()

    class Meta:
        db_table="bz_author"
        verbose_name="作者"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.author_name

#作者详情表
class AuthorDetail(BaseModel):
    phone=models.CharField(max_length=11)
    author=models.OneToOneField(to="Author",on_delete=models.CASCADE,related_name="detail")

    class Meta:
        db_table="bz_author_detail"
        verbose_name="作者详情"
        verbose_name_plural=verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name