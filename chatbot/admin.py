from django.contrib import admin
from .models import UserProfile, ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):  # Or admin.StackedInline for a different layout
    model = ChatMessage
    extra = 0  # Don't show extra empty forms
    readonly_fields = ('is_user', 'message', 'timestamp') # Make messages read-only in session view
    can_delete = False # Prevent deleting messages from session view
    ordering = ('timestamp',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'user__name', 'user__email')
    inlines = [ChatMessageInline] # Show messages within the session admin page

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'is_user', 'timestamp', 'message_preview')
    list_filter = ('session__user', 'is_user', 'timestamp', 'session')
    search_fields = ('message', 'session__title')
    readonly_fields = ('session', 'is_user', 'message', 'timestamp') # Make messages read-only

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message Preview'

# Optional: Unregister the simple registration if you only want the custom ones
# admin.site.unregister(UserProfile) # If it was registered simply before
