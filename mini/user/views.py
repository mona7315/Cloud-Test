from builtins import object
from fnmatch import filter
from webbrowser import register
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from user.models import Booking, Room


# Create your views here.
@login_required(login_url='/')
@permission_required('user.view_room', login_url='/')
def index(request):
 
    search_txt = request.POST.get('search','')
    all_room = Room.objects.filter(
        name__icontains= search_txt ).order_by('name')

    search_time = request.POST.get('time', '') 
    search_day = request.POST.get('day', '') 
    context = {
        'all_room': all_room,   
    }

    return render(request, 'user/index.html', context)


@login_required(login_url='/')
@permission_required('user.add_booking', login_url='/')
def booking(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    user = request.user.id
    book = Booking.objects.all()
    context = dict()

    if request.method == 'POST':
        st_time = request.POST.get('st_time')
        ed_time = request.POST.get('ed_time')
        reason = request.POST.get('reason')        
        date = request.POST.get('date')
       
        try:
            check = Booking.objects.filter(book_date=request.POST.get('date'), room_id__name=room.name)
        except ObjectDoesNotExist:
            check = None
        if check:
            context['error'] = 'ห้องนี้ถูกจองเรียบร้อยแล้ว กรุณาเปลี่ยนวันจองห้อง'
            
        else:
            booking_room = Booking.objects.create(
                room_id = room,
                start_time = st_time,
                end_time = ed_time,
                description = reason,
                book_by = User.objects.get(pk=user),
                book_date = date
            )
            booking_room.save()
            return redirect('bookinglist') 
    
    context['room'] = room
    context['room_id'] = rm_id
    context['book'] = book
    return render(request, 'user/booking.html', context=context)


@login_required(login_url='/')
@permission_required('user.view_booking', login_url='/')
def bookinglist(request):
    all_book = Booking.objects.all().order_by('book_date')
    user_id = request.user.id

    context = {
        'all_book' : all_book,
        'user_id' : user_id
    }
    return render(request, 'user/bookinglist.html', context)


@login_required(login_url='/')
@permission_required('user.change_room', login_url='/')
def edit(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    if request.method == 'POST':     

        room.name = request.POST.get('name')
        room.open_time = request.POST.get('st_time')
        room.close_time = request.POST.get('ed_time')
        room.capacity = request.POST.get('cap')
        room.save()

        return redirect('index')
    context = {
        'room': room,
        'room_id' : rm_id 
        }

    return render(request, 'user/edit.html', context)


@login_required(login_url='/')
@permission_required('user.add_room', login_url='/')
def add(request):
    context ={}

    if request.method == 'POST':
        name = request.POST.get('name')
        opentime = request.POST.get('st_time')
        closetime = request.POST.get('ed_time')
        capacity = request.POST.get('cap')

        try:
            room = Room.objects.get(name=request.POST.get('name'))
        except ObjectDoesNotExist:
            room = None

        if room:
            context = {
            'error' : "ห้องซ้ำ"
            }
            return render(request, 'user/add.html', context)     
        else:
            room = Room.objects.create(
            name = name,
            open_time = opentime,
            close_time = closetime,
            capacity = capacity
            )
            room.save()
            return redirect('index')
    

    return render(request, 'user/add.html', context)


@login_required(login_url='/')
@permission_required('user.delete_room', login_url='/')
def delete(request, rm_id):
    room = Room.objects.get(pk=rm_id)
    room.delete()
    return redirect('index')


@login_required(login_url='/')
@permission_required('user.change_room', login_url='/')
def accept(request, rm_id):
    book = Booking.objects.get(pk=rm_id)
    room = Room.objects.get(pk=book.room_id.room_id)

    if request.method == 'POST':
        book.status_remark = request.POST.get('reason')
        book.status = True
        

        book.save()

        return redirect('bookinglist')
    context = {
        'room' : room,
        'room_id' : rm_id,
        'book' : book, 
       
    }
    return render(request, 'user/accept.html', context)
