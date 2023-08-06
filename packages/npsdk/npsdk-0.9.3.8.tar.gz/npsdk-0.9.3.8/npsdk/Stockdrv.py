﻿from ctypes import *

#本示例尽量详细注释，没有注释的，请猜猜看
CHAR   = c_char
bool   = c_bool
BOOL   = c_int
INT8   = c_char
UCHAR  = c_ubyte
UINT8  = c_ubyte
BYTE   = c_ubyte
SHORT  = c_short
INT16  = c_short
USHORT = c_ushort
UINT16 = c_ushort
WORD   = c_ushort
INT    = c_int
INT32  = c_int
UINT   = c_uint
UINT32 = c_uint
LONG   = c_long
ULONG  = c_ulong
DWORD  = c_ulong
WCHAR  = c_wchar
UINT64 = c_ulonglong
FLOAT  = c_float
DOUBLE = c_double

LPCSTR  = POINTER(CHAR)
LPCVOID = POINTER(None)
NPSTR   = POINTER(CHAR)
LPSTR   = POINTER(CHAR)
PSTR    = POINTER(CHAR) 
NWPSTR  = POINTER(WCHAR)
LPWSTR  = POINTER(WCHAR)
PWSTR   = POINTER(WCHAR)

OEM_Ver2020  = 2020

class OEM_DATA_HEAD(Structure):     #通信头部 100 字节
    _pack_ = 1                      #对齐方式
    _fields_ = [                    #构体成员名称
        ("oemVer",    UINT),        #版本号
        ("type",      WCHAR * 10),  #各种子功能号：日线、5分钟线
        ("label",     WCHAR * 10),  #代码
        ("name",      WCHAR * 10),  #名称

        ("data",      UINT * 3),

        ("flag",      CHAR),        #-1设置某个值；0 服务器推送；1 读取本地数据
        ("askId",     INT),         #申请编号(内部功能)
        ("len",       INT),         #数据长度
        ("count",     INT),         #多少组数据
        ("temp1",     CHAR),        #预留
        ("temp2",     CHAR * 10)    #预留
        ]

    def __len__(self):
       return 100
       
    # ctypes结构体 转 字节流
    def encode(self): 
        return string_at(addressof(self), sizeof(self))

    # 字节流 转 ctypes结构体
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

class OEM_STKINFO(Structure):     #证券(100字节)  #2021.5.22改过字段
    _pack_ = 1
    _fields_ = [
    ('code',      WORD),            #序号
    ('market',    BYTE),            #市场MK_SH;MK_SZ，表明是上海、深圳等市场
    ('block',     BYTE),            #所属系统板块，BK_SHAG，BK_SZAG，表明是上海Ａ股，深圳Ａ股系统板块
    ('label',     WCHAR * 10),
    ('name',      WCHAR * 20),
    ('pointNum',  CHAR),            #小数点个数0、1、2、3
    ('hand',      WORD),            #每手股数
    ('last',      FLOAT),           #昨收
    ('limitUp',   FLOAT),           #涨停
    ('limitDown', FLOAT),           #跌停
    ('isIndex',   bool),            #是否指数*
    ('isDaPan',   bool),            #是否大盘*
    ('isStock',   bool),            #股票标识*
    ('bsNum',     CHAR),            #股票标识*
    ('pinYin',    CHAR * 12),
    ('temp',      CHAR * 5),        #
   ]

    # ctypes结构体 转 字节流
    def encode(self): 
        return string_at(addressof(self), sizeof(self))

    # 字节流 转 ctypes结构体
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

class OEM_MARKETINFO(Structure):       #市场内容(100字节)
    _pack_ = 1
    _fields_ = [
    ('mkId',       WORD),              #//市场代码, 'HS', 'SZ', 'JZ', 'HW' ..... 
    ('name',       WCHAR * 20),        #市场名称(英文简称，如 SHSE 表示上海交易所)
    ('tmCount',    SHORT),             #交易时段个数
    ('openTime',   SHORT * 8),         #开盘时间 1,2,3,4,5
    ('closeTime',  SHORT * 8),         #分钟数 比如 0X023A（570）表示 9:30)
    ('date',       UINT),              #数据日期（201301010）
    ('num',        WORD),              #该市场的证券个数
    ('temp',       CHAR * 18),
    ('stkInfo',    OEM_STKINFO * 10)
    ]
    # ctypes结构体 转 字节流
    def encode(self): 
        return string_at(addressof(self), sizeof(self))

    # 字节流 转 ctypes结构体
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

class OEM_REPORT(Structure):  #实时数据 400 字节，带*表示网际风内部数据，请跳过
    _pack_ = 1
    _fields_ = [
    ('label',      WCHAR * 10),              #代码
    ('name',       WCHAR * 10),              #名称
    ('time',       UINT),                    #成交时间(UTC时间，可以百度搜索相关转换)
    ('foot',   INT),                         #最后处理分钟数
    ('openDate',   UINT),                    #市场开盘日期零点
    ('openTime',   UINT),                    #市场开盘时间
    ('closeDate',  UINT),                    #市场日线日期零点

    ('open',       FLOAT),                   #今日开盘
    ('high',       FLOAT),                   #今日最高
    ('low',        FLOAT),                   #今日最低
    ('close',      FLOAT),                   #最新价格
    ('volume',     FLOAT),                   #总成交量
    ('amount',     FLOAT),                   #总成交金额
    ('inVol',      FLOAT),                   #外盘*
    ('pricesell',  FLOAT * 10),              #申卖价1,2,3,4,5
    ('volsell',    FLOAT * 10),              #申卖量1,2,3,4,5      
    ('vsellCha',   FLOAT * 10),              #申卖量变化*
    ('pricebuy',   FLOAT * 10),              #申买价1,2,3,4,5      
    ('volbuy',     FLOAT * 10),              #申买量1,2,3,4,5       
    ('vbuyCha',    FLOAT * 10),              #申买量变化*
    ('jingJia',    SHORT),                   #集合竞价
    ('avPrice',    FLOAT),                   #期货的结算价（平均价）
    ('isBuy',      CHAR),                    #0 下跌；1 上涨或平盘*
    ('nowv',       FLOAT),                   #现量
    ('nowa',       FLOAT),                   #分笔成交额(期货仓差)

    ('change',     FLOAT),                  #换手率*
    ('weiBi',      FLOAT),                  #委比*
    ('liangBi',    FLOAT),                  #量比*
    ('temp',       CHAR * 45),
    ]

    def __len__(self):
       return 400

    # ctypes结构体 转 字节流
    def encode(self): 
        return string_at(addressof(self), sizeof(self))

    # 字节流 转 ctypes结构体
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

"""
class OEM_TRACE(Structure):  #分笔 100 字节
    _pack_ = 1
    _fields_ = [
    ('time',      UINT),
    ('close',     FLOAT),      #现价
    ('volume',    FLOAT),      #成交量
    ('amount',    FLOAT),      #成交额
    ('traceNum',  INT),
    ('pricebuy',  FLOAT * 5),  #申买价1,2,3,4,5
    ('volbuy',    FLOAT * 5),
    ('pricesell', FLOAT * 5),
    ('volsell',   FLOAT * 5),
    ]

    def __len__(self):
       return 108

    # ctypes结构体 转 字节流
    def encode(self): 
        return string_at(addressof(self), sizeof(self))

    # 字节流 转 ctypes结构体
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)
"""

# 因为在sdk生成Dataframe时， df导入数据时把 FLOAT * 5 转成列表，列表成员居然为 float obj引用，
# 做K线属性字段值比较时，float obj引用id自然不一样, 故把 FLOAT *5 拆成 5个 FLOAT

class OEM_TRACE(Structure):  #分笔 100 字节
    _pack_ = 1
    _fields_ = [
    ('time',      UINT),
    ('close',     FLOAT),      #现价
    ('volume',    FLOAT),      #成交量
    ('amount',    FLOAT),      #成交额
    ('traceNum',  INT),
    ('pricebuy1',  FLOAT),  #申买价1,2,3,4,5
    ('pricebuy2',  FLOAT),
    ('pricebuy3',  FLOAT),
    ('pricebuy4',  FLOAT),
    ('pricebuy5',  FLOAT),
    ('volbuy1',    FLOAT),
    ('volbuy2',    FLOAT),
    ('volbuy3',    FLOAT),
    ('volbuy4',    FLOAT),
    ('volbuy5',    FLOAT),
    ('pricesell1', FLOAT),
    ('pricesell2', FLOAT),
    ('pricesell3', FLOAT),
    ('pricesell4', FLOAT),
    ('pricesell5', FLOAT),
    ('volsell1',   FLOAT),
    ('volsell2',   FLOAT),
    ('volsell3',   FLOAT),
    ('volsell4',   FLOAT),
    ('volsell5',   FLOAT),
    ]

    def __len__(self):
       return 108

    # ctypes结构体 转 字节流
    def encode(self): 
        return string_at(addressof(self), sizeof(self))

    # 字节流 转 ctypes结构体
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)


class RCV_KLINE(Structure):
    _pack_ = 1
    _fields_ = [
    ('time',     UINT),           #时间
    ('open',     FLOAT),          #开盘
    ('high',     FLOAT),          #最高
    ('low',      FLOAT),          #最低
    ('close',    FLOAT),          #现价
    ('volume',   FLOAT),          #成交量
    ('amount',   FLOAT),          #成交额
    ('temp',     FLOAT),          #预留
    ]

    # ctypes结构体 转 字节流
    def encode(self): 
        return string_at(addressof(self), sizeof(self))

    # 字节流 转 ctypes结构体
    def decode(self, data):
        memmove(addressof(self), data, sizeof(self))
        return len(data)

class OEM_SPLIT_HEAD(Structure):      #除权头  100 字节
    _pack_ = 1
    _fields_ = [
    ("label",      WCHAR * 10),   #代码
    ("name",       WCHAR * 10),   #名称
    ("num",        WORD),         #数量
    ("volume",     UINT),         #系统内部
    ("temp",       CHAR * 54),    #预留
    ]

class OEM_SPLIT(Structure):           #除权 100 字节
    _pack_ = 1                       
    _fields_ = [                     
    ('time',       UINT),             #时间
    ("give",       FLOAT),            #每股送
    ("allocate",   FLOAT),            #每股配
    ("price",      FLOAT),            #每股配价
    ("earnings",   FLOAT),            #每股红利
    ("explain",    WCHAR * 40),       #描述文本(预留)
   ]

class RCV_FINANCE(Structure):       #财务 250 字节
    _pack_ = 1
    _fields_ = [
    ("label",    WCHAR * 10),         #代码
    ("name",     WCHAR * 10),         #名称
    ('time',     INT),                #发布日期		年月日
    ('baoGao',   INT),                #报告日期
    ('shangShi', INT),                #上市日期
    ('meiGuShouYi', FLOAT),           #每股收益(元)，净利润/总股本
    ('shuiHou',  FLOAT),              #每股净资产(元)
    ('jzcsyl',   FLOAT),              #净资产收益率(%)
    ('mgjyxj',   FLOAT),              #每股经营现金
    ('mggjj',    FLOAT),              #每股公积金(元)
    ('mgwfp',    FLOAT),              #每股未分配利润(元)
    ('gdqybl',   FLOAT),              #股东权益比率(%)
    ('jlrtb',    FLOAT),              #净利润同比		10
    ('zysytb',   FLOAT),              #主营收益同比
    ('xsmll',    FLOAT),              #销售毛利率
    ('meiGuJingZhi', FLOAT),          #调整每股净资(元)
    ('zongZC',   FLOAT),              #总资产(万元)
    ('ldzc',     FLOAT),              #流动资产(万元)
    ('guDingZC', FLOAT),              #固定资产(万元)
    ('wuXingZC', FLOAT),              #无形资产(万元)
    ('ldfz',     FLOAT),              #流动负债(万元)
    ('cqfz',     FLOAT),              #长期负债(万元)
    ('zfz',      FLOAT),              #总负债	20
    ('quanYi',   FLOAT),              #股东权益(净资产 万元)
    ('ziBenGongJi', FLOAT),           #资本公积金(万元)
    ('xianJin',   FLOAT),             #经营现金流量
    ('tzxjl',     FLOAT),             #投资现金流量
    ('czxjl',     FLOAT),             #筹资现金流量
    ('xjzje',     FLOAT),             #现金增加额
    ('shouRu',    FLOAT),             #主营业务收入(万元)
    ('shouRuZhu', FLOAT),             #主营利润(万元)
    ('liRun',     FLOAT),             #营业利润(万元)
    ('shouYi',    FLOAT),             #投资收益		30
    ('qtlr',      FLOAT),             #营业外收支(万元)
    ('zongLiRun', FLOAT),             #利润总额(万元)
    ('jingLiRun', FLOAT),             #净利润(千元)
    ('weiFenPei', FLOAT),             #未分配利润(万元)
    ('zongGu',    FLOAT),             #总股本(万股)
    ('wxsAg',     FLOAT),             #无限售股合计
    ('liuTongAG', FLOAT),             #流通A股(万股)
    ('bGu',       FLOAT),             #B股(万股)
    ('hGu',       FLOAT),             #境外上市股(万股)
    ('qtltg',     FLOAT),             #其它流通股	40
    ('xsghj',     FLOAT),             #限售股合计
    ('gjg',       FLOAT),             #国家股(万股)
    ('frcg',      FLOAT),             #国有法人股
    ('frg',       FLOAT),             #境内法人股(万股)
    ('jnzrrg',    FLOAT),             #境内自然人股
    ('fqrfrg',    FLOAT),             #其他发起人股(万股)
    ('mjfrg',     FLOAT),             #募集法人股
    ('jwfrg',     FLOAT),             #境外法人股
    ('jwzrrg',    FLOAT),             #境外自然人股
    ('yxg',       FLOAT),             #优先股或其他	50(大智慧204字节结构)
    ('temp',      CHAR * 6),
]

class OEM_F10INFO(Structure):         #F10资料 50 字节
    _pack_ = 1
    _fields_ = [
    ('title',  WCHAR * 12),           #信息标题         
    ('from',   INT),                  #文件位置         
    ('len',    INT),                  #长度        
    ('temp',   CHAR * 18),            #预留         
]

class CText(Structure):               #转换文本
    _pack_ = 1
    _fields_ = [
    ('data',   WCHAR * 10240000),
    ]
