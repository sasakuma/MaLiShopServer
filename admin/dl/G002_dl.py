# -*- coding: utf-8 -*-

##############################################################################
#
#
#
##############################################################################

from imp import reload
import basic
reload(basic)
from basic import public
DEBUG,CLIENT_NAME=public.DEBUG,public.CLIENT_NAME

if DEBUG == '1':    
    import admin.dl.BASE_DL
    reload(admin.dl.BASE_DL)
from admin.dl.BASE_DL  import cBASE_DL


import hashlib , os , time , random

class cG002_dl(cBASE_DL):
    def init_data(self):

        self.GNL = [0,1,2,3,4,5,6]


    #在子类中重新定义         
    def myInit(self):
        self.src = 'G002'
        self.pk=self.usr_id
        pass

    def mRight(self):
            
        sql = u"""
            select usr_id
                ,access_key
                ,secret_key
                ,name
                ,domain
            from qiniu 
            
            where COALESCE(del_flag,0)=0 and usr_id=%s
        """
        L=self.db.fetch(sql,self.usr_id)
        return L

        
        #L,iTotal_length,iTotal_Page,pageNo,select_size=self.db.select_for_grid(sql,self.pageNo)
        #PL=[pageNo,iTotal_Page,iTotal_length,select_size]
        #return PL,L

    def get_local_data(self ):
        """获取 local 表单的数据
        """
        L = {}
        sql = """
            select usr_id
                ,access_key
                ,secret_key
                ,name
                ,domain
            from qiniu  where usr_id=%s

        """

        L = self.db.fetch( sql , self.usr_id)

        return L

    def local_add_save(self):
        

        """
        <p>这里是local 表单 ，add 模式下的保存处理</p>
        """
        
        #这些是操作权限
        dR={'R':'','MSG':'申请单 保存成功','B':'1','isadd':'','furl':''}  

        #获取表单参数
        access_key=self.GP('access_key','')#小程序appid
        secret_key=self.GP('secret_key','')#小程序secret
        name=self.GP('name','')#小程序对应的token
        domain =self.GP('domain','')
        data = {
                'access_key':access_key
                ,'secret_key':secret_key
                ,'name':name
                ,'usr_id':self.usr_id
                ,'domain':domain
             }

        # for k in list(data):
        #     if data[k] == '':
        #         data.pop(k)
        pk=''
        sql="select id from qiniu where usr_id=%s"%self.usr_id
        l,t=self.db.select(sql)
        if t>0:
            pk=l[0][0]

        if pk != '':  #update
            #如果是更新，就去掉cid，ctime 的处理.
            data['cid']=self.usr_id
            data['ctime']=self.getToday(6)
            #data.pop('random')

            self.db.update('qiniu' , data , " id = %s " % pk)
            
        else:  #insert
            #如果是插入 就去掉 uid，utime 的处理
            data['uid'] = self.usr_id
            data['utime'] = self.getToday(6)
            
            self.db.insert('qiniu' , data)
            #pk = self.db.insertid('mall_id')#这个的格式是表名_自增字段
            dR['isadd'] = 1
        #self.listdata_save(pk,danhao)
        dR['pk'] = pk
        
        return dR
