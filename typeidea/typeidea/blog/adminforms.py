from django import forms


class PostAdminForm(forms.ModelForm):
    """Form definition for PostAdmin."""

    desc = forms.CharField(widget= forms.Textarea, label = '摘要', required=False)
    # class Meta:
    #     """Meta definition for PostAdminform."""
    #     model = PostAdmin
    #     fields = ('',)
