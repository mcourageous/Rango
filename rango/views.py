from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm
def index(request):
	context = RequestContext(request)
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}
	for category in category_list:
		category.url = category.name.replace(' ', '_')
	return render_to_response('rango/index.html', context_dict, context)


def about(request):
	context = RequestContext(request)
	context_dict = {'welcome':'page serverd from about view'}
	return render_to_response('rango/about.html', context_dict, context)


def category(request, category_name_url):
	context = RequestContext(request)

	category_name = category_name_url.replace('_', ' ')
	context_dict = {'category_name': category_name}
	try:
		category = Category.objects.get(name=category_name)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
		context_dict['category_name_url'] = category_name
	except Category.DoesNotExist:
		pass

	return render_to_response('rango/category.html', context_dict, context)

def decode_url(request, category_name_url):
	decoded = category_name_url.replace('_', ' ')
	return decoded



def add_category(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()

	return render_to_response('rango/add_category.html', {'form':form}, context )


def add_page(request, category_name_url):
	context = RequestContext(request)
	category_name = decode_url(category_name_url)

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit=False)

			cat = Category.objects.get(name=category_name)
			page.category = cat

			page.views = 0

			page.save()

			return category(request, category_name_url)
		else:
			print form.errors
	else:
		form = PageForm

	return render_to_response('rango/add_page.html',
		{'category_name_url':category_name_url,
		'category_name':category_name,
		'form':form}, context)


def register(request):
	context = RequestContext(request)
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

		profile = profile_form.save(commit=False)
		profile.user = user_form


		if 'picture' in request.FILES:
			profile.picture = request.FILES['picture']

			profile.save()

			registered = True
		else:
			user_form = UserForm()
			profile_form = UserProfileForm()

		return render_to_response('rango/register.html',
			{'user_form':user_form, 'profile_form':profile_form, 'registered':registered}, context)




