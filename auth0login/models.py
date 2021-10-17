from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

class Ticket(models.Model):
    ticketName = models.CharField(max_length=40)    # チケット名称
    ticketGroup = models.CharField(max_length=20)   # チケットが権限を付与する Group
    ticketKeyword = models.CharField(max_length=20) # チケットのキーワード
    ticketCount = models.IntegerField(default= 0)             # チケット受付数（あくまで参考値）
    def __str__(self):
        return self.ticketName+":Key:"+self.ticketKeyword

# 個別のビデオを表現するクラス
class Media(models.Model):
    name = models.TextField()                   # ビデオの名前
    order = models.IntegerField(default= 0) # 表示順位
    vid  = models.CharField(max_length= 10)     # Vimeo上でのビデオID
    lecturer = models.CharField(max_length= 60) # 講師の名前
    theme = models.CharField(max_length=40)     # テーマ
    thumb_url = models.CharField(max_length=128, default='')# サムネールのURL (自動登録)
    duration =  models.IntegerField(default= 0) # ビデオの長さ（秒数）
    enabled = models.BooleanField(default=True) # ビデオがあるかないか（再生できるかどうか）
    viewCount = models.IntegerField(default= 0) # 視聴回数
    likeCount = models.IntegerField(default= 0) # いいね回数
    def __str__(self):
        return self.name+":"+self.lecturer

# 講義一式を表現するクラス
class Course(models.Model):
    name  = models.TextField()               # 講義名称
    order = models.IntegerField(default= 0) # 表示順位
    mlist = models.ManyToManyField(Media)    # Media 一覧
    group = models.ForeignKey(Group, on_delete=models.PROTECT)  # 対応するグループ
    def __str__(self):
        return self.name

# ビデオの視聴状況を使うためのデータ (再生が始まったタイミングで作成され, ページ遷移前に保存 )
# これが作成されたタイミングで Media の Viewカウントを追加
class MediaViewCount(models.Model):
    media = models.OneToOneField(Media, on_delete = models.PROTECT) # 対応ビデオ
    currentTime = models.IntegerField(default= 0)     # どこまで視聴したか（最後の状況）
    is_like = models.BooleanField(default=False)                    # Likeかどうか

# ユーザ プロフィール
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "profile") # 対応するユーザ
    affi = models.CharField(max_length=60)       # 所属・部局
    position = models.CharField(max_length = 40) # 役職・学年
    zip = models.CharField(max_length = 10)      # 郵便番号
    city = models.CharField(max_length = 30)     # 県・市
    # Video の視聴カウント
    viewcount = models.ManyToManyField(MediaViewCount)    # 視聴したMediaViewCount 一覧
    def __str__(self):
        return self.user.username


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
