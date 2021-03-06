# Generated by Django 2.0.5 on 2019-03-16 01:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('pub_data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('looks', models.PositiveIntegerField(default=0, verbose_name='浏览数')),
                ('author', models.CharField(default='死侍', max_length=30, verbose_name='文章作者')),
            ],
            options={
                'db_table': 'article',
                'ordering': ('-pub_data', '-looks'),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_uesr', models.CharField(default='莫得感情的杀手', max_length=20, verbose_name='评论者')),
                ('comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='评论内容')),
                ('review_data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='评论时间')),
                ('review_number', models.PositiveIntegerField(default=0, verbose_name='评论数量')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='user.Article', verbose_name='被评论的文章')),
            ],
            options={
                'db_table': 'review',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='账号')),
                ('password', models.CharField(max_length=300, verbose_name='密码')),
                ('register_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='注册时间')),
                ('nicename', models.CharField(default='梦魇神者', max_length=32, verbose_name='昵称')),
                ('article_number', models.PositiveIntegerField(default=0, verbose_name='文章数')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='pub_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='user.User', verbose_name='作者'),
        ),
    ]
