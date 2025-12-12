# Tanımlamalar
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)#,use_pages = True)

#---------------------
#solüst
trace_solüst = []
# ürün bazında ton başına enerji tüketimleri
fig = go.Figure()

dfürt_ind.sort_values('kwh_ton', ascending=False)
ort = dfürt_ind['kwh_ton'].mean()
dfürt_ind1 = dfürt_ind[:25]
dfürt_ind1 = dfürt_ind1.sort_values('kwh_ton', ascending=False)
isim = dfürt_ind1.index

#grafikleştirme
for idx,i in enumerate(dfürt_ind1.index):
    fig.add_trace(go.Bar(
        name=isim[idx],
        x = [dfürt_ind1.index[idx]],
        y = [dfürt_ind1['kwh_ton'].iloc[idx]],
        marker = dict(color=kol_renk.get(i)), opacity=.75,
        hovertemplate = ('<i>Ürün: </i>')+'%{x}'+
                '<br><i> Ortalama Tüketim: </i> %{y:.2f} (kWh/ton)<br>'+ 
                '<extra></extra>',
                showlegend=False
                 ))
fig.add_hline(
        y=ort,
        line_dash = 'dash',
        line_color = 'orange',
        opacity=1,
        annotation_text = (f'Ortalama {round(ort,2)} (kWh/ton)'),
        annotation_position = 'top right') 

fig.update_layout(showlegend = False,
    xaxis = dict(tickmode = 'linear'),
    yaxis = dict(gridcolor = 'lightgrey'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',                  
    #title=dict(text=(f"Ton Başına En Yüksek Ortalama Enerji Tüketen 25 Ürün (kWh/ton)")),
    hoverlabel = dict(font=dict(color='white'),bgcolor='grey')
    )

#fig.show()
trace_solüst = np.append(fig,trace_solüst)

#----------------------- 
#solort
trace_solort = []
#gün bazında toplam üretim ve toplam elektrik tüketimi oranlaması ve metrik oluşturma
fig = go.Figure()
dönem = 'gün'

indeks = dfürt.gün.unique()
dfsil10 = pd.DataFrame(index = indeks, columns=['tarih','top_en','top_ürt','oran'])

for idx,i in enumerate(indeks):
    dfgün_en = dfen.loc[dfen['gün']==i]
    dfgün_ür = dfürt.loc[dfürt['gün']==i]
    dfsil10['tarih'].iloc[idx] = dfgün_ür.index[0]
    dfsil10['top_en'].iloc[idx] = dfgün_en[hat_enrj].sum().sum()
    dfsil10['top_ürt'].iloc[idx] = dfgün_ür[hat_ürt].sum().sum()
    dfsil10['oran'].iloc[idx] = round(dfgün_ür[hat_ürt].sum().sum()/dfgün_en[hat_enrj].sum().sum(),2)
    
ort = dfsil10.oran.mean()
üst_sınır = ort + (1*dfsil10.oran.std())
alt_sınır = ort - (1*dfsil10.oran.std())

sınır_aşan = dfsil10.loc[dfsil10.oran>üst_sınır]
sınır_altı = dfsil10.loc[dfsil10.oran<alt_sınır]

tarih1 = sınır_aşan.tarih
tarih2 = sınır_altı.tarih

#grafikleştirme
fig.add_trace(go.Bar(
    name = str(indeks),
    x = dfsil10.tarih,
    y = dfsil10['oran'],
    marker = dict(color='green', opacity= 0.75),
    hovertemplate = ('<i>Tarih: </i>')+'%{x}'+
                '<br><i>Enerji Miktarı: </i> %{y:.2f} (kWh)<br>'+ 
                '<extra></extra>',
    showlegend=False
    ))
fig.add_trace(go.Scatter(
    x = sınır_aşan.tarih,
    y = sınır_aşan.oran,
    mode = 'markers',
    marker = dict(color = 'red'),
    opacity = .75,
    ))

fig.add_trace(go.Scatter(
    x = sınır_altı.tarih,
    y = sınır_altı.oran,
    mode = 'markers',
    marker = dict(color = 'brown'),
    opacity = .75,
    ))

fig.add_hline(
    y = ort,
    line_dash='dash',
    line_color='orange',
    opacity=1,
    annotation_text = (f'Ortalama {round(ort,2)}'),
    annotation_position = 'top right')

fig.add_hline(
    y = üst_sınır,
    line_dash='dash',
    line_color='indianred',
    opacity=.75,
    annotation_text = (f'Üst Sınır {round(üst_sınır,2)}'),
    annotation_position = 'top right')


fig.add_hline(
    y = alt_sınır,
    line_dash='dash',
    line_color='indianred',
    opacity=.75,
    annotation_text = (f'Üst Sınır {round(alt_sınır,2)}'),
    annotation_position = 'top right')


fig.update_layout(
    showlegend = False,
    xaxis=dict(tickmode = 'array', range=[dfsil10.tarih.min(), dfsil10.tarih.max()]),
    yaxis = dict(range=[0,dfsil10.oran.max()+5],gridcolor = 'lightgrey'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',                  
    #title = dict(text='Günlük Bazda 1 kg Ürün Üretmek İçin Gereken Enerji Miktarı Grafiği (kWh)'),
    hoverlabel = dict(font=dict(color='white'),bgcolor='grey')
    )

#fig.show()

#######################
#anomali rapor
ort = dfsil10.oran.mean()
üst_sınır = ort + dfsil10.oran.std()
sınır_aşan = dfsil10.loc[dfsil10.oran>üst_sınır]
tarih = sınır_aşan.tarih

liste = []
for idx,i in enumerate(tarih):
    qqq = str(tarih.iloc[idx]).split(sep='-')
    liste = np.append(qqq[1],liste)

ay,adet = np.unique(liste, return_counts=True)
sıklık = np.asarray((adet,ay)).T
sıklık = np.flip(sıklık[sıklık[:,0].argsort()])

df_anomali = pd.DataFrame(sıklık,columns=['ay','sıklık'])
df_anomali['oran'] = np.zeros(len(df_anomali))
df_anomali = df_anomali.astype(int)

for i in df_anomali.index:
    df_anomali.oran.iloc[i] = round(100*(df_anomali.sıklık.iloc[i]/df_anomali.sıklık.sum()),2)
    
df_anomali = df_anomali.sort_values('oran',ascending = False)
global metin_ano
metin_ano = (f'Birim enerji miktar aşımlarının;')
for i in df_anomali.index:
    metin_ano = metin_ano + (f'%{df_anomali.oran.iloc[i]} {df_anomali.ay.iloc[i]}. ayda,')
    #metin_ano = metin_ano + (f'meydana gelmiştir.')
metin_ano = metin_ano + (f'Birim enerji miktar aşımlarının yoğun olarak meydana geldiği aylar: {str(list(df_anomali.ay[:4]))[1:-1]}')

trace_solort = np.append(fig,trace_solort)
   
#------------------------
#sağüst
trace_sağüst = []
#seçili tarih aralığında ve ekipman bazında toplam enerji tüketimi
fig = go.Figure()

start_date = dfen.date_pick.min()
end_date = dfen.date_pick.max()
dftarih = dfen.loc[(dfen.date_pick>=start_date)&(dfen.date_pick<=end_date)]

alt_top = dftarih[hat_kolon].sum()
global sz
sz = 40

#grafikleştirme
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[0],
    title = dict(text='Hat 1 Pres'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[1],
    title = dict(text='Hat 1 Ekspander'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[2],
    title = dict(text='Hat 1 Kondüsyoner'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':2}))
#fig.add_trace(go.Indicator(
    #mode = "number",
    #value = alt_top[0]+alt_top[3]+alt_top[6]+alt_top[9],
    #title = dict(text='Pres Toplam'),
    #number={"font":{"size":sz}},
    #domain = {'row':4,'column':0})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[3],
    title = dict(text='Hat 2 Pres'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[4],
    title = dict(text='Hat 2 Ekspander'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[5],
    title = dict(text='Hat 2 Kondüsyoner'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':2}))
#fig.add_trace(go.Indicator(
    #mode = "number",
    #value = alt_top[1]+alt_top[4]+alt_top[7]+alt_top[10],
    #title = dict(text='Ekspander Toplam'),
    #number={"font":{"size":sz}},
    #domain = {'row':4,'column':1})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[6],
    title = dict(text='Hat 3 Pres'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[7],
    title = dict(text='Hat 3 Ekspander'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[8],
    title = dict(text='Hat 3 Kondüsyoner'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':2}))
#fig.add_trace(go.Indicator(
    #mode = "number",
    #value = alt_top[2]+alt_top[5]+alt_top[8]+alt_top[11],
    #title = dict(text='Kondüsyoner Toplam'),
    #number={"font":{"size":sz}},
    #domain = {'row':4,'column':2})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[9],
    title = dict(text='Hat 4 Pres'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[10],
    title = dict(text='Hat 4 Ekspander'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = alt_top[11],
    title = dict(text='Hat 4 Kondüsyoner'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':2})) 

fig.update_layout(
    grid = {'rows': 5, 'columns': 3, 'pattern': "independent"},
    title=dict(text=(f'Tarih: {tarih1} - {tarih2}   Ekipman Enerji Tüketimleri (kWh)')))

#fig.show()

trace_sağüst = np.append(fig,trace_sağüst)

#-------------------------
#sağort
trace_sağort = []
#hat bazında seçilen yemin toplam günlük üretim miktarı ve toplam çalışma zamanı ve harcanan enerji (1.hat, 2,hat vb.)
#seçili üründen çıkan ıskarta miktarı da raporlanacak.
fig = go.Figure()
h1_ısk_yüzde = np.random.uniform(0,0.0002)
h2_ısk_yüzde = np.random.uniform(0,0.0001)
h3_ısk_yüzde = np.random.uniform(0,0.00015)
h4_ısk_yüzde = np.random.uniform(0,0.00025)


start_date = dfürt.date_pick.min()
end_date = dfürt.date_pick.max()
dftarih = dfürt.loc[(dfürt.date_pick>=start_date)&(dfürt.date_pick<=end_date)]

ürün = '20 A'

dfür1 = dftarih.loc[dftarih['pr1_ürün'] == ürün]
dfür2 = dftarih.loc[dftarih['pr2_ürün'] == ürün]
dfür3 = dftarih.loc[dftarih['pr3_ürün'] == ürün]
dfür4 = dftarih.loc[dftarih['pr4_ürün'] == ürün]

h1_süre = len(dfür1)
h1_miktar = round(dfür1['pr1_miktar'].sum()/1000)
if h1_süre!=0:
    h1_hız = h1_miktar*1000/h1_süre
elif h1_süre == 0:
    h1_hız=0
h1_ıskarta = round(h1_miktar*h1_ısk_yüzde*1000,2) #kg tekrar çevirmek için

h2_süre = len(dfür2)
h2_miktar = round(dfür2['pr2_miktar'].sum()/1000)
if h2_süre!=0:
    h2_hız = h2_miktar*1000/h2_süre    
else:
    h2_hız=0
h2_ıskarta = h2_miktar*h2_ısk_yüzde*1000 #kg tekrar çevirmek için

h3_süre = len(dfür3)
h3_miktar = round(dfür3['pr3_miktar'].sum()/1000)
if h3_süre!=0:
    h3_hız = h3_miktar*1000/h3_süre
else:
    h3_hız =0
h3_ıskarta = h3_miktar*h3_ısk_yüzde*1000 #kg tekrar çevirmek için

h4_süre = len(dfür4)
h4_miktar = dfür4['pr4_miktar'].sum()/1000
if h4_süre!=0:
    h4_hız = round(h4_miktar*1000/h4_süre)
else:
    h4_hız=0
h4_ıskarta = h4_miktar*h4_ısk_yüzde*1000 #kg tekrar çevirmek için

#grafikleştirme
fig.add_trace(go.Indicator(
    mode = "number",
    value = h1_miktar,
    title = dict(text='Hat 1 miktar(ton)'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h1_süre,
    title = dict(text='Hat 1 süre(dk)'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h1_ıskarta,
    title = dict(text='Hat 1 ıskarta(kg)'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':2})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h1_hız,
    title = dict(text='Hat 1 hız(kg/dk)'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':3})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = h2_miktar,
    title = dict(text='Hat 2 miktar(ton)'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h2_süre,
    title = dict(text='Hat 2 süre(dk)'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h2_ıskarta,
    title = dict(text='Hat 2 ıskarta(kg)'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':2})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h2_hız,
    title = dict(text='Hat 2 hız(kg/dk)'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':3})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = h3_miktar,
    title = dict(text='Hat 3 miktar(ton)'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h3_süre,
    title = dict(text='Hat 3 süre(dk)'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h3_ıskarta,
    title = dict(text='Hat 3 ıskarta(kg)'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':2}))
fig.add_trace(go.Indicator(
    mode = "number",
    value = h3_hız,
    title = dict(text='Hat 3 hız(kg/dk)'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':3})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = h4_miktar,
    title = dict(text='Hat 4 miktar(ton)'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h4_süre,
    title = dict(text='Hat 4 süre(dk)'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = h4_ıskarta,
    title = dict(text='Hat 4 ıskarta(kg)'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':2}))
fig.add_trace(go.Indicator(
    mode = "number",
    value = h4_hız,
    title = dict(text='Hat 4 hız(kg/dk)'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':3})) 


fig.update_layout(
    grid = {'rows': 4, 'columns': 4, 'pattern': "independent"},
    title=dict(text=(f'Tarih: {tarih1} - {tarih2}   Ürün: {ürün}  Günlük Rapor')))

#fig.show()

trace_sağort = np.append(fig,trace_sağort)

#-------------------------
trace_solalt = []
#Seçili Tarih ve Hat Bazında Ekipmanların Elektrik Tüketim Dağılım Grafiği
fig = go.Figure()

start_date = dfen.date_pick.min()
end_date = dfen.date_pick.max()
dftarih = dfen.loc[(dfen.date_pick>=start_date)&(dfen.date_pick<=end_date)]

dftarih = dfen.loc[(dfen.date_pick>=start_date)&(dfen.date_pick<=end_date)]

indeks = np.arange(1)
dfsil1 = pd.DataFrame(index = indeks, columns = hat_enrj)

for idx,i in enumerate(hat_enrj):
    dfsil1[i].iloc[0] = dftarih[i].sum()

dfsil1 = dfsil1.transpose()

#grafikleştirme
fig.add_trace(go.Pie(labels = kolon_isim, values = dfsil1[0], opacity = 0.7))

fig.update_traces(
    hoverinfo = 'label+percent',
    textinfo = 'label+percent+value',
    textfont_size=10,
    marker=dict(line=dict(color='black', width=1)),
    hovertemplate = ('<i>Ekipman: </i>')+'%{label}'+
                '<br><i>Enerji Tüketim: </i> %{value} (kWh)'+ 
                '<br><i>Oran: </i> %{percent} (%)<br>'+
                '<extra></extra>',
    showlegend = False
    ) 

fig.update_layout(
    title=dict(text=(f'Enerji Tüketiminin Ekipmanlara Göre Dağılımları (kWh)')),
    hoverlabel = dict(font=dict(color='white'),bgcolor='grey')
)
    
#fig.show()

trace_solalt = np.append(fig,trace_solalt)

#---------------------------
#günlük rapor


#--------------------------------
# 5 parça bilgi
# üretim miktarı, datepickerrange ile paralel
#kartlar için kod
# kart1 Toplam Enerji Tüketimi
start_date = dfen.date_pick.min()
end_date = dfen.date_pick.max()

dftarih_en = dfen.loc[(dfen.tarih>=start_date)&(dfen.tarih<=end_date)]
kart_1 = (f'{dftarih_en[hat_enrj].sum().sum():,.0f}')

#kart2 Toplam Üretim Miktarı
dftarih_ürt = dfürt.loc[(dfürt.tarih>=start_date)&(dfürt.tarih<=end_date)]
kart_2 = (f'{dftarih_ürt[hat_ürt].sum().sum():,.0f}')

#kart3 Toplam Çalışma Süresi
hat1 = len(dftarih_ürt.loc[dftarih_ürt.pr1_miktar!=0])
hat2 = len(dftarih_ürt.loc[dftarih_ürt.pr2_miktar!=0])
hat3 = len(dftarih_ürt.loc[dftarih_ürt.pr3_miktar!=0])
hat4 = len(dftarih_ürt.loc[dftarih_ürt.pr4_miktar!=0])
kart_3 = (f'{hat1+hat2+hat3+hat4:,.0f}')

#kart4 Preslerin Tüketimi
pres_kol = dfen.columns[4:14:3]
kart_4 = (f'{dftarih_en[pres_kol].sum().sum():,.0f}')

#kart5 Preslerin Ton Başına Elektrik Tüketimi
kart_5 = (f'{1000*(dftarih_en[pres_kol].sum().sum()/dftarih_ürt[hat_ürt].sum().sum()):,.2f}')

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
                        start_date = min(dfen.date_pick),
                        end_date = max(dfen.date_pick),
                        min_date_allowed = dfen.date_pick.min(),
                        max_date_allowed = dfen.date_pick.max(),
                        updatemode = 'bothdates',
                        style = seçkont_gr_sty,
                        ),
    ], className = seçkont_div_cls
)#tarih div

tesis_seç = html.Div([#dropdown div
    dbc.Label('Tesis seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(tesis_list, value= tesis_list[0], multi = False, id= 'tesis_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

dönem_seç = html.Div([#dropdown div
    dbc.Label('Dönem seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(dönem_list, value= dönem_list[1], multi = False, clearable = False,id= 'dönem_ismi', 
                 style = seçkont_gr_sty),
    ], className = seçkont_div_cls    
)#dropdown div


ürün_seç = html.Div([#dropdown div
    dbc.Label('Ürün seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(ürün_list, value= ürün_list[1], multi = False, id= 'ürün_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

hat_seç = html.Div([#dropdown div
    dbc.Label('Hat seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(hat_kısalist, value= hat_kısalist[0], multi = False, id= 'hat_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div   

sayfa_seç = html.Div([
    dbc.Label('Sayfa seçimi',style = sayseç_lab_sty),
    dbc.Nav([    
        dbc.NavItem(dbc.NavLink("Üretim Paneli",  href="http://127.0.0.1:8072", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Enerji Paneli", active=True, href="http://127.0.0.1:8073", className = sayseç_nav_cls),
                   style = sayseç_nav_sty
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
        dbc.NavItem(dbc.NavLink("Otomasyon Paneli", href="http://127.0.0.1:8076", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Sipariş Paneli", href="http://127.0.0.1:8077", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
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

seçim_kontrol2 = dbc.Card([tarih_seç, tesis_seç, dönem_seç, ürün_seç, hat_seç,sayfa_seç], style = {'height':1030}, 
                         className = graf_div_cls)

#--------------------------------
#fonksiyonlar

#kart şeklindeki 4 adet metin alanı

kart_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Toplam Tüketim (kWh)'], className="text-nowrap"),
            html.H1(kart_1, id = 'kart_1', className="fs-2 text"),
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls
)


kart_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Toplam Üretim (ton)'], className="text-nowrap"),
            html.H1(kart_2, id = 'kart_2', className="fs-2 text"),           
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)


kart_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Toplam Süre (dk)'], className="text-nowrap"),
            html.H1(kart_3, id = 'kart_3', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Presler Tüketim (kWh)'], className="text-nowrap"),
            html.H1(kart_4, id = 'kart_4', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_5 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Pres Tüketim (kWh/ton)'], className="text-nowrap"),
            html.H1(kart_5, id = 'kart_5', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

solüst = html.Div([#solüst(1.grafik)
    dbc.Label(f'Ürün bazında ton başına enerji tüketimleri (kWh/ton)', id = 'solüst_başlık',size = 'lg', className='fw-bold'),
    dcc.Graph(id='solüst',
              figure = trace_solüst[0],
              style = graf_grph_sty   
             )], className = graf_div_cls
)#solüst(1.grafik)


solort = html.Div([#solalt(2.grafik)
    dbc.Label( f"Günlük Bazda 1 kg Ürün Üretmek İçin Gereken Enerji Miktarı Grafiği (kWh)", id = 'solort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='solort',
              figure = trace_solort[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)

solalt = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Tarih ve Hat Bazında Ekipmanların Elektrik Tüketim Dağılım Grafiği", id='solalt_başlık', size = 'lg',className='fw-bold'),
    dcc.Graph(id='solalt',
              figure = trace_solalt[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)


sağüst = html.Div([#sağüst(3.grafik)
    dbc.Label(f"Seçili Tarih Aralığında ve Ekipman Bazında Toplam Enerji Tüketimi", id = 'sağüst_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağüst',
              figure = trace_sağüst[0],
              style = graf_grph_sty
             )], className = graf_div_cls    
)#sağüst(3.grafik)

sağort = html.Div([#sağalt(4.grafik)
    dbc.Label( f"Seçili Tarih Aralığında Hat ve Ürün Bazında Günlük Üretim Miktarı, Çalışma Süresi ve Enerji Tüketimi", id = 'sağort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağort',
              figure = trace_sağort[0],
              style = graf_grph_sty
             )],  className = graf_div_cls
)#sağalt(4.grafik)

anomali = html.Div([
            dbc.Label("Anomali Raporu", size='lg',style= {'width':766,'height':50}, 
                      className = anom_label_cls),
            dcc.Textarea(id = 'anomali_rapor', value=[f'{metin_ano}\n\n'], 
                         disabled=True, readOnly=True, style = {'font-family':"Verdana",'width':766, 'height':450},
                         className = kart_göv_cls),
            ],className = graf_div_cls,
)#anomali alanı 

#----------------------------------------
gün_seç = html.Div([
    dbc.Label('Tarih ', style = {'font-size':'20px','width':172,'height':50},
                    className = anom_label_cls),    
    dcc.DatePickerSingle(id='gün_seç',
                        date = dfürt.date_pick.max(),
                        min_date_allowed = dfürt.date_pick.min(),
                        max_date_allowed = dfürt.date_pick.max(),
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
    dcc.Textarea(id = 'günlük_rap', value=[], disabled=True, 
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

