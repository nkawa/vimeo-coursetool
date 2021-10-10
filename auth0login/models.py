from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

class Ticket(models.Model):
    ticketName = models.CharField(max_length=40)    # チケット名称
    ticketGroup = models.CharField(max_length=20)   # チケットが権限を付与する Group
    ticketKeyword = models.CharField(max_length=20) # チケットのキーワード
    ticketCount = models.IntegerField               # チケット受付数（あくまで参考値）
    def __str__(self):
        return self.ticketName




def setTicket(user,keyw):
    if not user.is_authenticated:
        return False
    tickets = Ticket.objects.filter(ticketKeyword__exact=keyw)
    print("Filter Ticket",keyw,tickets)
    if len(tickets) == 0 :
        print("No ticket")
        return False
    else:
        tk = tickets[0]
        gp = Group.objects.filter(name__exact=tk.ticketGroup)
        print("find Group!")
        return True
