# Valify-Solution-Task


<P>Here you can Find Valify- Solution task task with Postgres dataBase and and tested by unittesting</p>

# Setup & Launch:

1. git clone https://github.com/yousefshalby/Valify-Soultions-Task.git

2. makevirtualvenv ==> python3 -m venv venv

3. source venv/bin/activate

4. cd project/

5. pip install -r requirement.txt

6. to create our Postgres database you will find credentials in (.env) file in project folder which contains settings you will find db_name and db_user and password

7. python manage.py makemigrations

8. python manage.py migrate

9. If you want to check all tests ==> python manage.py test

10. python manage.py runserver
