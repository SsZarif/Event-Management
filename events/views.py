from datetime import date
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

def homepage(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Query the Event model for events that match the search query in name or location (case-insensitive)
        events = Event.objects.filter(
            name__icontains=search_query
        ) | Event.objects.filter(
            location__icontains=search_query
        )
    else:
        events = Event.objects.all()
    
    return render(request, 'dashboard/home.html', {'events': events})

def organizer_dashboard(request):
    today = date.today()
    context = {
        'total_participants': Participant.objects.count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(start_time__gte=today).count(),
        'past_events': Event.objects.filter(start_time__lt=today).count(),
        'todays_events': Event.objects.filter(start_time__date=today)
    }

    event_type = request.GET.get('event_type')
    if event_type == 'total':
        context['events'] = Event.objects.all()
    elif event_type == 'upcoming':
        context['events'] = Event.objects.filter(start_time__gte=today)
    elif event_type == 'past':
        context['events'] = Event.objects.filter(start_time__lt=today)
    else:
        context['events'] = context['todays_events']

    # Handle the event detail modal if event_id is passed
    event_id = request.GET.get('event_id')
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
        context['selected_event'] = event

    return render(request, 'dashboard/organizer_dashboard.html', context)

def handle_form_submission(request, form_class, template_name, redirect_url, instance=None):
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = form_class(instance=instance)
    return render(request, template_name, {'form': form})

def create_event(request):
    return handle_form_submission(request, EventForm, 'event/create_event.html', 'event_list')

def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return handle_form_submission(request, EventForm, 'event/update_event.html', 'event_list', event)

def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event/delete_event.html', {'event': event})

def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(participants_count=Count('participants'))
    total_participants = events.aggregate(total_participants=Sum('participants_count'))['total_participants']
    return render(request, 'event/event_list.html', {'events': events, 'total_participants': total_participants})

def event_list_by_category(request, category_id):
    events = Event.objects.filter(category_id=category_id).select_related('category').prefetch_related('participants').annotate(participants_count=Count('participants'))
    total_participants = events.aggregate(total_participants=Sum('participants_count'))['total_participants']
    return render(request, 'event/event_list.html', {'events': events, 'total_participants': total_participants})

def event_list_by_date(request, start_date, end_date):
    events = Event.objects.filter(start_time__range=(start_date, end_date)).select_related('category').prefetch_related('participants').annotate(participants_count=Count('participants'))
    total_participants = events.aggregate(total_participants=Sum('participants_count'))['total_participants']
    return render(request, 'event/event_list.html', {'events': events, 'total_participants': total_participants})

def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participant/create_participant.html', {'form': form})

def update_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    return handle_form_submission(request, ParticipantForm, 'participant/update_participant.html', 'participant_list', participant)

def delete_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant/delete_participant.html', {'participant': participant})

def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'participant/participant_list.html', {'participants': participants})

def create_category(request):
    return handle_form_submission(request, CategoryForm, 'category/create_category.html', 'category_list')

def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return handle_form_submission(request, CategoryForm, 'category/update_category.html', 'category_list', category)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category/delete_category.html', {'category': category})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

