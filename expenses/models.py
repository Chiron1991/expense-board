from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField


class Tag(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class CostCenter(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Cost Center')
        verbose_name_plural = _('Cost Centers')

    def __str__(self):
        return self.name


class VariableCost(models.Model):
    date = models.DateField()
    cost = MoneyField(max_digits=19, decimal_places=2)
    notes = models.TextField(blank=True)

    cost_center = models.ForeignKey(CostCenter, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = _('Variable Cost')
        verbose_name_plural = _('Variable Costs')

    def __str__(self):
        return f'{self.cost_center.name}: {self.cost.amount} {self.cost.currency}'
