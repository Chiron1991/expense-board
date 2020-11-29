from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone
from djmoney.money import Money

from expenses.models import Tag, CostCenter, VariableCost


class Command(BaseCommand):
    def handle(self, *args, **options):
        t = Tag.objects.create(title='Groceries')
        Tag.objects.bulk_create([
            Tag(title='Eat Out'),
            Tag(title='Clothing'),
            Tag(title='Cosmetics'),
            Tag(title='Leisure'),
            Tag(title='Medical'),
        ])
        cc = CostCenter.objects.create(name='Costco')
        CostCenter.objects.bulk_create([
            CostCenter(name='Primark'),
            CostCenter(name='Pharmacy'),
            CostCenter(name='Giovanni\'s Pizza Palace'),
        ])
        vc = VariableCost.objects.create(
            date=timezone.now().date(),
            cost=Money('32.78', settings.CURRENCIES[0]),
            cost_center=cc,
        )
        vc.tags.set([t])
