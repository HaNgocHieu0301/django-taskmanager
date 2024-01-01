from django import forms


class InputCustom(forms.widgets.Input):
    template_name = 'forms/widgets/textinputtaskform.html'

    def get_context(self, name, value, attrs):
        print('text input')
        print(attrs)
        context = super(InputCustom, self).get_context(name, value, attrs)
        print('context:')
        print(context)
        return context


class TextareaCustom(forms.widgets.Textarea):
    template_name = 'forms/widgets/texareatinputtaskform.html'

    def get_context(self, name, value, attrs):
        print('text input')
        print(attrs)
        context = super(TextareaCustom, self).get_context(name, value, attrs)
        print('context:')
        print(context)
        return context
