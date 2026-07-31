from django.contrib import admin
from .models import Match, MatchGoalScorer


class MatchGoalScorerInline(admin.TabularInline):
    model = MatchGoalScorer
    extra = 1
    fields = (
        'team',
        'player_name',
        'is_extra_time',
        'is_penalty',
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'home_team', 'away_team', 'match_date', 'kickoff_time', 'competition',
        'status', 'home_score', 'away_score', 'result_label',
    )
    list_filter = ('status', 'competition')
    search_fields = ('home_team', 'away_team')
    list_editable = ('status', 'home_score', 'away_score')
    date_hierarchy = 'match_date'
    inlines = [MatchGoalScorerInline]
    fieldsets = (
        ('Fixture Details', {
            'fields': ('home_team', 'away_team', 'competition', 'match_date', 'kickoff_time', 'stadium')
        }),
        ('Status', {
            'fields': ('status',),
            'description': 'Set to Completed once the match has been played, then fill in the score below.'
        }),
        ('Normal Time Score', {
            'fields': ('home_score', 'away_score'),
        }),
        ('Extra Time (optional)', {
            'fields': ('home_score_et', 'away_score_et'),
            'description': 'Only fill these in if the match went to extra time.',
            'classes': ('collapse',),
        }),
        ('Penalty Shootout (optional)', {
            'fields': ('home_penalties', 'away_penalties'),
            'description': 'Only fill these in if the match was decided on penalties.',
            'classes': ('collapse',),
        }),
        ('Internal Notes', {
            'fields': ('match_report',),
            'description': 'For internal reference only - not displayed on the public site.',
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Result')
    def result_label(self, obj):
        return obj.result_label or '—'