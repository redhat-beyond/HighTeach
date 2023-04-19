from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_user_test_data(apps, schema_editor):
        from django.contrib.auth.models import User

        # Create a super user
        superuser = User()
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.username = 'admin'
        superuser.email = 'admin@gmail.com'
        superuser.set_password('admin1234')
        superuser.save()
        # Create normal users
        users_test_data = [
            ("Davidcoh", "David", "Cohen", "test$1234", "david@gmail.com"),
            ("RanyWhabi", "Rany", "Whabi", "test$8979", "rany@gmail.com"),
            ("IdanRosenberg", "Idan", "Rosenberg", "test$8979", "idan@gmail.com"),
            ("ShacharLevy", "Shachar", "Levy", "test$8979", "shachar@gmail.com"),
            ("YardenGazit", "Yarden", "Gazit", "test$8979", "yarden@gmail.com"),
            ("ShirazYom", "Shiraz", "Yom-Tov", "test$8979", "shiraz@gmail.com")
        ]

        with transaction.atomic():
            for USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL in users_test_data:
                user = User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)
                user.save()
                user.profile.bio = "Hi my name is " + FIRSTNAME + " " + LASTNAME
                user.profile.city = "Tel Aviv"
                user.profile.phone_number = "0541234567"
                user.save()

    operations = [
        migrations.RunPython(generate_user_test_data),
    ]
