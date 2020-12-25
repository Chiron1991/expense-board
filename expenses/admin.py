from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from expenses.models import CostCenter, Tag, VariableCost
from expenses.utils import related_object_link

# brand the admin from "Django" to "Expense Board"
admin.site.site_title = _('Expense Board administration')
admin.site.site_header = admin.site.site_title
admin.site.index_title = admin.site.site_title


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('title',)


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(VariableCost)
class VariableCostAdmin(admin.ModelAdmin):
    list_display = ('date', 'cost_center_name', 'cost', 'tag_list')
    ordering = ('-date', '-id')
    autocomplete_fields = ('cost_center',)

    @related_object_link
    def cost_center_name(self, obj):
        return obj.cost_center.name

    cost_center_name.short_description = _('Cost Center')

    def tag_list(self, obj):
        return sorted(tag.title for tag in obj.tags.all())

    tag_list.short_description = _('Tags')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('cost_center').prefetch_related('tags')
        return qs
