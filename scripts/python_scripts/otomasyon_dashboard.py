# Tanımlamalar
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)#,use_pages = True)

#---------------------
#solüst
trace_solüst = []
#histogram
giriş = 'Hat 2 Ekspander Hidrolik Basıncı'
kolon = oto_dict2.get(giriş)

hat_no = [x for x in kolon][3]
if hat_no == '1':
    df = dfotom1
elif hat_no == '2':
    df = dfotom2
elif hat_no == '3':
    df = dfotom3
elif hat_no == '4':
    df = dfotom4    
    
#histogram  
alt_sınırN = np.floor(df[kolon].median()-(df[kolon].std()))
üst_sınırN = np.ceil(df[kolon].median()+(df[kolon].std()))

q1= df[kolon].quantile(0.25)
q3= df[kolon].quantile(0.75)
alt_sınır = q1-(1.5*(q3-q1))
üst_sınır = q3+(1.5*(q3-q1))

        
fig = go.Figure()
fig.add_trace(go.Histogram(
    x=df[kolon],
    name= kolon,
    xbins = dict(start=df[kolon].min(), end=df[kolon].max(), size = (df[kolon].max()-df[kolon].min())/20),
    marker_color= oto_renk.get(giriş),
    opacity=0.5,
    hovertemplate = (f'<i>Değer Aralığı: </i>')+'%{x}'+
                '<br><i>Adet:</i> %{y}<br>'+ '<i>Otomasyon Verisi: </i>'+(f'{oto_dict1.get(kolon)}') +'<extra></extra>',
    showlegend = False
))

fig.add_vrect(x0=df[kolon].median(), x1= df[kolon].median(), line_dash="dash", line_color= 'green',opacity=0.5,
             annotation_text = (f'Ortalama değer : {round(df[kolon].median(),2)}'),
             annotation_position="bottom left")

fig.add_vrect(x0=alt_sınırN, x1= alt_sınırN, line_dash="dash", line_color= 'green',opacity=0.5,
             annotation_text = (f'NÇA {int(alt_sınırN)}-{int(üst_sınırN)}'),
             annotation_position="inside left")

fig.add_vrect(x0=üst_sınırN, x1= üst_sınırN, line_dash="dash", line_color= 'green',opacity=0.5,
             annotation_text = (f'NÇA {int(alt_sınırN)}-{int(üst_sınırN)}'),
             annotation_position="inside left")

fig.add_vrect(x0=alt_sınır, x1= alt_sınır, line_dash="dash", line_color= 'red',opacity=0.5,
             annotation_text = (f'Uç değer alt sınırı {int(alt_sınır)}'),
             annotation_position="inside left")

fig.add_vrect(x0=üst_sınır, x1= üst_sınır, line_dash="dash", line_color= 'red',opacity=0.5,
             annotation_text = (f'Uç değer üst sınırı {int(üst_sınır)}'),
             annotation_position="inside left")

fig.update_layout(
    title_text= (f'Seçili Parametre: {oto_dict1.get(kolon)}'), 
    xaxis_title_text='Değer', 
    yaxis_title_text='Adet',
    yaxis = dict(gridcolor = 'lightgrey'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    hoverlabel = dict(font=dict(color='white'),bgcolor='grey')
)

#fig.show()

trace_solüst = np.append(fig,trace_solüst)

#----------------------- 
#solort
trace_solort = []
#arıza sıklıkları ile nça dışı değerlerin korelasyon grafiği
giriş = 'Hat 2 Ekspander Hidrolik Basıncı'
kolon = oto_dict2.get(giriş)

dönem = 'hafta'

if '1ex' in kolon:
    df = dfotom1
    ekipman = 'ex'.capitalize()+'pander-1'
elif '1pr' in kolon:
    df = dfotom1
    ekipman = 'pr'.capitalize()+'es-1'
elif '1kd' in kolon:
    df= dfotom1
    ekipman = 'k'.capitalize()+'ondisyonel-1'
elif '2ex' in kolon:
    df = dfotom2
    ekipman = 'ex'.capitalize()+'pander-2'
elif '2pr' in kolon:
    df = dfotom2
    ekipman = 'pr'.capitalize()+'es-2'
elif '2kd' in kolon:
    df= dfotom2
    ekipman = 'k'.capitalize()+'ondisyonel-2'

elif '3ex' in kolon:
    df = dfotom3
    ekipman = 'ex'.capitalize()+'pander-3'
elif '3pr' in kolon:
    df = dfotom3
    ekipman = 'pr'.capitalize()+'es-3'
elif '3kd' in kolon:
    df= dfotom3
    ekipman = 'k'.capitalize()+'ondisyonel-3'

elif '4ex' in kolon:
    df = dfotom4
    ekipman = 'ex'.capitalize()+'pander-4'
elif '4pr' in kolon:
    df = dfotom4
    ekipman = 'pr'.capitalize()+'es-4' 
elif '4kd' in kolon:
    df= dfotom4
    ekipman = 'k'.capitalize()+'ondisyonel-4'
    
global dfsil61, dfsil62
df_ekip = df_arıza.loc[df_arıza['ekipman_adı']==ekipman]
indeks = df_ekip[dönem].unique()
dfsil61 = pd.DataFrame(index = indeks, columns=['arıza_süre'])

for idx,i in enumerate(indeks):
    a = df_ekip.loc[df_ekip[dönem]==i]
    dfsil61['arıza_süre'].iloc[idx] = a.müdahale_süresi.sum()
    
#nça dışı değerler df
hat_no = [x for x in kolon][3]
if hat_no == '1':
    df = dfotom1
elif hat_no == '2':
    df = dfotom2
elif hat_no == '3':
    df = dfotom3
elif hat_no == '4':
    df = dfotom4    
    
alt_sınırN = np.floor(df[kolon].median()-(df[kolon].std()))
üst_sınırN = np.ceil(df[kolon].median()+(df[kolon].std()))

df_ = df.loc[(df[kolon]<alt_sınırN)|(df[kolon]>üst_sınırN)]
df_ = df_.resample('H').asfreq() #dakika hassasiyetindeki veriyi saat hassasiyetine dönüştürmek için.

indeks = df_[dönem].unique()
dfsil62 = pd.DataFrame(index = indeks, columns=['NÇA_dışı'])
#anomali değerleri
for idx,i in enumerate(indeks):
    dfdönem = df_.loc[df_[dönem]==i]
    dfsil62['NÇA_dışı'].iloc[idx] = len(dfdönem[kolon])
    
#iki farklı ölçekteki değer grubunu eşdeğer hale getrimek için
pay = dfsil62.NÇA_dışı.max() 
payda = dfsil61.arıza_süre.max()
if pay>payda:
    çarp = pay/payda
else:
    çarp = payda/pay    
    

#grafikleştirme
fig = go.Figure()

fig.add_trace(go.Scatter(name='NÇA dışı değerler',
    x = dfsil62.index,
    y = dfsil62['NÇA_dışı']*çarp,
    mode = 'lines',
    marker = dict(color = 'red'),
    opacity = .4,
    hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                '<br><i>Adet:</i> %{y}<br>'+ '<extra></extra>',
    showlegend=True))

fig.add_trace(go.Bar(name='Arızalı süreler',
    x = dfsil61.index,
    y = dfsil61['arıza_süre'],
    width = 1,
    marker = dict(color = oto_renk.get(giriş)),
    opacity = 0.5,
    hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                '<br><i>Süre:</i> %{y} (dk)<br>'+ '<extra></extra>',
    showlegend=True))

fig.update_layout(
    xaxis = dict(tickmode='auto',range=[df_[dönem].min(),df_[dönem].max()]),
    xaxis_title_text=(f'{dönem.capitalize()}'),
    yaxis = dict(tickmode= 'auto',gridcolor = 'lightgrey'),
    yaxis_title_text='Süre (dk)',
    title = dict(text=f'Seçili Parametre : {oto_dict1.get(kolon)}'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    hoverlabel = dict(font=dict(color='white'),bgcolor='grey')
)
#fig.show()

# anomali kodlaması
dfsil62['arıza_süre'] = np.ones(len(dfsil62))
dfsil62 = dfsil62.iloc[1:]
dfsil62.index = dfsil62.index.astype('int64')

for idx,i in enumerate(dfsil61.index):
    a = dfsil61.arıza_süre.iloc[idx]
    b= dfsil61.index[idx]
    for ndx,n in enumerate(dfsil62.index):
        if dfsil62.index[ndx]==b:
            dfsil62.arıza_süre.iloc[ndx] = a
    
nça_max = dfsil62.sort_values('NÇA_dışı', ascending=False)
arıza_max = dfsil62.sort_values('arıza_süre', ascending=False)
nça_maxDönem = nça_max.index[:5]
nça_maxDönem = nça_maxDönem.sort_values()
nça_maxDönem = nça_maxDönem[~np.isnan(nça_maxDönem)]
nça_maxDönem = nça_maxDönem.astype(int)

arıza_maxDönem = arıza_max.index[:5]
arıza_maxDönem = arıza_maxDönem.sort_values()
arıza_maxDönem = arıza_maxDönem[~np.isnan(arıza_maxDönem)]
arıza_maxDönem = arıza_maxDönem.astype(int)

global oto_ano1,oto_ano2,oto_ano3
oto_ano1 = (f'Normal Çalışma Aralığı dışı değerlerin en fazla görüldüğü {dönem}lar : {(str(nça_maxDönem)[12:-17])}')
oto_ano2 = (f'Arıza sürelerinin en yüksek görüldüğü {dönem}lar : {(str(arıza_maxDönem)[12:-17])}')
ortak = (set(nça_maxDönem)&set(arıza_maxDönem))
ortak = (set(nça_maxDönem)&set(arıza_maxDönem))
if ortak == set():
    oto_ano3 = ('İki veri setinin ortak bir dönemleri yoktur.')
else:
    oto_ano3 = (f'İki veri setinin ortak dönemleri : {str(list(ortak))[1:-1]}. {dönem}')

trace_solort = np.append(fig,trace_solort)
   
#------------------------
#sağüst
trace_sağüst = []
#NÇA değer aşım grafiği

giriş = 'Hat 2 Ekspander Hidrolik Basıncı'
kolon = oto_dict2.get(giriş)

hat_no = [x for x in kolon][3]
if hat_no == '1':
    df = dfotom1
elif hat_no == '2':
    df = dfotom2
elif hat_no == '3':
    df = dfotom3
elif hat_no == '4':
    df = dfotom4    
    
alt_sınırN = np.floor(df[kolon].median()-(df[kolon].std()))
üst_sınırN = np.ceil(df[kolon].median()+(df[kolon].std()))

df_ = df.loc[(df[kolon]<alt_sınırN)|(df[kolon]>üst_sınırN)]
df_ = df_.resample('H').asfreq() #dakika hassasiyetindeki veriyi saat hassasiyetine dönüştürmek için.

#grafikleştirme
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_.index,
    y=df_[kolon],
    name= kolon, 
    mode = 'lines',
    marker_color='#330C73',
    opacity=0.5,
    showlegend=False
))

fig.add_trace(go.Scatter(
    x=df_.index,
    y=df_[kolon],
    name= kolon, 
    mode = 'markers',
    marker_color='red',
    opacity=0.5,
    hovertemplate = (f'<i>Tarih: : </i>')+'%{x}'+
                '<br><i>Değer:</i> %{y:.2f}<br>'+ '<i>Otomasyon Verisi: </i>'+(f'{kolon}') +'<extra></extra>',
    showlegend=False))

fig.add_hline(y=alt_sınırN, line_dash="dot", line_color= 'green', opacity=.5,
             annotation_text = (f'NÇA alt sınırı: {int(alt_sınırN)}'),
             annotation_position="bottom right")
fig.add_hline(y=üst_sınırN, line_dash="dot", line_color= 'green', opacity = 0.5,
             annotation_text = (f'NÇA üst sınırı: {int(üst_sınırN)}'),
             annotation_position="top right")

fig.update_layout(
    title_text= (f'Seçili Parametre: {oto_dict1.get(kolon)}'), 
    xaxis_title_text='Zaman', 
    yaxis_title_text='Değer',
    yaxis = dict(gridcolor = 'lightgrey'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    hoverlabel = dict(font=dict(color='white'),bgcolor='grey')
)
#fig.show()

# şekil 5 anomali kodlaması
a = df_.index
liste = []
for idx,i in enumerate(a):
    qqq = str(a[idx]).split(sep='-')
    liste = np.append(qqq[1],liste)

ay,adet = np.unique(liste, return_counts=True)
sıklık = np.asarray((adet,ay)).T
sıklık = np.flip(sıklık[sıklık[:,0].argsort()])

df_anomali = pd.DataFrame(sıklık,columns=['ay','sıklık'])
df_anomali['oran'] = np.zeros(len(df_anomali))
df_anomali = df_anomali.astype(int)

for i in df_anomali.index:
    df_anomali.oran.iloc[i] = round(100*(df_anomali.sıklık.iloc[i]/df_anomali.sıklık.sum()),2)
    
oto_ano4 = (f'Değer aşımlarının;')
oto_ano5 = ' '
for i in df_anomali.index:
    oto_ano5 = oto_ano5 + (f'%{df_anomali.oran.iloc[i]} {df_anomali.ay.iloc[i]}. ayda,')
oto_ano5 = oto_ano5 + (f'meydana gelmiştir.\n')
oto_ano6 = (f'Değer aşımlarının yoğun olarak meydana geldiği aylar: {str(list(df_anomali.ay[:4]))[1:-1]}')
    
trace_sağüst = np.append(fig,trace_sağüst)

#-------------------------
#sağort
trace_sağort = []
ürün = '20 A'
dönem = 'hafta'
giriş = 'Hat 2 Ekspander Hidrolik Basıncı'
kolon = oto_dict2.get(giriş)
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

if '1' in kolon:
    df = dfotom1
    hat = 'hat1'
elif '2' in kolon:
    df = dfotom2
    hat = 'hat2'
elif '3' in kolon:
    df = dfotom3
    hat = 'hat3'
else:
    df = dfotom4
    hat = 'hat4'

indeks = df[dönem].unique()
dfsil71 = pd.DataFrame(index=indeks, columns = ['ortalama'])

for idx, i in enumerate(dfsil71.index):
    dfdönem = df.loc[df[dönem]==i]
    dfürün = dfdönem.loc[dfdönem[hat]==ürün]
    dfsil71['ortalama'].iloc[idx] = dfürün[kolon].mean()

#nça dışı değerler df
hat_no = [x for x in kolon][3]
if hat_no == '1':
    df = dfotom1
elif hat_no == '2':
    df = dfotom2
elif hat_no == '3':
    df = dfotom3
elif hat_no == '4':
    df = dfotom4    
    
alt_sınırN = np.floor(df[kolon].median()-(df[kolon].std()))
üst_sınırN = np.ceil(df[kolon].median()+(df[kolon].std()))

df_ = df.loc[(df[kolon]<alt_sınırN)|(df[kolon]>üst_sınırN)]
df_ = df_.resample('H').asfreq() #dakika hassasiyetindeki veriyi saat hassasiyetine dönüştürmek için.

indeks = df_[dönem].unique()
dfsil72 = pd.DataFrame(index = indeks, columns=['NÇA_dışı'])
#anomali değerleri
for idx,i in enumerate(indeks):
    df_dönem = df_.loc[df_[dönem]==i]
    df_ürün = df_dönem.loc[df_dönem[hat]==ürün]    
    dfsil72['NÇA_dışı'].iloc[idx] = len(df_dönem[kolon])
    
if dönem == 'gün':
    dfsil72 = dfsil72
else:
    dfsil72 = dfsil72[1:]
    
#iki farklı ölçekteki değer grubunu eşdeğer hale getrimek için
pay = dfsil72.NÇA_dışı.max() 
payda = dfsil71.ortalama.max()
if pay>payda:
    çarp = pay/payda
else:
    çarp = payda/pay 
    
#grafikleştirme
fig = go.Figure()

fig.add_trace(go.Scatter(name='NÇA dışı değerler',
    x = dfsil72.index,
    y = dfsil72['NÇA_dışı']*çarp,
    mode = 'lines',
    marker = dict(color = 'red'),
    opacity = .4,
    hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                '<br><i>Adet:</i> %{y}<br>'+ '<extra></extra>',
    showlegend=True))

fig.add_trace(go.Bar(name=(f'Parametre Ortalamaları'),
    x = dfsil71.index,
    y = dfsil71['ortalama'],
    width = 1,
    marker = dict(color = oto_renk.get(giriş)),
    opacity=0.5,
    hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                '<br><i>Süre:</i> %{y} (dk)<br>'+ '<extra></extra>',
    showlegend=True))

fig.update_layout(
    xaxis = dict(tickmode= tick,range=[df_[dönem].min(),df_[dönem].max()]),
    xaxis_title_text=(f'{dönem.capitalize()}'),
    yaxis = dict(tickmode= 'auto',gridcolor = 'lightgrey'),    
    yaxis_title_text='Süre (dk)',
    title = dict(text=f'Seçili Ürün: {ürün} Seçili Parametre : {oto_dict1.get(kolon)}'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    hoverlabel = dict(font=dict(color='white'),bgcolor='grey')
)
#fig.show()

# anomali kodlaması
dfsil72['arıza_süre'] = np.ones(len(dfsil72))
dfsil72 = dfsil72.iloc[1:]
dfsil72.index = dfsil72.index.astype('int64')

for idx,i in enumerate(dfsil71.index):
    a = dfsil71['ortalama'].iloc[idx]
    b= dfsil71.index[idx]
    for ndx,n in enumerate(dfsil72.index):
        if dfsil72.index[ndx]==b:
            dfsil72['arıza_süre'].iloc[ndx] = a
    
nça_max = dfsil72.sort_values('NÇA_dışı', ascending=False)
arıza_max = dfsil72.sort_values('arıza_süre', ascending=False)
nça_maxDönem = nça_max.index[:5]
nça_maxDönem = nça_maxDönem.sort_values()
nça_maxDönem = nça_maxDönem[~np.isnan(nça_maxDönem)]
nça_maxDönem = nça_maxDönem.astype(int)

arıza_maxDönem = arıza_max.index[:5]
arıza_maxDönem = arıza_maxDönem.sort_values()
arıza_maxDönem = arıza_maxDönem[~np.isnan(arıza_maxDönem)]
arıza_maxDönem = arıza_maxDönem.astype(int)

oto_ano7 = (f'Normal Çalışma Aralığı dışı değerlerin en fazla görüldüğü {dönem}lar : {(str(nça_maxDönem)[12:-17])}')
oto_ano8 = (f'Arıza sürelerinin en yüksek görüldüğü {dönem}lar : {(str(arıza_maxDönem)[12:-17])}')
ortak = (set(nça_maxDönem)&set(arıza_maxDönem))
ortak = (set(nça_maxDönem)&set(arıza_maxDönem))
if ortak == set():
    oto_ano9 = ('İki veri setinin ortak bir dönemleri yoktur.')
else:
    oto_ano9 = (f'İki veri setinin ortak dönemleri : {str(list(ortak))[1:-1]}. {dönem}')
    
trace_sağort = np.append(fig,trace_sağort)

#-------------------------
#solalt
trace_solalt = []
fig = go.Figure()

start_date = dfoto.date_pick.min()
end_date = dfoto.date_pick.max()
dftarih = dfoto.loc[(dfoto.date_pick>=start_date)&(dfoto.date_pick<=end_date)]
sz = 45

dfotom1_tarih = dfotom1.loc[(dfotom1.date_pick>=start_date)&(dfotom1.date_pick<=end_date)]
dfotom2_tarih = dfotom2.loc[(dfotom2.date_pick>=start_date)&(dfotom2.date_pick<=end_date)]
dfotom3_tarih = dfotom3.loc[(dfotom3.date_pick>=start_date)&(dfotom3.date_pick<=end_date)]
dfotom4_tarih = dfotom4.loc[(dfotom4.date_pick>=start_date)&(dfotom4.date_pick<=end_date)]

#hat 1
exp_akım1 = round(dfotom1_tarih.hat1ex_akım.mean(),2)
exp_hid1 = round(dfotom1_tarih.hat1ex_hidbas.mean(),2)
pr_akım1 = round(dfotom1_tarih.hat1pr_akım.mean(),2)
exp_red1 = round(dfotom1_tarih.hat1ex_rsıcak.mean(),2)
#hat 2
exp_akım2 = round(dfotom2_tarih.hat2ex_akım.mean(),2)
exp_hid2 = round(dfotom2_tarih.hat2ex_hidbas.mean(),2)
pr_akım2 = round(dfotom2_tarih.hat2pr_akım.mean(),2)
exp_red2 = round(dfotom2_tarih.hat2ex_rsıcak.mean(),2)
#hat 3
exp_akım3 = round(dfotom3_tarih.hat3ex_akım.mean(),2)
exp_hid3 = round(dfotom3_tarih.hat3ex_hidbas.mean(),2)
pr_akım3 = round(dfotom3_tarih.hat3pr_akım.mean(),2)
exp_red3 = round(dfotom3_tarih.hat3ex_rsıcak.mean(),2)
#hat 4
exp_akım4 = round(dfotom4_tarih.hat4ex_akım.mean(),2)
exp_hid4 = round(dfotom4_tarih.hat4ex_hidbas.mean(),2)
pr_akım4 = round(dfotom4_tarih.hat4pr_akım.mean(),2)
exp_red4 = round(dfotom4_tarih.hat4ex_rsıcak.mean(),2)


#grafikleştirme
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_akım1,
    title = dict(text='Hat 1 Ekspander Akım'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_hid1,
    title = dict(text='Ekspander Hidrolik Bas.'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = pr_akım1,
    title = dict(text='Pres Akım'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':2})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_red1,
    title = dict(text='Ekspander Redüktör Sıcaklığı'),
    number={"font":{"size":sz}},
    domain = {'row':0,'column':3}))
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_akım2,
    title = dict(text='Hat 2 Ekspander Akım'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_hid2,
    title = dict(text='Ekspander Hidrolik Bas.'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = pr_akım2,
    title = dict(text='Pres Akım'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':2})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_red2,
    title = dict(text='Ekspander Redüktör Sıcaklığı'),
    number={"font":{"size":sz}},
    domain = {'row':1,'column':3})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_akım3,
    title = dict(text='Hat 3 Ekspander Akım'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_hid3,
    title = dict(text='Ekspander Hidrolik Bas.'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = pr_akım3,
    title = dict(text='Pres Akım'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':2})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_red3,
    title = dict(text='Ekspander Redüktör Sıcaklığı'),
    number={"font":{"size":sz}},
    domain = {'row':2,'column':3})) 

fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_akım4,
    title = dict(text='Hat 4 Ekspander Akım'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':0})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_hid4,
    title = dict(text='Ekspander Hidrolik Bas.'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':1})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = pr_akım4,
    title = dict(text='Pres Akım'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':2})) 
fig.add_trace(go.Indicator(
    mode = "number",
    value = exp_red4,
    title = dict(text='Ekspander Redüktör Sıcaklığı'),
    number={"font":{"size":sz}},
    domain = {'row':3,'column':3})) 

fig.update_layout(
    grid = {'rows': 4, 'columns': 4, 'pattern': "independent"},
    title=dict(text=(f'Tarih: {start_date} - {end_date}   Hat Bazında Parametre Raporu')))

#fig.show()


trace_solalt = np.append(fig,trace_solalt)

#---------------------------
#günlük rapor

#--------------------------------
# 5 parça bilgi
#dashboard versiyonu
giriş = 'Hat 2 Ekspander Hidrolik Basıncı'
kolon = oto_dict2.get(giriş)

kolon1 = 'hat1'+ kolon[4:]
kolon2 = 'hat2'+ kolon[4:]
kolon3 = 'hat3'+ kolon[4:]
kolon4 = 'hat4'+ kolon[4:]

start_date = dfoto.date_pick.min()
end_date = dfoto.date_pick.max()

dfotom1_tarih = dfotom1.loc[(dfotom1.date_pick>=start_date)&(dfotom1.date_pick<=end_date)]
kart_1 = (f'{giriş[6:]} min.{dfotom1_tarih[kolon1].min():,.2f}, maks.{dfotom1_tarih[kolon1].max():,.2f}, ort. {dfotom1_tarih[kolon1].mean():,.2f}')

dfotom2_tarih = dfotom2.loc[(dfotom2.date_pick>=start_date)&(dfotom2.date_pick<=end_date)]
kart_2 = (f'{giriş[6:]} min.{dfotom2_tarih[kolon2].min():,.2f}, maks.{dfotom2_tarih[kolon2].max():,.2f}, ort.{dfotom2_tarih[kolon2].mean():,.2f}')

dfotom3_tarih = dfotom3.loc[(dfotom3.date_pick>=start_date)&(dfotom3.date_pick<=end_date)]
kart_3 = (f'{giriş[6:]} min.{dfotom3_tarih[kolon3].min():,.2f}, maks.{dfotom3_tarih[kolon3].max():,.2f}, ort.{dfotom3_tarih[kolon3].mean():,.2f}')

dfotom4_tarih = dfotom4.loc[(dfotom4.date_pick>=start_date)&(dfotom4.date_pick<=end_date)]
kart_4 = (f'{giriş[6:]} min.{dfotom4_tarih[kolon4].min():,.2f}, maks.{dfotom4_tarih[kolon4].max():,.2f}, ort.{dfotom4_tarih[kolon4].mean():,.2f}')

kart_5 = []

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
                        start_date = min(dfoto.date_pick),
                        end_date = max(dfoto.date_pick),
                        min_date_allowed = dfoto.date_pick.min(),
                        max_date_allowed = dfoto.date_pick.max(),
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


ürün_seç = html.Div([#dropdown div
    dbc.Label('Ürün seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(ürün_list, value= ürün_list[1], multi = False, id= 'ürün_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

otom_seç = html.Div([#dropdown div
    dbc.Label('Parametre seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(oto_list, value= oto_list[14], multi = False, id= 'otom_ismi', clearable = False,
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
        dbc.NavItem(dbc.NavLink("Otomasyon Paneli", active=True, href="http://127.0.0.1:8075", className = sayseç_nav_cls),
                   style = sayseç_nav_sty),
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

seçim_kontrol2 = dbc.Card([tarih_seç, dönem_seç, ürün_seç, otom_seç,sayfa_seç], style = {'height':1030}, 
                         className = graf_div_cls)

#--------------------------------
#fonksiyonlar

#kart şeklindeki 4 adet metin alanı

kart_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Hat 1 Verileri'], className="text-nowrap"),
            html.H1(kart_1, id = 'kart_1', className="fs-5 text"),
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls
)


kart_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Hat 2 Verileri'], className="text-nowrap"),
            html.H1(kart_2, id = 'kart_2', className="fs-5 text"),           
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)


kart_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Hat 3 Verileri'], className="text-nowrap"),
            html.H1(kart_3, id = 'kart_3', className="fs-5 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Hat 4 Verileri'], className="text-nowrap"),
            html.H1(kart_4, id = 'kart_4', className="fs-5 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_5 = dbc.Card(
    dbc.CardBody(
        [
            html.H3([''], className="text-nowrap"),
            html.H1(kart_5, id = 'kart_5', className="fs-5 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

solüst = html.Div([#solüst(1.grafik)
    dbc.Label(f'Seçili Parametrenin Çalışma Aralıkları Dağılım Grafiği', id = 'solüst_başlık',size = 'lg', className='fw-bold'),
    dcc.Graph(id='solüst',
              figure = trace_solüst[0],
              style = graf_grph_sty   
             )], className = graf_div_cls
)#solüst(1.grafik)


solort = html.Div([#solalt(2.grafik)
    dbc.Label( f"Arıza Sıklıkları ile NÇA Dışı Değerlerin Korelasyon Grafiği", id = 'solort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='solort',
              figure = trace_solort[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)

solalt = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Tarih Aralığındaki Parametre Ortalamaları", id='solalt_başlık', size = 'lg',className='fw-bold'),
    dcc.Graph(id='solalt',
              figure = trace_solalt[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)


sağüst = html.Div([#sağüst(3.grafik)
    dbc.Label(f"Seçili Parametrenin NÇA Değerlerinin Aşıldığı Dönemlerin Yoğunluk Analiz Grafiği", id = 'sağüst_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağüst',
              figure = trace_sağüst[0],
              style = graf_grph_sty
             )], className = graf_div_cls    
)#sağüst(3.grafik)

sağort = html.Div([#sağalt(4.grafik)
    dbc.Label( f"Seçili Ürün Bazında Seçili Parametre Ortalamaları ile NÇA dışı Değerlerin Korelasyon Grafiği", id = 'sağort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağort',
              figure = trace_sağort[0],
              style = graf_grph_sty
             )],  className = graf_div_cls
)#sağalt(4.grafik)

anomali = html.Div([
            dbc.Label("Anomali Raporu", size='lg',style= {'width':766,'height':50}, 
                      className = anom_label_cls),
            dcc.Textarea(id = 'anomali_rapor', value=[f'{oto_ano1}\n{oto_ano2}\n{oto_ano3}\n\n{oto_ano4}\n{oto_ano5}\n{oto_ano6}\n\n{oto_ano7}\n{oto_ano8}\n{oto_ano9}'], 
                         disabled=True, readOnly=True, style = {'font-family':"Verdana",'width':766, 'height':450},
                         className = kart_göv_cls),
            ],className = graf_div_cls,
)#anomali alanı 

#----------------------------------------
gün_seç = html.Div([
    dbc.Label('Tarih ', style = {'font-size':'20px','width':172,'height':50},
                    className = anom_label_cls),    
    dcc.DatePickerSingle(id='gün_seç',
                        date = dfoto.date_pick.max(),
                        min_date_allowed = dfoto.date_pick.min(),
                        max_date_allowed = dfoto.date_pick.max(),
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
                     #dbc.Col([kart_5],width=2)
                    ]),           
            
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

