# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.

class GongyingshangGL (models.Model):
    name = models.CharField(max_length=30 , unique=True ,verbose_name=u'供应商名称')
    kaihuhang = models.CharField(max_length=30 , verbose_name=u'开户行')
    zhanghao = models.CharField(max_length=50 , verbose_name=u'帐号')
    hanghao = models.CharField(max_length=30 , verbose_name=u'行号')
    isedit = models.IntegerField(verbose_name=u'是否可更改')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PinleiGL(models.Model):
    pinleiname = models.CharField(max_length=30,verbose_name=u'品类名称')
    isedit = models.IntegerField(verbose_name=u'是否可更改')
    def __unicode__(self):
        return self.pinleiname


class HetongGL(models.Model):


    hetongNO = models.CharField(max_length=30,primary_key=True)
    name = models.ForeignKey(GongyingshangGL,verbose_name=u'供应商名称')
    pinleiname = models.ForeignKey(PinleiGL,verbose_name=u'品类名称')
    gongjia =  models.FloatField(verbose_name=u'供价')
    hetongshuliang = models.IntegerField(verbose_name=u'数量')
    hetongzongjia = models.FloatField(verbose_name=u'总价')
    kerukushuliang = models.IntegerField(verbose_name=u'可入库数量')
    hetongdate = models.DateField(verbose_name=u'签订日期')
    isedit = models.IntegerField(verbose_name=u'是否可更改')
    daifukuanjine = models.FloatField(blank=True,null=True,verbose_name=u'待付款金额')
    #hetongid = models.AutoField(primary_key=True)


    def __unicode__(self):
        return unicode(self.hetongNO)


class FukuanMX(models.Model):
    fukuanmx_date = models.DateField(verbose_name=u'付款日期')
    fukuanmx_name = models.CharField(max_length=30 ,verbose_name=u'供应商名称')
    fukuanmx_pinlei = models.CharField(max_length=30,verbose_name=u'品类')
    hetongNO = models.ForeignKey(HetongGL,verbose_name=u'合同编号')
    fukuanmx_fukuanjine = models.FloatField(verbose_name=u'付款金额')

    def __unicode__(self):
        return unicode(self.hetongNO)
    class Meta:
        ordering = ['fukuanmx_date']

class FukuanGL(models.Model):
    fukuangl_name = models.ForeignKey(GongyingshangGL,verbose_name=u'供应商名称')
    fukuangl_hetongNO = models.CharField(max_length=30,verbose_name=u'合同编号')
    fukuangl_pinlei = models.ForeignKey(PinleiGL,verbose_name=u'品类' )
    fukuangl_hetongzongjia = models.FloatField(verbose_name=u'合同总价')
    fukuangl_yifukuanjine = models.FloatField(blank=True,null=True,verbose_name=u'已付款金额')
    fukuangl_daifukuanjine = models.FloatField(blank=True,null=True,verbose_name=u'待付款金额')

    def __unicode__(self):
        return unicode(self.fukuangl_hetongNO)




class ChuRukuMX(models.Model):
    churukufangxiang_CHOICES = (('IN','入库'),('OUT','出库'))
    churukufangxiang = models.CharField(choices=churukufangxiang_CHOICES, max_length=10 , verbose_name = u'出/入库')
    churukumx_date = models.DateField(verbose_name=u'出/入库日期')
    churukumx_name = models.CharField(max_length=30 ,verbose_name=u'供应商名称')
    hetongNO = models.ForeignKey(HetongGL,verbose_name=u'合同编号')
    churukumx_gongjia = models.FloatField(verbose_name=u'供价')
    churukumx_pinlei = models.CharField(max_length=30 ,verbose_name=u'品类')
    churukumx_shuliang = models.IntegerField(verbose_name=u'出/入库数量')
    churukumx_zongjia = models.FloatField(verbose_name=u'出/入库总价')

    def __unicode__(self):
        return unicode(self.hetongNO)
    class Meta:
        ordering = ['churukumx_date']


class ChukuMX(models.Model):
    chukumx_date = models.DateField(verbose_name=u'日期')
    #chukumx_name = models.ForeignKey(HetongGL,to_field='name')
    hetongNO = models.ForeignKey(HetongGL,verbose_name=u'合同号')
    #chukumx_gongjia = models.ForeignKey(HetongGL, to_field='gongjia')
    chukumx_shuliang = models.IntegerField()
    chukumx_zongjia = models.FloatField()

    def __unicode__(self):
        return self.chukumx_hetongNO


class KucunGL(models.Model):
    kucungl_gongyingshangname = models.CharField(max_length=30,verbose_name=u'供应商名称')
    kucungl_hetongbianhao = models.CharField(max_length=30,verbose_name=u'合同号')
    kucungl_kucungongjia = models.FloatField(verbose_name=u'供价')
    kucungl_kucunshuliang = models.IntegerField(blank=True,null=True,verbose_name=u'库存数量')
    kucungl_kucunjine = models.FloatField(verbose_name=u'库存金额')
    kucungl_peileiname = models.CharField(max_length=30,verbose_name=u'品类')


    def __unicode__(self):
        return self.kucungl_gongyingshangname

    class Meta:
        ordering = ['kucungl_gongyingshangname']


class TODO(models.Model):
	todo_is_complete = models.BooleanField(verbose_name=u'是否完成')
	todo_create_date = models.DateField(verbose_name=u'创建日期')
	todo_complete_date = models.DateField(blank=True,null=True,verbose_name=u'完成日期')
	todo_content=models.CharField(max_length=300,verbose_name=u'内容')



	class Meta:
		ordering = ['todo_create_date']


















