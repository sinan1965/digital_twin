# Tanımlamalar
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)#,use_pages = True)

#---------------------
#solüst
trace_solüst = []
#tedarikçi adına göre sipariş miktarı kg.
fig = go.Figure()

global marka1
marka1 = dfsip.groupby('bayii')['sipariş_miktarı'].sum().sort_values(ascending=False)
marka1 = pd.DataFrame(marka1)

fig.add_trace(go.Bar(
        x =marka1.index,
        y =dfsip.groupby('bayii')['sipariş_miktarı'].sum().sort_values(ascending=False)/1000,
        marker=dict(color='red'),
        opacity=.5,
        hovertemplate = '<i>Bayii: </i>'+ '%{x}'+
                        '<br><i>Miktar:</i> %{y:,.0f} (ton) <br>'+
                        '<extra></extra>',
        showlegend = False
))

fig.update_layout(
        title_text= (''), 
        xaxis_title_text='Bayii İsmi', 
        yaxis_title_text='Sipariş Miktarı (ton)',
        #title=dict(text=(f"Bayii İsmine Göre Sipariş Miktarları (ton)")),
        hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
        yaxis = dict(gridcolor='lightgrey'),                          
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',                  
)
#fig.show()

trace_solüst = np.append(fig,trace_solüst)

#----------------------- 
#solort
trace_solort = []
#istenen teslim tarihine göre sipariş miktarı kg.
fig = go.Figure()

indeks = dfsip['tarih_n'].unique()
dfsil4 = pd.DataFrame(index = indeks, columns = ['sipariş_kg','kayan_ort_üretim'])
say = 0

for i in indeks:
    df_tarih = dfsip.loc[dfsip['tarih_n'] == i]
    top = df_tarih['sipariş_miktarı'].sum()/1000
    #top = len(df_tarih['sipariş_miktarı'])
    dfsil4['sipariş_kg'].iloc[say] = top
    say +=1

ort = dfsil4['sipariş_kg'].mean()
dfsil4['kayan_ort_üretim'] = dfsil4['sipariş_kg'].rolling(30,min_periods=1).mean()

#grafikleştirme
fig.add_trace(go.Bar(
             x= dfsil4.index,
             y= dfsil4['sipariş_kg'],
             marker_color='blue',
             opacity=0.5,
             hovertemplate = '<i>Tarih: </i>'+ '%{x}'+
                        '<br><i>Toplam sevkiyat miktarı:</i> %{y:,.2f} (ton)<br>'+
                        '<extra></extra>',
             showlegend = False

             ))
fig.add_trace(go.Scatter(
                x= dfsil4.index,
                y = dfsil4['kayan_ort_üretim'],
                marker=dict(color='orange', opacity = 0.8),
                hovertemplate = (f'<i>Tarih: </i>')+
                '%{x}'+'<br><i>Ort. Üretim:</i> %{y} (ton)<br>'+ '<extra></extra>',
                showlegend = False,
                mode = 'lines'))

for i in range(0,len(mevsim_tarih)):
        fig.add_vrect(x0=mevsim_tarih[i], x1= mevsim_tarih[i], line_dash = 'dash',line_color = 'red',opacity=0.3,
                     annotation_text = (f'{mevsim_isim[i]}'),
                     annotation_position = 'top right')

fig.update_layout(
        title_text= (''), 
        xaxis = dict(tickmode = 'array'),
        xaxis_title_text='Teslim Tarihi', 
        yaxis_title_text='Sipariş Miktarı (ton)',
        title=dict(text=(f"İstenen teslim tarihine göre sevkiyat miktarları (ton)")),
        hoverlabel = dict(font=dict(color='white'),bgcolor='grey'), 
        yaxis = dict(gridcolor='lightgrey'),                          
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',                  
        )
#fig.show()

# dfsil4 anomali kodlaması
dfsil4_kışA = dfsil4[:mevsim_tarih[0]]
dfsil4_kışB = dfsil4[mevsim_tarih[3]:]
dfsil4_kış = pd.concat([dfsil4_kışA,dfsil4_kışB], axis=0)

ort_list = [dfsil4_kış.sipariş_kg.mean(),(dfsil4[mevsim_tarih[0]:mevsim_tarih[1]]).sipariş_kg.mean(),dfsil4[mevsim_tarih[1]:mevsim_tarih[2]].sipariş_kg.mean(),
            dfsil4[mevsim_tarih[2]:mevsim_tarih[3]].sipariş_kg.mean()]
std_list = [dfsil4_kış.sipariş_kg.std(), (dfsil4[mevsim_tarih[0]:mevsim_tarih[1]]).sipariş_kg.std(), dfsil4[mevsim_tarih[1]:mevsim_tarih[2]].sipariş_kg.std(),
           dfsil4[mevsim_tarih[2]:mevsim_tarih[3]].sipariş_kg.std()]
min_list = [dfsil4_kış.sipariş_kg.min(), (dfsil4[mevsim_tarih[0]:mevsim_tarih[1]]).sipariş_kg.min(), dfsil4[mevsim_tarih[1]:mevsim_tarih[2]].sipariş_kg.min(),
           dfsil4[mevsim_tarih[2]:mevsim_tarih[3]].sipariş_kg.min()]

ano_solort1 = (f'{mevsim_dict.get(np.argmax(ort_list))} mevsiminde {np.max(ort_list):,.0f} ton ile en yüksek ortalama sipariş miktarına ulaşılmıştır.')
ano_solort2 = (f'Buna karşılık İlkbaharda {ort_list[1]:,.0f}, Yaz aylarında {ort_list[2]:,.0f}, Sonbahar da ise ortalama {ort_list[3]:,.0f} ton seviyelerine düşmüştür.')
ano_solort3 = (f'En istikrarlı ortalama sipariş seviyeleri {mevsim_dict.get(np.argmin(std_list))} aylarında gözlenmektedir.')
ano_solort4 = (f'{mevsim_dict.get(np.argmin(min_list))} mevsiminde {np.min(min_list):,.0f} ton ile en düşük ortalama sipariş miktarına ulaşılmıştır.')

trace_solort = np.append(fig,trace_solort)
   
#------------------------
#sağüst
trace_sağüst = []
#istenen teslim tarihine göre toplam sipariş miktarı ve karşılanamayanlar kg.
fig = go.Figure()

indeks1 = dfsip['tarih_n'].unique()
dfsil61 = pd.DataFrame(index = indeks1, columns = ['sipariş_kg'])
say1 = 0

for i in indeks1:
    df_tarih = dfsip.loc[dfsip['tarih_n'] == i]
    #top1 = len(df_tarih) # adetsel olarak
    top1 = df_tarih['sipariş_miktarı'].sum()/1000
    dfsil61['sipariş_kg'].iloc[say1] = top1
    say1 +=1

ort = dfsil61['sipariş_kg'].mean()

#----------------------------------
#karşılanamayan siparişlerin miktarı kg.
indeks2 = dfsip_off['tarih_n'].unique()
dfsil62 = pd.DataFrame(index=indeks2, columns = ['sipariş_kg'])

say2 = 0

for ii in indeks2:
    df_tarih = dfsip_off.loc[dfsip_off['tarih_n']==ii]
    #top2 = len(df_tarih) # adetsel olarak
    top2 = df_tarih['sipariş_miktarı'].sum()/1000
    dfsil62['sipariş_kg'].iloc[say2] = top2
    say2 +=1
#-----------------------------------

#grafikleştirme
fig.add_trace(go.Bar(
             x= dfsil61.index,
             y= dfsil61['sipariş_kg'],
             marker_color='blue',
             opacity=0.5,
             hovertemplate = '<i>Tarih: </i>'+ '%{x}'+
                        '<br><i>Sipariş adedi:</i> %{y:,.0f}<br>'+
                        '<extra></extra>',
             showlegend = False
             ))

fig.add_trace(go.Scatter(
             x= dfsil62.index,
             y= dfsil62['sipariş_kg'],
             mode= 'markers',
             marker = dict(color='red',size=10),
             opacity=1,
             hovertemplate = '<i>Tarih: </i>'+ '%{x}'+
                        '<br><i>Zamanında karşılanamayan sipariş adedi:</i> %{y:,.0f}<br>'+
                        '<extra></extra>',
             showlegend=False
             ))

fig.update_layout(
        title_text= (''), 
        xaxis = dict(tickmode = 'array', range=[dfsip.tarih_n.min(), dfsip.tarih_n.max()]),
        xaxis_title_text='Onay Tarihi', 
        yaxis_title_text='Sipariş Miktarı (adet)',
        hoverlabel = dict(font=dict(color='white')),
        yaxis = dict(gridcolor='lightgrey'),                          
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',  
    )
#fig.show()

# dfsil62 anomali kodlaması
ano_sağüst1 = (f'Bir yıllık sürede zamanında sipariş karşılanamayan gün sayısı: {len(dfsil61)-len(dfsil62)}')
ano_sağüst2 = (f'Zamanında karşılanamayan siparişlerin miktarı : {dfsil62.sipariş_kg.sum():,.2f} kg.')
ano_sağüst3 = (f'Zamanında karşılanamayan siparişlerin toplam sipariş miktarına oranı: %{100*(dfsil62.sipariş_kg.sum()/dfsil61.sipariş_kg.sum()):,.2f}')

dfsil62_kışA = dfsil62[:mevsim_tarih[0]]
dfsil62_kışB = dfsil62[mevsim_tarih[3]:]
dfsil62_kış = pd.concat([dfsil62_kışA,dfsil62_kışB], axis=0)

ort_list = [dfsil62_kış.sipariş_kg.mean(),(dfsil62[mevsim_tarih[0]:mevsim_tarih[1]]).sipariş_kg.mean(),dfsil62[mevsim_tarih[1]:mevsim_tarih[2]].sipariş_kg.mean(),
            dfsil62[mevsim_tarih[2]:mevsim_tarih[3]].sipariş_kg.mean()]
top_list = [dfsil62_kış.sipariş_kg.sum(),(dfsil62[mevsim_tarih[0]:mevsim_tarih[1]]).sipariş_kg.sum(),dfsil62[mevsim_tarih[1]:mevsim_tarih[2]].sipariş_kg.sum(),
            dfsil62[mevsim_tarih[2]:mevsim_tarih[3]].sipariş_kg.sum()]

ano_sağüst4 = (f'{mevsim_dict.get(np.argmax(ort_list))} mevsiminde {np.max(ort_list):,.0f} ton ile en yüksek ortalama sipariş miktarına ulaşılmıştır.')
ano_sağüst5 = (f'Buna karşılık siparişler İlkbaharda {ort_list[1]:,.0f}, Yaz aylarında {ort_list[2]:,.0f}, Sonbahar da ise ortalama {ort_list[3]:,.0f} ton seviyelerine düşmüştür.')
ano_sağüst6 = (f'Karşılanamayan sipariş miktarlarını mevsimler bazında incelediğimizde kış mevsiminde {top_list[0]:,.0f}, ilkbahar da {top_list[1]:,.0f}, yazın {top_list[2]:,.0f}, sonbahar da ise {top_list[3]:,.0f} ton olarak gerçekleşmiştir.')

trace_sağüst = np.append(fig,trace_sağüst)

#-------------------------
#sağort
trace_sağort = []
#tedarikçi adına göre sipariş miktarı kg.
fig = go.Figure()

marka8 = dfsip_off.groupby('bayii')['sipariş_miktarı'].sum().sort_values(ascending=False)
marka8 = pd.DataFrame(marka8)

fig.add_trace(go.Bar(
        x =marka8.index,
        y =dfsip_off.groupby('bayii')['sipariş_miktarı'].sum().sort_values(ascending=False)/1000,
        marker=dict(color='darkkhaki'),
        opacity=.5,
        hovertemplate = '<i>Bayii: </i>'+ '%{x}'+
                        '<br><i>Zamanında karşılanamayan sipariş miktarı:</i> %{y:,.0f} (ton)'+
                        '<extra></extra>',
        showlegend = False    
))

fig.update_layout(
        title_text= (''), 
        xaxis_title_text='Bayi İsmi', 
        yaxis_title_text='Sipariş Miktarı (ton)',
        hoverlabel = dict(font=dict(color='white'), bgcolor='grey'),
        yaxis = dict(gridcolor='lightgrey'),                          
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',                  
)
#fig.show()

#marka8 anomali rapor kodu
marka8 = marka8.sort_index(ascending=False)
marka1 = marka1.sort_index(ascending=False)
ano_sağort1 = (f'Bayi bazında zamanında karşılanamayan sipariş oranları:')
ano_sağort2 = []

for idx,i in enumerate(marka1.index):
    ano_sağort2 = np.append((f'{marka8.index[idx]} zamanında karşılanamayan sipariş oranı: %{100*(marka8.sipariş_miktarı.iloc[idx]/marka1.sipariş_miktarı.iloc[idx]):,.2f}'),ano_sağort2)    

ano_sağort2 = np.flip(ano_sağort2)
trace_sağort = np.append(fig,trace_sağort)

#-------------------------
#solalt
trace_solalt = []
#Zamanında Karşılanamayan Siparişlerin Haftanın Günlerine Göre Dağılım Grafiği
fig = go.Figure()
indeks = dfsip_off['hafta_günü'].unique()
dfsil_off = pd.DataFrame(index=indeks, columns = ['adet','kg','gün'])

say = 0

for hgün in indeks:
    a = dfsip_off.loc[dfsip_off['hafta_günü']==hgün]
    top_kg = a['sipariş_miktarı'].sum()/1000
    top_adet = len(a)
    dfsil_off['adet'].iloc[say] = top_adet
    dfsil_off['kg'].iloc[say] = top_kg
    say +=1
    

dfsil_off = dfsil_off.sort_index()

dfsil_off['gün'] = np.ones(len(dfsil_off))
for i in dfsil_off.index:
    a = dfsil_off.index[i]
    b = hafta_gün.get(a)
    dfsil_off['gün'].iloc[i] = b
    
dfsil_off = dfsil_off.set_index('gün')

#grafikleştirme
fig.add_trace(go.Scatter(
             x= dfsil_off.index,
             y= dfsil_off['adet'],
             mode= 'markers',
             marker =dict(color='red',symbol = 'triangle-up', size=15),
             opacity=1,
             hovertemplate = '<i>:Haftanın günü: </i>'+ '%{x}'+
                        '<br><i>Geciken sipariş adedi:</i> %{y} <br>'+
                        '<extra></extra>',
             showlegend = False
             ))

fig.update_layout(
        title_text= (''), 
        xaxis = dict(tickmode = 'linear'),
        xaxis_title_text='Haftanın Günleri', 
        yaxis_title_text='Karşılanamayan Sipariş (adet)',
        hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
        yaxis = dict(gridcolor='lightgrey'),                          
        paper_bgcolor = 'white',
        plot_bgcolor = 'white',                  
)
#fig.show()

#anomali kodlaması
dfsil_off['adet_yüzde'] = dfsil_off['adet']/dfsil_off['adet'].sum()
dfsil_off['kg_yüzde'] = dfsil_off['kg']/dfsil_off['kg'].sum()

dfsil_off1 = dfsil_off.sort_values('kg_yüzde', ascending =False)
dfsil_off2 = dfsil_off.sort_values('adet_yüzde', ascending =False)
ano_solalt2 = []
ano_solalt1 = (f'Haftanın günlerine göre zamanında karşılanamayan siparişlerin adet olarak oranları :')
for i in range(0,len(dfsil_off2)):
    ano_solalt2 = np.append((f'{dfsil_off2.index[i]} : %{(100*(dfsil_off2["adet_yüzde"].iloc[i])):,.2f}'),ano_solalt2)
ano_solalt2 = np.flip(ano_solalt2)

trace_solalt = np.append(fig,trace_solalt)

#---------------------------
#günlük rapor
global gr
gr = []
date = dfsip.date_pick.max()

df_ = dfsip.loc[dfsip['tarih_n']==date]

df_alt = df_.loc[df_['sevk_performansı']>=1]
if len(df_alt)==0:
    gr = np.append(('Seçilen tarihte zamanında karşılanmamış bir sipariş bulunmamaktadır.'),gr)
elif len(df_alt)>0:
    gr = np.append((f"{date} tarihindeki 1 gün ve üstü sevk performans dağılımı :"),gr)
    rapor = []
    for i in range(0,len(df_alt)):
        bayi = df_alt.bayii.iloc[i]
        miktar = f'{df_alt.sipariş_miktarı.sum()/1000:,.2f} ton'
        ürün = df_alt.ürün_adı.iloc[i]
        gr = np.append([bayi,miktar,ürün],gr)
    
gr = np.append((f"{date} tarihindeki toplam sipariş bedeli: {(df_['genel_toplam'].sum()):,.2f} TL\n"),gr)

gr = np.append((f"{date} tarihindeki sipariş adedi :{len(df_)}"),gr)

bayi = df_.bayii.unique()
dfsil9 = pd.DataFrame(columns= bayi)

for zdx,z in enumerate(bayi):
    dfbayi = df_.loc[df_.bayii==z]

    k1_list = dfbayi['kamyon_1'] 
    k2_list = dfbayi['kamyon_2'] 
    k3_list = dfbayi['kamyon_3'] 
    k4_list = dfbayi['kamyon_4'] 

    k1_list = k1_list[k1_list!=0.0].tolist()
    k2_list = k2_list[k2_list!=0.0].tolist()
    k3_list = k3_list[k3_list!=0.0].tolist()
    k4_list = k4_list[k4_list!=0.0].tolist()

    kamyon_liste = k1_list + k2_list + k3_list + k4_list
    

    çuval_liste = []

    for i in range(0,len(dfbayi)):
        a = np.floor(dfbayi.çuval_adet.iloc[i]/400)
        for n in range(0,int(a)):
            çuval_liste = np.append(int(400),çuval_liste)
        b = int(dfbayi.çuval_adet.iloc[i]-(a*400))
        çuval_liste = np.append(int(b), çuval_liste)
    
    çuval_liste = np.flip(çuval_liste)
    çuval_liste = çuval_liste.astype(int)
    
    gr = np.append((f'Bayi bazında sevkedilen ürünler ve miktarları:'),gr)
    gr = np.append((f'Bayi ismi:{z} '),gr)
    for kdx,k in enumerate(kamyon_liste):
        gr = np.append((f'Kamyon Plaka: {kamyon_liste[kdx]}  Çuval Adet:{çuval_liste[kdx]}  Ürün : {dfbayi.ürün_adı.iloc[0]}'),gr)

gr = np.append((f"{date} tarihindeki toplam sipariş miktarı: {(df_['sipariş_miktarı'].sum()/1000):,.2f} ton"),gr)
gr = np.flip(gr)    

#-------------------------
#anomali rapor
indeks = dfsip['ürün_adı'].unique()
dfsil5 = pd.DataFrame(index = indeks, columns = ['ürün_miktar'])
say = 0

for ürün in indeks:
    df_ = dfsip.loc[dfsip['ürün_adı']==ürün]
    top = df_['sipariş_miktarı'].sum()/1000
    dfsil5['ürün_miktar'].iloc[say]= round(top)
    say +=1
    
dfsil5 = dfsil5.sort_values('ürün_miktar', ascending = False)
dfsil_max = dfsil5[:5]

indeks = dfsip_off['ürün_adı'].unique()
dfsil8 = pd.DataFrame(index = indeks, columns = ['karşılanamayan_miktar'])
say = 0

for ürün in indeks:
    df_ = dfsip_off.loc[dfsip_off['ürün_adı'] == ürün]
    top = df_['sipariş_miktarı'].sum()/1000
    dfsil8['karşılanamayan_miktar'].iloc[say] = round(top)
    say += 1
    
dfsil8 = dfsil8.sort_values('karşılanamayan_miktar' ,ascending =False)

liste1 = dfsil5.index[:5]
liste1 = liste1.to_list()
liste2 = dfsil8.index[:5]
liste2 = liste2.to_list()

ano_1 = (f'En çok sipariş edilen ilk 5 ürün: ')
ano_2 = (f'{str(list(liste1))[1:-1]}') 
ano_3 = (f'Siparişi en fazla geç karşılanan ilk 5 ürün: ')
ano_4 = (f'{str(list(liste2))[1:-1]}')

#--------------------------------
# 5 parça bilgi
#kartlarla ilgili kodlar
start_date = dfsip.date_pick.min()
end_date = dfsip.date_pick.max()
dfkart = dfsip.loc[(dfsip.date_pick>=start_date)&(dfsip.date_pick<=end_date)]

#kart1 toplam sipariş miktarı
kart_1 = f'{dfkart.sipariş_miktarı.sum()/1000:,.0f}'

#kart2 geciken sipariş miktarı
dfkart_2 = dfkart.loc[dfkart.zamanında==1]
kart_2 = f'{dfkart_2.sipariş_miktarı.sum()/1000:,.0f}'

#kart3 en çok gecikme yaşayan bayii
dfkart_2 = dfkart.loc[dfkart.zamanında==1]
kart_3 = f'{str(list(dfkart_2.bayii.value_counts()[:1].index))[2:-2]}'

#kart4 en çok gecikme yaşanan gün
dfkart_2 = dfkart.loc[dfkart.zamanında==1]
kart_4 = f'{str(list(dfkart_2.gün_ismi.value_counts()[:1].index))[2:-2]}'

#kart5 toplam geciken gün sayısı
dfkart_2 = dfkart.loc[dfkart.zamanında==1]
a = dfkart_2.sevk_performansı.value_counts()[1:]
kart_5 = []
for i in range(0,len(a)):
    kart_5 = np.append((f'{a.index[i]} gün {dfkart_2.sevk_performansı.value_counts()[1:].iloc[i]} adet'),kart_5)
    
kart_5 = np.flip(kart_5)

#-------------------------
#--------------- alt kısımdaki kod sabit kalacak-----------------

#Tanımlamalar
image_path = 'C:/Users/Dell/Desktop/sc genel/FM/pazarlama/solution cube logo/solution-cube-new-logo-hori.png'

def sclogo(image_file):
    with open(image_file,'rb')as f:
        image = f.read()
    return "data: image/png;base64," + base64.b64encode(image).decode('utf-8')

sayfa_başlık = html.H1('Düzgünler Yem Sanayi Sayısal İkiz Analiz Paneli',style = saybaş_sty,
                       className= saybaş_cls)               

sc_logo = html.Img(src = sclogo(image_path), height='90px', className = logo_cls)


tarih_seç = html.Div([#tarih div
    dbc.Label('Tarih seçimi',style = seçkont_lab_sty),
    dcc.DatePickerRange(id='tarih_seç',
                        start_date = min(dfsip.date_pick),
                        end_date = max(dfsip.date_pick),
                        min_date_allowed = dfsip.date_pick.min(),
                        max_date_allowed = dfsip.date_pick.max(),
                        updatemode = 'bothdates',
                        style = seçkont_gr_sty,
                        ),
    ], className = seçkont_div_cls
)#tarih div

dönem_seç = html.Div([#dropdown div
    dbc.Label('Dönem seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(dönem_list, value= dönem_list[1], multi = False, clearable = False,id= 'dönem_ismi', 
                 style = seçkont_gr_sty),
    ], className = seçkont_div_cls    
)#dropdown div

tesis_seç = html.Div([#dropdown div
    dbc.Label('Tesis seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(tesis_list, value= tesis_list[0], multi = False, id= 'tesis_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

ürün_seç = html.Div([#dropdown div
    dbc.Label('Ürün seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(ürün_list, value= ürün_list[1], multi = False, id= 'ürün_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

bayii_seç = html.Div([#dropdown div
    dbc.Label('Bayii seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(bayii_list, value= bayii_list[0], multi = False, id= 'bayii_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div   

sayfa_seç = html.Div([
    dbc.Label('Sayfa seçimi',style = sayseç_lab_sty),
    dbc.Nav([    
        dbc.NavItem(dbc.NavLink("Üretim Paneli", href="http://127.0.0.1:8072", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Enerji Paneli", href="http://127.0.0.1:8073", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Personel Paneli", href="http://127.0.0.1:8074", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Otomasyon Paneli", href="http://127.0.0.1:8075", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Otomsayon Paneli", href="http://127.0.0.1:8076", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Sipariş Paneli", active=True, href="http://127.0.0.1:8077", className = sayseç_nav_cls),
                   style = sayseç_nav_sty),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Bakım Paneli", href="http://127.0.0.1:8078", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Forklift Paneli", href="http://127.0.0.1:8079", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("OEE Paneli", href="http://127.0.0.1:8080", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        ]),
    ],className = sayseç_div_cls
)    

seçim_kontrol1 = dbc.Card([sc_logo], style = {'height':130}, 
                          className = graf_div_cls)

seçim_kontrol2 = dbc.Card([tarih_seç, tesis_seç, dönem_seç, ürün_seç, bayii_seç,sayfa_seç], style = {'height':1030}, 
                         className = graf_div_cls)

#--------------------------------
#fonksiyonlar

#kart şeklindeki 4 adet metin alanı

kart_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Toplam Sipariş Miktarı'], className="text-nowrap"),
            html.H1(kart_1, id = 'kart_1', className="fs-2 text"),
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls
)


kart_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Geciken Sipariş Miktarı'], className="text-nowrap"),
            html.H1(kart_2, id = 'kart_2', className="fs-2 text"),           
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)


kart_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Gecikme Yaşanan Bayii'], className="text-nowrap"),
            html.H1(kart_3, id = 'kart_3', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Gecikme Yaşanan Gün'], className="text-nowrap"),
            html.H1(kart_4, id = 'kart_4', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_5 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Gecikme Gün Sayısı'], className="text-nowrap"),
            html.H1(kart_5, id = 'kart_5', className="fs-5 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

solüst = html.Div([#solüst(1.grafik)
    dbc.Label(f'Bayii İsmine Göre Sipariş Miktarları Grafiği (ton)', id = 'solüst_başlık',size = 'lg', className='fw-bold'),
    dcc.Graph(id='solüst',
              figure = trace_solüst[0],
              style = graf_grph_sty   
             )], className = graf_div_cls
)#solüst(1.grafik)


solort = html.Div([#solalt(2.grafik)
    dbc.Label( f"İstenen Teslim Tarihine Göre Sipariş Miktarları Grafiği (ton)", id = 'solort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='solort',
              figure = trace_solort[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)

solalt = html.Div([#solalt(2.grafik)
    dbc.Label( f"Geciken Siparişlerin Haftanın Günlerine Göre Dağılım Grafiği (adet)", id='solalt_başlık', size = 'lg',className='fw-bold'),
    dcc.Graph(id='solalt',
              figure = trace_solalt[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)


sağüst = html.Div([#sağüst(3.grafik)
    dbc.Label(f"İstenen Teslim Tarihine Göre Toplam ve Karşılanamayan Sipariş Miktarları Grafiği (ton)", id = 'sağüst_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağüst',
              figure = trace_sağüst[0],
              style = graf_grph_sty
             )], className = graf_div_cls    
)#sağüst(3.grafik)

sağort = html.Div([#sağalt(4.grafik)
    dbc.Label( f"Bayii İsmine Göre Zamanında Karşılanamayan Sipariş Miktarları Grafiği (ton)", id = 'sağort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağort',
              figure = trace_sağort[0],
              style = graf_grph_sty
             )],  className = graf_div_cls
)#sağalt(4.grafik)

anomali = html.Div([
            dbc.Label("Anomali Raporu", size='lg',style= {'width':766,'height':50}, 
                      className = anom_label_cls),
            dcc.Textarea(id = 'anomali_rapor', 
                         value=[(f'{ano_solort1}\n{ano_solort2}\n{ano_solort3}\n{ano_solort4}\n\n{ano_solalt1}\n{str(list(ano_solalt2))[1:-1]}\n\n{ano_sağüst1}\n{ano_sağüst2}\n{ano_sağüst3}\n\n\n{ano_sağort1}\n{str(list(ano_sağort2))[1:-1]}\n\n{ano_1}\n{ano_2}\n{ano_3}\n{ano_4}\n\n')], 
                         disabled=True, readOnly=True, style = {'font-family':"Verdana",'width':766, 'height':450},
                         className = kart_göv_cls),
            ],className = graf_div_cls,
)#anomali alanı 

#----------------------------------------
gün_seç = html.Div([
    dbc.Label('Tarih ', style = {'font-size':'20px','width':172,'height':50},
                    className = anom_label_cls),    
    dcc.DatePickerSingle(id='gün_seç',
                        date = dfsip.date_pick.max(),
                        min_date_allowed = dfsip.date_pick.min(),
                        max_date_allowed = dfsip.date_pick.max(),
                        style = {'font-size':'15px','width':172,'height':50})
    ], className = seçkont_div_cls
)#gün seç alanı

rapdönem_seç = html.Div([#dropdown div
    dbc.Label('Rapor dönemi', style = {'font-size':'20px','width':172,'height':50},
                    className = anom_label_cls),
    dcc.Dropdown(rapor_list, value= rapor_list[0], multi = False, clearable = False,id= 'rapdönem_seç', 
                 style = {'font-size':'15px','width':172,'height':50}),
    ], className = seçkont_div_cls    
)#dropdown div

rap_düğme = html.Div([
    html.Button("Raporla", n_clicks=1, id="rap_düğme", style = {'font-size':'20px','width':172,'height':50},
                    className = "bg-warning text-dark border-secondary rounded-pill shadow rounded"),
    ], className = seçkont_div_cls
)#raporlama düğmesi alanı

seçim_kontrol3 = dbc.Card([gün_seç,rapdönem_seç,rap_düğme], style = {'width':172,'height':500}, 
                         className = graf_div_cls)
#---------------------------------------------------

günlük_rap = html.Div([
    dbc.Label('Günlük Rapor', size='lg',style= {'width':566,'height':50}, 
                      className = anom_label_cls),
    dcc.Textarea(id = 'günlük_rap', value=[(f'{gr}')], disabled=True, 
                     readOnly=True, style = {'font-family':"Verdana",'width':566, 'height':450},
                 className = kart_göv_cls),
    ],className=graf_div_cls
)#günlük rapor alanı


app.layout = html.Div([#div
    
        dbc.Container([#container
            dbc.Row([dbc.Col([sayfa_başlık],width=12)]),
                       
            dbc.Row([dbc.Col([seçim_kontrol1],width=1),                      
                     dbc.Col([kart_1],width=2),
                     dbc.Col([kart_2],width=2),
                     dbc.Col([kart_3],width=2),
                     dbc.Col([kart_4],width=2),
                     dbc.Col([kart_5],width=2)]),           
            
            dbc.Row([dbc.Col([seçim_kontrol2],width=1),
                     dbc.Col([solüst,solort],width =6),
                     dbc.Col([sağüst,sağort],width =5)]),
            
            dbc.Row([dbc.Col([solalt],width =4),
                     dbc.Col([anomali],width =4),
                     dbc.Col([seçim_kontrol3],width =1),
                     dbc.Col([günlük_rap],width =3)
                    ]), 
            
        ], fluid = True, className = applayout_gövde_cls)#container
    
])#div

