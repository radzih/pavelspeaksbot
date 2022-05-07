from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Group


from .models import User, Word, Word_Category

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','telegram_id','level','learned_words')
    list_filter = ('level',)
    fields = ('telegram_id', 'level')

    def learned_words(self, obj):
        return len(obj.words.all())

class WordAdmin(admin.ModelAdmin):
    list_display = ('id','word', 'translate', 'category', 'level')
    list_filter = ('level','category')
    search_fields = ('word__startswith',)

class Word_CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category', 'level')
    list_filter = ('level',)
    search_fields = ('category__startswith',)


admin.site.register(User, UserAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Word_Category, Word_CategoryAdmin)
admin.site.unregister(DjangoUser)
admin.site.unregister(Group)
# Register your models here.
