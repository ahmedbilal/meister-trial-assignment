#!/bin/sh
source ../env/bin/activate
./manage.py shell -c "from stats.models import Country, City; russia = Country.objects.create(name='Russia'); City.objects.bulk_create([City(name='Novosibirsk', country=russia), City(name='Nizhny Novgorod', country=russia), City(name='Samara', country=russia), City(name='Omsk', country=russia), City(name='Kazan', country=russia), City(name='Ufa', country=russia), City(name='Chelyabinsk', country=russia)]);"
./manage.py shell -c "from django.contrib.auth import get_user_model; from stats.models import City; get_user_model().objects.create_user(username='briggs@meistery.net', email='briggs@meistery.net', password='password', gender='male', first_name='Briggs', last_name='Victoriads', age=6, city=City.objects.get(id=1));"
