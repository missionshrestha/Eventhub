from django.core.checks import messages
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import redirect, reverse,render
from django.views.generic import View
from users import models as user_models
from . import models,forms
import conversations


# Create your views here.
def go_conversation(request,organizer_pk,participants_pk):
    try:
        user_one = user_models.User.objects.get(pk=organizer_pk)
        user_two = user_models.User.objects.get(pk=participants_pk)
    except user_models.User.DoesNotExist:
        user_one = None
        user_two = None

    if user_one is not None and user_two is not None:
        # try:
        #     conversation = models.Conversation.objects.get(Q(participants=user_one) & Q(participants=user_two))
        # except models.Conversation.DoesNotExist:
        #     conversation = models.Conversation.objects.create()
        #     conversation.participants.add(user_one,user_two)

        conversation_query = models.Conversation.objects.filter(Q(participants=user_one)).filter(Q(participants=user_two))
        if conversation_query.count() == 0:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one,user_two)
        else:
            conversation = conversation_query[0]
        return redirect(reverse("conversations:detail",kwargs={"pk":conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args,**kwargs):
        pk = kwargs.get("pk")
        try:
            conversation = models.Conversation.objects.get(pk=pk)
        except models.Conversation.DoesNotExist:
            raise Http404
        form = forms.AddMessageForm()
        return render(self.request,"conversations/conversation_detail.html",{"conversation":conversation,"form":form})

    def post(self,*args,**kwargs):
        form = forms.AddMessageForm(self.request.POST)
        pk = kwargs.get("pk")
        try:
            conversation = models.Conversation.objects.get(pk=pk)
        except models.Conversation.DoesNotExist:
            raise Http404

        if form.is_valid():
            message = form.cleaned_data['message']
            models.Message.objects.create(message=message,user=self.request.user,conversation=conversation)
        return redirect(reverse("conversations:detail",kwargs={"pk":pk}))
