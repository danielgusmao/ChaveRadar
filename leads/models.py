from django.db import models


class Profile(models.Model):
    SOURCE_CHOICES = [
        ('official_api', 'API oficial'),
        ('manual', 'Importacao manual'),
        ('provider', 'Provedor licenciado'),
    ]

    handle = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual')
    active = models.BooleanField(default=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.handle


class Publication(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    platform_media_id = models.CharField(max_length=255, blank=True)
    permalink = models.URLField(max_length=1000)
    media_type = models.CharField(max_length=30, blank=True)
    caption_original = models.TextField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    property_type = models.CharField(max_length=150, blank=True)
    property_region = models.CharField(max_length=255, blank=True)
    transaction_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'permalink'], name='uq_profile_publication')
        ]

    def __str__(self):
        parts = [self.property_type, self.property_region]
        return ' - '.join(item for item in parts if item) or self.permalink


class Comment(models.Model):
    SOURCE_CHOICES = [
        ('official_api', 'API oficial'),
        ('manual', 'Importacao manual'),
        ('provider', 'Provedor licenciado'),
    ]

    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='comments')
    platform_comment_id = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=150)
    display_name = models.CharField(max_length=255, blank=True)
    text_original = models.TextField()
    displayed_date_original = models.CharField(max_length=100, blank=True)
    commented_at = models.DateTimeField(null=True, blank=True)
    captured_at = models.DateTimeField(auto_now_add=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='manual')
    raw_payload = models.JSONField(default=dict, blank=True)
    fingerprint = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.username}: {self.text_original[:60]}'


class Classification(models.Model):
    LEVEL_CHOICES = [
        ('high', 'Alto'),
        ('medium', 'Medio'),
        ('low', 'Baixo'),
        ('not_lead', 'Nao Lead'),
    ]
    REVIEW_CHOICES = [
        ('auto', 'Auto-aprovado'),
        ('pending', 'Pendente'),
        ('approved', 'Aprovado manualmente'),
        ('rejected', 'Rejeitado manualmente'),
    ]

    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='classification')
    is_lead = models.BooleanField(default=False)
    intents = models.JSONField(default=list)
    qualification = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='not_lead')
    evidence = models.JSONField(default=list)
    confidence = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    exclusion_reason = models.CharField(max_length=255, blank=True)
    review_status = models.CharField(max_length=20, choices=REVIEW_CHOICES, default='pending')
    classifier_version = models.CharField(max_length=50, default='0.2.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.comment.username} - {self.get_qualification_display()}'


class CollectionRun(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collection_runs')
    source_type = models.CharField(max_length=20)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    publications_found = models.PositiveIntegerField(default=0)
    comments_found = models.PositiveIntegerField(default=0)
    comments_new = models.PositiveIntegerField(default=0)
    comments_duplicate = models.PositiveIntegerField(default=0)
    comments_failed = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=30, default='running')
    error_message = models.TextField(blank=True)


class MonitoringProfile(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Aguardando conexao'),
        ('ok', 'Monitorado'),
        ('error', 'Erro'),
    ]

    handle = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    alerts_enabled = models.BooleanField(default=True)
    keywords = models.TextField(
        blank=True,
        help_text='Palavras adicionais deste perfil, separadas por virgula. Em branco usa a lista global.',
    )
    notes = models.TextField(blank=True)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    last_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    last_error = models.TextField(blank=True)
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instagram_monitoring_profiles',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['handle']
        verbose_name = 'Perfil monitorado do Instagram'
        verbose_name_plural = 'Perfis monitorados do Instagram'

    def save(self, *args, **kwargs):
        value = (self.handle or '').strip().lower()
        if value and not value.startswith('@'):
            value = '@' + value
        self.handle = value
        super().save(*args, **kwargs)

    def __str__(self):
        return self.handle
