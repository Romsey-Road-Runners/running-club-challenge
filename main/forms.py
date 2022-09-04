from django.forms import ModelForm, FileField
from main.models import Activity


class SubmitResultForm(ModelForm):
    class Meta:
        model = Activity
        fields = ["race", "start_time", "elapsed_time", "evidence_file"]

    def __init__(self, *args, **kwargs):
        super(SubmitResultForm, self).__init__(*args, **kwargs)
        self.fields["evidence_file"] = FileField(required=True)
