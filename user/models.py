from django.db import models
from django.utils import timezone

# 帐号
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('账号', max_length = 32, unique=True)
    password = models.CharField('密码', max_length = 300, null=False)
    register_time = models.DateTimeField('注册时间', default=timezone.now)
    nicename = models.CharField('昵称', max_length = 32, default="梦魇神者")
    article_number = models.PositiveIntegerField('文章数', default=0)
    class Meta:
        db_table = "user"
    
    def __str__(self):
        return self.nicename


# 文章
class Article(models.Model):
    title = models.CharField('标题', max_length=30, null=False)
    content = models.TextField('内容')
    pub_data = models.DateTimeField('发布时间', default=timezone.now)
    looks = models.PositiveIntegerField('浏览数', default=0)
    review_number = models.PositiveIntegerField('评论数量',default=0)
    author = models.CharField('文章作者', max_length=30, default="死侍")
    pub_author = models.ForeignKey("User", verbose_name = "作者", on_delete=models.CASCADE, related_name="articles")
    
    class Meta:
        db_table = 'article'
        ordering = ("-pub_data",'-looks',)
    
    def __str__(self):
        return self.title
# 评论
class Review(models.Model):
    comment_uesr = models.CharField('评论者', max_length=20, default="莫得感情的杀手")
    comment = models.CharField('评论内容', max_length=100, blank=True, null=True)
    review_data = models.DateTimeField('评论时间', default=timezone.now)
    article = models.ForeignKey("Article", verbose_name = "被评论的文章" ,on_delete=models.CASCADE, related_name="review")

    class Meta:
        db_table = "review"
        ordering = ("-review_data",)
    
    def __str__(self):
        return self.comment
    