from django.shortcuts import get_object_or_404, render

from .models import Mostra, Opera


def opere_base_view(request):
    """List all published sculptures."""
    opere = Opera.objects.filter(typology='S', published=True).order_by('pk')
    return render(request, 'opere/opere_base.html', {'opere': opere, 'typology': 'Opere'})


def gioielli_base_view(request):
    """List all published jewelry."""
    opere = Opera.objects.filter(typology='G', published=True).order_by('pk')
    return render(request, 'opere/opere_base.html', {'opere': opere, 'typology': 'Gioielli'})


def disegni_base_view(request):
    """List all published drawings."""
    opere = Opera.objects.filter(typology='D', published=True)
    return render(request, 'opere/opere_base.html', {'opere': opere, 'typology': 'Disegni'})


def opera_detail_view(request, slug):
    """Detail view for a single artwork."""
    opera = get_object_or_404(Opera, slug=slug, published=True)
    return render(request, 'opere/opera_detail.html', {'opera': opera})


def mostra_detail_view(request, slug):
    """Detail view for a single exhibition."""
    mostra = get_object_or_404(Mostra, slug=slug, published=True)
    return render(request, 'opere/mostra_detail.html', {'mostra': mostra})


def mostre_list_view(request):
    """List all published exhibitions."""
    mostre = Mostra.objects.filter(published=True)
    return render(request, 'opere/mostre_list.html', {'mostre': mostre})


def biografia_view(request):
    """Biography page with exhibitions grouped by type and year."""
    mostre_personali = Mostra.objects.filter(
        published=True, type='1'
    ).order_by('-beginning')
    mostre_collettive = Mostra.objects.filter(
        published=True, type='2'
    ).order_by('-beginning')
    return render(request, 'biografia.html', {
        'mostre_personali': mostre_personali,
        'mostre_collettive': mostre_collettive,
    })


def contatti_view(request):
    """Contact page with a simple form."""
    return render(request, 'contatti.html')
