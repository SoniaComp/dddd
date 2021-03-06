# Generated by Django 3.1.3 on 2020-11-27 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201126_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventComp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='기업명')),
                ('comp_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='사업자등록번호')),
                ('email', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': '이벤트:사전예약등록기업',
                'verbose_name_plural': '이벤트:사전예약등록기업',
                'db_table': 'event_comps',
            },
        ),
        migrations.AlterModelOptions(
            name='aianswer',
            options={'verbose_name': 'AI검색_만족도', 'verbose_name_plural': 'AI검색_만족도'},
        ),
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'AI_응답', 'verbose_name_plural': 'AI_응답'},
        ),
        migrations.RemoveField(
            model_name='question',
            name='satisfaction',
        ),
        migrations.AlterField(
            model_name='aianswer',
            name='answer',
            field=models.TextField(default='', verbose_name='AI검색_결과'),
        ),
        migrations.AlterField(
            model_name='event',
            name='answer',
            field=models.TextField(blank=True, default='', verbose_name='변호사_응답'),
        ),
    ]
