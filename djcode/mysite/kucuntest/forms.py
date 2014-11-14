#coding=utf-8
from django import forms
import re
from models import *
from django.forms import ModelForm,Textarea
from django.forms.extras.widgets import SelectDateWidget
import datetime
import views


class AddPinlei(ModelForm):
    class Meta:
        model = PinleiGL
        fields = ['pinleiname']

    def clean_pinleiname(self):
        pinleiname = self.cleaned_data['pinleiname']
        if PinleiGL.objects.filter(pinleiname=pinleiname).exists():
            html = u'%s已经存在，请检查。' % pinleiname
            raise forms.ValidationError(html)
        return pinleiname
class EditPinlei(ModelForm):
    class Meta:
        model = PinleiGL
        fields = ['pinleiname']

    def clean_pinleiname(self):
        pinleiname = self.cleaned_data['pinleiname']
        if PinleiGL.objects.filter(pinleiname=pinleiname).exists():
            html = u'%s已经存在，请检查。' % pinleiname
            raise forms.ValidationError(html)
        return pinleiname



class AddGongyingshang (forms.Form):
	name = forms.CharField(max_length=30 ,label=u'供应商名称')
	kaihuhang = forms.CharField(max_length=30 , label=u'开户行')
	zhanghao = forms.CharField(max_length=50 , label=u'帐号')
	hanghao = forms.CharField(max_length=30 , label=u'行号')


	def clean_name(self):
		name = self.cleaned_data['name']
		re_name = ur"[\u4e00-\u9fa5]*$"
		if not re.match(re_name,name):
			raise forms.ValidationError(u'只能包含中文且没有标点符号')
		elif GongyingshangGL.objects.filter(name=name).exists():
			html = u'%s已经存在，请检查。' % name
			raise forms.ValidationError(html)

		return name

	def clean_kaihuhang(self):
		kaihuhang = self.cleaned_data['kaihuhang']
		re_kaihuhang = ur"[\w\u4E00-\u9FA5\uF900-\uFA2D]*$"
		if not re.match(re_kaihuhang,kaihuhang):
			raise forms.ValidationError(u'只能包含中文及字母和数字.')
		return kaihuhang

	def clean_zhanghao(self):
		zhanghao = self.cleaned_data['zhanghao']
		re_zhanghao = ur"[0-9]*$"
		if not re.match(re_zhanghao,zhanghao):
			raise forms.ValidationError(u'只能包含数字且没有标点')
		return zhanghao

	def clean_hanghao(self):
		hanghao = self.cleaned_data['hanghao']
		re_hanghao = ur"[0-9]*$"
		if not re.match(re_hanghao,hanghao):
			raise forms.ValidationError(u'只能包含数字且没有标点')
		return hanghao

class EditGongyingshang(ModelForm):
    class Meta:
        model = GongyingshangGL
        fields = ['kaihuhang','zhanghao','hanghao']
    def clean_kaihuhang(self):
        kaihuhang = self.cleaned_data['kaihuhang']
        re_kaihuhang = ur"[\w\u4E00-\u9FA5\uF900-\uFA2D]*$"
        if not re.match(re_kaihuhang,kaihuhang):
            raise forms.ValidationError(u'只能包含中文及字母和数字.')
        return kaihuhang
    def clean_zhanghao(self):
        zhanghao = self.cleaned_data['zhanghao']
        re_zhanghao = ur"[0-9]*$"
        if not re.match(re_zhanghao,zhanghao):

            #messages.add_message(request, messages.ERROR, 'We did it!')
            raise forms.ValidationError(u'只能包含数字且没有标点')
        return zhanghao
    def clean_hanghao(self):
        hanghao = self.cleaned_data['hanghao']
        re_hanghao = ur"[0-9]*$"
        if not re.match(re_hanghao,hanghao):
            raise forms.ValidationError(u'只能包含数字且没有标点')
        return hanghao

class EditGongyingshangname(ModelForm):
    class Meta:
        model = GongyingshangGL
        fields = ['name','kaihuhang','zhanghao','hanghao']
    def clean_name(self):
        name = self.cleaned_data['name']
        re_name = ur"[\u4e00-\u9fa5]*$"
        if not re.match(re_name,name): #修改供应商时不再验证重复，直接save进行保存
            raise forms.ValidationError(u'只能包含中文且没有标点符号')

        return name
    def clean_kaihuhang(self):
        kaihuhang = self.cleaned_data['kaihuhang']
        re_kaihuhang = ur"[\w\u4E00-\u9FA5\uF900-\uFA2D]*$"
        if not re.match(re_kaihuhang,kaihuhang):
            raise forms.ValidationError(u'只能包含中文及字母和数字.')
        return kaihuhang
    def clean_zhanghao(self):
        zhanghao = self.cleaned_data['zhanghao']
        re_zhanghao = ur"[0-9]*$"
        if not re.match(re_zhanghao,zhanghao):
            raise forms.ValidationError(u'只能包含数字且没有标点')
        return zhanghao
    def clean_hanghao(self):
        hanghao = self.cleaned_data['hanghao']
        re_hanghao = ur"[0-9]*$"
        if not re.match(re_hanghao,hanghao):
            raise forms.ValidationError(u'只能包含数字且没有标点')
        return hanghao


class AddHetong (forms.Form):
    
    hetongNO = forms.CharField(max_length=30 , label=u'合同编号')
    name = forms.ModelChoiceField(queryset=GongyingshangGL.objects.all(), empty_label="(Nothing)" ,
                                  label=u'供应商')
    pinleiname = forms.ModelChoiceField(queryset=PinleiGL.objects.all(),empty_label="(Nothing)" ,
                                        label=u'品类')
    gongjia =  forms.FloatField(label=u'合同供价')
    hetongshuliang = forms.IntegerField(label=u'合同数量')
    #hetongzongjia = forms.FloatField(label=u'合同数量')
    #kerukushuliang = forms.IntegerField(label=u'可入库数量')
    hetongdate = forms.DateField(widget= SelectDateWidget(years=range(2013, 2020)),label=u'合同签订日期',)

    def clean_hetongNO(self):
        hetongNO = self.cleaned_data['hetongNO']
        re_hetongNO = ur"[A-Za-z0-9]*$"
        if not re.match(re_hetongNO , hetongNO):
            raise forms.ValidationError(u'只能使用字母数字且不能包含标点')
        elif HetongGL.objects.filter(hetongNO=hetongNO).exists():
            html = u'%s已经存在，请检查。' % hetongNO
            raise forms.ValidationError(html)

        return hetongNO
    def clean_hetongdate(self):
        hetongdate = self.cleaned_data['hetongdate']
        today = datetime.date.today()
        if hetongdate > today:
            html = u'今天的日期是%s,合同签日期不能大于当天日期！' %str(today)
            raise forms.ValidationError(html)
        return hetongdate

class EditHetong(ModelForm):
	class Meta:
		model = HetongGL
		fields = ['name', 'pinleiname','gongjia', 'hetongshuliang', 'hetongdate']
	def clean_hetongdate(self):
		hetongdate = self.cleaned_data['hetongdate']
		today = datetime.date.today()
		if hetongdate > today:
			html = u'今天的日期是%s,合同签日期不能大于当天日期！' %str(today)
			raise forms.ValidationError(html)
		return hetongdate
class AddChuRukumx(ModelForm):
    class Meta:
        model = ChuRukuMX
        fields = ['hetongNO','churukufangxiang','churukumx_shuliang', 'churukumx_date']


    def clean_churukumx_shuliang(self):
        churukufangxiang = self.cleaned_data['churukufangxiang']
        hetongNO = self.cleaned_data['hetongNO']
        churukumx_shuliang = self.cleaned_data['churukumx_shuliang']
        kerukushuliang = HetongGL.objects.get(hetongNO = hetongNO).kerukushuliang



        if churukufangxiang == 'IN':
            if churukumx_shuliang > kerukushuliang:
                html = u'合同号： %s可入库数量为%d，请重新填写。也可查看“合同列表”。'  % (hetongNO , kerukushuliang)
                raise forms.ValidationError(html)
        elif churukufangxiang == 'OUT':
            if churukufangxiang == 'OUT':
                if not KucunGL.objects.filter(kucungl_hetongbianhao = hetongNO).exists():
                    html=u'该合同没有入库记录，不能进行出库操作，请重新填写。'
                    raise forms.ValidationError(html)
            kucunshuliang = KucunGL.objects.get(kucungl_hetongbianhao = hetongNO).kucungl_kucunshuliang
            if churukumx_shuliang > kucunshuliang:
                html = u'合同号： %s库存数量为%d，请重新填写。也可查看“库存列表”。'  % (hetongNO , kucunshuliang)
                raise forms.ValidationError(html)
        return churukumx_shuliang

    def clean_churukumx_date(self):
        churukumx_date = self.cleaned_data['churukumx_date']
        today = datetime.date.today()
        hetongNO = self.cleaned_data['hetongNO']
        hetongdate = HetongGL.objects.get(hetongNO = hetongNO).hetongdate
        if churukumx_date > today:
            html = u'今天的日期是%s,日期不能大于当天日期！' %str(today)
            raise forms.ValidationError(html)
        if churukumx_date < hetongdate:
            html = u'合同签订日期为%s,出入库日期应当大于合同签订日期！' %str(hetongdate)
            raise forms.ValidationError(html)


        return churukumx_date

class AddFukuanMX(ModelForm): #增加付款明细表单
    class Meta:
        model = FukuanMX
        fields = ['hetongNO','fukuanmx_fukuanjine', 'fukuanmx_date'] #显示字段


    def clean_fukuanmx_date(self): #验证日期，不能大于当天日期
        hetongNO = self.cleaned_data['hetongNO']
        fukuanmx_date = self.cleaned_data['fukuanmx_date']
        today = datetime.date.today()
        hetongdate = HetongGL.objects.get(hetongNO = hetongNO).hetongdate
        if fukuanmx_date > today:
            html = u'今天的日期是%s,日期不能大于当天日期！' %str(today)
            raise forms.ValidationError(html)
        if fukuanmx_date < hetongdate:
            html = u'合同签订日期为%s,付款日期应当大于合同签订日期！' %str(hetongdate)
            raise forms.ValidationError(html)
        return fukuanmx_date

    def clean_fukuanmx_fukuanjine(self): #验证输入数量，不能大于付款管理中待付款金额
        hetongNO1 = self.cleaned_data['hetongNO']
        fukuanmx_fukuanjine = self.cleaned_data['fukuanmx_fukuanjine']
        fukuangl = FukuanGL.objects.get(fukuangl_hetongNO = hetongNO1)
        daifukuanjine = fukuangl.fukuangl_daifukuanjine
        if fukuanmx_fukuanjine > daifukuanjine:
            html = u'合同号： %s待付款金额为%d，请重新填写。也可查看“合同列表”。'  % (hetongNO1 , daifukuanjine)
            raise forms.ValidationError(html)

        return fukuanmx_fukuanjine


class EditFukuanMX(ModelForm): #编辑付款明细表单
    class Meta:
        model = FukuanMX
        fields = ['fukuanmx_fukuanjine', 'fukuanmx_date'] #显示字段

    def clean_fukuanmx_date(self): #验证日期，不能大于当天日期
        hetongNO = views.hetongno()
        fukuanmx_date = self.cleaned_data['fukuanmx_date']
        today = datetime.date.today()
        hetongdate = HetongGL.objects.get(hetongNO = hetongNO).hetongdate
        if fukuanmx_date > today:
            html = u'今天的日期是%s,日期不能大于当天日期！' %str(today)
            raise forms.ValidationError(html)
        if fukuanmx_date < hetongdate:
            html = u'合同签订日期为%s,付款日期应当大于合同签订日期！' %str(hetongdate)
            raise forms.ValidationError(html)
        return fukuanmx_date

    def clean_fukuanmx_fukuanjine(self): #验证输入数量，不能大于付款管理中待付款金额
        hetongNO1 = views.hetongno()
        id = views.id() #读取views中的全局变量，由id（）读出
        yiqianshu = FukuanMX.objects.get(id = id).fukuanmx_fukuanjine  #以前输入的数据
        fukuanmx_fukuanjine = self.cleaned_data['fukuanmx_fukuanjine'] #本次输入的数据
        chae = yiqianshu-fukuanmx_fukuanjine #以前数据与本次数据的差额
        daifukuanjine = FukuanGL.objects.get(fukuangl_hetongNO = hetongNO1).fukuangl_daifukuanjine + chae #需要更新的待付款数据为：已有待付款数据+差额。
        if daifukuanjine <  0: #入差额小于0,则输出数据溢出
            html = u'合同号： 如果本次输入%d，则合同号:%s的付款总额将大于合同总额，请重新输入。'  % (fukuanmx_fukuanjine,hetongNO1)
            raise forms.ValidationError(html)
        return fukuanmx_fukuanjine

class EditChurukuMX(ModelForm):
    class Meta:
        model = ChuRukuMX
        fields = ['churukumx_shuliang','churukumx_date']

    def clean_churukumx_shuliang(self):
        churukumx_shuliang = abs(self.cleaned_data['churukumx_shuliang'])
        id = views.id()
        churukumx = ChuRukuMX.objects.get(id = id)
        yiqianshuju = churukumx.churukumx_shuliang
        churukufangxiang = churukumx.churukufangxiang
        hetongNO = churukumx.hetongNO
        caozuo = views.caozuo()
        if caozuo == 'updata':
            if churukufangxiang == 'IN':
                chae = yiqianshuju - churukumx_shuliang #差额等于以前数-本次输入数
                yiqianrukuzongshu = sum(ChuRukuMX.objects.filter(churukufangxiang='IN',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True)) #已存在的入库总数
                genggaihourukuzongshu = yiqianrukuzongshu -chae #更改后的入库总数
                hetongshu = HetongGL.objects.get(hetongNO=hetongNO).hetongshuliang #合同数量
                yiqianchukuzongshu = abs(sum(ChuRukuMX.objects.filter(churukufangxiang='OUT',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True))) #已存在的出库总数

                if genggaihourukuzongshu >  hetongshu:  #如果更改后的入库数量大于合同数量则溢出
                    html = u'如果填写%d，则超出合同号： %s的合同数量%d，请重新填写。'  % (churukumx_shuliang,hetongNO , hetongshu)
                    raise forms.ValidationError(html)
                if genggaihourukuzongshu < yiqianchukuzongshu: #更改后的入库总数小于已存在的出库总数则溢出
                    html = u'如果填写%d，则会导致合同号：%s的入库总数小于已存在的出库总数%s，请重新填写。' %(churukumx_shuliang,hetongNO,yiqianchukuzongshu)
                    raise forms.ValidationError(html)
            if churukufangxiang == 'OUT':
                churukumx_shuliang = -churukumx_shuliang #将本次输入数转为负数
                chae = yiqianshuju -churukumx_shuliang #差额等于以前数-本次输入数
                yiqianchukuzongshu = sum(ChuRukuMX.objects.filter(churukufangxiang='OUT',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True))#已存在的出库总数
                yiqianrukuzongshu = sum(ChuRukuMX.objects.filter(churukufangxiang='IN',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True)) #已存在的入库总数
                if yiqianchukuzongshu - chae + yiqianrukuzongshu < 0 : #如果已存在的出库总数-差额+已存在的入库总数小于0则溢出
                    html = u'如果填写%d，则会导致合同号：%s的出库总数大于已存在的入库总数%s，请重新填写。' %(churukumx_shuliang,hetongNO,yiqianrukuzongshu)
                    raise forms.ValidationError(html)
        if caozuo == 'del':
            if churukufangxiang == 'IN':
                chae = yiqianshuju #删除时输入数据为0
                yiqianrukuzongshu = sum(ChuRukuMX.objects.filter(churukufangxiang='IN',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True))
                genggaihourukuzongshu = yiqianrukuzongshu -chae
                yiqianchukuzongshu = abs(sum(ChuRukuMX.objects.filter(churukufangxiang='OUT',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True)))

                if genggaihourukuzongshu < yiqianchukuzongshu:
                    html = u'如果填写%d，则会导致合同号：%s的入库总数小于已存在的出库总数%s，请重新填写。' %(churukumx_shuliang,hetongNO,yiqianchukuzongshu)
                    raise forms.ValidationError(html)
            if churukufangxiang == 'OUT':
                chae = yiqianshuju
                yiqianchukuzongshu = sum(ChuRukuMX.objects.filter(churukufangxiang='OUT',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True))
                yiqianrukuzongshu = sum(ChuRukuMX.objects.filter(churukufangxiang='IN',hetongNO=hetongNO).values_list('churukumx_shuliang',flat=True))
                if yiqianchukuzongshu - chae + yiqianrukuzongshu < 0 :
                    html = u'如果填写%d，则会导致合同号：%s的出库总数大于已存在的入库总数%s，请重新填写。' %(churukumx_shuliang,hetongNO,yiqianrukuzongshu)
                    raise forms.ValidationError(html)

        return churukumx_shuliang
    def clean_churukumx_date(self):
        churukumx_date = self.cleaned_data['churukumx_date']
        today = datetime.date.today()
        hetongNO = views.hetongno()
        hetongdate = HetongGL.objects.get(hetongNO = hetongNO).hetongdate
        caozuo = views.caozuo()
        if caozuo == 'updata':

            if churukumx_date > today:
                html = u'今天的日期是%s,日期不能大于当天日期！' %str(today)
                raise forms.ValidationError(html)
            if churukumx_date < hetongdate:
                html = u'合同签订日期为%s,出入库日期应当大于合同签订日期！' %str(hetongdate)
                raise forms.ValidationError(html)
        if caozuo == 'del':
            pass


        return churukumx_date


class Todo(ModelForm):
	class Meta:
		model = TODO
		fields = ['todo_is_complete','todo_content']
		widgets = {
            'todo_content': Textarea(attrs={'cols': 40, 'rows': 5}),
        }

class EditTodo(ModelForm):
	class Meta:
		model = TODO
		fields = ['todo_is_complete','todo_create_date','todo_complete_date','todo_content']
		widgets = {'todo_content': Textarea(attrs={'cols': 40, 'rows': 5}),}

class Yijian(ModelForm):
	class Meta:
		model = yijian
		fields = ['yijian_email','yijian_neirong']
		widgets = {
            'yijian_neirong': Textarea(attrs={'cols': 40, 'rows': 7}),
        }

	def clean_yijian_email(self):
		email = self.cleaned_data['yijian_email'].lower().strip()
		re_email = ur"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
		if email != '':
			if not re.match(re_email,email):
				html = u'%s不是有效邮件地址，请重新填写。'  % (email)
				raise forms.ValidationError(html)
		else:
			pass
		return email
	def clean_yijian_neirong(self):
		neirong = self.cleaned_data['yijian_neirong']
		if len(neirong) < 3:
			html = u'多输入两个字吧。'
			raise forms.ValidationError(html)
		return neirong

class EditYijian(ModelForm):
	class Meta:
		model = yijian
		fields = ['url','yijian_riqi','yijian_email','yijian_neirong']
		widgets = {'yijian_neirong': Textarea(attrs={'cols': 40, 'rows': 7}),}






"""

class EditFukuanMX(ModelForm):
    class Meta:
        model = FukuanMX
        fields = ['fukuanmx_date', 'fukuanmx_fukuanjine' ,'hetongNO']
    def clean_fukuanmx_date(self): #验证日期，不能大于当天日期
        hetongNO = self.cleaned_data['hetongNO']
        fukuanmx_date = self.cleaned_data['fukuanmx_date']
        today = datetime.date.today()
        hetongdate = HetongGL.objects.get(hetongNO = hetongNO).hetongdate
        if fukuanmx_date > today:
            html = u'今天的日期是%s,日期不能大于当天日期！' %str(today)
            raise forms.ValidationError(html)
        if fukuanmx_date < hetongdate:
            html = u'合同签订日期为%s,付款日期应当大于合同签订日期！' %str(hetongdate)
            raise forms.ValidationError(html)
        return fukuanmx_date

    def clean_fukuanmx_fukuanjine(self): #验证输入数量，不能大于付款管理中待付款金额
        hetongNO = self.cleaned_data['hetongNO']
        fukuanmx_fukuanjine = self.cleaned_data['fukuanmx_fukuanjine']
        fukuangl = FukuanGL.objects.get(fukuangl_hetongNO = hetongNO)
        daifukuanjine = fukuangl.fukuangl_daifukuanjine
        if fukuanmx_fukuanjine > daifukuanjine:
            html = u'合同号： %s待付款金额为%d，请重新填写。也可查看“合同列表”。'  % (hetongNO , daifukuanjine)
            raise forms.ValidationError(html)

        return fukuanmx_fukuanjine
"""




"""
def clean_fukuanmx_date(self): #验证日期，不能大于当天日期
        #cleaned_data = super(EditFukuanMX, self).clean()
        hetongNO = self.cleaned_data['hetongNO']
        fukuanmx_date = self.cleaned_data['fukuanmx_date']
        today = datetime.date.today()
        hetongdate = HetongGL.objects.get(hetongNO = hetongNO).hetongdate
        if fukuanmx_date > today:
            html = u'今天的日期是%s,日期不能大于当天日期！' %str(today)
            raise forms.ValidationError(html)
        if fukuanmx_date < hetongdate:
            html = u'合同签订日期为%s,付款日期应当大于合同签订日期！' %str(hetongdate)
            raise forms.ValidationError(html)
        return fukuanmx_date


    def clean_fukuanmx_fukuanjine(self): #验证输入数量，不能大于付款管理中待付款金额
        hetongNO = self.cleaned_data['hetongNO']
        id = self.cleaned_data['id']
        yiqianshu = FukuanMX.objects.get(id = id).fukuanmx_fukuanjine  #以前输入的数据
        fukuanmx_fukuanjine = self.cleaned_data['fukuanmx_fukuanjine'] #本次输入的数据
        chae = yiqianshu-fukuanmx_fukuanjine #以前数据与本次数据的差额
        daifukuanjine = FukuanGL.objects.get(fukuangl_hetongNO = hetongNO).fukuangl_daifukuanjine + chae #需要更新的待付款数据为：已有待付款数据+差额。
        if daifukuanjine <  0: #入差额小于0,则输出数据溢出
            html = u'合同号： 如果本次输入%d，则合同号:%s的付款总额将大于合同总额，请重新输入。'  % (fukuanmx_fukuanjine,hetongNO)
            raise forms.ValidationError(html)
        return fukuanmx_fukuanjine
"""



