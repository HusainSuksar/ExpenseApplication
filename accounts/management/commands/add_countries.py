from django.core.management.base import BaseCommand
# Lib For First Solution
# import pycountry
# from accounts.models import Country
# import flag
# from googletrans import Translator
# For Call Commands In code
from django.core.management import call_command


# command to get all countries and added to database
class Command(BaseCommand):
    help = 'Add Countries to DataBase'

    def handle(self, *args, **kwargs):
        ################################################################################################################
        # get country name and code from pycountry and translate name to ar by googletrans and get emoji from flag lib
        ################################################################################################################
        # translator = Translator()
        # l = []
        # for c in list(pycountry.countries):
        #     l.append(c.name)
        # s = ' | '.join([str(elem) for elem in l])
        # translations = translator.translate(s, dest='ar')
        # ar = translations.text.split('|')
        # for a, c in zip(ar, list(pycountry.countries)):
        #     co = Country.objects.create(name_en=c.name, name_ar=a,
        #                                 logo=flag.flag(c.alpha_2))
        #     # print(co)
        ################################################################################################################
        # Load data from json file extracted by (python manage.py dumpdata accounts.Country --indent=1 > ./country.json)
        ################################################################################################################
        call_command('loaddata', 'accounts/management/commands/country.json', app='accounts')
        self.stdout.write("Countries Added")
        # you can run command more than one time because country.json has PK and overwrite all rows
        # self.stdout.write("you should run this commend one time")
