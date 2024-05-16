from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from bbs.models import Category, Article, Tag
from django.views.generic import TemplateView
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_SSID = os.getenv("GOOGLE_API_SSID")
GOOGLE_API_JSON = os.getenv("GOOGLE_API_JSON")
IMG_PATH = os.getenv("IMG_PATH")
EXCEL_PATH = os.getenv("EXCEL_PATH")

from django.shortcuts import render, redirect
from .forms import ContactForm
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt , pandas as pd

def paginate_queryset(request, queryset, count):
	paginator = Paginator(queryset, count)
	page = request.GET.get('page')
	try:
		page_obj = paginator.page(page)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)
	return page_obj

def index(request):
	articles = Article.objects.order_by('-id')
	page_obj = paginate_queryset(request, articles, 6)
	return render(request,'bbs/index.html',{'articles': page_obj.object_list,'page_obj': page_obj})

def category(request, category):
	category = Category.objects.get(name=category)
	articles = Article.objects.order_by('-id').filter(category=category)
	page_obj = paginate_queryset(request, articles, 6)
	return render(request, 'bbs/list.html',{'category': category, 'articles': page_obj.object_list,'page_obj': page_obj })

def tag(request, tag):
	tag = Tag.objects.get(name=tag)
	articles = Article.objects.order_by('-id').filter(tag=tag)
	page_obj = paginate_queryset(request, articles, 6)
	return render(request, 'bbs/list.html',{'tag': tag, 'articles': page_obj.object_list,'page_obj': page_obj })

from datetime import datetime

def detail(request, slug):
	entries = Article.objects.order_by('-id')[:3]
	article = get_object_or_404(Article, slug=slug)

	excel_file_path = EXCEL_PATH + 'weight.xlsx'
	workbook = pd.ExcelFile(excel_file_path)
	worksheet = workbook.parse('weight')

	col_values = worksheet.iloc[:, 0].dropna().values

	pngDate = str(col_values[-1])
	weight_png_date = pd.to_datetime(pngDate).date()

	article_updated_at = article.updated_at


	current_year = datetime.now().year
	formatted_date = f"{current_year}/{weight_png_date.month}/{weight_png_date.day}"
	weight_png_date = datetime.strptime(formatted_date, '%Y/%m/%d').date()


	with plt.style.context('Solarize_Light2'):
		plt.rcParams["figure.figsize"] = (12, 6)
		plt.ylim(66, 84)

		plt.plot(worksheet['date'], worksheet['weight'], marker='o', color='#4e3b2f')
		plt.title('Weight Graph')
		plt.xlabel('Date')
		plt.ylabel('Weight')

		plt.xticks(worksheet['date'], rotation=45, ha='right')

		plt.grid(True)
		plt.tight_layout()
		plt.savefig(IMG_PATH + 'weight.png')

	if article.slug == "fitness":
		if article_updated_at > weight_png_date:
			latest_date = article_updated_at
		else:
			latest_date = weight_png_date
	else:
		latest_date = article_updated_at

	params = {
		'article': article,
		'entries': entries,
		'pngDate': pngDate,
		'latest_date': latest_date,
	}

	return render(request,'bbs/detail.html', params)


def complete(request):
	entries = Article.objects.order_by('-id')[:3]
	article = Article.objects.order_by('-id')
	return render(request, 'bbs/complete.html', {'article':article,'entries': entries})

def contact_form(request):
	entries = Article.objects.order_by('-id')[:3]
	article = Article.objects.order_by('-id')
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			sender = form.cleaned_data['sender']
			myself = form.cleaned_data['myself']
			recipients = [settings.EMAIL_HOST_USER]
			if myself:
				recipients.append(sender)
			try:
				send_mail(subject, message, sender, recipients)
			except BadHeaderError:
				return HttpResponse('Invalid header found')
			return redirect('bbs:complete')
	else:
		form = ContactForm()
	return render(request, 'bbs/contact.html', {'form': form,'article':article,'entries': entries})
