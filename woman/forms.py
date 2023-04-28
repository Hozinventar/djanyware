from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class PostFormOld(forms.Form):
    # initial  по умолчнию чекбокс будет тру
    # empty_label  отображать значение которое еще не выбрано
    # widget  переопределяем класс формы для отображения и указывает атрибуты . по ним работает бутстрап к примеру
    # без связи с БД
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': "form-input"}))  # widget для лейбла input
    slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, "rows": 10}), label="Контент")                  # widget для лейбла Textarea
    is_published = forms.BooleanField(required=False, initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="категория не выбрана")


class PostForm(forms.ModelForm):
    """
    класс нужен чтобы не дублировать форму для отобржения
    наследуется от модели БД
    Вместо янового указания Label тянется атрибут verbose_name из модели

    """
    def __init__(self, *args, **kwargs):
        """ таким способом можно переопределить к примеру значение если поле не выбрано"""
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "категория не выбрана"

    class Meta:
        model = Woman
        fields = '__all__'  #  отобразить все поля кроме тех что заполяются автоматически. На практике так не рекомендуют
        # порядок отображения полей завсит от последоватности атрибутов в модели
        # fields = ["title", "slug", "content", "is_published", "cat"]  # рекомендуют явно указывать. переопределяется порядок полей.
        widgets = {
            "title": forms.TextInput(attrs={'class': "form-input"}),
            'content': forms.Textarea(attrs={'cols': 60, "rows": 10})
        }  # позволяет присвоить классы css в коде тут а не в шаблоне

    def clean_title(self):
        """ кастомный валидатор по полю title.
         Записываем условия для атриута. если оно не выполняется , то ошибка
         Если другое поле, то изменить имя функции
        clean_blablabla
        """
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError("Длинна превышает 200 символов")

        return title


class RegisterUserForm(UserCreationForm):
    """ переопределяем стандартный класс UserCreationForm"""
    username = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': "form-label"}))  # widget для лейбла input
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-input"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': "form-label"}))  # widget для лейбла input
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': "form-label"}))  # widget для лейбла input

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]  # атрибуты формы по умочанию. можно посмотреть в коде html при рендере страницы формы
        # в джанго widgets не работает для формы UserCreationForm. Поэтому они определены в начале
        # widgets = {
        #     "username": forms.TextInput(attrs={'class': "form-input"}),
        #     'password1': forms.PasswordInput(attrs={'class': "form-input"}),
        #     'password2': forms.PasswordInput(attrs={'class': "form-input"})
        # }


class LoginUserForm(AuthenticationForm):

    """ имена трибутов необходимо указывать такие же как в базовой форме иначе будет расширение формы на такой атрибут"""
    username = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': "form-input"}))  # widget для лейбла input
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': "form-input"}))  # widget для лейбла input

    """ класс мета не обяхательно указывать """


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': "form-input"}))
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, "rows": 10}), label="Контент")
    captch = CaptchaField()
