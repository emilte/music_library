# imports
from django.views import View
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth import get_user_model

from wiki import models as wiki_models
from wiki import forms as wiki_forms

User = get_user_model()
# End: imports -----------------------------------------------------------------

# Functions


# End: Functions ---------------------------------------------------------------

class GenericAddModel(View):
    template = None # (*) Required
    form_class = None # (*)
    redirect_name = None # (*)
    redirect_id = None
    success_msg = "Lagringen var vellykket!"
    error_msg = "Lagringen var misslykket!"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            try:
                obj.creator = request.user
            except Exception as e:
                print(e)

            try:
                obj.created = timezone.now()
            except Exception as e:
                print(e)

            try:
                obj.last_editor = request.user
            except Exception as e:
                print(e)

            try:
                obj.last_edited = timezone.now()
            except Exception as e:
                print(e)

            obj.save()
            try:
                obj.save_m2m()
            except Exception as e:
                print(e)
            messages.success(request, self.success_msg)

            if self.redirect_id:
                return redirect(self.redirect_name, getattr(obj, self.redirect_id))
            else:
                return redirect(self.redirect_name)
        else:
            messages.error(request, self.error_msg)
            return render(request, self.template, {'form': form})


class GenericEditModel(GenericAddModel):
    model = None # Required

    def get(self, request, modelID):
        instance = self.model.objects.get(id=modelID)
        form = self.form_class(instance=instance)
        return render(request, self.template, {'form': form, 'modelID': modelID})

    def post(self, request, modelID):
        instance = self.model.objects.get(id=modelID)
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                instance.last_editor = request.user
                instance.last_edited = timezone.now()
            except Exception as e:
                print(e)
            finally:
                instance.save()

            messages.success(request, self.success_msg)

            if self.redirect_id:
                return redirect(self.redirect_name, getattr(instance, self.redirect_id))
            else:
                return redirect(self.redirect_name)
        else:
            messages.error(request, self.error_msg)
            return render(request, self.template, {'form': form, 'modelID': modelID})


dashboard_dec = [
    login_required,
    # permission_required('wiki.change_page', login_url='forbidden')
]
@method_decorator(dashboard_dec, name='dispatch')
class Dashboard(View):
    template = 'wiki/dashboard2.html'

    def get(self, request):
        # messages.info(request, "OBS: Under utvikling")
        folders = wiki_models.Folder.objects.all()
        single_pages = wiki_models.Page.objects.filter(folder=None)
        root_folders = wiki_models.Folder.objects.filter(root_folder=None) # (**) dashboard2

        return render(request, self.template, {
            'folders': folders,
            'single_pages': single_pages,
            'root_folders': root_folders, # (**)
        })



page_view_dec = [
    login_required,
    # permission_required('wiki.view_page', login_url='forbidden')
]
@method_decorator(page_view_dec, name='dispatch')
class PageView(View):
    template = 'wiki/page_view3.html'

    def get(self, request, page_path):

        page = wiki_models.Page.objects.get(path=page_path)

        for folder in page.root_path():
            if folder.perm:
                if not request.user.has_perm(folder.perm):
                    return redirect("forbidden")

        # Needed for dashboard
        folders = wiki_models.Folder.objects.all() # (*) dashboard
        single_pages = wiki_models.Page.objects.filter(folder=None)
        root_folders = wiki_models.Folder.objects.filter(root_folder=None) # (**) dashboard2


        return render(request, self.template, {
            'page': page,
            'folders': folders, # (*)
            'single_pages': single_pages,
            'root_folders': root_folders, # (**)
        })


add_page_dec = [
    login_required,
    permission_required('wiki.create_page', login_url='forbidden')
]
@method_decorator(add_page_dec, name='dispatch')
class AddPage(GenericAddModel):
    template = 'wiki/page_form.html'
    form_class = wiki_forms.PageForm
    redirect_name = 'wiki:page_view'

    # def dispatch(self, request, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     modelID = kwargs.get('modelID')
    #     if modelID and not self.redirect_name:
    #         self.redirect_name =
    #
    #     return super(GenericAddModel, self).dispatch(request, *args, **kwargs)



edit_page_dec = [
    login_required,
    permission_required('wiki.change_page', login_url='forbidden')
]
@method_decorator(edit_page_dec, name='dispatch')
class EditPage(GenericEditModel):
    template = 'wiki/page_form.html'
    form_class = wiki_forms.PageForm
    redirect_name = 'wiki:dashboard'
    model = wiki_models.Page



add_folder_dec = [
    login_required,
    permission_required('wiki.create_folder', login_url='forbidden')
]
@method_decorator(add_folder_dec, name='dispatch')
class AddFolder(GenericAddModel):
    template = 'wiki/folder_form.html'
    form_class = wiki_forms.FolderForm
    redirect_name = 'wiki:dashboard'



edit_folder_dec = [
    login_required,
    permission_required('wiki.change_folder', login_url='forbidden')
]
@method_decorator(edit_folder_dec, name='dispatch')
class EditFolder(GenericEditModel):
    template = 'wiki/folder_form.html'
    form_class = wiki_forms.FolderForm
    redirect_name = 'wiki:dashboard'
    model = wiki_models.Folder
