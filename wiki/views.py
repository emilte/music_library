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
    success_msg = "Lagringen var vellykket!"
    error_msg = "Lagringen var misslykket!"
    redirect_name = None

    def get(self, request):
        form = self.form_class(initial={'creator': request.user})
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            try:
                if not instance.id:
                    instance.creator = request.user
                    instance.created = timezone.now()
                instance.last_editor = request.user
                instance.last_edited = timezone.now()
            except Exception as e:
                print(e)
            finally:
                instance.save()
            messages.success(request, self.success_msg)
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
            print( form.cleaned_data )

            instance = form.save(commit=False)
            try:
                instance.last_editor = request.user
                instance.last_edited = timezone.now()
            except Exception as e:
                print(e)
            finally:
                instance.save()

            messages.success(request, self.success_msg)
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
    template = 'wiki/dashboard.html'

    def get(self, request):
        messages.info(request, "OBS: Under utvikling")
        folders = wiki_models.Folder.objects.all()
        single_pages = wiki_models.Page.objects.filter(folder=None)

        return render(request, self.template, {
            'folders': folders,
            'single_pages': single_pages,
        })



page_view_dec = [
    login_required,
    # permission_required('wiki.view_page', login_url='forbidden')
]
@method_decorator(page_view_dec, name='dispatch')
class PageView(View):
    template = 'wiki/page_view2.html'

    def get(self, request, page_path):
        page = wiki_models.Page.objects.get(path=page_path)

        # Needed for dashboard
        folders = wiki_models.Folder.objects.all()
        single_pages = wiki_models.Page.objects.filter(folder=None)

        return render(request, self.template, {
            'page': page,
            'folders': folders,
            'single_pages': single_pages,
        })


add_page_dec = [
    login_required,
    permission_required('wiki.create_page', login_url='forbidden')
]
@method_decorator(add_page_dec, name='dispatch')
class AddPage(GenericAddModel):
    template = 'wiki/page_form.html'
    form_class = wiki_forms.PageForm
    redirect_name = 'wiki:dashboard'

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
