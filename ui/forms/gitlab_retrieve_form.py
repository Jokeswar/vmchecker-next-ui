from django import forms


class GitlabRetriveForm(forms.Form):
    gitlab_project_id = forms.IntegerField(label="Project Id")
    gitlab_private_token = forms.CharField(label="Private Token")
