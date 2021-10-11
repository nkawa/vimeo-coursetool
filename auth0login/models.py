from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

class Ticket(models.Model):
    ticketName = models.CharField(max_length=40)    # チケット名称
    ticketGroup = models.CharField(max_length=20)   # チケットが権限を付与する Group
    ticketKeyword = models.CharField(max_length=20) # チケットのキーワード
    ticketCount = models.IntegerField(default= 0)             # チケット受付数（あくまで参考値）
    def __str__(self):
        return self.ticketName

# 個別のビデオを表現するクラス
class Media(models.Model):
    name = models.TextField()                   # ビデオの名前
    vid  = models.CharField(max_length= 10)     # Vimeo上でのビデオID
    lecturer = models.CharField(max_length= 60) # 講師の名前
    theme = models.CharField(max_length=40)     # テーマ
    enabled = models.BooleanField(default=True) # ビデオがあるかないか

# 講義一式を表現するクラス
class Course(models.Model):
    name  = models.TextField()               # 講義名称
    mlist = models.ManyToManyField(Media)    # Media 一覧
    group = models.ForeignKey(Group, on_delete=models.PROTECT)  # 対応するグループ


# 特定のユーザからのチケット登録　OKならGroup登録してTrue
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
        print("find Group!", gp)
        if len(gp) > 0:
            user.groups.add(gp[0])
            tk.ticketCount += 1
            tk.save()
            user.save()
            return True        
        return False
