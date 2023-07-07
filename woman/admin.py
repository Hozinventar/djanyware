from django.contrib import admin

# Register your models here.
from .models import *
from django.utils.safestring import mark_safe


class WomanAdmin(admin.ModelAdmin):
    list_display = ('id', "title", "content", "get_html_photo", "time_create", "is_published", "cat", "user")
    list_display_links = ("title",)  # если не указывать, то автоматом будет только pk(id)
    # если указать,то только эти поля будут иметь ссылку на редактирование
    search_fields = ("title", "content")  # по каким полям осуществлять поиск.
    list_editable = ("is_published", "cat")  # эти поля можно поменять в режиме отображения список
    list_filter = ("is_published", "time_create")  # по этим полям можно фильтроваь в режиме отображения список. панель фильтра справа
    prepopulated_fields = {"slug": ("title",)}  # автозаполнение на основе поля name когда редактируем
    fields = ("title", "slug", "content", "photo", "get_html_photo", "time_create", "time_update", "cat", "user")  # переопределяем поля, что можно изменить
    readonly_fields = ("time_create", "time_update", "get_html_photo")  # поля что нельзя редактировать. только для чтения.
    # Должны быть добавлены в атрибут fields

    def get_html_photo(self, object):
        """ возвражает миниатюры фоток. называние функци рандомное
        mark_safe - функция которая не экранирует теги, html
        """
        if object.photo:    # Если есть фото то отобразить, если не прописать условие ,
            # то так где нет фотки страница не сможет быть показана
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    get_html_photo.short_description = "миниатюра"  # для того чтобы переопределить название в таблице


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', "name")
    list_display_links = ("pk", "name",)  # если не указывать, то автоматом будет только pk(id)
    search_fields = ("name",)  # по каким полям осуществлять поиск.
    prepopulated_fields = {"slug": ("name",)}  # автозаполнение на основе поля name


@admin.register(Human)
class HumanAdmin(admin.ModelAdmin):
    list_display = ('pk', "name", "age", "work")


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('pk', "name", "street", "funcstr")


admin.site.register(Woman, WomanAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = "Панель о женьщинах"
admin.site.site_header = "о женьщинах2"

# admin.site.register(Human, HumanAdmin)
# admin.site.register(Work, WorkAdmin)

