# Generated by Django 4.1.4 on 2022-12-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dating_Site_App', '0007_alter_profile_profilephoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profilephoto',
            field=models.ImageField(blank=True, default='None_profilePic.jpg', upload_to='images/'),
        ),
    ]