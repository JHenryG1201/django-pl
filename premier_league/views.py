from django.views.generic import ListView, DetailView, FormView
from .models import Team, Player, Fixture, Guess
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import ContactForm, GuessForm
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.core.mail import EmailMessage

# Create your views here.
class HomePageView(ListView):
    model = Team
    template_name = 'index.html'
    def get_queryset(self):
        queryset = {
            'teams' : Team.objects.order_by('rank'),
            'next_fixture_list': Fixture.objects.all().filter(finished = False).order_by('kickoff_time')[:10],
        }
        return queryset
    
class TeamDetailPageView(DetailView):
    model = Team
    template_name = 'team_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        fixtures = Fixture.objects.all().filter(Q(team1_id = self.object.pk) | Q(team2_id = self.object.pk)).order_by('kickoff_time')
        players = Player.objects.all().filter(team_id = self.object.pk)
        context['fixtures'] = fixtures
        context['players'] = players
        return context

class TeamPageView(ListView):
    model = Team
    template_name = 'team_list.html'

class PlayerDetailPageView(DetailView):
    model = Player
    template_name = 'player_detail.html'

class PlayerPageView(ListView):
    model = Player
    template_name = 'player_list.html'
    paginate_by = 30

class FixturePageView(ListView):
    model = Fixture
    template_name = 'fixture_list.html'
    paginate_by = 10

class ContactPageView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('premier_league:contact')
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'お問い合わせ：{}'.format(title)

        message = '送信者名：{0}\nメールアドレス:{1}\nタイトル:{2}\nメッセジー:\n{3}'.format(name, email, title, message)

        from_email = 'test@gmail.com'

        to_list = ['test@gmail.com']

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list)

        message.send()

        messages.success(self.request, 'お問い合わせは正常に送信されました。')

        return super().form_valid(form)
    
class FixtureDetailPageView(FormMixin, DetailView):
    model = Fixture
    template_name = 'fixture_detail.html'
    form_class = GuessForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        guesses = Guess.objects.all().filter(fixture_id = self.object.id)
        print(guesses)
        context['guesses'] = guesses
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        guess = form.save(commit=False)
        guess.fixture = self.get_object()
        guess.save()
        return super().form_valid(form)