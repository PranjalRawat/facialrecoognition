from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.conf import settings
from .forms import UploadFile, UploadRecFile, DeleteFile
from recognizer.models import *
import os
import shutil
from facial_recognition.settings.local import BASE_DIR
from django.core.files.storage import FileSystemStorage
import facial_recognition.train_dataset as train_set
import facial_recognition.recognize as recognizer
import facial_recognition.data as data
import facial_recognition.delete_face_from_dataset as delete_data
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponseRedirect

def index(request):
    return render(request,"index.html")

class train(FormView):

    form_class = UploadFile
    template_name = 'train.html'
    success_url = '/train_dataset/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        
        if form.is_valid():
            title = form.cleaned_data['title']
            try:
                os.mkdir(str(BASE_DIR) +'/known_faces/'+ str(title)+'/')
            except:
                pass
            fs = FileSystemStorage(location=(str(BASE_DIR) +'/known_faces/'+ str(title)+'/'))
            for f in files:
                filename = fs.save(f.name,f)
            train_set.train()
            shutil.rmtree(str(BASE_DIR) +'/known_faces/')
            context = {
                "sucess": 'Sucessfully Trained dataset for',
                "title": title
                
            }
            return render(request, 'train.html', context)
        else:
            return self.form_invalid(form)


class recognize(FormView,SuccessMessageMixin):
    
    form_class = UploadRecFile
    template_name = 'recognize.html'
    success_url = '/recognize/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        
        if form.is_valid():
            fs = FileSystemStorage(location=(str(BASE_DIR) +'/unknown_faces/'))
            for f in files:
                filename = fs.save(f.name,f)
            
            success_message = recognizer.recognize()
            shutil.rmtree(str(BASE_DIR) +'/unknown_faces/')
            context = {
                "faces": success_message[0],
                "total": success_message[1],
                "time": success_message[2]
            }
            return render(request, 'recognize.html', context)
            
        else:
            return self.form_invalid(form)


class delete(FormView):
    
    form_class = DeleteFile
    template_name = 'delete.html'
    success_url = '/delete/'
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        if form.is_valid():
            title = form.cleaned_data['title'] 
            a=delete_data.delete(title)
            if a:
                context = {
                    "sucess": 'Sucessfully Deleted data for',
                    "title": title
                    
                }
                return render(request, 'delete.html', context)
            else:
                context = {
                    "sucess": 'Not Found data for',
                    "title": title
                    
                }
                return render(request, 'delete.html', context)
        else:
            return self.form_invalid(form)

def dataset(request):
    template_name = 'faces.html'
       
    li = data.faces()
    a=[]
    for i in li:
        a.append(i.replace('_',' '))

    context = {
                "name_list": a,
            }
    return render(request, 'faces.html', context)