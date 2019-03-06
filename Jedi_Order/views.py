from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404

from .forms import CandidateForm, ChallengeForm, JediSelectForm, AddPadawan
from .models import Challenge, Candidate, Jedi


class NewCandidateView(CreateView):
    form_class = CandidateForm
    template_name = 'Jedi_Order/new_candidate.html'

    def get_success_url(self):
        return reverse('try-challenge', kwargs={'candidate_id': self.object.pk,
                                                'order_id': self.object.planet_id})


class ChallengeView(FormView):
    form_class = ChallengeForm
    template_name = 'Jedi_Order/try_challenge.html'
    success_url = reverse_lazy('passed')

    def get_form_kwargs(self):
        candidate_id = self.kwargs.get('candidate_id', None)
        candidate = get_object_or_404(Candidate, id=candidate_id)
        order_id = self.kwargs.get('order_id', None)
        questions = get_object_or_404(Challenge, order_id=order_id).question.all()
        form_kwargs = super(ChallengeView, self).get_form_kwargs()
        form_kwargs['candidate'] = candidate
        form_kwargs['questions'] = [(q.id, q.text) for q in questions]
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(ChallengeView, self).form_valid(form)


class JediSelectView(FormView):
    form_class = JediSelectForm
    template_name = 'Jedi_Order/select_jedi.html'

    def form_valid(self, form):
        return redirect(reverse('jedi', kwargs={'jedi_id': form.cleaned_data['jedi'].id}))


class JediView(ListView):
    template_name = 'Jedi_Order/jedis_candidates.html'
    context_object_name = 'candidates'

    def get_queryset(self):
        jedi_id = self.kwargs.get('jedi_id', None)
        jedi = get_object_or_404(Jedi, id=jedi_id)
        return Candidate.objects.filter(planet=jedi.planet)

    def get_context_data(self, **kwargs):
        context = super(JediView, self).get_context_data(**kwargs)
        context['jedi_id'] = self.kwargs['jedi_id']
        return context


class CandidateToPadawanView(DetailView, FormMixin):
    model = Candidate
    template_name = 'Jedi_Order/candidate_detail.html'
    pk_url_kwarg = 'candidate_id'
    form_class = AddPadawan
    success_url = '/'

    def get_initial(self):
        candidate_id = self.kwargs.get('candidate_id', None)
        candidate = get_object_or_404(Candidate, id=candidate_id)
        jedi_id = self.kwargs.get('jedi_id', None)
        jedi = get_object_or_404(Jedi, id=jedi_id)
        return {'candidate': candidate,
                'jedi': jedi}

    def form_valid(self, form):
        form.save()
        return super(CandidateToPadawanView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class JediListView(ListView):
    queryset = Jedi.with_padawans.all()
    template_name = 'Jedi_Order/list_jedi.html'
    context_object_name = 'jedis'


class JediListMoreThanOneView(JediListView):
    queryset = Jedi.with_padawans.more_than_one()
