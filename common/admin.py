from django.contrib.admin import ModelAdmin, StackedInline
from django.db.models import JSONField

from common.widgets import JSONEditorWidget


class BaseAdmin(ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }


class BaseStackedInline(StackedInline):
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }
