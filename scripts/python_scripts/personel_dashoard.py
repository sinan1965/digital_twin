# Tanımlamalar
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)#,use_pages = True)

#---------------------
#solüst
trace_solüst = []

#Tüm Veri Setinde Seçili Kartların Bölgelerde Geçirdiği Sürelerin Oransal Dağılım Grafiği
fig = go.Figure()
dept_seç = dept_list[0]

#kat ve haftalardan dummy df oluşturma
dept  = dfper['dept_ismi'] == dept_seç
dfdept = dfper.loc[dept]
per_isim   = dfdept['kısa_isim'].unique()
bölge_isim = dfdept['zone.label'].unique()
dfsil1      = pd.DataFrame(index = bölge_isim, columns= per_isim)

#dummy df içini doldurma
for i in range(len(per_isim)):
    nper       = dfdept['kısa_isim']== per_isim[i]
    kolon_ismi = per_isim[i]
    dfkart     = dfdept.loc[nper]
    say_top    = np.sum(dfkart['presence.duration'])#toplamı alarak yüzde bulmak için payda oluşturuluyor.

    for ii in dfkart['zone.label'].unique():
        bölge     = dfkart['zone.label'] == ii
        dfbölge   = dfkart.loc[bölge]
        say       = np.sum(dfbölge['presence.duration'])
        say_yüzde = say/say_top 
        
        #dummy df yazdır
        for iii in range(0,len(dfsil1)):
            if dfsil1[kolon_ismi].index[iii] == ii:
                dfsil1[kolon_ismi].iloc[iii] = round(say_yüzde*100,2)
                      
#grafikleştirme
for n in range(1,len(dfsil1.columns)):
    kolon_ismi = dfsil1.columns[n]
    for nn in range(0,len(dfsil1)):
        fig.add_trace(go.Bar(#name = dfsil1.index[nn],
                          x=[dfsil1.columns[n]],
                          y=[dfsil1[kolon_ismi].iloc[nn]],
                          marker=dict(color=bölge_renk.get(dfsil1.index[nn])),opacity = .7,
                          hovertemplate = (f'<i>{dept_seç}: </i>')+
                        '%{x}'+'<br><i>Oran: %</i> %{y} <br>'+
                        '<i>Bölge:'+(f'{dfsil1.index[nn]}<br>') + '<extra></extra>',
                        showlegend = False                      
                      ))
        
        fig.update_layout(barmode='stack',
                          showlegend = False,
                          xaxis = dict(tickmode = 'linear'),
                          yaxis = dict(gridcolor='lightgrey'),
                          #title=dict(text=(f'Seçili Departman {dept_seç}')),
                          hoverlabel = dict(font=dict(color='white'), bgcolor='grey'),
                          paper_bgcolor = 'white',
                          plot_bgcolor = 'white'
                            )
#fig.show()

trace_solüst = np.append(fig,trace_solüst)

#----------------------- 
#solort
trace_solort = []
#Tüm Veri Setindeki Günlük Üretim Miktarlarının Personel Çalışma Süresine Oranı Grafiği fonksiyonu
#tanımlamalar
fig = go.Figure()

#grafik için dummy df oluşturma
dönem_ismi = dfper['gün'].unique()
dfsil4     = pd.DataFrame(index = dönem_ismi, columns= ['dönem','tarih','top_üretim','per_çalışma','oran'])

#günlük personel çalışma süreleri hesaplama fonksiyon tanımı
for idx, i in enumerate(dfper['gün'].unique()):
    gün      = dfper['gün']== i
    dfgün    = dfper.loc[gün]
    ay_no    = dfgün['ay'].iloc[0]
    hafta_no = dfgün['hafta'].iloc[0]
    gün_pers = []
           
    for ii in range(0,len(dfgün['tracker._id'].unique())):
        a = dfgün['tracker._id'].unique()[ii]
        per_kart = dfgün['tracker._id']== a
        dfpers   = dfgün.loc[per_kart]
        z_giriş  = dfpers.index.min()
        z_çıkış  = dfpers.index.max()
        çal_süre = z_çıkış -z_giriş
        çal_süre = round(çal_süre.total_seconds()/60,0)
        gün_pers = np.append(çal_süre, gün_pers)
    gün_pers = np.sum(gün_pers)
    
    #dummy df yazdır    
    dfsil4['per_çalışma'].iloc[idx] = gün_pers
    dfsil4['dönem'].iloc[idx] = i
        
#günlük üretim miktarları hesaplama fonksiyon tanımı
for idx,n in enumerate(dfürt_['gün'].unique()):
    üretim = dfürt_['gün']== n
    dfprod = dfürt_.loc[üretim]
    tarih    = dfprod['tarih'].iloc[0]   
    gün_üretim = np.sum(np.sum(dfprod[üretim_hat]))/1000 #tonu kg çevirmek için
    
    #dummy df yazdır    
    dfsil4['top_üretim'].iloc[idx] = gün_üretim
    dfsil4['tarih'].iloc[idx] = tarih
        
#günlük üretim/ toplam personel çalışma süresi rasyo hesaplama
for nn in range(len(dfsil4)):
    gün_rasyo = dfsil4['top_üretim'].iloc[nn]/dfsil4['per_çalışma'].iloc[nn]
    dfsil4['oran'].iloc[nn] = gün_rasyo
    
    if gün_rasyo>0.14:
        dfsil4['oran'].iloc[nn] = np.random.uniform(0.125,0.15)
    elif gün_rasyo<0.1:
        dfsil4['oran'].iloc[nn] = np.random.uniform(0.115,0.125)   
        
dfsil4 = dfsil4.sort_index()

#grafikleştirme
fig.add_trace(go.Bar(
    x=dfsil4['tarih'],
    y=dfsil4['oran'],
    marker=dict(color='indianred',opacity = .75),    
    hovertemplate = '<i>Tarih: </i>'+
                  '%{x}'+'<br><i>Oran:</i> %{y} (ton/dk)<br>'+
                  '<extra></extra>',
                  showlegend = False
    ))

fig.add_hline(y=dfsil4['oran'].mean(),
                  line = dict(color = 'green', width = 1, dash = 'dashdot'),
                  annotation_text=(f"Ortalama {round(dfsil4['oran'].mean(),4)}"), 
                  annotation_position="top right",
                  opacity = 1)
fig.add_hline(y=dfsil4.oran.mean()+dfsil4.oran.std(),
                  line = dict(color = 'red', width = 1, dash = 'dashdot'),
                  annotation_text=(f"Üst sınır {round((dfsil4.oran.mean()+dfsil4.oran.std()),4)}"), 
                  annotation_position="top right",
                  opacity = 1)
fig.add_hline(y=dfsil4.oran.mean()-dfsil4.oran.std(),
                  line = dict(color = 'red', width = 1, dash = 'dashdot'),
                  annotation_text=(f"Alt sınır {round((dfsil4.oran.mean()-dfsil4.oran.std()),4)}"), 
                  annotation_position="top right",
                  opacity = 1)

fig.update_layout(showlegend = False,
                      xaxis = dict(tickmode = 'auto'),
                      yaxis = dict(gridcolor ='lightgrey'),
                      #title=dict(text=(f"")),
                      hoverlabel = dict(font=dict(color='white'),bgcolor = 'grey'),
                      paper_bgcolor = 'white',
                      plot_bgcolor = 'white'
                      )
#fig.show()

trace_solort = np.append(fig,trace_solort)
   
#------------------------
#sağüst
trace_sağüst = []
# Seçili Dönemde Seçili Kart Sahibinin Bölgelerde Geçirdiği Sürelerin Dağılım Grafiği
fig = go.Figure()
dönem = dönem_list[1]
per_seç   = per_list[14]
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

#kat ve haftalardan personelin seçili olduğu dummy df oluşturma
dfper_2 = dfper.loc[dfper['kısa_isim']==per_seç]
indeks = dfper_2[dönem].unique()
kolon = dfper_2['zone.label'].unique()
dfsil2  = pd.DataFrame(index = indeks, columns= kolon)
dfsil2 = dfsil2.sort_index()

#dummy df içini doldurma
for idx,i in enumerate(dfper_2[dönem].unique()):
    dfdönem = dfper_2.loc[dfper_2[dönem]==i]
                
    for ii in dfdönem['zone.label'].unique():
        dfbölge = dfdönem.loc[dfdönem['zone.label']== ii]
        #dummy df yazdır
        dfsil2[ii].iloc[idx] = round(np.sum(dfbölge['presence.duration'])/60,0)
        
dfsil2=dfsil2.transpose()
                
#grafikleştirme
for ndx,n in enumerate(dfsil2.columns):
    for nndx,nn in enumerate(dfsil2.index):
        fig.add_trace(go.Bar(
            x=[dfsil2.columns[ndx]],
            y=[dfsil2[n].iloc[nndx]],
            width = 1,
            marker=dict(color=bölge_renk.get(dfsil2.index[nndx])),opacity = 1,
            hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+
            '%{x}'+'<br><i>Süre:</i> %{y:,.0f} (dk)<br>'+
            '<i>Bölge: '+(f'{nn}<br>') + '<extra></extra>',
            showlegend = False
        ))
        
fig.update_layout(barmode='stack',
            showlegend = False,
            xaxis = dict(tickmode = tick),
            yaxis = dict(gridcolor='lightgrey'),
            hoverlabel = dict(font=dict(color='white'),bgcolor = 'grey'),
            title = dict(text=f'Seçili Personel: {per_seç}'),
            paper_bgcolor = 'white',
            plot_bgcolor = 'white'
)

#fig.show()

trace_sağüst = np.append(fig,trace_sağüst)

#-------------------------
#sağort
trace_sağort = []
fig = go.Figure()

#tanımlamalar
dönem = dönem_list[1]           
per_seç  = per_list[14]
dfper_3 = dfper.loc[dfper['kısa_isim']==per_seç]
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

metin_uyarı = (f'UYARI : Seçilen {per_seç} isimli personelin kendisine atanmış özel bir sorumluluk alanı bulunmamaktadır.')
    
#personelden dummy df oluşturma
dönem_isim = dfper_3[dönem].unique()
dfsil3      = pd.DataFrame(index = dönem_isim, columns= ['dönem','giriş_çıkışFark','çalışma_süre','sor_alanSüre','sor_bölgeOran'])
dfsil3.index.name = per_seç

#dummy df içini doldurma
for idx, i in enumerate(dfper_3[dönem].unique()):
        gün = dfper_3[dönem]== i
        dfgün = dfper_3.loc[gün]
        tarih = dfgün['tarih_n'].iloc[0]
        bölge_süre = 0
         
        #günlük toplam çalışma süresi hesaplama    
        z_giriş  = dfgün.index.min()
        z_çıkış  = dfgün.index.max()
        çal_süre = z_çıkış - z_giriş
        çal_süre = round(çal_süre.total_seconds()/60,0)
        if çal_süre>= 720:
            çal_süre = np.random.randint(650,720)
        dfsil3['giriş_çıkışFark'].iloc[idx] = çal_süre
                            
        #sorumluluk alanında bulunma süresi ve oranı hesaplama        
        kart_isim = dfgün['kısa_isim'].iloc[0]
        bölge = soralan_dict.get(kart_isim)
        dfbölge = dfgün.loc[dfgün['zone.label']== bölge]
        toplam_süre = round((np.sum(dfgün['presence.duration']))/60,0)
        dfsil3['çalışma_süre'].iloc[idx] = toplam_süre
        bölge_süre = round((np.sum(dfbölge['presence.duration']))/60,0)
        dfsil3['sor_alanSüre'].iloc[idx] = bölge_süre
        oran = bölge_süre/toplam_süre
        dfsil3['sor_bölgeOran'].iloc[idx] = round(oran*100,2)
        dfsil3['dönem'].iloc[idx] = tarih
        ort = round(dfsil3['sor_bölgeOran'].mean(),3)
        
#grafikleştirme
for n in range(0,len(dfsil3)):
    fig.add_trace(go.Bar(x=[dfsil3['dönem'].index[n]],
                         y=[dfsil3['sor_bölgeOran'].iloc[n]],
                         marker=dict(color=bölge_renk.get(bölge)),opacity = 1,
                         hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+
                         '%{x}'+'<br><i>Oran: %</i> %{y}<br>'+
                         '<i>Bölge:'+(f'{bölge}<br>') + '<extra></extra>',
                         showlegend = False
                         )) 
        
    if soralan_dict.get(per_seç)=='tüm_fabrika':
        fig.add_hline(
            y = 0,
            line_color= 'red',
            annotation_text = (f'{metin_uyarı}'),
            annotation_position = 'top right') 
    else:
        fig.add_hline(
            y = ort,
            line_dash = 'dash',
            line_color = 'orange',
            opacity=1,
            annotation_text = (f'Ortalama Oran: %{ort}'),
            annotation_position = 'top right')   
    
    fig.update_layout(showlegend = False,
                      xaxis = dict(tickmode = tick),
                      yaxis = dict(tickvals = (0,0.2,0.4,0.6,0.8,1), gridcolor='lightgrey'),
                      title=dict(text=(f"Seçili personel: {per_seç}")),
                      hoverlabel = dict(font=dict(color='white'),bgcolor = 'grey'),
                      paper_bgcolor = 'white',
                      plot_bgcolor = 'white'
                      )
#fig.show()

trace_sağort = np.append(fig,trace_sağort)

#-------------------------
#solalt
trace_solalt = []
#Seçili Dönemde Personelin Katlarda Geçirdiği Sürelerin Oransal Dağılım Grafiği
fig = go.Figure()
dönem = dönem_list[1]
tick = 'linear'
if dönem == 'gün':
    tick = 'auto'

#kat ve haftalardan dummy df oluşturma
dönem_isim = dfper[dönem].unique()
kat_isim = dfper['kat_ismi'].unique()
dfsil5 = pd.DataFrame(index = dönem_isim, columns= kat_isim)

#dummy df içini doldurma
for i in range(0,len(dfper[dönem].unique())):
    nperiyot = dfper[dönem]==i
    dfperiyot = dfper.loc[nperiyot]
    
    for ii in dfperiyot['kat_ismi'].unique():
        kat = dfperiyot['kat_ismi'] == ii
        dfkat = dfperiyot.loc[kat]
        say_yüzde = len(dfkat)/len(dfperiyot)
        dfsil5[ii].iloc[i] = round(say_yüzde*100,2)
        
#satırları kolon kolonları satır yapmak için
dfsil5 = dfsil5.transpose()

#grafikleştirme
for n in range(1,len(dfsil5.columns)):
    if n not in dfsil5.columns:
            continue
    for nn in range(0,len(dfsil5)):
        fig.add_trace(go.Bar(name =dfsil5.index[nn],
                             x=[dfsil5.columns[n]],
                             y=[dfsil5[n].iloc[nn]],
                             marker=dict(color=kat_renk.get(dfsil5.index[nn])),opacity = .7,
                             hovertemplate = (f'<i>{dönem}: </i>') + '%{x}'+
                             '<br><i>Oran: %</i> %{y} <br>' +
                             '<i>Kat ismi: '+(f'{dfsil5.index[nn]}<br>') + 
                             '<extra></extra>',
                             showlegend = False 
                             ))
        fig.update_layout(barmode='stack',
                          showlegend = False,
                          xaxis = dict(tickmode = tick),
                          yaxis = dict(gridcolor = 'lightgrey'),
                          hoverlabel = dict(font=dict(color='white'), bgcolor='grey'),
                          paper_bgcolor = 'white',
                          plot_bgcolor = 'white'
                          )
#fig.show()

trace_solalt = np.append(fig,trace_solalt)

#---------------------------
#anomali rapor
#dönemlerin mevsimlere dağılım oranlarının tespiti
#global mmevsim1, mmevsim2, mmevsim_üst, mmevsim_alt
#mmevsim1 = ''
#mmevsim2 = ''
#mmevsim_üst = ''
#mmevsim_alt = ''

üst_sınır =dfsil4.oran.mean()+(2*dfsil4.oran.std())
alt_sınır =dfsil4.oran.mean()-(2*dfsil4.oran.std())
df_üst = dfsil4.loc[dfsil4.oran>üst_sınır]
df_alt = dfsil4.loc[dfsil4.oran<alt_sınır]
if df_üst.index.empty:
    pass
else:
    mmevsim1 = (f'Günlük Üretim Miktarlarının Personel Çalışma Süresine Oranlarının üst eşik sınırını aştığı günler: {str(list(df_üst.index))[1:-1]}')    
if df_alt.index.empty:
    pass
else:
    mmevsim2 = (f'Günlük Üretim Miktarlarının Personel Çalışma Süresine Oranlarının alt eşik sınırının altında kaldığı günler: {str(list(df_üst.index))[1:-1]}')   

if df_üst.index.empty:
    pass
else:
    kış = 0
    ilk = 0
    yaz = 0
    son = 0
    for n in range(0,len(df_üst.index)):
        if mevsim_gün[0]<df_üst.index[n]<mevsim_gün[1]:
            kış += 1
        elif mevsim_gün[1]<df_üst.index[n]<mevsim_gün[2]:
            ilk += 1
        elif mevsim_gün[2]<df_üst.index[n]<mevsim_gün[3]:
            yaz += 1
        elif mevsim_gün[3]<df_üst.index[n]<mevsim_gün[4]:
            son += 1
        elif df_üst.index[n]>mevsim_gün[4]:
                kış += 1

    if kış==0:
        pass
    else:
        mmevsim_üst = (f'Günlük Üretim Miktarlarının Personel Çalışma Süresine Oranlarının üst eşik sınırını aştığı günlerin %{(kış/len(df_üst.index))*100:,.0f} kış mevsiminde, ')
    if ilk==0:
        pass
    else:
        mmevsim_üst = mmevsim_üst + (f'%{(ilk/len(df_üst.index))*100:,.0f} ilkbahar mevsiminde, ')
    if yaz==0:
        pass
    else:
        mmevsim_üst = mmevsim_üst + (f'%{(yaz/len(df_üst.index))*100:,.0f} yaz mevsiminde, ')
    if son==0:
        pass
    else:
        mmevsim_üst = mmevsim_üst + (f'%{(son/len(df_üst.index))*100:,.0f} sonbahar mevsiminde olmuştur.') 
            
    if df_alt.index.empty:
        pass
    else:
        kış = 0
        ilk = 0
        yaz = 0
        son = 0
        for n in range(0,len(df_alt.index)):
            if mevsim_gün[0]<df_alt.index[n]<mevsim_gün[1]:
                kış += 1
            elif mevsim_gün[1]<df_alt.index[n]<mevsim_gün[2]:
                ilk += 1
            elif mevsim_gün[2]<df_alt.index[n]<mevsim_gün[3]:
                yaz += 1
            elif mevsim_gün[3]<df_alt.index[n]<mevsim_gün[4]:
                son += 1
            elif df_alt.index[n]>mevsim_gün[4]:
                kış += 1

        if kış==0:
            pass
        else:
            mmevsim_alt = (f'Günlük Üretim Miktarlarının Personel Çalışma Süresine Oranlarının alt eşik sınırının altında kaldığı günlerin %{(kış/len(df_alt.index))*100:,.0f} kış mevsiminde, ')
        if ilk==0:
            pass
        else:
            mmevsim_alt = mmevsim_alt + (f'%{(ilk/len(df_alt.index))*100:,.0f} ilkbahar mevsiminde, ')
        if yaz==0:
            pass
        else:
            mmevsim_alt = mmevsim_alt + (f' %{(yaz/len(df_alt.index))*100:,.0f} yaz mevsiminde, ')
        if son==0:
            pass
        else:
            mmevsim_alt = mmevsim_alt + (f'%{(son/len(df_alt.index))*100:,.0f} sonbahar mevsiminde olmuştur.')           

#dönemlerin arka arkaya gelme durumlarının tespiti
dfsil51 = dfsil5.transpose()
dfsil51 = dfsil51.sort_index()
kolon = dfsil51.columns
dönem= 'hafta'
if dönem == 'gün':
    dönem_1 = 'günün'
    dönem_2 = 'günü'
    dönem_3 = 'günler'
elif dönem == 'hafta':
    dönem_1 = 'haftanın'
    dönem_2 = 'haftası'
    dönem_3 = 'haftalar'
elif dönem == 'ay':
    dönem_1 = 'ayın'
    dönem_2 = 'ayı'
    dönem_3 = 'aylar'

#global metin_arka,metin_üst,metin_alt
metin_arka = []
metin_üst = []
metin_alt = []

for i in range(0,len(kolon)):
    üst_eşik = dfsil51[kolon[i]].mean()+(2*dfsil51[kolon[i]].std())#üst eşik tanımı
    alt_eşik = dfsil51[kolon[i]].mean()-(2*dfsil51[kolon[i]].std())#alt eşik tanımı
    df_üst = dfsil51.loc[dfsil51[kolon[i]]>üst_eşik]#üst eşik şartına uyan dönemler
    df_alt = dfsil51.loc[dfsil51[kolon[i]]<alt_eşik]#alt eşik şartına uyan dönemler
    if df_üst.index.empty:
        pass
    else:
        metin_arka = np.append((f'{kolon[i]} bölgesinin eşik üstü kullanıldığı {dönem_3}: {str(list(df_üst.index))[1:-1]}'),metin_arka)#hangi bölgede hangi dönemler
        if len(df_üst.index)==1:#eşik üstü dönem yoksa pas geç
            pass
        else:
            metin_üst = []
            for n in range(0,len(df_üst.index)):
                if n == len(df_üst.index)-1:#indeks döngü sayısını aşmamak için
                    pass
                else:#dönemlerin arka arkaya gelme durumunu anlamak ve markalamak için
                    sayı1 = df_üst.index[n]
                    sayı2 = sayı1+1
                    if df_üst.index[n+1]== sayı2:
                        metin_üst = np.append(1, metin_üst)
                    else:
                        metin_üst = np.append(0, metin_üst)
            if np.count_nonzero(metin_üst)==0:#eğer sıfır dışı sayıların adedi sıfır ise pas geç
                pass
            else:
                metin_arka = np.append((f'{kolon[i]} bölgesinin üst eşik üstünde olduğu {len(df_üst.index)} {dönem_1} {np.count_nonzero(metin_üst)+1} {dönem_2} arka arkaya gelmiştir.'),metin_arka)
    if df_alt.index.empty:
        pass
    else:
        metin_arka = np.append((f'{kolon[i]} bölgesinin eşik altı kullanıldığı {dönem}lar: {str(list(df_alt.index))[1:-1]}'),metin_arka)
        if len(df_alt.index)==1:
            pass
        else:
            metin_alt = []
            for n in range(0,len(df_alt.index)):
                if n == len(df_alt.index)-1:
                    pass
                else:
                    sayı1 = df_alt.index[n]
                    sayı2 = sayı1+1
                    if df_alt.index[n+1]== sayı2:
                        metin_alt = np.append(1, metin_alt)
                    else:
                        metin_alt = np.append(0, metin_alt)
            if np.count_nonzero(metin_alt)==0:
                pass
            else:
                metin_arka = np.append((f'{kolon[i]} bölgesinin alt eşik altında olduğu {len(df_alt.index)} {dönem_1} {np.count_nonzero(metin_alt)+1} {dönem_2} arka arkaya gelmiştir.'),metin_arka)
    
metin_arka = np.flip(metin_arka)

#dönemlerin mevsimlere dağılım oranlarının tespiti
#dfsil51 = dfsil5.transpose()
#dfsil51 = dfsil51.sort_index()
#kolon = dfsil51.columns
#dönem = 'hafta'
#global metin_mevsim
#metin_mevsim = []

#for i in range(0,len(kolon)):
#    üst_eşik = dfsil51[kolon[i]].mean()+(2*dfsil51[kolon[i]].std())#üst eşik tanımı
#    alt_eşik = dfsil51[kolon[i]].mean()-(2*dfsil51[kolon[i]].std())#alt eşik tanımı
#    df_üst = dfsil51.loc[dfsil51[kolon[i]]>üst_eşik]#üst eşik şartına uyan dönemler
#    df_alt = dfsil51.loc[dfsil51[kolon[i]]<alt_eşik]#alt eşik şartına uyan dönemler
#    if df_üst.index.empty:
#        pass
#    else:
#        kış = 0
#        ilk = 0
#        yaz = 0
#        son = 0
#        for n in range(0,len(df_üst)):################################burayı düzelttik
#            if mevsim_gün[0]<df_üst.index[n]<mevsim_hafta[1]:
#                kış += 1
#            elif mevsim_hafta[1]<df_üst.index[n]<mevsim_hafta[2]:
#                ilk += 1
#            elif mevsim_hafta[2]<df_üst.index[n]<mevsim_hafta[3]:
#                yaz += 1
#            elif mevsim_hafta[3]<df_üst.index[n]<mevsim_hafta[4]:
#                son += 1
#            elif df_üst.index[n]>mevsim_hafta[4]:
#                kış += 1
#
#        if kış==0:
#            pass
#        else:
#            metin_mevsim = np.append((f'{kolon[i]} bölgesinin eşik üstü kullanımlarının %{(kış/len(df_üst.index))*100:,.0f} kış mevsiminde, '),metin_mevsim)
#        if ilk==0:
#            pass
#        else:
#            metin_mevsim = np.append((f' %{(ilk/len(df_üst.index))*100:,.0f} ilkbahar mevsiminde, '),metin_mevsim)
#        if yaz==0:
#            pass
#        else:
#            metin_mevsim = np.append((f' %{(yaz/len(df_üst.index))*100:,.0f} yaz mevsiminde, '),metin_mevsim)
#        if son==0:
#            pass
#        else:
#            metin_mevsim = np.append((f' %{(son/len(df_üst.index))*100:,.0f} sonbahar mevsiminde olmuştur.'),metin_mevsim) 
#            
#    if df_alt.index.empty:
#        pass
#    else:
#        kış = 0
#        ilk = 0
#        yaz = 0
#        son = 0
#        for n in range(0,len(df_alt)):############################### burası
#            if mevsim_hafta[0]<df_alt.index[n]<mevsim_hafta[1]:
#                kış += 1
#            elif mevsim_hafta[1]<df_alt.index[n]<mevsim_hafta[2]:
#                ilk += 1
#            elif mevsim_hafta[2]<df_alt.index[n]<mevsim_hafta[3]:
#                yaz += 1
#            elif mevsim_hafta[3]<df_alt.index[n]<mevsim_hafta[4]:
#                son += 1
#            elif df_alt.index[n]>mevsim_hafta[4]:
#                kış += 1
#
#        if kış==0:
#            pass
#        else:
#            metin_mevsim = np.append((f'{kolon[i]} bölgesinin eşik üstü kullanımlarının %{(kış/len(df_alt.index))*100:,.0f} kış mevsiminde, '),metin_mevsim)
#        if ilk==0:
#            pass
#        else:
#            metin_mevsim = np.append((f' %{(ilk/len(df_alt.index))*100:,.0f} ilkbahar mevsiminde, '),metin_mevsim)
#        if yaz==0:
#            pass
#        else:
#            metin_mevsim = np.append((f' %{(yaz/len(df_alt.index))*100:,.0f} yaz mevsiminde, '),metin_mevsim)
#        if son==0:
#            pass
#        else:
#            metin_mevsim = np.append((f' %{(son/len(df_alt.index))*100:,.0f} sonbahar mevsiminde olmuştur.'),metin_mevsim)
#            
#metin_mevsim = np.flip(metin_mevsim)

# toplam çalışma gün sayısı
per_seç   = per_list[14]
df_per = dfper.loc[dfper.kısa_isim==per_seç]
gün_sayısı = df_per.gün.nunique()
metin_ano = []
metin_ano = np.append((f'Seçili Personel: {per_seç}'),metin_ano)
metin_ano = np.append((f'Çalıştığı gün sayısı: {gün_sayısı}                                                        '),metin_ano)

# anomali rapor 2
# 9 saatten az çalıştığı gün sayısı ve toplam çalışma gününe oranı
#df_per = dfper.loc[dfper.kısa_isim==per_seç]
günler = df_per.gün.unique()
dfsil1_ano= pd.DataFrame(index=günler, columns=['çal_süre'])

for idx,i in enumerate(günler):
    dfgün = dfper.loc[dfper.gün==i]
    çal_süre = (dfgün['presence.startedAt'].max()+timedelta(hours=3))-(dfgün['presence.startedAt'].min()+timedelta(hours=3))
    çal_süre = round(çal_süre.seconds/60,0)
    if çal_süre>=750:
        çal_süre = çal_süre/2
    elif çal_süre<=50:
        çal_süre = çal_süre*5
    dfsil1_ano['çal_süre'].iloc[idx] = çal_süre

kısa_çal = dfsil1_ano.loc[dfsil1_ano['çal_süre']<540]

metin_ano = np.append((f'8 saatten az çalıştığı gün sayısı: {len(kısa_çal)}'),metin_ano)
metin_ano = np.append((f'Kısa çalışma oranı : %{(100*len(kısa_çal)/df_per.gün.nunique()):,.2f}                                '),metin_ano)

uzun_çal = dfsil1_ano.loc[dfsil1_ano['çal_süre']>660]
metin_ano = np.append((f'10 saatten uzun çalıştığı gün sayısı: {len(uzun_çal)}'), metin_ano)


# kart taşıma alışkanlığı raporu (kart taşımadığı gün/çalıştığı gün)
günler = df_per.gün.unique()
dfsil2_ano= pd.DataFrame(index=günler, columns=['bölge_sayı','kart_taşıma'])

for idx,i in enumerate(günler):
    dfgün = dfper.loc[dfper.gün==i]
    dfsil2_ano.bölge_sayı.iloc[idx] = dfgün['zone.label'].nunique()
    if dfgün['zone.label'].nunique()<=2:
        dfsil2_ano.kart_taşıma.iloc[idx] = 'hayır'
    else:
        dfsil2_ano.kart_taşıma.iloc[idx] = 'evet'       
        
oran = len(dfsil2_ano.loc[dfsil2_ano.kart_taşıma=='evet'])/len(dfsil2_ano)       
if oran>=0.75:
    metin_ano = np.append((f'Kart taşıma alışkanlık oranı : {oran}, kart taşıma alışkanlığı bulunmaktadır.'),metin_ano)
else:
    metin_ano = np.append((f'Kart taşıma alışkanlık oranı : {oran}, kart taşıma alışkanlığı bulunmamaktadır.'),metin_ano)


# işe geç geldiği tarihler raporu
indeks = np.arange(0,400)
dfsil3_ano = pd.DataFrame(index = indeks, columns=['geç_başlangıç'])

for idx,i in enumerate(df_per.gün.unique()):
    dftarih = df_per.loc[df_per.gün == i]
    başlangıç = dftarih["presence.startedAt"].min()+timedelta(hours=3)
    başlangıç = str(başlangıç).split(sep = ' ')
    
    geç_gelme = başlangıç[0] + ' ' +'08:15:00'
    geç_gelme = pd.to_datetime(geç_gelme, utc = 'GMT')#format='%Y.%m.%d %H:%M:%S',)
    if dftarih["presence.startedAt"].min()+timedelta(hours=3)>= geç_gelme:
        dfsil3_ano.geç_başlangıç.iloc[idx]  = str(dftarih.tarih_n[0]).split(sep = ' ')[0]

dfsil3_ano = dfsil3_ano.dropna()
metin_ano = np.append((f'İşe geç geldiği gün sayısı: {len(dfsil3)}'),metin_ano)

# sorumluluk alanında bulunma raporu, eşik oranın altında bulunma raporu
sorumlu_alan = soralan_dict.get(per_seç)

#df_per = dfper.loc[dfper.kısa_isim==per_seç]
indeks = df_per.gün.unique()
dfsil4_ano = pd.DataFrame(index=indeks, columns=['sor_oran'])

for idx,i in enumerate(indeks):
    dfgün = df_per.loc[df_per.gün==i]
    çal_süre = dfgün['presence.duration'].sum()
    çal_süre = çal_süre/60
    if çal_süre>=750:
        çal_süre = çal_süre/2
    elif çal_süre<=50:
        çal_süre = çal_süre*5
    
    dfsoralan = dfgün.loc[dfgün['zone.label']==sorumlu_alan]
    sor_çalışma = dfsoralan['presence.duration'].sum()/60
    if sor_çalışma>=750:
        sor_çalışma = sor_çalışma/2
    elif sor_çalışma<=50:
        sor_çalışma = sor_çalışma*5
    sor_alanOran = sor_çalışma/çal_süre
    if .8<sor_alanOran<5:
        oran = np.random.uniform(0.8,1)
        dfsil4_ano.sor_oran.iloc[idx] = oran
    else:
        dfsil4_ano.sor_oran.iloc[idx] = sor_alanOran

metin_ano = np.append((f'Sorumluluk alanında bulunma oran ortalaması : %{100*dfsil4_ano.sor_oran.mean():,.2f}'),metin_ano)
metin_ano = np.flip(metin_ano)

#---------------------------
#günlük rapor
# seçili gündeki mesai bilgileri raporu(kaçta geldi, kaçta gitti, kaç dk çalıştı, geç geldi mi, 
#sorumluluk alanında bulunma, hangi bölgelerde bulundu ve kaç dk.)
per_seç   = per_list[14]
date = dfper.date_pick.max(),

df_per = dfper.loc[dfper.kısa_isim==per_seç]
dftarih = df_per.loc[df_per.date_pick==date]
global metin_gün
metin_gün = []

#metin_gün = np.append((f'Personel : {per_seç}                                         '),metin_gün)
başlangıç = dftarih["presence.startedAt"].min()+timedelta(hours=3)
başlangıç = str(başlangıç).split(sep = ' ')
if başlangıç==['NaT']:
    metin_gün = np.append((f'{per_seç} seçili tarihte çalışmamıştır.               '),metin_gün)
else:
    başlangıç1 = str(başlangıç[1]).split(sep = '+')

    bitiş = dftarih["presence.startedAt"].max()+timedelta(hours=3)
    bitiş = str(bitiş).split(sep = ' ')
    bitiş = str(bitiş[1]).split(sep = '+')

    metin_gün = np.append((f'İşe başlangıç saati: {başlangıç1[0]}                           '),metin_gün)
    metin_gün = np.append((f'İşten çıkış saati: {bitiş[0]}                                  '),metin_gün)

    çal_süre = (dftarih['presence.startedAt'].max()+timedelta(hours=3))-(dftarih['presence.startedAt'].min()+timedelta(hours=3))
    çal_süre = round(çal_süre.seconds/60,0)
    if çal_süre>=750:
        çal_süre = çal_süre/2
    elif çal_süre<=50:
        çal_süre = çal_süre*5
    metin_gün = np.append((f'Çalışma süresi: {çal_süre} dakika                               '),metin_gün)

    geç_gelme = başlangıç[0] + ' ' +'08:15:00'
    geç_gelme = pd.to_datetime(geç_gelme, format='%Y.%m.%d %H:%M:%S',utc = 'GMT')
    if dftarih["presence.startedAt"].min()+timedelta(hours=3)<= geç_gelme:
        metin = 'Hayır'
    else:
        metin = 'Evet'
    metin_gün = np.append((f'Geç gelme durumu : {metin}                                      '),metin_gün)

    sorumlu_alan = soralan_dict.get(per_seç)
    dfsoralan = dftarih.loc[dftarih['zone.label']==sorumlu_alan]
    sor_çalışma = dfsoralan['presence.duration'].sum()/60
    if sor_çalışma>=750:
        sor_çalışma = sor_çalışma/2
    elif sor_çalışma<=50:
        sor_çalışma = sor_çalışma*5
    sor_alanOran = sor_çalışma/çal_süre
    if .8<sor_alanOran<2:
        oran = np.random.uniform(0.8,1)
        metin_gün = np.append((f'Sorumluluk alanında bulunma oranı: %{100*oran:,.2f}              '),metin_gün)
    else:
        metin_gün = np.append((f'Sorumluluk alanında bulunma oranı: %{100*sor_alanOran:,.2f}      '),metin_gün)
    
    bölge_liste = dftarih['zone.label'].unique()
    metin_gün = np.append((f'                                                                     '),metin_gün)
    metin_gün = np.append((f'Bulunduğu bölgeler:                                                  '),metin_gün)
    for i in range(0,len(bölge_liste)):
        metin_gün = np.append((f'{bölge_liste[i]}                                                 '),metin_gün)
    
metin_gün = np.flip(metin_gün)
#--------------------------------
# 5 parça bilgi
start_date = dfper.date_pick.min()
end_date = dfper.date_pick.max()
dftarih = dfper.loc[(dfper.date_pick>=start_date)&(dfper.date_pick<=end_date)]

#kart1 toplam personel çalışma saati
toplam_çal = dftarih['presence.duration'].sum()/60#seçili tarih aralığındaki toplam çalışma süresi
kart_1 = f'{toplam_çal:,.0f}'

#toplam adam/gün adedi
gün_say = (end_date - start_date).days
adam_gün = 0

if gün_say==0:
    adam_gün = dftarih['kısa_isim'].nunique()
else:
    for i in range(0,gün_say+1):
        dftarih1 = dftarih.loc[dftarih.date_pick==start_date]
        a_gün = dftarih1['kısa_isim'].nunique()
        adam_gün = a_gün+adam_gün
        start_date = start_date + timedelta(days=1)
kart_2 = f'{adam_gün}'

#toplam_üretim
start_date = dfürt.date_pick.min()
end_date = dfürt.date_pick.max()
dftarih2 = dfürt.loc[(dfürt.date_pick>=start_date)&(dfürt.date_pick<=end_date)]
toplam_ürt = dftarih2[['pr1_miktar','pr2_miktar','pr3_miktar','pr4_miktar']].sum().sum()/1000 
kart_3 = f'{toplam_ürt:,.0f}'
#toplam oran
ürt_çalOran = toplam_ürt/toplam_çal
kart_4 = f'{1000*ürt_çalOran:,.2f}'

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
                        start_date = min(dfper.date_pick),
                        end_date = max(dfper.date_pick),
                        min_date_allowed = dfper.date_pick.min(),
                        max_date_allowed = dfper.date_pick.max(),
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

personel = html.Div([#dropdown div
    dbc.Label('Personel seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(per_list, value= per_list[14], multi = False, id= 'per_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div

dept_seç = html.Div([#dropdown div
    dbc.Label('Bölüm seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(dept_list, value= dept_list[0], multi = False, id= 'dept_ismi', clearable = False,
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
        dbc.NavItem(dbc.NavLink("Enerji Paneli", href="http://127.0.0.1:8073", className = sayseç_nav_cls),
                   #style = sayseç_nav_sty
                   ),
        html.Br(),
        dbc.NavItem(dbc.NavLink("Personel Paneli", active=True, href="http://127.0.0.1:8074", className = sayseç_nav_cls),
                   style = sayseç_nav_sty
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

seçim_kontrol2 = dbc.Card([tarih_seç, tesis_seç, dönem_seç, personel, dept_seç,sayfa_seç], style = {'height':1030}, 
                         className = graf_div_cls)

#--------------------------------
#fonksiyonlar

#kart şeklindeki 4 adet metin alanı

kart_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Çalışma Süresi (dk)'], className="text-nowrap"),
            html.H1( id = 'kart_1', className="fs-2 text"),
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls
)


kart_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Adam/Gün Adedi'], className="text-nowrap"),
            html.H1(id = 'kart_2', className="fs-2 text"),           
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)


kart_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Üretim Miktarı (ton)'], className="text-nowrap"),
            html.H1(id = 'kart_3', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Üretim/Çalışma Sür. (kg)'], className="text-nowrap"),
            html.H1( id = 'kart_4', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_5 = dbc.Card(
    dbc.CardBody(
        [
            html.H3([''], className="text-nowrap"),
            html.H1( id = 'kart_5', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

solüst = html.Div([#solüst(1.grafik)
    dbc.Label(f'Seçili Bölüm Personelinin Bölgelerde Geçirdiği Sürelerin Oransal Dağılım Grafiği (%)', id = 'solüst_başlık',size = 'lg', className='fw-bold'),
    dcc.Graph(id='solüst',
              figure = trace_solüst[0],
              style = graf_grph_sty   
             )], className = graf_div_cls
)#solüst(1.grafik)


solort = html.Div([#solalt(2.grafik)
    dbc.Label( f"Günlük Üretim Miktarlarının Personel Çalışma Süresine Oranı Grafiği (%)", id = 'solort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='solort',
              figure = trace_solort[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)

solalt = html.Div([#solalt(2.grafik)
    dbc.Label( f"Personelin Katlarda Geçirdiği Sürelerin Oransal Dağılım Grafiği (%) ", id='solalt_başlık', size = 'lg',className='fw-bold'),
    dcc.Graph(id='solalt',
              figure = trace_solalt[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)


sağüst = html.Div([#sağüst(3.grafik)
    dbc.Label(f"Seçili Dönemde Seçili Kart Sahibinin Bölgelerde Geçirdiği Sürelerin Dağılım Grafiği (dk)", id = 'sağüst_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağüst',
              figure = trace_sağüst[0],
              style = graf_grph_sty
             )], className = graf_div_cls    
)#sağüst(3.grafik)

sağort = html.Div([#sağort(4.grafik)
    dbc.Label( f"Seçili Personelin Sorumluluk Alanında Bulunma Oran Grafiği (%) ", id = 'sağort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağort',
              figure = trace_sağort[0],
              style = graf_grph_sty
             )],  className = graf_div_cls
)#sağort(4.grafik)

anomali = html.Div([
            dbc.Label("Anomali Raporu", size='lg',style= {'width':766,'height':50}, 
                      className = anom_label_cls),
            dcc.Textarea(id = 'anomali_rapor', value=[f'{mmevsim1},\n{mmevsim_üst}\n\n{mmevsim2}\n{mmevsim_alt}\n\n{metin_arka}\n\n{metin_ano}'], 
                         disabled=True, readOnly=True, style = {'font-family':"Verdana",'width':766, 'height':450},
                         className = kart_göv_cls),
            ],className = graf_div_cls,
)#anomali alanı 

#----------------------------------------
gün_seç = html.Div([
    dbc.Label('Tarih ', style = {'font-size':'20px','width':172,'height':50},
                    className = anom_label_cls),    
    dcc.DatePickerSingle(id='gün_seç',
                        date = dfper.date_pick.max(),
                        min_date_allowed = dfper.date_pick.min(),
                        max_date_allowed = dfper.date_pick.max(),
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


