# Generated by Django 2.0.5 on 2019-02-24 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Jedi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('right_answer', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='jedi',
            name='planet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jedi_Order.Planet'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Jedi_Order.Planet'),
        ),
        migrations.AddField(
            model_name='challenge',
            name='question',
            field=models.ManyToManyField(to='Jedi_Order.Question'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='jedi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Jedi_Order.Jedi'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='planet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jedi_Order.Planet'),
        ),
        migrations.AddField(
            model_name='answer',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jedi_Order.Candidate'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jedi_Order.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('candidate', 'question')},
        ),
    ]