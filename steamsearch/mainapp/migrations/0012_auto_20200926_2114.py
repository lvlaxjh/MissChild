# Generated by Django 3.1 on 2020-09-26 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_thanks'),
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='唯一id')),
                ('name', models.TextField(default='none', verbose_name='走失者-姓名')),
                ('sex', models.TextField(default='0', verbose_name='走失者-性别')),
                ('birthday', models.TextField(default='none$none$none', verbose_name='走失者-出生日期')),
                ('height', models.TextField(default='none', verbose_name='走失者-身高')),
                ('weight', models.TextField(default='none', verbose_name='走失者-体重')),
                ('timeL', models.TextField(default='none$none$none$none$none', verbose_name='走失者-出生日期')),
                ('site', models.TextField(default='none', verbose_name='走失者-走失地区')),
                ('text', models.TextField(default='none', verbose_name='走失者-描述')),
                ('kinName', models.TextField(default='none', verbose_name='亲属-称呼')),
                ('kinLink', models.TextField(default='none', verbose_name='亲属-联系方式')),
            ],
        ),
        migrations.CreateModel(
            name='PeopleImg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='唯一id')),
                ('imgFile', models.ImageField(blank=True, null=True, upload_to='checkImg', verbose_name='失联者图片')),
                ('onePeople', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainapp.people', verbose_name='该图片所属信息')),
            ],
        ),
        migrations.RemoveField(
            model_name='examineimg',
            name='examine',
        ),
        migrations.DeleteModel(
            name='Thanks',
        ),
        migrations.DeleteModel(
            name='Total',
        ),
        migrations.RemoveField(
            model_name='statistics',
            name='allrecord',
        ),
        migrations.DeleteModel(
            name='ExamineImg',
        ),
        migrations.DeleteModel(
            name='ToExamine',
        ),
    ]