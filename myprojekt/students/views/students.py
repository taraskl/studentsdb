﻿#-*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student, Group

# Create your views here.
def student_list(request):
	students = Student.objects.all()
	
	# try to order studenys list	
	order_by = request.GET.get('order_by', '')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
		
	# paginate students
	paginator = Paginator(students, 4) # Show 4 student per pag
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		students = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		students = paginator.page(paginator.num_pages)
	
	return render(request, 'students/students_list.html',
		{'students':students})

def students_add(request):
	# Якщо форма була запощена:
	if request.method == "POST":
		if request.POST.get('add_button') is not None:
			#data for student object
			data={'middle_name':request.POST.get('middle_name'),
				 'notes':request.POST.get('notes')}
			#errors collection
			errors={}
			
			#validate user input
			first_name=request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Ім'я є обов'язковим"
			else:
				data['first_name'] = first_name
			
			last_name=request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов'язковим"
			else:
				data['last_name'] = last_name
			
			birthday=request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов'язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except ValueError:
					errors['birthday'] = u"Ведіть коректний формат дати"
				else:
					data['birthday'] = birthday
					
			ticket=request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Білет є обов'язковим"
			else:
				data['ticket'] = ticket
									
			student_group=request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Група є обов'язковим"
			else:
				group = Group.objects.filter(pk=student_group)
				if len(group) !=1:
					errors['student_group'] = u"Оберіть коректну рупу"
				else:
					data['student_group'] = group[0]
				
			photo=request.FILES.get('photo')
			if photo:
				data['photo'] = photo
				
			#зберігаємо студента
			if not errors:
				group = Group.objects.get(pk=request.POST['student_group'])
				student = Student(**data)
				student.save()
				return  HttpResponseRedirect(reverse('home'))
			else: 
				return render(request, 'students/students_add.html',
				{'groups': Group.objects.all().order_by('title'),
				 'errors': errors})
		elif request.POST.get('cancel_button') is not None:
			return  HttpResponseRedirect(reverse('home'))
	else:
		return render(request, 'students/students_add.html',
			{'groups': Group.objects.all().order_by('title')})
		
def students_edit(request, sid):
	return HttpResponse('student %s edit form' %sid)
	