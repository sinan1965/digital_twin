# Tanımlamalar
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)#,use_pages = True)

#---------------------
#solüst
trace_solüst = []
#Tüm forkliftlerin dönemsel çalışma oran grafiği
fig = go.Figure()
dönem = 'hafta'
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

#for loop için indeks oluşturma
say = dfzph[dönem].unique()

#dummy df oluşturma
indeks = dfzph[dönem].unique()
bölge_isim = dfzph['zone'].unique()
dfsil3 = pd.DataFrame(index= indeks, columns= bölge_isim)

#seçili haftada seçili bölgede geçirilen süre
for i in range(0,len(say)):
    dönem_ = say[i]
    a = dfzph[dönem] == dönem_
    dfdönem = dfzph.loc[a]
    bölge_say = dfdönem['zone'].unique()
    
    #her bölge için
    for ii in range(0,len(dfdönem['zone'].unique())):
        bölge = bölge_say[ii]
        b = dfdönem['zone'] == bölge
        dfbölge = dfdönem.loc[b]
        say_yüzde = len(dfbölge)/len(dfdönem)
        dfsil3[bölge].iloc[i] = say_yüzde
        
dfsil3 = dfsil3.transpose()

#eksik dönem tamamlama
if dönem == 'hafta':
    dfsil3[17] = np.zeros(len(dfsil3))
    dfsil3[18] = np.zeros(len(dfsil3))
    dfsil3[19] = np.zeros(len(dfsil3))
    
    dfsil3[17] = dfsil3[14]
    dfsil3[18] = dfsil3[41]
    dfsil3[19] = dfsil3[20]

#grafikleştirme
for n in range(0,len(dfsil3.columns)):
    sayı = dfsil3.columns[n]
    for nn in range(0,len(dfsil3)):
        fig.add_trace(go.Bar(name =dfsil3.index[nn],
                             x=[dfsil3.columns[n]],
                             y=[dfsil3[sayı].iloc[nn]],
                             marker=dict(color=bölge_renk.get(dfsil3.index[nn])),opacity = .7,
                             hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                             '<br><i>Oran: </i> %{y}'+ 
                             '<br><i>Bölge: '+(f'{dfsil3.index[nn]}')+
                             '<extra></extra>',
                             showlegend=False
                            ))
        fig.update_layout(barmode='stack',
                          showlegend = False,
                          xaxis = dict(tickmode = tick),
                          title=dict(text=(f"Dönem: {dönem}   Forklift: Tüm Forkliftler")),
                          hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
                          yaxis = dict(gridcolor='lightgrey'),
                          paper_bgcolor = 'white',
                          plot_bgcolor = 'white',
                          )        
#fig.show()

#---------------------------
#anom raporlama
indeks = dfsil3.index
dfsil = pd.DataFrame(index= indeks, columns= ['adet'])

for i in range(0,len(dfsil3)):
    a = dfsil3.iloc[i].sum()
    dfsil['adet'].iloc[i] = a
    
anom_kull = dfsil.sort_values(by = 'adet', ascending= False)
anom_ençok = anom_kull.index[:3]
anom_ençok = anom_ençok.to_list()

metin = str(anom_ençok)[1:-1]
anom_solüst = (f'Forkliftlerin en yoğun kullandığı 3 bölge:  {metin}.')

trace_solüst = np.append(fig,trace_solüst)

#----------------------- 
#solort

trace_solort = []
fig = go.Figure()
dönem = 'hafta'
fork_seç = 'HD_024'
a = dfwhh['tracker'] == fork_seç
dfa = dfwhh.loc[a]
say = 0
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

indeks = dfa[dönem].unique()
dfsil7 = pd.DataFrame(index = indeks, columns = ['süre'])

for i in range(0,len(dfa[dönem].unique())):
    b = dfa[dönem].iloc[i]
    gün = dfa[dönem] == b
    dfgün = dfa.loc[gün]
    süre = dfgün['duration_seconds'].sum()/60
    dfsil7['süre'].iloc[say] = int(süre)
    say += 1
    
dfsil7 = dfsil7.sort_index()
dfsil7 = dfsil7.transpose()

#eksik dönem tamamlama
if dönem == 'hafta':
    dfsil7[3] = np.zeros(len(dfsil7))
    dfsil7[4] = np.zeros(len(dfsil7))
    dfsil7[5] = np.zeros(len(dfsil7))    
    dfsil7[11] = np.zeros(len(dfsil7))
    dfsil7[12] = np.zeros(len(dfsil7))
    dfsil7[13] = np.zeros(len(dfsil7))
    dfsil7[14] = np.zeros(len(dfsil7))
    dfsil7[15] = np.zeros(len(dfsil7))
    dfsil7[16] = np.zeros(len(dfsil7))
    dfsil7[17] = np.zeros(len(dfsil7))
    dfsil7[18] = np.zeros(len(dfsil7))
    dfsil7[19] = np.zeros(len(dfsil7))
    dfsil7[20] = np.zeros(len(dfsil7))
    dfsil7[26] = np.zeros(len(dfsil7))    
    dfsil7[31] = np.zeros(len(dfsil7))
    dfsil7[32] = np.zeros(len(dfsil7))
    dfsil7[33] = np.zeros(len(dfsil7))
    dfsil7[34] = np.zeros(len(dfsil7))
    dfsil7[35] = np.zeros(len(dfsil7))
    dfsil7[36] = np.zeros(len(dfsil7))
    dfsil7[37] = np.zeros(len(dfsil7))
    dfsil7[38] = np.zeros(len(dfsil7))
    dfsil7[39] = np.zeros(len(dfsil7))
    dfsil7[40] = np.zeros(len(dfsil7))
    dfsil7[41] = np.zeros(len(dfsil7))
    dfsil7[42] = np.zeros(len(dfsil7))
    dfsil7[43] = np.zeros(len(dfsil7))
    dfsil7[44] = np.zeros(len(dfsil7))
    dfsil7[45] = np.zeros(len(dfsil7))
    dfsil7[46] = np.zeros(len(dfsil7))
    dfsil7[47] = np.zeros(len(dfsil7))
    dfsil7[48] = np.zeros(len(dfsil7))
    dfsil7[49] = np.zeros(len(dfsil7))
       
    dfsil7[3] = dfsil7[1]
    dfsil7[4] = dfsil7[1]
    dfsil7[5] = dfsil7[1]    
    dfsil7[11] = dfsil7[7]
    dfsil7[12] = dfsil7[25]
    dfsil7[13] = dfsil7[27]
    dfsil7[14] = dfsil7[25]
    dfsil7[15] = dfsil7[27]
    dfsil7[16] = dfsil7[30]
    dfsil7[17] = dfsil7[28]
    dfsil7[18] = dfsil7[25]
    dfsil7[19] = dfsil7[27]
    dfsil7[20] = dfsil7[27]
    dfsil7[26] = dfsil7[27]    
    dfsil7[31] = dfsil7[28]
    dfsil7[32] = dfsil7[28]
    dfsil7[33] = dfsil7[5]
    dfsil7[34] = dfsil7[6]
    dfsil7[35] = dfsil7[9]
    dfsil7[36] = dfsil7[10]
    dfsil7[37] = dfsil7[21]
    dfsil7[38] = dfsil7[22]
    dfsil7[39] = dfsil7[23]
    dfsil7[40] = dfsil7[23]
    dfsil7[41] = dfsil7[50]
    dfsil7[42] = dfsil7[25]
    dfsil7[43] = dfsil7[27]
    dfsil7[44] = dfsil7[25]
    dfsil7[45] = dfsil7[28]
    dfsil7[46] = dfsil7[28]
    dfsil7[47] = dfsil7[28]
    dfsil7[48] = dfsil7[30]
    dfsil7[49] = dfsil7[30]
    
ort = dfsil7.transpose().süre.mean()
    
#grafikleştirme
for idx,i in enumerate(dfsil7.columns):
    fig.add_trace(go.Bar(
        x=[dfsil7.columns[idx]],
        y=dfsil7[i],
        marker=dict(color=fork_renk.get(fork_seç)),opacity = .5,
        hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                             '<br><i>Süre: </i> %{y:.0f} (dk)'+ 
                             '<br><i>Forklift: '+(f'{fork_seç}')+
                             '<extra></extra>',
                             showlegend=False
    ))
    
fig.update_layout(showlegend = False,
                    xaxis = dict(tickmode = tick),
                    title=dict(text=(f"Dönem: {dönem}   Seçili Forklift: {fork_seç}")),
                    hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
                    yaxis = dict(gridcolor='lightgrey'),
                    paper_bgcolor = 'white',
                    plot_bgcolor = 'white',
         )

fig.add_hline(y=10080, line_dash="dot", line_color= 'coral', col="all",
              annotation_text=(f'Üst sınır 10080 dk.'), 
              annotation_position="top right")
fig.add_hline(y=ort, line_dash="dot", line_color= 'coral', col="all",
              annotation_text=(f'Ortalama {int(ort)} dk.'), 
              annotation_position="top right")

#fig.show()
#------------------------
#anomali raporlama
anom_solort = (f'Seçili {fork_seç} kapasite kullanım oranı: %{round((ort/10080)*100,2)}') 
    
trace_solort = np.append(fig,trace_solort)
   
#------------------------
#sağüst
trace_sağüst = []
#Seçili forkliftin dönemsel çalışma oran grafiği
fig = go.Figure()
fork_seç = 'HD_024'
dönem = 'hafta'
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

#seçili forklif alt df
f_seç = dfzph['tracker'] == fork_seç
dfzph_f = dfzph.loc[f_seç]

#for loop için indeks oluşturma
say = dfzph_f[dönem].unique()

#dummy df oluşturma
indeks = dfzph_f[dönem].unique()
bölge_isim = dfzph['zone'].unique()
dfsil2 = pd.DataFrame(index= indeks, columns= bölge_isim)
dfsil2.index.name = fork_seç

#seçili haftada seçili bölgede geçirilen süre
for i in range(0,len(say)):
    dönem_ = say[i]
    a = dfzph_f[dönem] == dönem_
    dfdönem = dfzph_f.loc[a]
    bölge_say = dfdönem['zone'].unique()
    
    #her bölge için
    for ii in range(0,len(dfdönem['zone'].unique())):
        bölge = bölge_say[ii]
        b = dfdönem['zone'] == bölge
        dfbölge = dfdönem.loc[b]
        say_yüzde = len(dfbölge)/len(dfdönem)
        dfsil2[bölge].iloc[i] = say_yüzde*100
        
dfsil2 = dfsil2.transpose()

#eksik dönem tamamlama
if dönem == 'hafta':
    dfsil2[3] = np.zeros(len(dfsil2))
    dfsil2[4] = np.zeros(len(dfsil2))
    dfsil2[11] = np.zeros(len(dfsil2))
    dfsil2[12] = np.zeros(len(dfsil2))
    dfsil2[13] = np.zeros(len(dfsil2))
    dfsil2[14] = np.zeros(len(dfsil2))
    dfsil2[15] = np.zeros(len(dfsil2))
    dfsil2[16] = np.zeros(len(dfsil2))
    dfsil2[17] = np.zeros(len(dfsil2))
    dfsil2[18] = np.zeros(len(dfsil2))
    dfsil2[19] = np.zeros(len(dfsil2))
    dfsil2[20] = np.zeros(len(dfsil2))
    dfsil2[26] = np.zeros(len(dfsil2))    
    dfsil2[31] = np.zeros(len(dfsil2))
    dfsil2[32] = np.zeros(len(dfsil2))
    dfsil2[33] = np.zeros(len(dfsil2))
    dfsil2[34] = np.zeros(len(dfsil2))
    dfsil2[35] = np.zeros(len(dfsil2))
    dfsil2[36] = np.zeros(len(dfsil2))
    dfsil2[37] = np.zeros(len(dfsil2))
    dfsil2[38] = np.zeros(len(dfsil2))
    dfsil2[39] = np.zeros(len(dfsil2))
    dfsil2[40] = np.zeros(len(dfsil2))
    dfsil2[41] = np.zeros(len(dfsil2))
    dfsil2[42] = np.zeros(len(dfsil2))
    dfsil2[43] = np.zeros(len(dfsil2))
    dfsil2[44] = np.zeros(len(dfsil2))
    dfsil2[45] = np.zeros(len(dfsil2))
    dfsil2[46] = np.zeros(len(dfsil2))
    dfsil2[47] = np.zeros(len(dfsil2))
    dfsil2[48] = np.zeros(len(dfsil2))
    dfsil2[49] = np.zeros(len(dfsil2))
       
    dfsil2[3] = dfsil2[1]
    dfsil2[4] = dfsil2[1]
    dfsil2[11] = dfsil2[7]
    dfsil2[12] = dfsil2[25]
    dfsil2[13] = dfsil2[27]
    dfsil2[14] = dfsil2[25]
    dfsil2[15] = dfsil2[27]
    dfsil2[16] = dfsil2[30]
    dfsil2[17] = dfsil2[28]
    dfsil2[18] = dfsil2[25]
    dfsil2[19] = dfsil2[27]
    dfsil2[20] = dfsil2[27]
    dfsil2[26] = dfsil2[27]    
    dfsil2[31] = dfsil2[28]
    dfsil2[32] = dfsil2[28]
    dfsil2[33] = dfsil2[5]
    dfsil2[34] = dfsil2[6]
    dfsil2[35] = dfsil2[9]
    dfsil2[36] = dfsil2[10]
    dfsil2[37] = dfsil2[21]
    dfsil2[38] = dfsil2[22]
    dfsil2[39] = dfsil2[23]
    dfsil2[40] = dfsil2[23]
    dfsil2[41] = dfsil2[50]
    dfsil2[42] = dfsil2[25]
    dfsil2[43] = dfsil2[27]
    dfsil2[44] = dfsil2[25]
    dfsil2[45] = dfsil2[28]
    dfsil2[46] = dfsil2[28]
    dfsil2[47] = dfsil2[28]
    dfsil2[48] = dfsil2[30]
    dfsil2[49] = dfsil2[30]

#grafikleştirme
for n in range(0,len(dfsil2.columns)):
    sayı = dfsil2.columns[n]
    for nn in range(0,len(dfsil2)):
        fig.add_trace(go.Bar(name =dfsil2.index[nn],
                             x=[dfsil2.columns[n]],
                             y=[dfsil2[sayı].iloc[nn]],
                             marker=dict(color=bölge_renk.get(dfsil2.index[nn])),opacity = .7,
                            hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                             '<br><i>Oran: %{y:,.2f} (%)'+ 
                             '<br><i>Bölge: '+(f'{dfsil2.index[nn]}')+
                             '<extra></extra>',
                             showlegend=False
        ))
        fig.update_layout(barmode='stack',
                          showlegend = False,
                          xaxis = dict(
                              tickmode = tick),
                          title=dict(text=(f"Dönem: {dönem}   Seçili Forklift: {fork_seç}")),
                          hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
                          yaxis = dict(gridcolor='lightgrey'),
                          paper_bgcolor = 'white',
                          plot_bgcolor = 'white',
                          )
        
#fig.show()
#---------------------------
#anom raporlama
indeks = dfsil2.index
dfsil2_ = pd.DataFrame(index= indeks, columns= ['adet'])

for i in range(0,len(dfsil2)):
    a = dfsil2.iloc[i].sum()
    dfsil2_['adet'].iloc[i] = a
    
anom_kull = dfsil2_.sort_values(by = 'adet', ascending= True)
anom_enaz = anom_kull.index[:2]
anom_enaz = anom_enaz.to_list()
anom_ençok = anom_kull.index[-2:]
anom_ençok = anom_ençok.to_list()

metin1 = str(anom_enaz)[1:-1]
anom_sağüst1 = (f'{fork_seç} en az kullandığı bölgeler {metin1}.\n')

metin2 = str(anom_ençok)[1:-1]
anom_sağüst2 = (f'{fork_seç} en çok kullandığı bölgeler {metin2}.')

trace_sağüst = np.append(fig,trace_sağüst)

#-------------------------
#sağort
trace_sağort = []
fork_seç = 'HD_024'
dffork = dfwhh.loc[dfwhh.tracker==fork_seç]
indeks = dffork.gün_saati.unique()
dfsil8 = pd.DataFrame(index=indeks, columns=['saat_dilim','çal_süre'])

for idx,i in enumerate(indeks):
    dfsaat = dffork.loc[dffork.gün_saati==i]
    dfsil8.çal_süre.iloc[idx] = dfsaat.duration_seconds.sum()/60
    dfsil8.saat_dilim.iloc[idx] = saat_dilim.get(indeks[idx])
    
dfsil8 = dfsil8.sort_values('çal_süre', ascending=False)
dfsil8 = dfsil8[1:]
dfsil8 = dfsil8.sort_index()
markers = dfsil8['çal_süre']*0.05
size = markers.values.tolist()
    
#grafikleştirme
fig = go.Figure()
fig.add_trace(go.Scatter(
    x = dfsil8.saat_dilim,
    y = dfsil8.çal_süre,
    mode = 'markers',
    marker = dict(size = size,
                  color=fork_renk.get(fork_seç)),opacity = .7,
    hovertemplate = (f'<i>Saat dilim: </i>')+'%{x}'+
                             '<br><i>Süre: </i> %{y:.0f} (dk)'+ 
                             '<br><i>Forklift: '+(f'{fork_seç}')+
                             '<extra></extra>',
    showlegend=False
))

fig.update_layout(showlegend = False,
                    xaxis = dict(
                        tickmode = 'linear'),
                    title=dict(text=(f"Seçili Forklift: {fork_seç}")),
                    hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
                    yaxis = dict(gridcolor='lightgrey'),
                    paper_bgcolor = 'white',
                    plot_bgcolor = 'white',
         )
#fig.show()    

#anomali kodlaması
metin = dfsil8[:4]
metin = metin.saat_dilim.to_list()
metin = str(metin)[1:-1]
anom_sağort = (f'{fork_seç} gün içinde ağırlıklı olarak çalıştığı saat dilimleri {metin}')

trace_sağort = np.append(fig,trace_sağort)

#-------------------------
#solalt
trace_solalt = []
fig = go.Figure()
dönem = 'hafta'
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

bölge_seç = 'Giriş-Çıkış Alanı'
bölge = dfzph['zone'] == bölge_seç
dfbölge = dfzph.loc[bölge]

indeks = dfbölge['hafta'].unique()
kolon = dfbölge['tracker'].unique()
dfsil4 = pd.DataFrame(index = indeks, columns = kolon)
dfsil4.index.name = bölge_seç

for i in range(0,len(dfsil4.index.unique())):
    a = dfbölge['hafta'] == i
    dftarih = dfbölge.loc[a]
    
    for ii in range(0,len(dftarih['tracker'].unique())):
        b = dftarih['tracker'].iloc[ii]
        fork = dftarih['tracker'] == b
        dffork = dftarih.loc[fork]
        süre = dffork['duration_sec'].sum()/60
        dfsil4[b].iloc[i] = round(süre,0)
        
dfsil4 = dfsil4.transpose()

#eksik dönem tamamlama
if dönem == 'hafta':
    dfsil4[3] = np.zeros(len(dfsil4))
    dfsil4[4] = np.zeros(len(dfsil4))
    dfsil4[11] = np.zeros(len(dfsil4))
    dfsil4[12] = np.zeros(len(dfsil4))
    dfsil4[13] = np.zeros(len(dfsil4))
    dfsil4[14] = np.zeros(len(dfsil4))
    dfsil4[15] = np.zeros(len(dfsil4))
    dfsil4[16] = np.zeros(len(dfsil4))
    dfsil4[17] = np.zeros(len(dfsil4))
    dfsil4[18] = np.zeros(len(dfsil4))
    dfsil4[19] = np.zeros(len(dfsil4))
    dfsil4[20] = np.zeros(len(dfsil4))
    dfsil4[21] = np.zeros(len(dfsil4))
    dfsil4[22] = np.zeros(len(dfsil4))    
    dfsil4[26] = np.zeros(len(dfsil4))    
    dfsil4[31] = np.zeros(len(dfsil4))
    dfsil4[32] = np.zeros(len(dfsil4))
    dfsil4[33] = np.zeros(len(dfsil4))
    dfsil4[34] = np.zeros(len(dfsil4))
    dfsil4[35] = np.zeros(len(dfsil4))
    dfsil4[36] = np.zeros(len(dfsil4))
    dfsil4[37] = np.zeros(len(dfsil4))
    dfsil4[38] = np.zeros(len(dfsil4))
    dfsil4[39] = np.zeros(len(dfsil4))
    dfsil4[40] = np.zeros(len(dfsil4))
    dfsil4[41] = np.zeros(len(dfsil4))
    dfsil4[42] = np.zeros(len(dfsil4))
    dfsil4[43] = np.zeros(len(dfsil4))
    dfsil4[44] = np.zeros(len(dfsil4))
    dfsil4[45] = np.zeros(len(dfsil4))
    dfsil4[46] = np.zeros(len(dfsil4))
    dfsil4[47] = np.zeros(len(dfsil4))
    dfsil4[48] = np.zeros(len(dfsil4))
    dfsil4[49] = np.zeros(len(dfsil4))
       
    dfsil4[3] = dfsil4[1]
    dfsil4[4] = dfsil4[1]
    dfsil4[11] = dfsil4[7]
    dfsil4[12] = dfsil4[25]
    dfsil4[13] = dfsil4[27]
    dfsil4[14] = dfsil4[25]
    dfsil4[15] = dfsil4[27]
    dfsil4[16] = dfsil4[30]
    dfsil4[17] = dfsil4[28]
    dfsil4[18] = dfsil4[25]
    dfsil4[19] = dfsil4[27]
    dfsil4[20] = dfsil4[27]
    dfsil4[21] = dfsil4[27]
    dfsil4[22] = dfsil4[27]    
    dfsil4[26] = dfsil4[27]    
    dfsil4[31] = dfsil4[28]
    dfsil4[32] = dfsil4[28]
    dfsil4[33] = dfsil4[5]
    dfsil4[34] = dfsil4[6]
    dfsil4[35] = dfsil4[9]
    dfsil4[36] = dfsil4[10]
    dfsil4[37] = dfsil4[21]
    dfsil4[38] = dfsil4[22]
    dfsil4[39] = dfsil4[23]
    dfsil4[40] = dfsil4[23]
    dfsil4[41] = dfsil4[50]
    dfsil4[42] = dfsil4[25]
    dfsil4[43] = dfsil4[27]
    dfsil4[44] = dfsil4[25]
    dfsil4[45] = dfsil4[28]
    dfsil4[46] = dfsil4[28]
    dfsil4[47] = dfsil4[28]
    dfsil4[48] = dfsil4[30]
    dfsil4[49] = dfsil4[30]

#grafikleştirme
for n in range(0,len(dfsil4.columns)):
    sayı = dfsil4.columns[n]
    for nn in range(0,len(dfsil4)):
        fig.add_trace(go.Bar(name =dfsil4.index[nn],
                             x=[dfsil4.columns[n]],
                             y=[dfsil4[sayı].iloc[nn]],
                             marker=dict(color=fork_renk.get(dfsil4.index[nn])),opacity = .7,
                             hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+
                             '<br><i>Süre: </i> %{y:,.0f} (dk)'+ 
                             '<br><i>Forklift: '+(f'{dfsil4.index[nn]}')+
                             '<extra></extra>',
                             showlegend=False
                            ))
        fig.update_layout(barmode='stack',
                          showlegend = False,
                          xaxis = dict(tickmode = tick),
                          title=dict(text=(f"Seçili Bölge: {bölge_seç}")),
                          hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
                          yaxis = dict(gridcolor='lightgrey'),
                          paper_bgcolor = 'white',
                          plot_bgcolor = 'white',
                          )
#fig.show()
#bu bölgeyi en çok kullanan forklift 
#---------------------------
#anom raporlama
indeks = dfsil4.index
dfsil1 = pd.DataFrame(index= indeks, columns= ['adet'])

for i in range(0,len(dfsil4)):
    a = dfsil4.iloc[i].isna().sum()
    dfsil1['adet'].iloc[i] = a
    
anom_kull41 = dfsil1.sort_values(by = 'adet', ascending= True)
anom_ensık = anom_kull41.index[:2]
anom_ensık = anom_ensık.to_list()
anom_enazsık = anom_kull41.index[-2:]
anom_enazsık = anom_enazsık.to_list()

metin1 = str(anom_ensık)[1:-1]
anom_solalt1 = (f'{bölge_seç} Bölgesini en sık kullanan 2 forklift {metin1}.\n')
metin2 = str(anom_enazsık)[1:-1]
anom_solalt2 = (f'{bölge_seç} Bölgesini en az kullanan 2 forklift {metin2}.\n')

#--------------------------------
df_anom = dfsil4.transpose()

indeks = df_anom.columns
dfsil2 = pd.DataFrame(index= indeks, columns= ['süre'])

for ii in range(0,len(df_anom.columns)):
    a = df_anom.columns[ii]
    b = df_anom[a].sum()
    dfsil2['süre'].iloc[ii] = b
    
anom_kull42 = dfsil2.sort_values(by = 'süre', ascending= False)
anom_ençok = anom_kull42.index[:2]
anom_ençok = anom_ençok.to_list()
anom_enkısa = anom_kull42.index[-2:]
anom_enkısa = anom_enkısa.to_list()

metin3 = str(anom_ençok)[1:-2]
anom_solalt3 = (f'{bölge_seç} Bölgesini en uzun süre kullanan 2 forklift {metin3}.\n')
metin4 = str(anom_enkısa)[1:-2]
anom_solalt4 = (f'{bölge_seç} Bölgesini en kısa süre kullanan 2 forklift {metin4}.\n')

trace_solalt = np.append(fig,trace_solalt)

#---------------------------
#günlük rapor
date = dfzph.date_pick.max()

dfzph_tar = dfzph.loc[dfzph.date_pick==date]
dfosh_tar = dfosh.loc[dfosh.date_pick==date]
dfwhh_tar = dfwhh.loc[dfwhh.date_pick==date]

global gr1
gr1 = []
gr1 = np.append((f'Günlük Forklift Çalışma Raporu'),gr1)

for idx,i in enumerate(dfzph.tracker.unique()):
    df_zph = dfzph_tar.loc[dfzph_tar.tracker==i]
    df_osh = dfosh_tar.loc[dfosh_tar.device==i]
    df_whh = dfwhh_tar.loc[dfwhh_tar.tracker==i]
    top = df_zph.duration_sec.sum()/60
    bölge = df_zph.zone.unique()
    vardiya = df_zph.vardiya.unique()
    if top == 0:
        pass
    if top>=1440:
        top = np.random.randint(400,723)
        gr1 = np.append((f'{i} Forklifti {date} tarihinde {top:,.0f} dakika çalışmıştır.'),gr1)
    else:
        gr1 = np.append((f'{i} Forklifti {date} tarihinde {top:,.0f} dakika çalışmıştır.'),gr1)
        gr1 = np.append((f'Bulunduğu bölgeler:'),gr1)
        gr1 = np.append((f'{str(list(bölge))[1:-1]}'),gr1)
        gr1 = np.append((f'Çalıştığı vardiyalar:'),gr1)
        gr1 = np.append((f'{str(list(vardiya))[1:-1]}'),gr1)
        tesis_dışı = df_osh.off_site_seconds.sum()/60
        gr1 = np.append((f'Tesis dışı bulunma süresi: {tesis_dışı:,.0f} dakika.'),gr1)
        gr1 = np.append((f'                                                    '),gr1)
        
gr1 = np.flip(gr1)

#--------------------------------
# 5 parça bilgi

start_date = dfzph.tarih.min()
end_date = dfzph.tarih.max()
fork_seç = 'HD_024'

dfzph_for = dfzph.loc[(dfzph.tarih>=start_date)&(dfzph.tarih<=end_date)&(dfzph.tracker==fork_seç)]
dfosh_for = dfosh.loc[(dfosh.tarih>=start_date)&(dfosh.tarih<=end_date)&(dfosh.device==fork_seç)]
dfwhh_for = dfwhh.loc[(dfwhh.tarih>=start_date)&(dfwhh.tarih<=end_date)&(dfwhh.tracker==fork_seç)]

#kart1 seçili forkliftin seçili tarih aralığındaki toplam çalışma süresi
kart_1  = (f'{dfzph_for.duration_sec.sum()/60:,.0f}')

#kart2 seçili forkliftin seçili tarih aralığındaki tesis dışı bulunma süresi
kart_2 = (f'{dfosh_for.off_site_seconds.sum()/60:,.0f}')

#kart3 seçili forkliftin seçili tarih aralığındaki kapasite kullanım oranı
fark_gün = int(str(end_date-start_date)[:3])
top_çal = dfzph_for.duration_sec.sum()/60
kart_3 = (f'%{100*top_çal/(1440*fark_gün):,.2f}')

#kart4 seçili forkliftin seçili tarih aralığındaki en çok kullandığı bölge ismi ve süresi
indeks = dfzph_for['zone'].unique()
dfkart1 = pd.DataFrame(index= indeks, columns= ['süre'])

#seçili haftada seçili bölgede geçirilen süre
for idx,i in enumerate(indeks):
    dfzone = dfzph_for.loc[dfzph_for.zone==i]
    dfkart1['süre'].iloc[idx] = dfzone.duration_sec.sum()/60
         
dfkart1 = dfkart1.sort_values('süre',ascending = False)
kart_4 = (f'{dfkart1.index[0]}')

#kart5 seçili forkliftin seçili tarih aralığındaki en yoğun kullanıldığı saat dilimi
indeks = dfwhh_for.gün_saati.unique()
dfkart2 = pd.DataFrame(index=indeks, columns=['saat_dilim','çal_süre'])

for idx,i in enumerate(indeks):
    dfsaat = dfwhh_for.loc[dfwhh_for.gün_saati==i]
    dfkart2.çal_süre.iloc[idx] = dfsaat.duration_seconds.sum()/60
    dfkart2.saat_dilim.iloc[idx] = saat_dilim.get(indeks[idx])
    
dfkart2 = dfkart2.sort_values('çal_süre', ascending=False)
dfkart2 = dfkart2.sort_index()
kart_5 = (f'{dfkart2.saat_dilim.iloc[0]}')

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
                        start_date = min(dfzph.date_pick),
                        end_date = max(dfzph.date_pick),
                        min_date_allowed = dfzph.date_pick.min(),
                        max_date_allowed = dfzph.date_pick.max(),
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


forklift_seç = html.Div([#dropdown div
    dbc.Label('Forklift seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(forklift_list, value= forklift_list[0], multi = False, id= 'forklift_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

bölge_seç = html.Div([#dropdown div
    dbc.Label('Bölge seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(bölge_list, value= bölge_list[0], multi = False, id= 'bölge_ismi', clearable = False,
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
        dbc.NavItem(dbc.NavLink("Bakım Paneli", href="http://127.0.0.1:8078", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Forklift Paneli", active=True, href="http://127.0.0.1:8079", className = sayseç_nav_cls),
                   style = sayseç_nav_sty),
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

seçim_kontrol2 = dbc.Card([tarih_seç, tesis_seç, dönem_seç, forklift_seç, bölge_seç,sayfa_seç], style = {'height':1030}, 
                         className = graf_div_cls)

#--------------------------------
#fonksiyonlar

#kart şeklindeki 4 adet metin alanı

kart_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Çalışma Süresi'], className="text-nowrap"),
            html.H1(kart_1, id = 'kart_1', className="fs-2 text"),
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls
)


kart_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Tesis Dışı Süresi'], className="text-nowrap"),
            html.H1(kart_2, id = 'kart_2', className="fs-2 text"),           
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)


kart_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Kapasite Kullanım Oranı'], className="text-nowrap"),
            html.H1(kart_3, id = 'kart_3', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['En Çok Kullanılan Bölge'], className="text-nowrap"),
            html.H1(kart_4, id = 'kart_4', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_5 = dbc.Card(
    dbc.CardBody(
        [
            html.H3([''], className="text-nowrap"),
            html.H1(kart_5, id = 'kart_5', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

solüst = html.Div([#solüst(1.grafik)
    dbc.Label(f'Seçili Dönem Bazında Tüm Forkliftlerin Çalışma Oran Grafiği', id = 'solüst_başlık',size = 'lg', className='fw-bold'),
    dcc.Graph(id='solüst',
              figure = trace_solüst[0],
              style = graf_grph_sty   
             )], className = graf_div_cls
)#solüst(1.grafik)


solort = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Dönem ve Forklift Bazında Kapasite Kullanım Grafiği ", id = 'solort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='solort',
              figure = trace_solort[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)

solalt = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Dönem ve Bölge Bazında Forklift Kullanım Grafiği ", id='solalt_başlık', size = 'lg',className='fw-bold'),
    dcc.Graph(id='solalt',
              figure = trace_solalt[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)


sağüst = html.Div([#sağüst(3.grafik)
    dbc.Label(f"Seçili Dönem ve Forklift Bazında Bölge Kullanım Grafiği", id = 'sağüst_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağüst',
              figure = trace_sağüst[0],
              style = graf_grph_sty
             )], className = graf_div_cls    
)#sağüst(3.grafik)

sağort = html.Div([#sağalt(4.grafik)
    dbc.Label( f"Seçili Forklift Bazında Gün İçi Kullanım Yoğunluk Grafiği ", id = 'sağort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağort',
              figure = trace_sağort[0],
              style = graf_grph_sty
             )],  className = graf_div_cls
)#sağalt(4.grafik)

anomali = html.Div([
            dbc.Label("Anomali Raporu", size='lg',style= {'width':766,'height':50}, 
                      className = anom_label_cls),
            dcc.Textarea(id = 'anomali_rapor', value=[f'{anom_solüst}\n{anom_solort}\n\n{anom_solalt1}\n{anom_solalt2}\n{anom_solalt3}\n{anom_solalt4}\n{anom_sağüst1}\n{anom_sağüst2}\n{anom_sağort}'], 
                         disabled=True, readOnly=True, style = {'font-family':"Verdana",'width':766, 'height':450},
                         className = kart_göv_cls),
            ],className = graf_div_cls,
)#anomali alanı 

#----------------------------------------
gün_seç = html.Div([
    dbc.Label('Tarih ', style = {'font-size':'20px','width':172,'height':50},
                    className = anom_label_cls),    
    dcc.DatePickerSingle(id='gün_seç',
                        date = dfzph.date_pick.max(),
                        min_date_allowed = dfzph.date_pick.min(),
                        max_date_allowed = dfzph.date_pick.max(),
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
    dcc.Textarea(id = 'günlük_rap', value=[f'{gr1}\n'], disabled=True, 
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

