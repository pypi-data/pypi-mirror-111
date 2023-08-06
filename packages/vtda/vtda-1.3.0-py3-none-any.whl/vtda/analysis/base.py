# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 21:23:50 2021

@author: ZSL
"""
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from vtda.util.util import weight_factor

#解决中文乱码问题
plt.rcParams["font.sans-serif"]='SimHei'
#解决负号无法正常显示问题
plt.rcParams["axes.unicode_minus"]= False

def choose_windows(name='hanning', N=512,fix_meth='幅值修正'):
    '''
    本函数用来生成窗函数和修正系数
    修正方式分为能量修正和幅值修正   

    Parameters
    ----------
    name : TYPE, optional
        穿函数名. The default is 'hanning'.
    N : TYPE, optional
        生成数据的长度. The default is 512.
    fix_meth : TYPE, optional
        修正方式. The default is '幅值修正'.

    Returns
    -------
    np格式的窗函数
    '''

# Rect/Hanning/Hamming
    if name == 'hamming':
        window =np.hamming(N) 
        xishu_fuzhi=1.85
        xishu_nengliang=1.59
        if fix_meth=='幅值修正':
            res_xishu=xishu_fuzhi
        elif fix_meth=='能量修正':
            res_xishu=xishu_nengliang   
        #np.array([0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1)) for n in range(N)])
    elif name == 'hanning':
        window=np.hanning(N)
        xishu_fuzhi=2
        xishu_nengliang=1.63
        if fix_meth=='幅值修正':
            res_xishu=xishu_fuzhi
        elif fix_meth=='能量修正':
            res_xishu=xishu_nengliang        
        #window = np.array([0.5 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) for n in range(N)])
    elif name == 'rect':
        window = np.ones(N)
        xishu_fuzhi=1
        xishu_nengliang=1
        if fix_meth=='幅值修正':
            res_xishu=xishu_fuzhi
        elif fix_meth=='能量修正':
            res_xishu=xishu_nengliang
    return window*res_xishu

def fft(y,
        sample_rate =4096,
        fft_size = 4096,
        window='hanning'
        ,cdxs=0.75,
        fix_meth='幅值修正',
        meth='线性平均'
        ):
    '''
    傅里叶变换函数
    :param x: 为输入数据
    :param sample_rate: 数据采样率
    :param fft_size: 分析点数，默认为512Hz    
    :param cdxs: 重叠系数,默认为0.75 
    单独运算fft采用幅值修正，计算倍频程及振级采用能量修正
    '''
    #fft_size=len(y)
    try:
        y=y.dropna()
        y=y.fillna(0) 
        y=np.array(y)        
    except:
        pass
    n_zong=max(math.ceil((len(y)-fft_size)/(round((1-cdxs),5)*fft_size))+1,1)#上取整
    res=np.zeros(int(fft_size/2))
    #fix_meth='能量修正'
    #del res_y
    y=y-y.mean()
    res=[]
    for i in np.arange(n_zong):
        pass

        y_=y[int(i*round((1-cdxs),5)*fft_size):int(i*round((1-cdxs),5)*fft_size+fft_size)][:int(fft_size)]   
        if len(y_)>0:
            if len(y_)<fft_size: #长度不够进行补零处理
                y_=np.append(y_, np.array([0]*(int(fft_size)-len(y_))), axis=0)
            N=fft_size
            fft_y=np.abs(np.fft.fft(y_*choose_windows(name=window,N=len(y_),fix_meth=fix_meth)))/(0.5*len(y_))
            res.append(fft_y)
    
            # try:
            #     res_y=(fft_y+res_y)/2
            # except:
            #     #第一次没有平均值 
            #     res_y=fft_y
            try:  #经测试先计算最后统一平均的方式和dasp频率特性一致，所以
                res_y+=fft_y[range(int(N/2))]
            except:
                #第一次没有平均值 
                res_y=fft_y[range(int(N/2))]
    # aa=pd.DataFrame(res).T
    # with pd.ExcelWriter(dir_+'/test_fft.xlsx') as writer:
    #     aa.to_excel(writer, sheet_name='计算时间')  
    #res_y=res_y/n_zong
    # pd.DataFrame(asd).plot()        
    res_y[0]=res_y[0]/2
    if n_zong>1:
        rms_z=np.sqrt(np.sum([ i*i for i in y])/(len(y)))
        rms_av=rms_z
        rms_1=np.sqrt(sum(res_y[range(int(N/2))]*res_y[range(int(N/2))])/2)
        xishu=rms_av/rms_1
        res_y=res_y*xishu
        # np.sqrt(sum(res_y1*res_y1)/2)
        # np.sqrt(np.sum([ i*i for i in res_y1])/2)
        #res_y=np.sqrt(res_y[range(int(N/2))]/n_zong)#/((n_zong-1)*(cdxs))#n_zong/np.sqrt(2)
    else:
        res_y=res_y[range(int(N/2))]
    #res_x=np.linspace(0,sample_rate/2,int(fft_size/2) )
    return list(np.arange(0,sample_rate/2,sample_rate/fft_size)),list(res_y)#pd.DataFrame({'frac':res_x,'fft':res_y}).set_index('frac')


def octave_3(y, 
             sample_rate=4096,
             fft_size = 4096, 
             window='hanning',
             cdxs=0.75,
             meth='线性平均',
             base=0.000001,
             res_type='db',
             frec='all', #输出频率
             ):
    #x=aaaa[28]
    fl=1 #默认起始频谱
    fh=sample_rate/2 #默认截止频率
    #倍频程中心频率计算有两种方法：以2或者10为基底计算 但是两种方法各有利弊，在个别频段均不是整数
    #iso266对中心频率进行了取整规定，故不在进行计算，直接引用标准
    fc_base = [1,1.25,1.6,2,2.5,3.15,4,5,6.3,8] #1/3倍频程中心频率 基础频率值  其余在此基础上乘10扩展即可
    cf=fc_base+[i*10 for i in fc_base]+[i*100 for i in fc_base]+[i*1000 for i in fc_base]+[i*10000 for i in fc_base]
    if frec=='all':
        cf=[i for i in cf if i<fh ]
    else:
        #frec=[10,500]
        ls=min(fh,frec[1])
        cf=[i for i in cf if i<=ls and i>=frec[0]]
    lf=[i/(2**(1/6)) for i in cf]        
    rf=[i*2**(1/6) for i in cf]    
    
    res_x,res_y_=fft(y,
                     sample_rate=sample_rate,
                     fft_size =fft_size,
                     cdxs=cdxs,
                     fix_meth='能量修正',
                     window=window,
                     meth=meth)
    res_y=[]
    res_x=np.array(res_x)
    res_y_=np.array(res_y_)
    for i in range(len(cf)):
        pass
        ibf= np.where((res_x >= lf[i]) & (res_x < rf[i])) 
        rms=np.sqrt(np.sum([ i*i for i in res_y_[ibf]])/2)
        if res_type=='db':
            if rms>0:
                res_y.append(20*math.log10(rms/base))
            else:
                res_y.append(0)
        elif res_type=='线性':
            res_y.append(rms)
    return cf,res_y

def base_level(  y,
                 weight=None,
                 base=0.000001,                         
                 sample_rate=4096,
                 fft_size = None,
                 fft_len=None,
                 window='hanning',
                 cdxs=0.5,
                 frec='all', #计权因子频率范围
                 n=2 #结果保留精度，即小数点后位数
                 ):
    '''
    计算振级的基本函数，能够计算Z振级和A声级，本质上只是更换计权曲线和计权频率而已
    Parameters
    ----------
    y : TYPE
        待计算数据，可以为np.ndarray或者 pd.Series格式
    zweight : TYPE, optional
        计权曲线，默认为 None
    sample_rate : TYPE, optional
        采样点数，默认为4096，如果待计算数据为pd.Series格式，其中有采样频率信息，则优先采用其信息。
    fft_size : TYPE, optional
        分析点数，默认为采样点数，即分析窗长为1秒
    fft_len : TYPE, optional
        分析长度，默认为1秒  其和分析点数功能相同，输入一个即可，分析长度优先级高于分析点数
    window : TYPE, optional
        加窗，默认为汉宁窗
    cdxs : TYPE, optional
        重叠系数，默认为0.5
    frec : TYPE, optional
        计权频率的范围，默认为None，可以为[1,80],表示只计算1-80Hz的频率内的能量
    Returns
    -------
    返回两个结果list，一个为时间，另一个为随时间变化的振级

    '''
    
    weight=weight_factor(weight=weight,frec=frec) #一定会传入一个计权因子和频率范围
#    
#    
#    if frec==None and weight==None:
#        weight=[0]*100 
#    elif frec==None and weight!=None:
#        weight=weight_factor(weight=weight)
#    elif frec!=None and weight==None:
#        weight=[0]*100
#    elif frec!=None and weight!=None:       
#        weight=weight_factor(weight=weight,frec=frec)         
    if len(weight)==0:
        print(str(weight)+str(frec)+'计权因子选取错误，请检查')
    #y=aa[1]  res_tigui_acce_21_24['que_dan'][21][300:2000]['que0']
    if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series):
        sample_rate=1/(y.index[1]-y.index[0])
        y=y.fillna(0)
        y=np.array(y)        
    elif isinstance(y, np.ndarray):
        pass
    else:
        print("{} 错误数据输入格式。。。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))             
    if fft_size == None :  #不输入分析点数默认
       fft_size= sample_rate
    if fft_len!=None:
       fft_size=fft_len*sample_rate
       
    n_zong=max(math.ceil((len(y)-fft_size)/(round((1-cdxs),5)*fft_size))+1,1)#上取整
    res=np.zeros(int(fft_size/2))
    vl_z=[]
    vl_zonethirds2=[]
    y_z=[]

    for i in np.arange(n_zong):
        pass
        y_=y[int(i*round((1-cdxs),5)*fft_size):int(i*round((1-cdxs),5)*fft_size+fft_size)][:int(fft_size)] 
        if len(y_)>0:
            res_x,onethird=octave_3(y_,
                                    sample_rate =sample_rate,
                                    fft_size = fft_size,
                                    cdxs=cdxs,
                                    window=window,
                                    res_type='db',
                                    base=base,
                                    frec=frec,
                                    )
            # if len(res_x)>=len(zweight):
            #     zweight=zweight+[0]*(len(res_x)-len(zweight))
            # else:
            #     zweight=zweight[:len(res_x)]
            
            if len(res_x)>=len(weight):
                onethird=onethird[:len(weight)]#zweight+[0]*(len(res_x)-len(zweight))
            else:
                weight=weight[:len(res_x)]#onethird+[0]*(len(weight)-len(res_x))
            vl_zonethird=10**((np.array(weight)+np.array(onethird))*0.1) 
            #print(len(y_),i)
            vl_z_=10*math.log10(sum(vl_zonethird)) 
            vl_z.append(round(vl_z_,n))
            deta_x=(fft_size/sample_rate)*round((1-cdxs),5)
    #res_x=np.linspace(0,deta_x*n_zong,n_zong)           
    return list(np.arange(0,deta_x*n_zong,deta_x)),vl_z


def rms_time(y):
    '''
    在时域内对信号求有效值
    '''
    return np.sqrt(np.sum([ i*i for i in y])/(len(y)))

def rms_frec(y,sample_rate=4096,fft_size = 4096, window='hanning',cdxs=0.5):
    '''
    在频谱内对信号求有效值

    '''
    res_x,res_y_=fft(y,
                     sample_rate=sample_rate,
                     fft_size =fft_size,
                     cdxs=cdxs,
                     fix_meth='能量修正',
                     window=window,
                     meth='线性平均')
    rms=np.sqrt(np.sum([ i*i for i in res_y_])/2)    
    return rms

if __name__ == '__main__':


    
    import vtda
    dir_='D:/quant/git/vtda/test_data_dasp'
    name='20210227南宁地铁2号线上行16+018啊'
    data,info=vtda.read_dasp_data(name,dir_=dir_)
    i=10
    j=5
    #dasp  1-5通道频谱有效值:11.2475 14.6698  0.41429  0.03633  0.04221
    #dasp  1-5通道频谱总极值:141.02 143.33  112.36  91.21  92.52
    dasp_rms=np.array([11.2475,14.6698,0.41429,0.03633,0.04221])
    dasp_db=np.array([141.02,143.33,112.36,91.21,92.52])   
    python_rms_time=[]
    python_rms_frec=[]    
    for j in range(1,6):
        pass
        print(j)
        python_rms_time.append(rms_time(data[i][j]) ) 
        python_rms_frec.append(rms_frec(data[i][j],float(info[i][j]['采样频率']),float(info[i][j]['采样频率']),cdxs=0.75))   
    a,b=fft(data[i][j],sample_rate =float(info[i][j]['采样频率']),fft_size = float(info[i][j]['采样频率']),window='rect',cdxs=0.75,fix_meth='幅值修正',meth='线性平均')
    plt.plot(a,b)  
    a,b=octave_3(data[i][j],sample_rate =float(info[i][j]['采样频率']),fft_size = float(info[i][j]['采样频率']),window='rect',cdxs=0.75,meth='线性平均')

    plt.figure(figsize=(15, 12))
    plt.plot(a,b) 
    plt.semilogx()
    
   