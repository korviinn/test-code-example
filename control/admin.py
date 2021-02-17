from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team, Match, UserBet


class TelegramUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        base_fields = self.get_fields(request, obj)
        return ((None, {'fields': base_fields}),)


class TeamAdmin(admin.ModelAdmin):
    pass


class MatchAdmin(admin.ModelAdmin):
    pass


class UserBetAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, TelegramUserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(UserBet, UserBetAdmin)
