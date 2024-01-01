from django import forms


class InputCustom(forms.widgets.Input):
    template_name = 'forms/widgets/textinputlogin.html'

    def get_context(self, name, value, attrs):
        print('text input')
        print(attrs)
        context = super(InputCustom, self).get_context(name, value, attrs)
        print('context:')
        print(context)
        return context


