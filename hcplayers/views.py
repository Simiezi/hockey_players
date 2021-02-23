from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hitcount.views import HitCountDetailView
from django.contrib.postgres.search import SearchVector

from .models import Player
from .forms import CommentForm, SearchForm


def post_list(request):
    object_list = Player.objects.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)

    return render(request,
                  'hcplayers/playrs/list.html',
                  {'page': page,
                   'players': players})


class PlayerDetailView(HitCountDetailView):
    model = Player
    context_object_name = 'player'
    count_hit = True
    template_name = 'hcplayers/playrs/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Player, slug=self.kwargs.get('player'))
        comments = self.object.comments.filter(active=True)
        context = self.get_context_data(object=self.object)
        new_comment = None
        comment_form = CommentForm
        context['comment_form'] = comment_form
        context['new_comment'] = new_comment
        context['comments'] = comments
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        new_comment = None
        if comment_form.is_valid():
            context = super().get_context_data(**kwargs)
            new_comment = comment_form.save(commit=False)
            new_comment.player = get_object_or_404(Player, slug=self.kwargs.get('player'))
            new_comment.save()
            context['comment_form'] = CommentForm
            context['new_comment'] = new_comment
            return self.render_to_response(context=context)
        else:
            context = super().get_context_data(**kwargs)
            context['comment_form'] = comment_form
            return self.render_to_response(context=context)

def player_detail(request, player):
    player = get_object_or_404(Player,
                               slug=player)
    comments = player.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.player = player
            new_comment.save()
    else:
        comment_form = CommentForm
    return render(request,
                  'hcplayers/playrs/detail.html',
                  {'player': player,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def player_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Player.objects.annotate(
                search=SearchVector('first_name', 'last_name')
            ).filter(search=query)

    return render(request,
                  'hcplayers/playrs/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})