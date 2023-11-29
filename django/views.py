from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def simpleUpload(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploadFileUrl = fs.url(filename)
        return render(request, "core/simple_upload.html", {"uploadedFileUrl": uploadFileUrl})