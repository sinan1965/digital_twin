# Tanımlamalar
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)#,use_pages = True)

#---------------------
#solüst
trace_solüst = []
#Hat ve Ekipman Bazında Arıza Süreleri Dağılım Grafiği
fig = go.Figure()

dfh1 = dfbak.loc[dfbak.hat_no=='Hat 1']
dfh2 = dfbak.loc[dfbak.hat_no=='Hat 2']
dfh3 = dfbak.loc[dfbak.hat_no=='Hat 3']
dfh4 = dfbak.loc[dfbak.hat_no=='Hat 4']

h1_ekip = dfh1.ekipman_adı.unique()
h2_ekip = dfh2.ekipman_adı.unique()
h3_ekip = dfh3.ekipman_adı.unique()
h4_ekip = dfh4.ekipman_adı.unique()

indeks = dfh1.ekipman_adı.unique()
dfsil1 = pd.DataFrame(index=indeks, columns= ['arıza_süre'])

for idx,i in enumerate(h1_ekip):
    dfekip = dfh1.loc[dfh1.ekipman_adı==i]
    dfsil1.arıza_süre.iloc[idx]= dfekip.müdahale_süresi.sum()
    
dfsil1 = dfsil1.sort_values('arıza_süre',ascending =False)

indeks = dfh2.ekipman_adı.unique()
dfsil2 = pd.DataFrame(index=indeks, columns= ['arıza_süre'])

for idx,i in enumerate(h2_ekip):
    dfekip = dfh2.loc[dfh2.ekipman_adı==i]
    dfsil2.arıza_süre.iloc[idx]= dfekip.müdahale_süresi.sum()
    
dfsil2 = dfsil2.sort_values('arıza_süre',ascending =False)

indeks = dfh3.ekipman_adı.unique()
dfsil3 = pd.DataFrame(index=indeks, columns= ['arıza_süre'])

for idx,i in enumerate(h3_ekip):
    dfekip = dfh3.loc[dfh3.ekipman_adı==i]
    dfsil3.arıza_süre.iloc[idx]= dfekip.müdahale_süresi.sum()
    
dfsil3 = dfsil3.sort_values('arıza_süre',ascending =False)

indeks = dfh4.ekipman_adı.unique()
dfsil4 = pd.DataFrame(index=indeks, columns= ['arıza_süre'])

for idx,i in enumerate(h4_ekip):
    dfekip = dfh4.loc[dfh4.ekipman_adı==i]
    dfsil4.arıza_süre.iloc[idx]= dfekip.müdahale_süresi.sum()
    
dfsil4 = dfsil4.sort_values('arıza_süre',ascending =False)

#grafikleştirme
for i in range(0,len(dfsil1)):
    fig.add_trace(go.Bar(
        x = dfsil1.index,
        y = dfsil1.arıza_süre,
        marker = dict(color = 'coral', opacity = 0.75),
        hovertemplate = '<i>Ekipman: </i>'+'%{x} <br>'+
                    '<i>Hat no :1 <br>'+
                    '<i>Toplam Arıza Süresi:</i> '+(f'{dfsil1.arıza_süre[i]:,.0f} (dk)')+ 
                    '<extra></extra>',
                    showlegend = False
    ))
    
for i in range(0,len(dfsil2)):
    fig.add_trace(go.Bar(
        x = dfsil2.index,
        y = dfsil2.arıza_süre,
        marker = dict(color = 'orange', opacity = 0.75),
        hovertemplate = '<i>Ekipman: </i>'+'%{x} <br>'+
                    '<i>Hat no :2 <br>'+
                    '<i>Toplam Arıza Süresi:</i> '+(f'{dfsil2.arıza_süre[i]:,.0f} (dk)')+ 
                    '<extra></extra>',
                    showlegend = False
    ))
    
for i in range(0,len(dfsil3)):
    fig.add_trace(go.Bar(
        x = dfsil3.index,
        y = dfsil3.arıza_süre,
        marker = dict(color = 'green', opacity = 0.75),
        hovertemplate = '<i>Ekipman: </i>'+'%{x} <br>'+
                    '<i>Hat no :3 <br>'+
                    '<i>Toplam Arıza Süresi:</i> '+(f'{dfsil3.arıza_süre[i]:,.0f} (dk)')+ 
                    '<extra></extra>',
                    showlegend = False
    ))

for i in range(0,len(dfsil4)):
    fig.add_trace(go.Bar(
        x = dfsil4.index,
        y = dfsil4.arıza_süre,
        marker = dict(color = 'lightblue', opacity = 0.75),
        hovertemplate = '<i>Ekipman: </i>'+'%{x} <br>'+
                    '<i>Hat no :4 <br>'+
                    '<i>Toplam Arıza Süresi:</i> '+(f'{dfsil4.arıza_süre[i]:,.0f} (dk)')+ 
                    '<extra></extra>',
                    showlegend = False
    ))

fig.update_layout(
    barmode = 'group',
    showlegend = False,
    xaxis = dict(tickmode = 'linear'),
    #title=dict(text=(f"")),
    xaxis_title = dict(text =f'Ekipman'),
    yaxis_title = dict(text = 'Süre (dk)'),
    hoverlabel = dict(font=dict(color= 'white'), bgcolor='grey'),
    yaxis = dict(gridcolor='lightgrey'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    )

#fig.show()

trace_solüst = np.append(fig,trace_solüst)

#----------------------- 
#solort
trace_solort = []
#Arıza süre/dönem analizi (gün, hafta, ay)
fig = go.Figure()
dönem = 'hafta'
tick = 'linear'

ay_çalDak = 19*60*26
haf_çalDak = 19*60*6

if dönem == 'hafta':
    çalDak = haf_çalDak
elif dönem == 'ay':
    çalDak = ay_çalDak
elif dönem == 'gün':
    tick = 'auto'

dfarıza = dfbak.loc[dfbak.arıza_bakım=='Arıza']

indeks = dfbak[dönem].unique()
dfsil5 = pd.DataFrame(index = indeks, columns = ['müd_süreTop','duruş_oran'])

for idx,i in enumerate(indeks):
    dfdönem = dfarıza.loc[dfarıza[dönem] == i]
    dfsil5.müd_süreTop.iloc[idx] = np.sum(dfdönem.müdahale_süresi)
    dfsil5.duruş_oran.iloc[idx] = round((100*dfsil5.müd_süreTop.iloc[idx]/çalDak),2)
    
ort = round(dfsil5['müd_süreTop'].mean(),2)

#grafikleştirme
for n in range(0,len(dfsil5)):
    fig.add_trace(go.Bar(x=[dfsil5.index[n]],
                         y=[dfsil5.müd_süreTop.iloc[n]],
                         marker = dict(color = 'coral', opacity = 0.75),
                         hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                             '<br><i>Süre:</i> '+(f'{dfsil5.müd_süreTop.iloc[n]:,.0f} (dk)')+ 
                             '<extra></extra>',
                              showlegend = False
                         ))
    
fig.add_hline(y=ort, line = dict(color = 'green', width = 1, dash = 'dashdot'),
                  annotation_text=(f'Ortalama {int(ort)} (dk)'), 
                  annotation_position="bottom right",
                  opacity = 1)

fig.update_layout(showlegend = False,
                      xaxis = dict(tickmode = tick,
                                 ),
                      title=dict(text=(f"Seçili dönem:{dönem.capitalize()}")),
                      xaxis_title = dict(text =f'{dönem.capitalize()}'),
                      yaxis_title = dict(text = 'Süre (dk)'),
                      hoverlabel = dict(font=dict(color= 'white'), bgcolor='grey'),
                      yaxis = dict(gridcolor='lightgrey'),
                      paper_bgcolor = 'white',
                      plot_bgcolor = 'white',
         )
#fig.show()


#anomali kodlaması
dfsil5 = dfsil5.sort_values('müd_süreTop', ascending=False)
üst_sınır = dfsil5.müd_süreTop.mean() + dfsil5.müd_süreTop.std()
sınır_aşan = dfsil5.loc[dfsil5.müd_süreTop>=üst_sınır]
tarih = sınır_aşan.index

ano_solort1 = (f'{dönem.capitalize()} bazında arızalı süre olarak üst sınırı aşan {dönem}lar :')
ano_solort2 = (f'{str(list(tarih))[1:-1]}')

ano_solort3 = (f'Arızaların en yoğun olarak meydana geldiği {dönem}lar: ')
ano_solort4 = (f'{str(list(tarih[:3]))[1:-1]}')

trace_solort = np.append(fig,trace_solort)
   
#------------------------
#sağüst
trace_sağüst = []
#ekipman arıza bakım süreleri oransal dağılım
fig = go.Figure()

dfsil4 = pd.DataFrame(index = ekip_list, columns = ['bakım_süreOran', 'arıza_süreOran'])

for idx,i in enumerate(ekip_list):
    dfekip = dfbak.loc[dfbak.ekipman_adı==i]    
    #arızalar
    dfarıza = dfekip.loc[dfekip.arıza_bakım=='Arıza']
    dfsil4.arıza_süreOran.iloc[idx] = np.sum(dfarıza.müdahale_süresi)/np.sum(dfekip.müdahale_süresi)   
    #bakımlar
    dfbakım = dfekip.loc[dfekip.arıza_bakım=='Bakım']
    dfsil4.bakım_süreOran.iloc[idx] = np.sum(dfbakım.müdahale_süresi)/np.sum(dfekip.müdahale_süresi)
    
dfsil4 = dfsil4.sort_values('bakım_süreOran', ascending = False)    
dfsil4 = dfsil4.transpose()

#grafikleştirme
for idx, n in enumerate(dfsil4.columns):
    for nn in range(len(dfsil4)):
        if nn == 0:
            renk_a = 'royalblue'
        else:
            renk_a = 'coral'
        fig.add_trace(go.Bar(
                             x=[n],
                             y=[dfsil4[n].iloc[nn]],
                             marker = dict(color = renk_a, opacity = 0.75),
                             hovertemplate = (f'<i>Ekipman: </i>')+'%{x}'+
                             '<br><i>Oran:</i> '+(f'%{100*dfsil4[n].iloc[nn]:.2f}')+ 
                             '<extra></extra>',
                              showlegend = False
            ))
        
        fig.update_xaxes(tickmode= 'linear',
                         tickvals = [ekip_list[idx]],
                         tickangle = 270,
                         )
        
fig.update_layout(barmode='stack',
                          showlegend = False,
                          #title = 'Ekipman Bazında Arıza ve Bakım Süreleri Oransal Dağılım Grafiği (%)',
                          xaxis_title = dict(text ='Ekipmanlar'),
                          yaxis_title = dict(text = 'Oran (%)'),
                          hoverlabel = dict(font=dict(color= 'white'), bgcolor='grey'),
                          yaxis = dict(gridcolor='lightgrey'),
                          paper_bgcolor = 'white',
                          plot_bgcolor = 'white',
                          )                  
#fig.show()
    

trace_sağüst = np.append(fig,trace_sağüst)

#-------------------------
#sağort
trace_sağort = []
#aynı ekipmanda arıza tekrarlanma sıklığı fonksiyonu(sağalt)
fig = go.Figure()

hat = 'Hat 1'
ekipman = 'Değirmen'
arıza = 'Elek Arızası'

#seçili hat, ekipman ve arıza türünden oluşan alt df oluşturma
dfhat = dfbak.loc[dfbak.hat_no==hat]
dfekip = dfhat.loc[dfhat.ekipman_adı==ekipman]
dfarıza = dfekip.loc[dfekip.ab_türü==arıza]

#alt df'ten dummy df oluşturma
indeks = dfarıza.index.unique()
dfsil6 = pd.DataFrame(index = indeks, columns = ['süre_fark','sıklık','arıza_süre'])

#dummy df tarih farkları oluşturma ve 4 günden daha sık oluşan arızaları dfsil6['sıklık'] kolonunda işaretleme
for idx,i in enumerate(indeks):
    dfsil6['arıza_süre'].iloc[idx] = dfarıza.müdahale_süresi.iloc[idx]
    
for ndx,n in enumerate(indeks):
    if ndx == len(indeks)-1:
        break
    else:
        dfsil6['süre_fark'].iloc[ndx+1] = dfsil6.index[ndx+1]-dfsil6.index[ndx]
        if dfsil6['süre_fark'].iloc[ndx+1]<=timedelta(days=4):
            dfsil6['sıklık'].iloc[ndx+1] = 1
        else:
            dfsil6['sıklık'].iloc[ndx+1] = 0

#grafikleştirme
for n in range(0,len(dfsil6)):
    fig.add_trace(go.Bar(x=[dfsil6.index[n]],
                         y=[dfsil6['arıza_süre'].iloc[n]],
                         marker = dict(color = ekip_renk.get(ekipman),opacity = 1),
                         hovertemplate = '<i>Tarih: </i> %{x}'+
                             '<br><i>Süre:</i> '+(f'{dfsil6.arıza_süre.iloc[n]:,.0f} (dk)')+ 
                             '<extra></extra>',
                              showlegend = False
                         ))
fig.add_trace(go.Scatter(
        x= dfsil6.index[dfsil6.sıklık==1],
        y= dfsil6.sıklık.loc[dfsil6.sıklık==1]*10, 
        mode= 'markers',
        marker = dict(color='red',size=10, symbol='x'),
    ))
    
fig.update_layout(showlegend = False,
                  xaxis = dict(tickmode = 'array'),
                  xaxis_title = 'Tarih',
                  yaxis_title = 'Süre',
                  title=dict(text=(f"Seçili hat:{hat} Seçili ekipman: {ekipman} Seçili arıza:{arıza}")), 
                  hoverlabel = dict(font=dict(color= 'white'), bgcolor='grey'),
                  yaxis = dict(gridcolor='lightgrey'),
                  paper_bgcolor = 'white',
                  plot_bgcolor = 'white',
                  )
#fig.show()


#anomali rapor
sınır_aşan = dfsil6.loc[dfsil6.sıklık==1]
tarih = sınır_aşan.index

liste = []
for idx,i in enumerate(tarih):
    qqq = str(tarih[idx]).split(sep='-')
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
ano_sağort = []
ano_sağort = np.append((f'{hat}. hat {ekipman} {arıza} arıza sıklığı istatistikleri:'),ano_sağort)
for i in df_anomali.index:
    ano_sağort = np.append((f'%{df_anomali.oran.iloc[i]} {df_anomali.ay.iloc[i]}. ayda,'),ano_sağort)
ano_sağort = np.append((f'meydana gelmiştir.'),ano_sağort)
ano_sağort = np.append((f'{hat}. hat {ekipman} {arıza} arızasının yoğun olarak meydana geldiği aylar: '),ano_sağort)
ano_sağort = np.append((f'{str(list(df_anomali.ay[:3]))[1:-1]}'),ano_sağort)
ano_sağort = np.flip(ano_sağort)

trace_sağort = np.append(fig,trace_sağort)

#-------------------------
#solalt
trace_solalt = []
#Duruş süresi analizi (hafta, ay)
fig = go.Figure()
dönem = 'hafta'

ay_çalDak = 19*60*26
haf_çalDak = 19*60*6

if dönem == 'hafta':
    çalDak = haf_çalDak
elif dönem == 'ay':
    çalDak = ay_çalDak
elif dönem == 'gün':
    tick = 'auto'

dfarıza = dfbak.loc[dfbak.arıza_bakım=='Arıza']

indeks = dfbak[dönem].unique()
dfsil7 = pd.DataFrame(index = indeks, columns = ['müd_süreTop','duruş_oran','top_oran'])

for idx,i in enumerate(indeks):
    dfdönem = dfarıza.loc[dfarıza[dönem] == i]
    dfsil7.müd_süreTop.iloc[idx] = np.sum(dfdönem.müdahale_süresi)
    dfsil7.duruş_oran.iloc[idx] = round((100*dfsil7.müd_süreTop.iloc[idx]/çalDak),2)
    dfsil7.top_oran.iloc[idx] = 100-round((100*dfsil7.müd_süreTop.iloc[idx]/çalDak),2)
        
ort = round(dfsil7.duruş_oran.mean(),2)

#grafikleştirme
for n in range(0,len(dfsil7)):
    fig.add_trace(go.Bar(x=[dfsil7.index[n]],
                         y=[dfsil7.duruş_oran.iloc[n]],
                         marker = dict(color = 'coral', opacity = 0.75),
                         hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                             '<br><i>Arızalı Süre Oranı:</i> '+(f'%{dfsil7.duruş_oran.iloc[n]:,.2f}')+ 
                             '<extra></extra>',
                              showlegend = False
                         ))
    
    fig.add_trace(go.Bar(x=[dfsil7.index[n]],
                         y=[dfsil7.top_oran.iloc[n]],
                         marker = dict(color = 'grey', opacity = 0.5),
                         hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                             '<br><i>Çalışma Süre Oranı:</i> '+(f'%{dfsil7.top_oran.iloc[n]:,.2f}')+ 
                             '<extra></extra>',
                              showlegend = False
                         ))
    
fig.add_hline(y=ort, line = dict(color = 'green', width = 1, dash = 'dashdot'),
                  annotation_text=(f'Ortalama Duruş Süresi Oranı %{ort}'), 
                  annotation_position="bottom right",
                  opacity = 1)

fig.update_layout(barmode='stack',
                  showlegend = False,
                  xaxis = dict(tickmode = tick),
                  title=dict(text=(f"seçili dönem :{dönem.capitalize()}")),
                  xaxis_title = dict(text =f'{dönem.capitalize()}'),
                  yaxis_title = dict(text = 'Oran (%)'),
                  hoverlabel = dict(font=dict(color= 'white'), bgcolor='grey'),
                  yaxis = dict(gridcolor='lightgrey'),
                  paper_bgcolor = 'white',
                  plot_bgcolor = 'white',
         )
#fig.show()

#anomali kodlaması
dfsil7 = dfsil7.sort_values('müd_süreTop', ascending=False)
üst_sınır = round(dfsil7.duruş_oran.mean(),2) + round(dfsil7.duruş_oran.std(),2)
aşan_ort = dfsil7.loc[dfsil7.duruş_oran>üst_sınır]
ano_solalt1 = (f'Arızalı süre oranlarının üst sınırı aştığı {dönem}lar :')
ano_solalt2 = (f'{str(list(aşan_ort.index))[1:-1]}')

a = aşan_ort.loc[aşan_ort.index>26]
ano_solalt3 = (f'                                        ')
if len(a.index)>len(aşan_ort.index)/2:
    ano_solalt4 = (f'Arızalı süre oranlarının üst sınırı aştığı dönemler yoğunlukla yılın ikinci yarısında meydana gelmiştir.')
elif len(a.index)<len(aşan_ort.index):
    ano_solalt4 = (f'Arızalı süre oranlarının üst sınırı aştığı dönemler yoğunlukla yılın ilk yarısında meydana gelmiştir.')    

trace_solalt = np.append(fig,trace_solalt)

#---------------------------
#günlük rapor

#-----------------------------
#Anomali raporu
dönem = 'hafta'
hat = 'Hat 1'
if hat == 'Hat 1':
    hat_ürt = 'pr1_miktar'
elif hat == 'Hat 2':
    hat_ürt = 'pr2_miktar'
elif hat == 'Hat 3':
    hat_ürt = 'pr3_miktar'
elif hat == 'Hat 4':
    hat_ürt = 'pr4_miktar'
    
indeks = dfürt[dönem].unique()
dfsil_ürt = pd.DataFrame(index = indeks, columns = ['Hat 1','Hat 2','Hat 3','Hat 4'])

for idx,i in enumerate(indeks):
    dfdönem = dfürt.loc[dfürt[dönem] == i]
    dfsil_ürt[hat].iloc[idx] = round(dfdönem[hat_ürt].sum()/1000,2)        
    
# dfen
#Arıza süre/dönem analizi (gün, hafta, ay)(sağorta),
fig = go.Figure()

if hat == 'Hat 1':
    hat_ürt = ['hat1_pr_en','hat1_ex_en','hat1_kd_en']
elif hat == 'Hat 2':
    hat_ürt = ['hat2_pr_en','hat2_ex_en','hat2_kd_en']
elif hat == 'Hat 3':
    hat_ürt = ['hat3_pr_en','hat3_ex_en','hat3_kd_en']
elif hat == 'Hat 4':
    hat_ürt = ['hat4_pr_en','hat4_ex_en','hat4_kd_en']
    
indeks = dfen[dönem].unique()
dfsil_en = pd.DataFrame(index = indeks, columns = ['Hat 1','Hat 2','Hat 3','Hat 4'])

for idx,i in enumerate(indeks):
    dfdönem = dfen.loc[dfen[dönem] == i]
    dfsil_en[hat].iloc[idx] = round(dfdönem[hat_ürt].sum().sum(),2)        
    
# dfoto
#Arıza süre/dönem analizi (gün, hafta, ay)(sağorta),
fig = go.Figure()

if hat == 'Hat 1':
    hat_oto = 'hat1ex_çsıcak'
elif hat == 'Hat 2':
    hat_oto = 'hat2ex_çsıcak'
elif hat == 'Hat 3':
    hat_oto = 'hat3ex_çsıcak'
elif hat == 'Hat 4':
    hat_oto = 'hat4ex_çsıcak'
    
indeks = dfoto[dönem].unique()
dfsil_oto = pd.DataFrame(index = indeks, columns = ['Hat 1','Hat 2','Hat 3','Hat 4'])

for idx,i in enumerate(indeks):
    dfdönem = dfoto.loc[dfoto[dönem] == i]
    dfsil_oto[hat].iloc[idx] = round(dfdönem[hat_oto].mean(),2)        
    

# dfbak
#Arıza süre/dönem analizi (gün, hafta, ay)(sağorta),
fig = go.Figure()

dfarıza = dfbak.loc[dfbak.arıza_bakım=='Arıza']
dfhat = dfarıza.loc[dfarıza.hat_no==hat]

indeks = dfarıza[dönem].unique()
dfsil_bak = pd.DataFrame(index = indeks, columns = ['Hat 1','Hat 2','Hat 3','Hat 4'])

for idx,i in enumerate(indeks):
    dfdönem = dfhat.loc[dfhat[dönem] == i]
    dfsil_bak[hat].iloc[idx] = dfdönem.müdahale_süresi.sum()        
    
#-----------------------------------
#hat = '2'

bak =dfsil_bak[hat]
oto =dfsil_oto[hat]
ürt =dfsil_ürt[hat]
en =dfsil_en[hat]

df_ana = pd.DataFrame(index=dfsil_ürt.index, columns=['bak','oto','ürt','en','bakoto','bakürt','baken','otoürt',
                                                      'otoen','ürten'])

df_ana['bak'] = bak
df_ana['ürt'] = ürt
df_ana['oto'] = oto
df_ana['en'] = en

df_ana = df_ana.astype(float)

for idx,i in enumerate(df_ana.index):
    #bakım ile otomasyon ilişkisi
    df_ana.bakoto.iloc[idx] = (df_ana.bak.iloc[idx]/df_ana.oto.iloc[idx])#*1000
    #bakım ile üretim ilişkisi
    df_ana.bakürt.iloc[idx] = (df_ana.bak.iloc[idx]/df_ana.ürt.iloc[idx])#*1000
    #bakım ile enerji ilişkisi
    df_ana.baken.iloc[idx] = (df_ana.bak.iloc[idx]/df_ana.en.iloc[idx])#*1000
    #otomasyon ile üretim ilişkisi
    df_ana.otoürt.iloc[idx] = (df_ana.oto.iloc[idx]/df_ana.ürt.iloc[idx])#*1000
    #otomasyon ile enerji ilişkisi
    df_ana.otoen.iloc[idx] = (df_ana.oto.iloc[idx]/df_ana.en.iloc[idx])#*1000
    #üretim ile enerji ilişkisi
    df_ana.ürten.iloc[idx] = (df_ana.ürt.iloc[idx]/df_ana.en.iloc[idx])#*1000
    

sonuç = 0
var = df_ana.bakoto.var() 
std = df_ana.bakoto.std()- df_ana.bakoto.mean()
maxmin = df_ana.bakoto.max()-df_ana.bakoto.min()

if var<1 and std<0 and maxmin<1:
    sonuç = 3
elif var<1 and std>1 and maxmin<1:
    sonuç = 2
elif var<1 and std>1 and maxmin>1:
    sonuç = 1

if sonuç==3:
    ano_1 = (f'Arıza süreleriyle otomasyon değerleri arasındaki ilişki yüksek kararlılıkta, anomali seviyesi düşük.')
elif sonuç ==2:
    ano_1 = (f'Arıza süreleriyle otomasyon değerleri arasındaki ilişki orta kararlılıkta, anomali seviyesi orta.')
elif sonuç ==1:
    ano_1 = (f'Arıza süreleriyle otomasyon değerleri arasındaki ilişki düşük kararlılıkta, anomali seviyesi yüksek.')
elif sonuç ==0:
    ano_1 = (f'Arıza süreleriyle otomasyon değerleri arasındaki ilişki çok düşük kararlılıkta, anomali seviyesi çok yüksek.')

sonuç = 0
var = df_ana.bakürt.var() 
std = df_ana.bakürt.std()- df_ana.bakürt.mean()
maxmin = df_ana.bakürt.max()-df_ana.bakürt.min()

if var<1 and std<0 and maxmin<1:
    sonuç = 3
elif var<1 and std>1 and maxmin<1:
    sonuç = 2
elif var<1 and std>1 and maxmin>1:
    sonuç = 1
    
if sonuç==3:
    ano_2 = (f'Arıza süreleriyle üretim miktarları arasındaki ilişki yüksek kararlılıkta, anomali seviyesi düşük.')
elif sonuç ==2:
    ano_2 = (f'Arıza süreleriyle üretim miktarları arasındaki ilişki orta kararlılıkta, anomali seviyesi orta.')
elif sonuç ==1:
    ano_2 = (f'Arıza süreleriyle üretim miktarları arasındaki ilişki düşük kararlılıkta, anomali seviyesi yüksek.')
elif sonuç ==0:
    ano_2 = (f'Arıza süreleriyle üretim miktarları arasındaki ilişki çok düşük kararlılıkta, anomali seviyesi çok yüksek.')

sonuç = 0
var = df_ana.baken.var() 
std = df_ana.baken.std()- df_ana.baken.mean()
maxmin = df_ana.baken.max()-df_ana.baken.min()

if var<1 and std<0 and maxmin<1:
    sonuç = 3
elif var<1 and std>1 and maxmin<1:
    sonuç = 2
elif var<1 and std>1 and maxmin>1:
    sonuç = 1

if sonuç==3:
    ano_3 = (f'Arıza süreleriyle enerji tüketimi arasındaki ilişki yüksek kararlılıkta, anomali seviyesi düşük.')
elif sonuç ==2:
    ano_3 = (f'Arıza süreleriyle enerji tüketimi arasındaki ilişki orta kararlılıkta, anomali seviyesi orta.')
elif sonuç ==1:
    ano_3 = (f'Arıza süreleriyle enerji tüketimi arasındaki ilişki düşük kararlılıkta, anomali seviyesi yüksek.')
elif sonuç ==0:
    ano_3 = (f'Arıza süreleriyle enerji tüketimi arasındaki ilişki çok düşük kararlılıkta, anomali seviyesi çok yüksek.')

sonuç = 0
var = df_ana.otoürt.var() 
std = df_ana.otoürt.std()- df_ana.otoürt.mean()
maxmin = df_ana.otoürt.max()-df_ana.otoürt.min()

if var<1 and std<0 and maxmin<1:
    sonuç = 3
elif var<1 and std>1 and maxmin<1:
    sonuç = 2
elif var<1 and std>1 and maxmin>1:
    sonuç = 1
    
if sonuç==3:
    ano_4 = (f'Otomasyon değerleriyle üretim miktarları arasındaki ilişki yüksek kararlılıkta, anomali seviyesi düşük.')
elif sonuç ==2:
    ano_4 = (f'Otomasyon değerleriyle üretim miktarları arasındaki ilişki orta kararlılıkta, anomali seviyesi orta.')
elif sonuç ==1:
    ano_4 = (f'Otomasyon değerleriyle üretim miktarları arasındaki ilişki düşük kararlılıkta, anomali seviyesi yüksek.')
elif sonuç ==0:
    ano_4 = (f'Otomasyon değerleriyle üretim miktarları arasındaki ilişki çok düşük kararlılıkta, anomali seviyesi çok yüksek.')

sonuç = 0
var = df_ana.otoen.var() 
std = df_ana.otoen.std()- df_ana.otoen.mean()
maxmin = df_ana.otoen.max()-df_ana.otoen.min()

if var<1 and std<0 and maxmin<1:
    sonuç = 3
elif var<1 and std>1 and maxmin<1:
    sonuç = 2
elif var<1 and std>1 and maxmin>1:
    sonuç = 1

if sonuç==3:
    ano_5 = (f'Otomasyon değerleriyle enerji tüketimleri arasındaki ilişki yüksek kararlılıkta, anomali seviyesi düşük.')
elif sonuç ==2:
    ano_5 = (f'Otomasyon değerleriyle enerji tüketimleri arasındaki ilişki orta kararlılıkta, anomali seviyesi orta.')
elif sonuç ==1:
    ano_5 = (f'Otomasyon değerleriyle enerji tüketimleri arasındaki ilişki düşük kararlılıkta, anomali seviyesi yüksek.')
elif sonuç ==0:
    ano_5 = (f'Otomasyon değerleriyle enerji tüketimleri arasındaki ilişki çok düşük kararlılıkta, anomali seviyesi çok yüksek.')

sonuç = 0
var = df_ana.ürten.var() 
std = df_ana.ürten.std()- df_ana.ürten.mean()
maxmin = df_ana.ürten.max()-df_ana.ürten.min()

if var<1 and std<0 and maxmin<1:
    sonuç = 3
elif var<1 and std>1 and maxmin<1:
    sonuç = 2
elif var<1 and std>1 and maxmin>1:
    sonuç = 1
    
if sonuç==3:
    ano_6 = (f'Üretim miktarlarıyla enerji tüketimleri arasındaki ilişki yüksek kararlılıkta, anomali seviyesi düşük.')
elif sonuç ==2:
    ano_6 = (f'Üretim miktarlarıyla enerji tüketimleri arasındaki ilişki orta kararlılıkta, anomali seviyesi orta.')
elif sonuç ==1:
    ano_6 = (f'Üretim miktarlarıyla enerji tüketimleri arasındaki ilişki düşük kararlılıkta, anomali seviyesi yüksek.')
elif sonuç ==0:
    ano_6 = (f'Üretim miktarlarıyla enerji tüketimleri arasındaki ilişki çok düşük kararlılıkta, anomali seviyesi çok yüksek.')

#----------------------
#arıza sıklığı uyarı raporu 
dfarıza = dfbak.loc[dfbak.arıza_bakım=='Arıza']
ano_7 = (f'Arıza sıklığı istatistikleri:\n')
ano_8 = dfarıza.groupby('hat_no')[['ekipman_adı','ab_türü']].value_counts().sort_values(ascending=False)[:10]

#--------------------------------
# 5 parça bilgi
#arızalara ortalama müdahele süresi, ortalama bakım süresi 
dfarıza = dfbak.loc[dfbak.arıza_bakım=='Arıza']
dfbakım = dfbak.loc[dfbak.arıza_bakım =='Bakım']

start_date = dfbak.date_pick.min()
end_date = dfbak.date_pick.max()
dftarih1 = dfarıza.loc[(dfarıza.date_pick>=start_date)&(dfarıza.date_pick<=end_date)]
dftarih2 = dfbakım.loc[(dfbakım.date_pick>=start_date)&(dfbakım.date_pick<=end_date)]

kart_1 = (f'{dftarih1.müdahale_süresi.sum():,.0f}')
kart_2 = (f'{dftarih1.müdahale_süresi.sum()/len(dftarih1):,.2f}')
kart_3 = (f'{dftarih2.müdahale_süresi.sum():,.0f}')
kart_4 = (f'{dftarih2.müdahale_süresi.sum()/len(dftarih2):,.2f}')
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
                        start_date = min(dfbak.date_pick),
                        end_date = max(dfbak.date_pick),
                        min_date_allowed = dfbak.date_pick.min(),
                        max_date_allowed = dfbak.date_pick.max(),
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


hat_seç = html.Div([#dropdown div
    dbc.Label('Hat seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(hat_list, value= hat_list[0], multi = False, id= 'hat_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

ekipman_seç = html.Div([#dropdown div
    dbc.Label('Ekipman seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(list(tüm_seçim.keys()), value= ekipman_list[0], multi = False, id= 'ekipman_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div   

arıza_seç = html.Div([#dropdown div
    dbc.Label('Arıza seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(options = [],  multi = False, id= 'arıza_ismi', clearable = False,
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
        dbc.NavItem(dbc.NavLink("Otomasyon Paneli", href="http://127.0.0.1:8076", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Sipariş Paneli", href="http://127.0.0.1:8077", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Bakım Paneli", active=True, href="http://127.0.0.1:8078", className = sayseç_nav_cls),
                   style = sayseç_nav_sty),
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

seçim_kontrol2 = dbc.Card([tarih_seç, tesis_seç, dönem_seç, hat_seç, ekipman_seç, arıza_seç, sayfa_seç], style = {'height':1030}, 
                         className = graf_div_cls)

#--------------------------------
#fonksiyonlar

#kart şeklindeki 4 adet metin alanı

kart_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Toplam Arıza Süresi'], className="text-nowrap"),
            html.H1(kart_1, id = 'kart_1', className="fs-2 text"),
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls
)


kart_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Ortalama Arıza Süresi'], className="text-nowrap"),
            html.H1(kart_2, id = 'kart_2', className="fs-2 text"),           
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)


kart_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Toplam Bakım Süresi'], className="text-nowrap"),
            html.H1(kart_3, id = 'kart_3', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Ortalama Bakım Süresi'], className="text-nowrap"),
            html.H1(kart_4, id = 'kart_4', className="fs-2 text"), 
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
    dbc.Label(f'Hat ve Ekipman Bazında Arıza Süreleri Dağılım Grafiği (dk)', id = 'solüst_başlık',size = 'lg', className='fw-bold'),
    dcc.Graph(id='solüst',
              figure = trace_solüst[0],
              style = graf_grph_sty   
             )], className = graf_div_cls
)#solüst(1.grafik)


solort = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Dönem Bazında Arıza Sürelerinin Dağılım Grafiği (dk)", id = 'solort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='solort',
              figure = trace_solort[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)

solalt = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Dönem Bazında Arızalı Süre Oranları (%)", id='solalt_başlık', size = 'lg',className='fw-bold'),
    dcc.Graph(id='solalt',
              figure = trace_solalt[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)


sağüst = html.Div([#sağüst(3.grafik)
    dbc.Label(f"Ekipman Bakım Arıza Sürelerinin Oransal Dağılım Grafiği (%)", id = 'sağüst_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağüst',
              figure = trace_sağüst[0],
              style = graf_grph_sty
             )], className = graf_div_cls    
)#sağüst(3.grafik)

sağort = html.Div([#sağalt(4.grafik)
    dbc.Label( f"Seçili Hat, Ekipman ve Arıza Bazında Sıklık Analiz Grafiği", id = 'sağort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağort',
              figure = trace_sağort[0],
              style = graf_grph_sty
             )],  className = graf_div_cls
)#sağalt(4.grafik)

anomali = html.Div([
            dbc.Label("Anomali Raporu", size='lg',style= {'width':766,'height':50}, 
                      className = anom_label_cls),
            dcc.Textarea(id = 'anomali_rapor', value=[(f'{hat} Numaralı hat:{ano_1}\n{ano_2}\n{ano_3}\n{ano_4}\n{ano_5}\n{ano_6}\n\n{ano_7}\n{ano_8}\n\n{ano_solort1}\n{ano_solort2}\n{ano_solort3}\n{ano_solort4}\n\n{ano_solalt1}\n{ano_solalt2}\n{ano_solalt3}\n{ano_solalt4}\n\n{list(ano_sağort)}')], 
                         disabled=True, readOnly=True, style = {'font-family':"Verdana",'width':766, 'height':450},
                         className = kart_göv_cls),
            ],className = graf_div_cls,
)#anomali alanı 

#----------------------------------------
gün_seç = html.Div([
    dbc.Label('Tarih ', style = {'font-size':'20px','width':172,'height':50},
                    className = anom_label_cls),    
    dcc.DatePickerSingle(id='gün_seç',
                        date = dfbak.date_pick.max(),
                        min_date_allowed = dfbak.date_pick.min(),
                        max_date_allowed = dfbak.date_pick.max(),
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

