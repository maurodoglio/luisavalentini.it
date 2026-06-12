from django.db import models


class Mostra(models.Model):
    """Exhibition (Mostra) model - personal or collective exhibitions."""

    TYPES = (
        ('1', 'Personali'),
        ('2', 'Collettive'),
    )

    name = models.CharField(max_length=100, verbose_name='Nome')
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField(verbose_name='Descrizione')
    published = models.BooleanField(verbose_name='Pubblicato', default=False)
    type = models.CharField(max_length=1, choices=TYPES, verbose_name='Tipologia')
    beginning = models.DateField(verbose_name='Data di inizio')

    class Meta:
        verbose_name_plural = 'mostre'
        verbose_name = 'mostra'
        ordering = ['-beginning']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/mostra/{self.slug}'


class Opera(models.Model):
    """Artwork (Opera) model - sculptures, jewelry, and drawings."""

    OPERA_TYPE = (
        ('S', 'Sculture'),
        ('G', 'Gioielli'),
        ('D', 'Disegni'),
    )

    title = models.CharField(max_length=100, verbose_name='Titolo')
    slug = models.SlugField(max_length=100, unique=True)
    pubdate = models.DateTimeField(auto_now_add=True, verbose_name='Data di creazione')
    last_modified = models.DateTimeField(auto_now=True, verbose_name='Data ultima modifica')
    published = models.BooleanField(verbose_name='Pubblicato', default=True)
    content = models.TextField(verbose_name='Descrizione', blank=True)
    image = models.ImageField(upload_to='opere', verbose_name='Immagine')
    thumb = models.ImageField(upload_to='opere_thumb', verbose_name='Miniatura')
    creation_year = models.CharField(max_length=4, verbose_name='Anno')
    typology = models.CharField(max_length=1, choices=OPERA_TYPE, default='S')

    class Meta:
        verbose_name_plural = 'Opere'
        ordering = ['-creation_year', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/opera/{self.slug}'
