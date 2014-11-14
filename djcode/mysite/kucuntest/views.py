# coding=utf-8
from django.shortcuts import render_to_response, get_object_or_404,get_list_or_404
from forms import *
from models import *
from django.views.generic import ListView
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin
from django.contrib.auth import logout
import datetime




# Create your views here.
idglobal = 0  #定义全局变量，以便在form中使用
hetongNOglobal = ''
caozuoglobal = ''
churukufangxiangglobal = ''
yiqianshujuglobal = 0


def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/demo/')

def id():
	return idglobal  #返回全局变量


def hetongno():
	return hetongNOglobal

def caozuo():
	return caozuoglobal

def churukufangxiang():
	return churukufangxiangglobal

def yiqianshuju():
	return yiqianshujuglobal


def demo(request):
	return render_to_response('demo.html', locals(),context_instance=RequestContext(request))

def liuchengtu(request):
	title = u'流程图'
	listleibie = 'liuchengtu'
	return render_to_response('liuchengtu.html',locals() ,context_instance=RequestContext(request))


@login_required
def addpinlei(request):
	title = u'添加品类信息'
	listleibie = 'pl'
	erbuyanzheng = False
	erbuyanzhengneirong = u'提交后如果增加相应合同则无法修改！'
	if request.method == 'POST':
		form = AddPinlei(request.POST)
		if form.is_valid():
			pinleiname = form.cleaned_data['pinleiname']
			p = PinleiGL(pinleiname=pinleiname, isedit=1)
			messages.add_message(request, messages.SUCCESS, '数据添加成功！')
			p.save()
			return HttpResponseRedirect('/pinlei/pinleilist/')
	else:
		form = AddPinlei()
	return render_to_response('add.html', locals(),context_instance=RequestContext(request))

@login_required
def addgongyingshang(request):
	title = u'添加供应商信息'
	listleibie = 'gys'
	erbuyanzheng = False
	erbuyanzhengneirong = u'提交后如果增加相应合同则无法修改供应商名称！'
	if request.method == 'POST':
		form = AddGongyingshang(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			kaihuhang = form.cleaned_data['kaihuhang']
			zhanghao = form.cleaned_data['zhanghao']
			hanghao = form.cleaned_data['hanghao']
			p = GongyingshangGL(name=name, kaihuhang=kaihuhang, zhanghao=zhanghao, hanghao=hanghao, isedit=1)
			p.save()
			messages.add_message(request, messages.SUCCESS, '数据添加成功！')
			return HttpResponseRedirect('/gongyingshang/gongyingshanglist/')
	else:
		form = AddGongyingshang()
	return render_to_response('add.html', locals(),context_instance=RequestContext(request))


@login_required
def addhetong(request):
	title = u'添加合同'
	listleibie='ht'
	erbuyanzheng = False
	erbuyanzhengneirong = u'添加合同信息后，在没有录入相关付款或库存记录的情况下可以进行修改，否则将无法修改。确定提交吗？'

	if request.method == 'POST':

		form = AddHetong(request.POST)

		if form.is_valid():
			hetongNO = form.cleaned_data['hetongNO']
			name = form.cleaned_data['name']
			#name = form_name.get('name')
			pinleiname = form.cleaned_data['pinleiname']
			#pinleiname = form_pinleiname.get('pinleiname')
			#name = form(initial = {'name': GongyingshangGL.name })
			#pinleiname = form(initial = {'pinleiname': PinleiGL.pinleiname })
			gongjia = form.cleaned_data['gongjia']
			hetongshuliang = form.cleaned_data['hetongshuliang']
			#kerukushuliang = form.cleaned_data['kerukushuliang']
			kerukushuliang = hetongshuliang
			hetongdate = form.cleaned_data['hetongdate']
			zongjia = gongjia * hetongshuliang
			isedit = 0

			p = HetongGL(name=name, hetongNO=hetongNO, pinleiname=pinleiname,
			             gongjia=gongjia, hetongshuliang=hetongshuliang, kerukushuliang=kerukushuliang,
			             hetongdate=hetongdate, hetongzongjia=zongjia, isedit=1, daifukuanjine=zongjia)
			p.save()
			#cd = {'hetongNO':hetongNO,'name':name,'pinleiname':pinleiname,'gongjia':gongjia,
			#'hetongshuliang':hetongshuliang,'kerukushuliang':kerukushuliang,'hetongdate':hetongdate,
			#'zongjia':zongjia}
			#return render_to_response('shuchujieguo.html',{'cd':cd})
			q = FukuanGL(fukuangl_name=name, fukuangl_hetongNO=hetongNO, fukuangl_pinlei=pinleiname,
			             fukuangl_hetongzongjia=zongjia, fukuangl_yifukuanjine=0, fukuangl_daifukuanjine=zongjia)
			q.save()

			j = PinleiGL.objects.filter(pinleiname=pinleiname)
			j.update(isedit=isedit)

			k = GongyingshangGL.objects.filter(name=name)
			k.update(isedit=isedit)
			messages.add_message(request, messages.SUCCESS, '数据添加成功！')


			#return render_to_response('caozuochenggong.html')
			return HttpResponseRedirect('/hetong/hetonglist/')

	else:
		form = AddHetong()
	return render_to_response('add.html', locals(),context_instance=RequestContext(request))

@login_required
def addchurukumx(request, hetongno):
	title = u'添加出入库记录'
	listleibie='crk'
	if hetongno == 'null':
		hetongNO = 'null'
	else:
		hetongNO = hetongno
		if not HetongGL.objects.filter(hetongNO=hetongNO).exists():
			return HttpResponseNotFound

	erbuyanzheng = False
	erbuyanzhengneirong = u'录入信息后该合同将无法进行修改，请确认全部信息！提交吗？'
	if request.method == 'POST':
		form = AddChuRukumx(request.POST)

		if form.is_valid():
			churukufangxiang = form.cleaned_data['churukufangxiang']
			hetongNO = form.cleaned_data['hetongNO']
			churukumx_shuliang = form.cleaned_data['churukumx_shuliang']
			churukumx_date = form.cleaned_data['churukumx_date']
			hetong = HetongGL.objects.get(hetongNO=hetongNO)
			churukumx_name = hetong.name
			churukumx_gongjia = hetong.gongjia
			churukumx_pinlei = hetong.pinleiname
			kerukushuliang = hetong.kerukushuliang

			if churukufangxiang == 'IN':
				churukumx_zongjia = churukumx_shuliang * churukumx_gongjia
				#对出入库明细中入库且合同号为指定合同号的所有记录求和，如明细中没有该记录则和为0
				yirukushulinag = sum(ChuRukuMX.objects.filter(churukufangxiang='IN',
				                                              hetongNO=hetongNO).values_list('churukumx_shuliang',
				                                                                             flat=True))
				kerukushuliang = kerukushuliang - churukumx_shuliang  #需要更新的可入库数量为：合同管理中的合同数量-已经入库的数量-本次输入的数量
				j = HetongGL.objects.filter(hetongNO=hetongNO)
				j.update(kerukushuliang=kerukushuliang, isedit=0)

				if not KucunGL.objects.filter(kucungl_hetongbianhao=hetongNO).exists():  #如果合同号在库存管理中不存在

					p = ChuRukuMX(churukufangxiang=churukufangxiang, hetongNO=hetongNO,
					              churukumx_shuliang=churukumx_shuliang,
					              churukumx_date=churukumx_date, churukumx_gongjia=churukumx_gongjia,
					              churukumx_name=churukumx_name, churukumx_pinlei=churukumx_pinlei,
					              churukumx_zongjia=churukumx_zongjia)

					q = KucunGL(kucungl_hetongbianhao=hetongNO, kucungl_gongyingshangname=churukumx_name,
					            kucungl_kucungongjia=churukumx_gongjia, kucungl_kucunshuliang=churukumx_shuliang,
					            kucungl_kucunjine=churukumx_zongjia, kucungl_peileiname=churukumx_pinlei)
					q.save()  #记录存入库存管理
					p.save()  #记录存入出入库明细
				else:  #如果合同编号在库存管理中存在
					kucungl = KucunGL.objects.get(kucungl_hetongbianhao=hetongNO)
					kucunshuliang = kucungl.kucungl_kucunshuliang + churukumx_shuliang

					kucunjine = kucungl.kucungl_kucunjine + churukumx_zongjia
					p = ChuRukuMX(churukufangxiang=churukufangxiang, hetongNO=hetongNO,
					              churukumx_shuliang=churukumx_shuliang,
					              churukumx_date=churukumx_date, churukumx_gongjia=churukumx_gongjia,
					              churukumx_name=churukumx_name, churukumx_pinlei=churukumx_pinlei,
					              churukumx_zongjia=churukumx_zongjia)

					q = KucunGL.objects.filter(kucungl_hetongbianhao=hetongNO)
					p.save()  #记录存入出入库明细
					q.update(kucungl_kucunshuliang=kucunshuliang, kucungl_kucunjine=kucunjine)  #   更新库存管理中库存数量和金额

			elif churukufangxiang == 'OUT':
				churukumx_shuliang = -churukumx_shuliang  #出库数量为负数
				churukumx_zongjia = churukumx_shuliang * churukumx_gongjia
				kucungl = KucunGL.objects.get(kucungl_hetongbianhao=hetongNO)
				kucunshuliang = kucungl.kucungl_kucunshuliang + churukumx_shuliang
				kucunjine = kucungl.kucungl_kucunjine + churukumx_zongjia

				p = ChuRukuMX(churukufangxiang=churukufangxiang, hetongNO=hetongNO,
				              churukumx_shuliang=churukumx_shuliang,
				              churukumx_date=churukumx_date, churukumx_gongjia=churukumx_gongjia,
				              churukumx_name=churukumx_name, churukumx_pinlei=churukumx_pinlei,
				              churukumx_zongjia=churukumx_zongjia)
				p.save()
				q = KucunGL.objects.filter(kucungl_hetongbianhao=hetongNO)
				q.update(kucungl_kucunshuliang=kucunshuliang, kucungl_kucunjine=kucunjine)
			messages.add_message(request, messages.SUCCESS, '数据添加成功！')
			return HttpResponseRedirect('/kucun/kucunlist/')
			#return render_to_response('shuchujieguo.html',{'cd':cd})
	else:
		form = AddChuRukumx()
		if hetongNO != 'null':
			form.fields['hetongNO'].queryset = HetongGL.objects.filter(hetongNO=hetongNO)  #指定外键下拉框选择范围，可以使用查询条件
			#form.fields['churukufangxiang'] = forms.ChoiceField(choices=[('IN','入库')]) #指定一个列表
			#forms.ChoiceField(choices=[ (o.id, str(o)) for o in Waypoint.objects.all()])#可以生成一个动态的下拉列表

	return render_to_response('add.html', locals(),context_instance=RequestContext(request))

@login_required
def editgongyingshang(request, id):
	id = int(id)
	listleibie='gys'
	editgongyingshang = get_object_or_404(GongyingshangGL, id=id)
	isedit = editgongyingshang.isedit
	nameorNO = editgongyingshang.name
	fangfatishi = u'如果该供应商存在相应合同信息，则无法修改名称。'
	fangfatishidis = False
	title = u'编辑供应商信息'
	erbuyanzheng = True
	erbuyanzhengneirong = u'确认提交吗？'
	if isedit == 1:
		isdel = True
	else:
		isdel = False
	if request.method == 'POST':
		form = EditGongyingshang(instance=editgongyingshang, data=request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, '数据更新成功！')
			#return HttpResponseRedirect('/caozuochenggong/1')
			#return HttpResponseRedirect(chongdingxiang)
			return HttpResponseRedirect('/gongyingshang/gongyingshanglist/')


	else:
		form = EditGongyingshang(instance=editgongyingshang)
	return render_to_response('edit.html',locals(),context_instance=RequestContext(request))

@login_required
def editgongyingshangname(request, id):
	id = int(id)
	editgongyingshang = get_object_or_404(GongyingshangGL, id=id)
	isedit = editgongyingshang.isedit
	nameorNO = editgongyingshang.name
	listleibie='gys'
	fangfatishi = u'如果需要更改供应商名称或者删除供应商，需要在“合同管理”中删除该供应商下所有合同内容。'
	fangfatishidis = False
	title = u'编辑供应商信息'
	erbuyanzheng = False
	erbuyanzhengneirong = u'确认提交吗？'
	chongdingxiang = "/gongyingshang/editgongyingshang/" + str(id)
	if isedit == 1:
		isdel = True
	else:
		return HttpResponseRedirect(chongdingxiang)
	if request.method == 'POST':
		form = EditGongyingshangname(instance=editgongyingshang, data=request.POST)
		if request.POST.has_key("updata"):
			if form.is_valid():
				form.save()

				messages.add_message(request, messages.SUCCESS, '数据更新成功！')
				return HttpResponseRedirect('/gongyingshang/gongyingshanglist/')
		if request.POST.has_key("del"):
			#if form.is_valid(): #删除时只是需要在表单中显示相关数据，但不需要进行数据验证。
			q = GongyingshangGL.objects.filter(id = id)
			q.delete()
			messages.add_message(request, messages.SUCCESS, '数据删除成功！')
			return HttpResponseRedirect('/gongyingshang/gongyingshanglist')

	else:
		form = EditGongyingshangname(instance=editgongyingshang)
	return render_to_response('edit.html',locals(),context_instance=RequestContext(request))

@login_required
def editpinlei(request, id):
	id = int(id)
	editpinlei = get_object_or_404(PinleiGL, id=id)
	isedit = editpinlei.isedit
	nameorNO = editpinlei.pinleiname
	listleibie='pl'
	fangfatishi = u'如果该品类用以生成合同，则该品类无法被修改或删除，即使删除合同信息后亦无法更改或删除该品类信息，请小心录入！'
	fangfatishidis = True
	title = u'编辑品类信息'
	erbuyanzheng = True
	erbuyanzhengneirong = u'确认提交吗？'
	chongdingxiang = "/pinlei/pinleilist/"
	if isedit == 1:
		isdel = True
	else:
		return HttpResponseRedirect(chongdingxiang)
	if request.method == 'POST':
		form = EditPinlei(instance=editpinlei, data=request.POST)
		if request.POST.has_key("updata"):
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, '数据更新成功！')
				return HttpResponseRedirect('/pinlei/pinleilist/')
		if request.POST.has_key("del"):  #if form.is_valid(): #删除时只是需要在表单中显示相关数据，不需要进行数据验证。
			q = PinleiGL.objects.filter(id=id)
			q.delete()
			messages.add_message(request, messages.SUCCESS, '数据删除成功！')
			return HttpResponseRedirect('/pinlei/pinleilist/')
	else:
		form = EditPinlei(instance=editpinlei)
	return render_to_response('edit.html',locals(),context_instance=RequestContext(request))

@login_required
def editfukuanmx(request, id):
	global idglobal  #引入全局变量
	global hetongNOglobal
	id = int(id)
	idglobal = id  #更改全局变量
	editfukuanmx = get_object_or_404(FukuanMX, id=id)
	listleibie='fkmx'
	hetongNO = editfukuanmx.hetongNO
	hetongNOglobal = hetongNO
	yiqianshu = editfukuanmx.fukuanmx_fukuanjine
	fangfatishi = u'如果该品类用以生成合同，则该品类无法被修改或删除，即使删除合同信息后亦无法更改或删除该品类信息，请小心录入！'
	fukuangl = FukuanGL.objects.get(fukuangl_hetongNO=hetongNO)
	daifukuan = fukuangl.fukuangl_daifukuanjine
	yifukuan = fukuangl.fukuangl_yifukuanjine
	fangfatishidis = False
	title = u'编辑付款信息'
	erbuyanzheng = False  #是否在提交数据时弹出对话框
	erbuyanzhengneirong = u'确认提交吗？'
	isdel = True

	if request.method == 'POST':
		form = EditFukuanMX(instance=editfukuanmx, data=request.POST)
		if request.POST.has_key("updata"):
			if form.is_valid():
				fukuanmx_fukuanjine = form.cleaned_data['fukuanmx_fukuanjine']  #本次输入的数据
				chae = yiqianshu - fukuanmx_fukuanjine
				daifukuan = daifukuan + chae
				yifukuan = yifukuan - chae
				j = HetongGL.objects.filter(hetongNO=hetongNO)
				j.update(daifukuanjine=daifukuan)
				q = FukuanGL.objects.filter(fukuangl_hetongNO=hetongNO)
				q.update(fukuangl_daifukuanjine=daifukuan, fukuangl_yifukuanjine=yifukuan)
				form.save()
				messages.add_message(request, messages.SUCCESS, '数据更新成功！')
				return HttpResponseRedirect('/fukuan/fukuangllist/')
		if request.POST.has_key("del"):  #if form.is_valid(): #删除时只是需要在表单中显示相关数据，不需要进行数据验证。
			chae = editfukuanmx.fukuanmx_fukuanjine
			daifukuan = daifukuan + chae
			yifukuan = yifukuan - chae
			k = HetongGL.objects.filter(hetongNO=hetongNO)
			k.update(daifukuanjine=daifukuan)
			j = FukuanGL.objects.filter(fukuangl_hetongNO=hetongNO)
			j.update(fukuangl_daifukuanjine=daifukuan, fukuangl_yifukuanjine=yifukuan)
			q = FukuanMX.objects.filter(id=id)
			q.delete()
			messages.add_message(request, messages.SUCCESS, '数据删除成功！')
			return HttpResponseRedirect('/fukuan/fukuangllist/')

	else:
		form = EditFukuanMX(instance=editfukuanmx)
	return render_to_response('edit.html',locals(),context_instance=RequestContext(request))


class pinleilist(LoginRequiredMixin,ListView):
	model = PinleiGL
	template_name = 'list.html'
	context_object_name = 'pinleilist'



	def get_context_data(self,**kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
		context = super(pinleilist, self).get_context_data(**kwargs)
		#context = self.dispatch(self,**kwargs)
		context['listleibie'] = 'pl'
		context['title'] = u'品类管理'  #不能同时添加多个模板变量，需要一行一行添加
		context['request'] = self.request #附加request的信息，为模板提供变量值
		return context




class gongyingshanglist(LoginRequiredMixin,ListView):
	model = GongyingshangGL
	template_name = 'list.html'
	#效果好像是指定返回的值在模板中的变量名称
	context_object_name = 'gongyingshanglist'

	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
		context = super(gongyingshanglist, self).get_context_data(**kwargs)
		context['listleibie'] = 'gys'
		context['title'] = u'供应商管理'  #不能同时添加多个模板变量，需要一行一行添加
		context['request'] = self.request
		return context


class hetonglist(LoginRequiredMixin,ListView):
	model = HetongGL
	template_name = 'list.html'
	context_object_name = 'hetonglist'

	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
		context = super(hetonglist, self).get_context_data(**kwargs)
		context['listleibie'] = 'ht'
		context['title'] = u'合同管理'  #不能同时添加多个模板变量，需要一行一行添加
		context['request'] = self.request
		return context


class kucunlist(LoginRequiredMixin,ListView):
	model = KucunGL
	template_name = 'list.html'
	context_object_name = 'kucunlist'

	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
		context = super(kucunlist, self).get_context_data(**kwargs)
		context['listleibie'] = 'kc'
		context['title'] = u'库存管理'  #不能同时添加多个模板变量，需要一行一行添加
		context['request'] = self.request
		return context


class churukulist(LoginRequiredMixin,ListView):
	model = ChuRukuMX
	template_name = 'list.html'

	def get_queryset(self): #取得url中额外参数

		self.hetongNO = self.kwargs['hetongno'] #对应url配置中的关键字配置名称
		if self.hetongNO != 'null':

			self.churukulist = get_list_or_404(ChuRukuMX, hetongNO= self.hetongNO) #获得一个列表显示多个结果，get_object_or_404获得单个结果
			return ChuRukuMX.objects.filter(hetongNO =self.churukulist)
		else:
			self.churukulist = get_list_or_404(ChuRukuMX)
			return ChuRukuMX.objects.all()

	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
		context = super(churukulist, self).get_context_data(**kwargs)
		context['churukulist'] = self.churukulist #将变量名添加到输出结果中
		context['chukuzongshu'] = abs(sum(ChuRukuMX.objects.filter(hetongNO = self.hetongNO ,churukufangxiang='OUT').values_list('churukumx_shuliang',flat=True)))
		context['rukuzongshu'] = sum(ChuRukuMX.objects.filter(hetongNO = self.hetongNO ,churukufangxiang='IN').values_list('churukumx_shuliang',flat=True))
		context['listleibie'] = 'crk'
		context['title'] = u'出入库明细表'  #不能同时添加多个模板变量，需要一行一行添加
		context['request'] = self.request
		return context


class fukuangllist(LoginRequiredMixin,ListView):
	model = FukuanGL
	template_name = 'list.html'
	context_object_name = 'fukuangllist'

	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
		context = super(fukuangllist, self).get_context_data(**kwargs)
		context['listleibie'] = 'fkl'
		context['title'] = u'付款管理列表'  #不能同时添加多个模板变量，需要一行一行添加
		context['request'] = self.request
		return context


class fukuanmxlist(LoginRequiredMixin,ListView): #不能添加额外参数
	model = FukuanMX
	template_name = 'list.html'

	#context_object_name = 'fukuanmxlist'
	def get_queryset(self): #取得url中额外参数

		self.hetongNO = self.kwargs['hetongno'] #对应url配置中的关键字配置名称
		if self.hetongNO != 'null':

			self.fukuanmxlist = get_list_or_404(FukuanMX, hetongNO= self.hetongNO) #获得一个列表显示多个结果，get_object_or_404获得单个结果
			return FukuanMX.objects.filter(hetongNO =self.fukuanmxlist)
		else:
			self.fukuanmxlist = get_list_or_404(FukuanMX)
			return FukuanMX.objects.all()
		#return FukuanMX.objects.filter(hetongNO =self.fukuanmxlist) #详细见https://docs.djangoproject.com/en/1.6/topics/class-based-views/generic-display/#dynamic-filtering
	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
		context = super(fukuanmxlist, self).get_context_data(**kwargs)
		context['fukuanmxlist'] = self.fukuanmxlist #将变量名添加到输出结果中
		context['listleibie'] = 'fkmx'
		context['title'] = u'付款明细列表'  #不能同时添加多个模板变量，需要一行一行添加
		context['request'] = self.request
		return context

@login_required
def edithetong(request, hetongno):
	edithetong = get_object_or_404(HetongGL, hetongNO=hetongno)
	hetongNO = hetongno
	isedit = edithetong.isedit
	nameorNO = edithetong.hetongNO
	listleibie='ht'
	fangfatishi = u'如果该合同已经存在出/入库操作或付款操作，则无法再被编辑，请小心操作！'
	fangfatishidis = True
	title = u'编辑合同信息'
	erbuyanzheng = True
	erbuyanzhengneirong = u'确认提交吗？'
	chongdingxiang = "/hetong/hetonglist/"

	if isedit == 1:
		isdel = True
	else:
		return HttpResponseRedirect(chongdingxiang)

	if request.method == 'POST':

		form = EditHetong(instance=edithetong, data=request.POST)
		if request.POST.has_key("updata"):
			if form.is_valid():
				name = form.cleaned_data['name']
				gongjia = form.cleaned_data['gongjia']
				pinleiname = form.cleaned_data['pinleiname']
				hetongdate = form.cleaned_data['hetongdate']
				hetongshuliang = form.cleaned_data['hetongshuliang']
				kerukushuliang = hetongshuliang
				zongjia = gongjia * hetongshuliang

				p = HetongGL.objects.filter(hetongNO=hetongNO)
				p.update(name=name, gongjia=gongjia, hetongshuliang=hetongshuliang,
				         hetongdate=hetongdate, hetongzongjia=zongjia,
				         kerukushuliang=kerukushuliang, pinleiname=pinleiname,daifukuanjine=zongjia)

				q = FukuanGL.objects.filter(fukuangl_hetongNO=hetongNO)

				q.update(fukuangl_name=name, fukuangl_pinlei=pinleiname, fukuangl_hetongzongjia=zongjia,
				         fukuangl_daifukuanjine=zongjia)
				messages.add_message(request, messages.SUCCESS, '数据更新成功！')
				return HttpResponseRedirect('/hetong/hetonglist/')

		if request.POST.has_key("del"):
			#if form.is_valid(): #删除时只是需要在表单中显示相关数据，但不需要进行数据验证。
			j = FukuanGL.objects.filter(fukuangl_hetongNO = hetongNO)
			j.delete()
			q = HetongGL.objects.filter(hetongNO=hetongNO)
			q.delete()
			messages.add_message(request, messages.SUCCESS, '数据删除成功！')
			return HttpResponseRedirect('/hetong/hetonglist/')

	else:
		form = EditHetong(instance=edithetong)
	return render_to_response('edit.html',locals(),context_instance=RequestContext(request))



@login_required
def editchuruku(request,id):
	global idglobal
	global churukufangxiangglobal
	global hetongNOglobal
	global yiqianshujuglobal
	title = u'添加出入库记录'
	isdel = True
	id = int(id)
	idglobal = id
	churukumx = get_object_or_404(ChuRukuMX,id = id)
	listleibie='crk'
	yiqianshuju = churukumx.churukumx_shuliang
	yiqianshujuglobal = yiqianshuju
	churukufangxiang = churukumx.churukufangxiang
	churukufangxiangglobal = churukufangxiang
	hetongNO = churukumx.hetongNO
	hetongNOglobal = hetongNO

	if request.method == 'POST':
		form = EditChurukuMX(instance=churukumx, data=request.POST)
		if request.POST.has_key("updata"):
			global caozuoglobal
			caozuoglobal = 'updata'
			if form.is_valid():
				if churukufangxiang == 'IN':
					shuliang = form.cleaned_data['churukumx_shuliang']
					date = form.cleaned_data['churukumx_date']
					kucungl = KucunGL.objects.get(kucungl_hetongbianhao = hetongNO)
					kucunshuliang = kucungl.kucungl_kucunshuliang
					gongjia = kucungl.kucungl_kucungongjia
					chae = yiqianshuju - shuliang
					kucunshuliang = kucunshuliang-chae
					kucunjine = kucunshuliang * gongjia
					kerukushuliang = HetongGL.objects.get(hetongNO=hetongNO).kerukushuliang + chae
					q = KucunGL.objects.filter(kucungl_hetongbianhao = hetongNO)
					q.update(kucungl_kucunshuliang = kucunshuliang,kucungl_kucunjine=kucunjine)
					j = HetongGL.objects.filter(hetongNO=hetongNO)
					j.update(kerukushuliang=kerukushuliang)
					k = ChuRukuMX.objects.filter(id=id)
					k.update(churukumx_shuliang = shuliang,churukumx_date=date)
					messages.add_message(request, messages.SUCCESS, '数据更新成功！')
					return HttpResponseRedirect('/kucun/kucunlist/')
				if churukufangxiang == 'OUT':
					shuliang = form.cleaned_data['churukumx_shuliang']
					shuliang = -shuliang
					date = form.cleaned_data['churukumx_date']
					kucungl = KucunGL.objects.get(kucungl_hetongbianhao = hetongNO)
					kucunshuliang = kucungl.kucungl_kucunshuliang
					gongjia = kucungl.kucungl_kucungongjia
					chae = yiqianshuju - shuliang
					kucunshuliang = kucunshuliang-chae
					kucunjine = kucunshuliang * gongjia
					q = KucunGL.objects.filter(kucungl_hetongbianhao = hetongNO)
					q.update(kucungl_kucunshuliang = kucunshuliang,kucungl_kucunjine=kucunjine)
					k = ChuRukuMX.objects.filter(id=id)
					k.update(churukumx_shuliang = shuliang,churukumx_date=date)
					messages.add_message(request, messages.SUCCESS, '数据更新成功！')
					return HttpResponseRedirect('/kucun/kucunlist/')
		if request.POST.has_key("del"):
			caozuoglobal = 'del'
			if form.is_valid():
				if churukufangxiang == 'IN':
					shuliang = 0
					kucungl = KucunGL.objects.get(kucungl_hetongbianhao = hetongNO)
					kucunshuliang = kucungl.kucungl_kucunshuliang
					gongjia = kucungl.kucungl_kucungongjia
					chae = yiqianshuju - shuliang
					kucunshuliang = kucunshuliang-chae
					kucunjine = kucunshuliang * gongjia
					kerukushuliang = HetongGL.objects.get(hetongNO=hetongNO).kerukushuliang + chae
					q = KucunGL.objects.filter(kucungl_hetongbianhao = hetongNO)
					q.update(kucungl_kucunshuliang = kucunshuliang,kucungl_kucunjine=kucunjine)
					j = HetongGL.objects.filter(hetongNO=hetongNO)
					j.update(kerukushuliang=kerukushuliang)
					k = ChuRukuMX.objects.filter(id=id)
					k.delete()
					messages.add_message(request, messages.SUCCESS, '数据删除成功！')
					return HttpResponseRedirect('/kucun/kucunlist/')
				if churukufangxiang == 'OUT':
					shuliang = 0
					shuliang = -shuliang
					kucungl = KucunGL.objects.get(kucungl_hetongbianhao = hetongNO)
					kucunshuliang = kucungl.kucungl_kucunshuliang
					gongjia = kucungl.kucungl_kucungongjia
					chae = yiqianshuju - shuliang
					kucunshuliang = kucunshuliang-chae
					kucunjine = kucunshuliang * gongjia
					q = KucunGL.objects.filter(kucungl_hetongbianhao = hetongNO)
					q.update(kucungl_kucunshuliang = kucunshuliang,kucungl_kucunjine=kucunjine)
					k = ChuRukuMX.objects.filter(id=id)
					k.delete()
					messages.add_message(request, messages.SUCCESS, '数据删除成功！')
					return HttpResponseRedirect('/kucun/kucunlist/')
	else:
		form = EditChurukuMX(instance=churukumx)
	return render_to_response('edit.html', locals(),context_instance=RequestContext(request))


@login_required
def addfukuanmx(request, hetongno):
	title = u'添加付款记录'
	listleibie='fkmx'
	if hetongno == 'null':
		hetongNO = 'null'
	else:
		hetongNO = hetongno
		if not HetongGL.objects.filter(hetongNO=hetongNO).exists():
			return HttpResponseNotFound
	erbuyanzheng = False
	erbuyanzhengneirong = u'录入信息后该合同将无法进行修改，请确认全部信息！提交吗？'
	if request.method == 'POST':

		form = AddFukuanMX(request.POST)

		if form.is_valid():
			hetongNO = form.cleaned_data['hetongNO']
			fukuanmx = HetongGL.objects.get(hetongNO=hetongNO)
			name = fukuanmx.name
			pinlei = fukuanmx.pinleiname

			fukuanjine = form.cleaned_data['fukuanmx_fukuanjine']
			fukuandate = form.cleaned_data['fukuanmx_date']
			fukuangl = FukuanGL.objects.get(fukuangl_hetongNO=hetongNO)
			yifukuanjine = fukuangl.fukuangl_yifukuanjine + fukuanjine
			daifukuanjine = fukuangl.fukuangl_daifukuanjine - fukuanjine
			p = FukuanMX(fukuanmx_name=name, hetongNO=hetongNO, fukuanmx_date=fukuandate, fukuanmx_pinlei=pinlei,
			             fukuanmx_fukuanjine=fukuanjine)
			p.save()

			q = FukuanGL.objects.filter(fukuangl_hetongNO=hetongNO)
			q.update(fukuangl_yifukuanjine=yifukuanjine, fukuangl_daifukuanjine=daifukuanjine)
			j = HetongGL.objects.filter(hetongNO=hetongNO)
			j.update(isedit=0)
			k = HetongGL.objects.filter(hetongNO=hetongNO)
			k.update(daifukuanjine=daifukuanjine)

			messages.add_message(request, messages.SUCCESS, '数据添加成功！')
			#return render_to_response('caozuochenggong.html')
			return HttpResponseRedirect('/fukuan/fukuangllist/')

	else:
		form = AddFukuanMX()
		if hetongNO != 'null':
			form.fields['hetongNO'].queryset = HetongGL.objects.filter(hetongNO=hetongNO)  #指定外键下拉框选择范围，可以使用查询条件
	return render_to_response('add.html',locals(),context_instance=RequestContext(request))

@login_required
def TodoCreate(request): #不能添加额外参数
	title = u'添加TODO'
	if not request.user.username == 'admin':
		messages.add_message(request, messages.WARNING, '这个模块只能由Admin使用,请重新登录！')
		return HttpResponseRedirect('/accounts/login/')
	if request.method == 'POST':

		form = Todo(request.POST)

		if form.is_valid():
			complete = form.cleaned_data['todo_is_complete']
			content = form.cleaned_data['todo_content']
			create_date = datetime.date.today()
			complete_date = datetime.date.today()

			p = TODO(todo_is_complete=complete, todo_content=content, todo_create_date=create_date,todo_complete_date=complete_date)
			p.save()



			messages.add_message(request, messages.SUCCESS, '数据添加成功！')
			#return render_to_response('caozuochenggong.html')
			return HttpResponseRedirect('/todo/todolist/')

	else:
		form = Todo()
	return render_to_response('add.html',locals(),context_instance=RequestContext(request))


class TodoList(LoginRequiredMixin,ListView): #不能添加额外参数
	model = TODO
	template_name = 'list.html'
	context_object_name = 'todolist'
	"""
	def get(self, request,**kwargs): #判断用户名，这里似乎只能使用get函数名称
		if self.request.user.username != 'admin':
			messages.add_message(request, messages.WARNING, '这个模块只能由Admin使用，请重新登录！')
			return HttpResponseRedirect('/accounts/login/')
		else:
			return super(TodoList, self).get_context_data(**kwargs)
	"""
	def dispatch(self, request, *args, **kwargs): #判断用户名
		if not self.request.user.username == 'admin':
			messages.add_message(request, messages.WARNING, '这个模块只能由Admin使用，请重新登录！')
			return HttpResponseRedirect('/accounts/login/')
		else:
			return super(TodoList, self).dispatch(request, *args, **kwargs)




	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
			context = super(TodoList, self).get_context_data(**kwargs)
			#context['todolist'] = self.todolist #将变量名添加到输出结果中
			context['listleibie'] = 'todo'
			context['title'] = u'ToduList'  #不能同时添加多个模板变量，需要一行一行添加
			context['request'] = self.request
			return context


@login_required
def edittodo(request, id):
	id = int(id)
	edittodo = get_object_or_404(TODO, id=id)
	listleibie='todo'
	title = u'edittodo'
	isdel = True

	if not request.user.username == 'admin':
		messages.add_message(request, messages.WARNING, '这个模块只能由Admin使用,请重新登录！')
		return HttpResponseRedirect('/accounts/login/')
	if request.method == 'POST':
		form = EditTodo(instance=edittodo, data=request.POST)
		if request.POST.has_key("updata"):
			if form.is_valid():
				todo_is_complete = form.cleaned_data['todo_is_complete']
				if todo_is_complete == True:
					todo_complete_date = datetime.date.today()
					todo_content = form.cleaned_data['todo_content']
					q = TODO.objects.filter(id = id)
					q.update(todo_is_complete = todo_is_complete,todo_complete_date = todo_complete_date,todo_content = todo_content)
					messages.add_message(request, messages.SUCCESS,'数据更新成功！')
				else:
					form.save()
					messages.add_message(request, messages.SUCCESS, '数据更新成功！')
				return HttpResponseRedirect('/todo/todolist/')
		if request.POST.has_key("del"):  #if form.is_valid(): #删除时只是需要在表单中显示相关数据，不需要进行数据验证。
			q = TODO.objects.filter(id=id)
			q.delete()
			messages.add_message(request, messages.SUCCESS, '数据删除成功！')
			return HttpResponseRedirect('/todo/todolist')
	else:
		form = EditTodo(instance=edittodo)
	return render_to_response('edit.html',locals(),context_instance=RequestContext(request))


def YijianCreate(request,url):
	url = url
	title = u'留言板'
	listleibie='yijian'
	if request.method == 'POST':

		form = Yijian(request.POST)

		if form.is_valid():
			yijian_email_raw = form.cleaned_data['yijian_email']
			if not yijian_email_raw != '':
				yijian_email = yijian_email_raw
			else:
				yijian_email = None
			yijian_neirong = form.cleaned_data['yijian_neirong']
			yijian_riqi = datetime.date.today()
			p = yijian(url = url,yijian_email=yijian_email,yijian_riqi=yijian_riqi,yijian_neirong=yijian_neirong)
			p.save()
			messages.add_message(request, messages.SUCCESS, '留言成功，谢谢！')
			return HttpResponseRedirect(url)

	else:
		form = Yijian()
	return render_to_response('add.html',locals(),context_instance=RequestContext(request))


@login_required
def edityijian(request, id):
	id = int(id)
	edityijian = get_object_or_404(yijian, id=id)
	listleibie='yijian'
	title = u'edityijian'
	isdel = True

	if not request.user.username == 'admin':
		messages.add_message(request, messages.WARNING, '这个模块只能由Admin使用,请重新登录！')
		return HttpResponseRedirect('/accounts/login/')
	if request.method == 'POST':
		form = EditYijian(instance=edityijian, data=request.POST)
		if request.POST.has_key("updata"):
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, '数据更新成功！')
				return HttpResponseRedirect('/yijian/yijianlist/')
		if request.POST.has_key("del"):  #if form.is_valid(): #删除时只是需要在表单中显示相关数据，不需要进行数据验证。
			q = yijian.objects.filter(id=id)
			q.delete()
			messages.add_message(request, messages.SUCCESS, '数据删除成功！')
			return HttpResponseRedirect('/yijian/yijianlist')
	else:
		form = EditYijian(instance=edityijian)
	return render_to_response('edit.html',locals(),context_instance=RequestContext(request))


class yijianlist(LoginRequiredMixin,ListView): #不能添加额外参数
	model = yijian
	template_name = 'list.html'
	context_object_name = 'yijianlist'

	def dispatch(self, request, *args, **kwargs): #判断用户名
		if not self.request.user.username == 'admin':
			messages.add_message(request, messages.WARNING, '这个模块只能由Admin使用，请重新登录！')
			return HttpResponseRedirect('/accounts/login/')
		else:
			return super(yijianlist, self).dispatch(request, *args, **kwargs)
	def get_context_data(self, **kwargs):  #向输出到模板的内容中添加其他模板变量，可用作在模板中临时添加另一列内容（使用queset）而无需更改数据库
			context = super(yijianlist, self).get_context_data(**kwargs)
			#context['todolist'] = self.todolist #将变量名添加到输出结果中
			context['listleibie'] = 'yijian'
			context['title'] = u'yijianlist'  #不能同时添加多个模板变量，需要一行一行添加
			context['request'] = self.request
			return context

