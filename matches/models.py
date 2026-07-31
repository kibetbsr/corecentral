from django.db import models
 
# The one place that defines "us" — used to determine win/loss and to default the home team
CLUB_NAME = "Kipsolu Central FC"
 
# Accepted variations of the club name (all lowercase, no extra spaces) — add more here if needed
CLUB_ALIASES = {"kipsolu central fc", "kipsolu cfc", "kcfc"}
 
 
class Match(models.Model):
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('COMPLETED', 'Completed'),
        ('POSTPONED', 'Postponed'),
    ]
 
    COMPETITION_CHOICES = [
        ('FRIENDLY', 'Friendly'),
        ('TOURNAMENT', 'Tournament'),
    ]
 
    home_team = models.CharField(max_length=100, default=CLUB_NAME)
    away_team = models.CharField(max_length=100)
 
    competition = models.CharField(
        max_length=20, choices=COMPETITION_CHOICES, default='FRIENDLY'
    )
    match_date = models.DateField()
    kickoff_time = models.TimeField()
    stadium = models.CharField(max_length=150, default='Kipsolu Green Grounds')
 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UPCOMING')
 
    # Normal time score (90 minutes)
    home_score = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Home team score (normal time)'
    )
    away_score = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Away team score (normal time)'
    )
 
    # Extra time score - optional, only used if the match went to extra time
    home_score_et = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Home team score (after extra time)',
        help_text='Leave blank if the match did not go to extra time.'
    )
    away_score_et = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Away team score (after extra time)',
        help_text='Leave blank if the match did not go to extra time.'
    )
 
    # Penalty shootout score - optional, only used if the match was decided on penalties
    home_penalties = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Home team penalties',
        help_text='Leave blank if the match was not decided on penalties.'
    )
    away_penalties = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Away team penalties',
        help_text='Leave blank if the match was not decided on penalties.'
    )
 
    match_report = models.TextField(
        blank=True,
        help_text='Optional internal notes about the match. Not shown on the public site.'
    )
 
    class Meta:
        ordering = ['match_date', 'kickoff_time']
 
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.match_date})"
 
    @property
    def kipsolu_side(self):
        """Returns 'HOME', 'AWAY', or None if Kipsolu isn't in this match at all.
        Matching is case-insensitive and accepts known name variations (see CLUB_ALIASES)."""
        if self.home_team.strip().lower() in CLUB_ALIASES:
            return 'HOME'
        if self.away_team.strip().lower() in CLUB_ALIASES:
            return 'AWAY'
        return None
 
    @property
    def went_to_extra_time(self):
        return self.home_score_et is not None and self.away_score_et is not None
 
    @property
    def went_to_penalties(self):
        return self.home_penalties is not None and self.away_penalties is not None
 
    @property
    def result_label(self):
        """
        WIN / DRAW / LOSS from Kipsolu's perspective, using the final applicable score,
        priority order:
        1. Penalty shootout (if decided on penalties)
        2. Extra time score (if went to extra time but not penalties)
        3. Normal time score
        """
        if self.status != 'COMPLETED' or self.kipsolu_side is None:
            return None
 
        us_is_home = self.kipsolu_side == 'HOME'
 
        if self.went_to_penalties:
            us, them = (self.home_penalties, self.away_penalties) if us_is_home \
                else (self.away_penalties, self.home_penalties)
        elif self.went_to_extra_time:
            us, them = (self.home_score_et, self.away_score_et) if us_is_home \
                else (self.away_score_et, self.home_score_et)
        else:
            if self.home_score is None or self.away_score is None:
                return None
            us, them = (self.home_score, self.away_score) if us_is_home \
                else (self.away_score, self.home_score)
 
        if us > them:
            return 'WIN'
        if us < them:
            return 'LOSS'
        return 'DRAW'
 
    @property
    def score_display(self):
        """
        Builds the final score line for the public site, always shown as
        "home - away", e.g.: "2 - 1", "2 - 1 (AET)", "1 - 1 (Home won 4-3 on penalties)".
        """
        if self.home_score is None or self.away_score is None:
            return None
 
        if self.went_to_penalties:
            base = f"{self.home_score_et} - {self.away_score_et}" if self.went_to_extra_time \
                else f"{self.home_score} - {self.away_score}"
            outcome = 'Home won' if self.home_penalties > self.away_penalties else 'Away won'
            return f"{base} ({outcome} {self.home_penalties}-{self.away_penalties} on penalties)"
 
        if self.went_to_extra_time:
            return f"{self.home_score_et} - {self.away_score_et} (AET)"
 
        return f"{self.home_score} - {self.away_score}"
 
 
class MatchGoalScorer(models.Model):
    TEAM_CHOICES = [
        ('HOME', 'Home team'),
        ('AWAY', 'Away team'),
    ]
 
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='scorers'
    )
 
    team = models.CharField(
        max_length=4, choices=TEAM_CHOICES, default='HOME',
        help_text='Which side this goal was scored for.'
    )
 
    player_name = models.CharField(max_length=100)
 
    is_extra_time = models.BooleanField(
        default=False,
        help_text="Check if this goal was scored during extra time."
    )
 
    is_penalty = models.BooleanField(
        default=False,
        help_text="Check if this goal was scored during a penalty shootout."
    )
 
    class Meta:
        ordering = ['id']
        verbose_name = 'Goal Scorer'
        verbose_name_plural = 'Goal Scorers'
 
    def __str__(self):
        suffix = ""
        if self.is_penalty:
            suffix = " (P)"
        elif self.is_extra_time:
            suffix = " (+ET)"
 
        return f"{self.player_name} ({self.get_team_display()}){suffix} ({self.match})"