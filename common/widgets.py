from django.forms.widgets import Widget


class JSONEditorWidget(Widget):
    template_name = "catalog/widgets/jsoneditor.html"

    def __init__(self, attrs=None, editor_attrs=None):
        self.editor_attrs = {"style": ("min-height: 600px; width: 70%;")} | (
            editor_attrs or {}
        )

        super().__init__(attrs)

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)

        id_ = ctx["widget"]["attrs"]["id"]
        ctx["widget"]["editor_attrs"] = {"id": id_ + "_editor"} | self.editor_attrs

        return ctx

    class Media:
        css = {
            "screen": ["catalog/css/vendor/jse-theme-dark.css"],
        }
