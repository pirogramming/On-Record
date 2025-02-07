from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaries', '0009_merge_0007_diary_friend_alter_diary_date_0008_plant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='plant_adv',
            field=models.CharField(default='한결같이 우리집 베란다에 있는 모습', max_length=50),
        ),
    ]
