# Tanımlamalar
external_stylesheets = [dbc.themes.MINTY]
app = dash.Dash(__name__, external_stylesheets= external_stylesheets)

#---------------------
#solüst
#seçili dönemdeki (gün, ay, hafta, çeyrek,yıl) ürünlerin üretim miktarları (kg.)
trace_solüst = []
fig = go.Figure()
dönem='hafta'
toplam = 0
if dönem=='gün':
    roll=30
    mevsim = [60,152,244,335]
    çeyrek = [91,182,273]
elif dönem=='hafta':
    roll=4
    mevsim = [9,22,35,48]
    çeyrek = [14,27,40]
elif dönem=='ay':
    roll=3
    mevsim = [2,5,8,11]
    çeyrek = [3,6,9]
elif dönem=='çeyrek':
    roll=1
    mevsim = [1,2,3,4]
    çeyrek = [1,2,3,4]

global dfsil1    
indeks = dfürt[dönem].unique()
dfsil1 = pd.DataFrame(index = indeks, columns=['üretim_ton','üretim_n','0_temel','kayan_ort_üretim'])

for idx,i in enumerate (dfürt[dönem].unique()):
    a = dfürt.loc[dfürt[dönem]==i]
    sonuç = a[['pr1_miktar','pr2_miktar','pr3_miktar','pr4_miktar']].sum().sum()
    #toplam = sonuç.sum()
    dfsil1['üretim_ton'].iloc[idx] = round(sonuç/1000,0)
    #dfsil1['üretim_n'].iloc[idx] = f'{toplam/1000:,.0f}'
ort = dfsil1['üretim_ton'].mean()
dfsil1['0_temel']= dfsil1['üretim_ton'] / dfsil1['üretim_ton'].max()
dfsil1['kayan_ort_üretim'] = dfsil1['üretim_ton'].rolling(roll,min_periods=1).mean()

if dönem == 'hafta':
    dfsil1 = dfsil1.drop(52, axis=0)
else:
    pass

#grafikleştirme
fig.add_trace(go.Bar(
                x= dfsil1.index,
                y= dfsil1['üretim_ton'],
                marker= dict(color='blue', opacity=0.4),
                hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+
                '%{x}'+'<br><i>Üretim:</i> %{y:,.0f} (ton)<br>'+ '<extra></extra>',
                showlegend = False
                ))

fig.add_trace(go.Scatter(
                x= dfsil1.index,
                y = dfsil1['kayan_ort_üretim'],
                marker=dict(color='orange', opacity = 0.8),
                hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+
                '%{x}'+'<br><i>Ort. Üretim:</i> %{y:,.0f} (ton)<br>'+ '<extra></extra>',
                showlegend = False,
                mode = 'lines'))

if dönem =='hafta':
    for i in range(0,len(mevsim_hafta)):
        fig.add_vrect(x0=mevsim_hafta[i], x1= mevsim_hafta[i], line_dash = 'dash',line_color = 'red',opacity=0.3,
                     annotation_text = (f'{mevsim_isim[i]}'),
                     annotation_position = 'top right')
elif dönem== 'ay':
    for i in range(0,len(mevsim_ay)):
        fig.add_vrect(x0=mevsim_ay[i], x1= mevsim_ay[i], line_dash = 'dash',line_color = 'red',opacity=0.3,
                     annotation_text = (f'{mevsim_isim[i]}'),
                     annotation_position = 'top right')
elif dönem=='gün':
    for i in range(0,len(mevsim_gün)):
        fig.add_vrect(x0=mevsim_gün[i], x1= mevsim_gün[i], line_dash = 'dash',line_color = 'red',opacity=0.3,
                     annotation_text = (f'{mevsim_isim[i]}'),
                     annotation_position = 'top right')    

        fig.update_layout(showlegend = False,
                  xaxis = dict(tickmode = 'auto'),
                  yaxis = dict(gridcolor='lightgrey'),
                  paper_bgcolor = 'white',
                  plot_bgcolor = 'white',
                  #title=dict(text=(f"{dönem.capitalize()} Bazında Üretim Miktarları Grafiği (ton)")),
                  hoverlabel = dict(font=dict(color='white'),bgcolor='grey'),
                  )
#fig.show()

# dfsil1 anomali kodlaması
dfsil1_kışA = dfsil1[:mevsim[0]]
dfsil1_kışB = dfsil1[mevsim[3]:]
dfsil1_kış = pd.concat([dfsil1_kışA,dfsil1_kışB], axis=0)

ort_list = [dfsil1_kış.üretim_ton.mean(),(dfsil1[mevsim[0]:mevsim[1]]).üretim_ton.mean(),dfsil1[mevsim[1]:mevsim[2]].üretim_ton.mean(),
            dfsil1[mevsim[2]:mevsim[3]].üretim_ton.mean()]
std_list = [dfsil1_kış.üretim_ton.std(), (dfsil1[mevsim[0]:mevsim[1]]).üretim_ton.std(), dfsil1[mevsim[1]:mevsim[2]].üretim_ton.std(),
           dfsil1[mevsim[2]:mevsim[3]].üretim_ton.std()]
min_list = [dfsil1_kış.üretim_ton.min(), (dfsil1[mevsim[0]:mevsim[1]]).üretim_ton.min(), dfsil1[mevsim[1]:mevsim[2]].üretim_ton.min(),
           dfsil1[mevsim[2]:mevsim[3]].üretim_ton.min()]

metin11_ano = (f'{dönem.capitalize()} Bazında Üretim Miktarları Grafiği (ton)')
metin1_ano = (f'{mevsim_dict.get(np.argmax(ort_list))} mevsiminde {np.max(ort_list):,.0f} ton ile {dönem} bazında en yüksek ortalama üretim miktarına ulaşılmıştır. ')
metin1_ano = metin1_ano + (f'Buna karşılık İlkbaharda {ort_list[1]:,.0f}, Yaz aylarında {ort_list[2]:,.0f}, Sonbahar da ise ortalama {ort_list[3]:,.0f} ton seviyelerine düşmüştür. ')
metin1_ano = metin1_ano + (f'{dönem.capitalize()} bazında en istikrarlı ortalama üretim seviyeleri {mevsim_dict.get(np.argmin(std_list))} aylarında gözlenmektedir. ')
metin1_ano = metin1_ano + (f'{mevsim_dict.get(np.argmin(min_list))} mevsiminde {np.min(min_list):,.0f} ton ile {dönem} bazında en düşük ortalama üretim miktarına ulaşılmıştır. ')
metin1_ano = metin1_ano + (f'{dönem.capitalize()} bazında yapılan en yüksek üretim {dfsil1.üretim_ton.max():,.0f} ton ile {np.argmax(dfsil1.üretim_ton)+1}. {dönem} yapılmıştır. ')
metin1_ano = metin1_ano + (f'Bu değeri en yüksek kapasite olarak kabul edersek tüm veri setinde kapasite kullanımı %{100*(dfürt[["pr1_miktar","pr2_miktar","pr3_miktar","pr4_miktar"]].sum().sum()/1000)/(dfsil1.üretim_ton.max()*52):,.2f} olarak karşımıza çıkmaktadır. ')


#rapor kodlaması
metin1 = []
metin1 = np.append((f'Genel üretim istatistikleri:'),metin1)
metin1 = np.append((f'                                                                      '),metin1)
if dönem == 'gün':
    dfsil1 = dfsil1.loc[dfsil1.üretim_ton>0]
#1. Ortalamanın standart sapma kadar üstündeki ve altındaki haftaların listesi ve metin
üst_dönem = dfsil1.loc[dfsil1.üretim_ton>= (dfsil1.üretim_ton.mean() + dfsil1.üretim_ton.std())]
alt_dönem = dfsil1.loc[dfsil1.üretim_ton<= (dfsil1.üretim_ton.mean() - dfsil1.üretim_ton.std())]
if (üst_dönem.empty) or (alt_dönem.empty):
    pass
else:
    metin1 = np.append((f'Üst eşik sınırı olan {(dfsil1.üretim_ton.mean() + dfsil1.üretim_ton.std()):,.0f} tondan yüksek olan dönemler: '),metin1)
    metin1 = np.append((f'{str(list(üst_dönem.index))[1:-1]}'),metin1)
    metin1 = np.append((f'Alt eşik sınırı olan {(dfsil1.üretim_ton.mean() - dfsil1.üretim_ton.std()):,.0f} tondan düşük olan dönemler: '),metin1)
    metin1 = np.append((f'{str(list(alt_dönem.index))[1:-1]}'),metin1)

    y1 = len(üst_dönem.loc[üst_dönem.index<çeyrek[1]])
    y2 = len(üst_dönem.loc[üst_dönem.index>çeyrek[1]])

    metin1 = np.append((f'Üst eşik miktarını aşan dönemlerin %{100*(y1/len(üst_dönem)):,.0f} yılın ilk yarısında;'),metin1)
    metin1 = np.append((f'Üst eşik miktarını aşan dönemlerin %{100*(y2/len(üst_dönem)):,.0f} yılın ikinci yarısında meydana gelmiştir.'),metin1)

    ç1 = len(alt_dönem.loc[alt_dönem.index<çeyrek[1]])
    ç4 = len(alt_dönem.loc[alt_dönem.index>çeyrek[1]])

    metin1 = np.append((f'Alt eşik miktarından düşük dönemlerin %{100*(ç1/len(alt_dönem)):,.0f} yılın ilk yarısında;'),metin1)
    metin1 = np.append((f'Alt eşik miktarından düşük dönemlerin %{100*(ç4/len(alt_dönem)):,.0f} yılın ikinci yarısında meydana gelmiştir.'),metin1)

#2. Min ve max dönemlerin listesi ve metin ve her dönem değerinin bütün içindeki oranı
min_dönem = np.argmin(dfsil1.üretim_ton)
max_dönem = np.argmax(dfsil1.üretim_ton)
min_oran = np.min(dfsil1.üretim_ton)/dfsil1.üretim_ton.sum()
max_oran = np.max(dfsil1.üretim_ton)/dfsil1.üretim_ton.sum()
metin1 = np.append((f'En düşük üretim yapılan {dönem} {dfsil1.üretim_ton.min():,.0f} ton ile {min_dönem+1}. {dönem} olmuştur.'),metin1)
metin1 = np.append((f'Bu miktar bugüne kadar yapılan tüm üretimin %{100*min_oran:,.2f} denk gelmektedir.'),metin1)
metin1 = np.append((f'En yüksek üretim yapılan {dönem} {dfsil1.üretim_ton.max():,.0f} ton ile {max_dönem+1}. {dönem} olmuştur.'),metin1)
metin1 = np.append((f'Bu miktar bugüne kadar yapılan tüm üretimin %{100*max_oran:,.2f} denk gelmektedir.'),metin1)

#çeyrek ortalamaları
df_kış = dfsil1.üretim_ton[:çeyrek[0]].mean()
df_ilk = dfsil1.üretim_ton[çeyrek[0]:çeyrek[1]].mean()
df_yaz = dfsil1.üretim_ton[çeyrek[1]:çeyrek[2]].mean()
df_son = dfsil1.üretim_ton[çeyrek[2]:].mean()
metin1 = np.append((f'İlk çeyrek üretim ortalaması {df_kış:,.0f} tondur.'),metin1)
metin1 = np.append((f'İkinci çeyrek üretim ortalaması {df_ilk:,.0f} tondur.'),metin1)
metin1 = np.append((f'Üçüncü çeyrek üretim ortalaması {df_yaz:,.0f} tondur.'),metin1)
metin1 = np.append((f'Dördüncü çeyrek üretim ortalaması {df_son:,.0f} tondur.'),metin1)

# haftalık raporda biten hafta ile bir önceki haftanın karşılaştırması yapılacak.
son_dönem = dfsil1.index.max()
son_ürt = dfsil1.üretim_ton[-1:].iloc[0]
bir_ürt = dfsil1.üretim_ton[-2:-1].iloc[0]
tüm_ort = dfsil1.üretim_ton[:-2].mean()

if son_ürt > bir_ürt:
    metin1 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile bir önceki üretim miktarından {bir_ürt:,.0f} tondan %{np.abs(100-(100*(son_ürt/bir_ürt))):,.2f} yüksek gerçekleşmiştir."),metin1)
else:
    metin1 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile bir önceki üretim miktarı olan {bir_ürt:,.0f} tondan %{100*(son_ürt/bir_ürt):,.2f} düşük gerçekleşmiştir."),metin1)    

# haftalık raporda biten hafta ile yıl başından bu yana tüm haftaların ortalamalarının karşılaştırması yapılacak.
if son_ürt > tüm_ort:
    metin1 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile diğer tüm önceki dönemlerin ortalaması olan {tüm_ort:,.0f} tondan %{np.abs(100-(100*(son_ürt/tüm_ort))):,.2f} yüksek gerçekleşmiştir."),metin1)
else:
    metin1 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile diğer tüm önceki dönemlerin ortalaması olan {tüm_ort:,.0f} tondan %{100*(son_ürt/tüm_ort):,.2f} düşük gerçekleşmiştir."),metin1)
    
metin1 = np.flip(metin1)

trace_solüst = np.append(fig,trace_solüst)
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#solort
#seçili dönemdeki, (gün, ay, hafta, çeyrek,yıl) ürünlerin üretim miktarlarının bir önceki döneme göre artış azalış grafiği
trace_solort = []
fig = go.Figure()
dönem='hafta'
toplam = 0
if dönem=='gün':
    roll=30
    çeyrek = [91,182,273]    
elif dönem=='hafta':
    roll=4
    çeyrek = [14,27,40]
elif dönem=='ay':
    roll=3
    çeyrek = [3,6,9]
elif dönem=='çeyrek':
    roll=1
    çeyrek = [1,2,3,4]       
else:
    roll=1
    
global dfsil4
indeks = dfürt[dönem].unique()
dfsil4 = pd.DataFrame(index = indeks, columns=['hat1','hat1_ort','hat2','hat2_ort','hat3','hat3_ort','hat4','hat4_ort'])
say = 0

for idx,i in enumerate (dfürt[dönem].unique()):
    a = dfürt.loc[dfürt[dönem]==i]
    hat1 = a['pr1_miktar'].sum()
    hat2 = a['pr2_miktar'].sum()
    hat3 = a['pr3_miktar'].sum()
    hat4 = a['pr4_miktar'].sum()
    
    dfsil4['hat1'].iloc[idx] = round(hat1/1000,0)
    dfsil4['hat2'].iloc[idx] = round(hat2/1000,0)
    dfsil4['hat3'].iloc[idx] = round(hat3/1000,0)
    dfsil4['hat4'].iloc[idx] = round(hat4/1000,0)
    
    dfsil4['hat1_ort'] = dfsil4['hat1'].rolling(roll,min_periods=1).mean()
    dfsil4['hat2_ort'] = dfsil4['hat2'].rolling(roll,min_periods=1).mean()
    dfsil4['hat3_ort'] = dfsil4['hat3'].rolling(roll,min_periods=1).mean()
    dfsil4['hat4_ort'] = dfsil4['hat4'].rolling(roll,min_periods=1).mean()
    
if dönem == 'hafta':
    dfsil4 = dfsil4.drop(52, axis=0)
else:
    pass    
                       
#grafikleştirme
fig.add_trace(go.Bar(name= '1. Hat',
                x = dfsil4.index,
                y = dfsil4['hat1'],
                marker = dict(color='orange', opacity=.8),
                hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+ '%{x}'+'<br><i>Hat: 1</i>' +
                '<br><i>Üretim:</i> %{y:,.0f} (ton)<br>'+ '<extra></extra>',
                ))
fig.add_trace(go.Bar(name='2. Hat',
                 x = dfsil4.index,
                 y = dfsil4['hat2'],
                 marker = dict(color='blue', opacity=0.8),
                 hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+'<br><i>Hat: 2</i>' +
                '<br><i>Üretim:</i> %{y:,.0f} (ton)<br>'+ '<extra></extra>',
                 ))
fig.add_trace(go.Bar(name='3. Hat',
                 x = dfsil4.index,
                 y = dfsil4['hat3'],
                 marker = dict(color='green', opacity=0.8),
                 hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+'<br><i>Hat: 3</i>' +
                '<br><i>Üretim:</i> %{y:,.0f} (ton)<br>'+ '<extra></extra>',
                 ))
fig.add_trace(go.Bar(name='4. Hat',
                 x = dfsil4.index,
                 y = dfsil4['hat4'],
                 marker = dict(color='coral', opacity=0.8),
                 hovertemplate = (f'<i>{dönem.capitalize()}: </i>')+'%{x}'+'<br><i>Hat: 4</i>' +
                '<br><i>Üretim:</i> %{y:,.0f} (ton)<br>'+ '<extra></extra>',
                 ))
fig.add_trace(go.Scatter(name= '1. Hat Kayan Ort.',
                 x = dfsil4.index,
                 y = dfsil4['hat1_ort'],
                 mode = 'lines',
                 line_dash = 'dot',
                 marker = dict(color='orange', opacity=0.1),
                 ))
fig.add_trace(go.Scatter(name='2. Hat Kayan Ort.',
                 x = dfsil4.index,
                 y = dfsil4['hat2_ort'],
                 mode= 'lines',
                 line_dash = 'dot',
                 marker = dict(color='blue', opacity=0.1),
                 ))
fig.add_trace(go.Scatter(name='3. Hat Kayan Ort.',
                 x = dfsil4.index,
                 y = dfsil4['hat3_ort'],
                 mode = 'lines',
                 line_dash = 'dot',
                 marker = dict(color='green', opacity=0.1),
                 ))
fig.add_trace(go.Scatter(name='4. Hat Kayan Ort.',
                 x = dfsil4.index,
                 y = dfsil4['hat4_ort'],
                 mode = 'lines',
                 line_dash = 'dot',
                 marker = dict(color='coral', opacity=0.1),
                 ))                 
fig.update_layout(barmode= 'group',
                  showlegend = True,
                  xaxis = dict(tickmode = 'auto'),
                  yaxis = dict(gridcolor='lightgrey'),
                  paper_bgcolor = 'white',
                  plot_bgcolor = 'white',
                  #title=dict(text=(f"{dönem.capitalize()} ve Hat Bazında Üretim Miktarı (ton)")),
                  hoverlabel = dict(font=dict(color='white'),bgcolor='grey'))
#fig.show()

# dfsil4 anomali kodlama
if dönem == 'çeyrek':
    pass
else:
    dfsil4_ort = [dfsil4.hat1.mean(), dfsil4.hat2.mean(), dfsil4.hat3.mean(), dfsil4.hat4.mean()]
    dfsil4_std = [dfsil4.hat1.std(), dfsil4.hat2.std(), dfsil4.hat3.std(), dfsil4.hat4.std()]
    dfsil4_top = [dfsil4.hat1.sum(), dfsil4.hat2.sum(), dfsil4.hat3.sum(), dfsil4.hat4.sum()]
    metin4_ano = (f"{dönem.capitalize()} ve Hat Bazında Üretim Miktarı (ton)")
    metin41_ano = (f'Yıllık olarak {dönem.capitalize()} bazında en yüksek ortalama üretim {int(np.max(dfsil4_ort)):,.0f} ton ile {np.argmax(dfsil4_ort)+1}. hatta gerçekleşmiştir.')
    metin41_ano = metin41_ano + (f'{dönem.capitalize()} bazında en istikrarlı üretim {np.argmin(dfsil4_std)+1}. hatta gerçekleşmiştir.')
    metin41_ano = metin41_ano + (f'En yüksek yıllık üretim {int(np.max(dfsil4_top)):,.0f} ton ile {np.argmax(dfsil4_ort)+1}. hatta gerçekleşmiştir.')

    #rapor kodlaması
    metin4 = []
    kısa_hatlist = ['hat1','hat2','hat3','hat4']
    metin4 = np.append((f'Hat bazında genel üretim istatistikleri'),metin4)

    for hat in (kısa_hatlist):
        metin4 = np.append((f'Hat no:  {hat.capitalize()}'),metin4)
    
        if dönem == 'gün':
            dfsil4 = dfsil4.loc[dfsil4[hat]>0]
        #1. Ortalamanın standart sapma kadar üstündeki ve altındaki haftaların listesi ve metin
        üst_dönem = dfsil4.loc[dfsil4[hat]>= (dfsil4[hat].mean() + dfsil4[hat].std())]
        alt_dönem = dfsil4.loc[dfsil4[hat]<= (dfsil4[hat].mean() - dfsil4[hat].std())]
        metin4 = np.append((f'Üst eşik sınırı olan {(dfsil4[hat].mean() + dfsil4[hat].std()):,.0f} tondan yüksek olan dönemler: '),metin4)
        metin4 = np.append((f'{str(list(üst_dönem.index))[1:-1]}'),metin4)
        metin4 = np.append((f'Alt eşik sınırı olan {(dfsil4[hat].mean() - dfsil4[hat].std()):,.0f} tondan düşük olan dönemler: '),metin4)
        metin4 = np.append((f'{str(list(alt_dönem.index))[1:-1]}'),metin4)

        y1 = len(üst_dönem.loc[üst_dönem.index<çeyrek[1]])
        y2 = len(üst_dönem.loc[üst_dönem.index>çeyrek[1]])

        metin4 = np.append((f'Üst eşik miktarını aşan dönemlerin %{100*(y1/len(üst_dönem)):,.2f} yılın ilk yarısında;'),metin4)
        metin4 = np.append((f'Üst eşik miktarını aşan dönemlerin %{100*(y2/len(üst_dönem)):,.2f} yılın ikinci yarısında meydana gelmiştir.'),metin4)

        ç1 = len(alt_dönem.loc[alt_dönem.index<çeyrek[1]])
        ç4 = len(alt_dönem.loc[alt_dönem.index>çeyrek[1]])

        metin4 = np.append((f'Alt eşik miktarından düşük dönemlerin %{100*(ç1/len(alt_dönem)):,.2f} yılın ilk yarısında;'),metin4)
        metin4 = np.append((f'Alt eşik miktarından düşük dönemlerin %{100*(ç4/len(alt_dönem)):,.2f} yılın ikinci yarısında meydana gelmiştir.'),metin4)

        #2. Min ve max dönemlerin listesi ve metin ve her dönem değerinin bütün içindeki oranı
        min_dönem = np.argmin(dfsil4[hat])
        max_dönem = np.argmax(dfsil4[hat])
        min_oran = np.min(dfsil4[hat])/dfsil4[hat].sum()
        max_oran = np.max(dfsil4[hat])/dfsil4[hat].sum()
        metin4 = np.append((f'En düşük üretim yapılan {dönem} {dfsil4[hat].min():,.0f} ton ile {min_dönem+1}. {dönem} olmuştur.'),metin4)
        metin4 = np.append((f'Bu miktar bugüne kadar yapılan tüm üretimin %{100*min_oran:,.2f} denk gelmektedir.'),metin4)
        metin4 = np.append((f'En yüksek üretim yapılan {dönem} {dfsil4[hat].max():,.0f} ton ile {max_dönem+1}. {dönem} olmuştur.'),metin4)
        metin4 = np.append((f'Bu miktar bugüne kadar yapılan tüm üretimin %{100*max_oran:,.2f} denk gelmektedir.'),metin4)

        #çeyrek ortalamaları
        df_kış = dfsil4[hat][:çeyrek[0]].mean()
        df_ilk = dfsil4[hat][çeyrek[0]:çeyrek[1]].mean()
        df_yaz = dfsil4[hat][çeyrek[1]:çeyrek[2]].mean()
        df_son = dfsil4[hat][çeyrek[2]:].mean()
        metin4 = np.append((f'İlk çeyrek üretim ortalaması {df_kış:,.0f} tondur.'),metin4)
        metin4 = np.append((f'İkinci çeyrek üretim ortalaması {df_ilk:,.0f} tondur.'),metin4)
        metin4 = np.append((f'Üçüncü çeyrek üretim ortalaması {df_yaz:,.0f} tondur.'),metin4)
        metin4 = np.append((f'Dördüncü çeyrek üretim ortalaması {df_son:,.0f} tondur.'),metin4)

        # haftalık raporda biten hafta ile bir önceki haftanın karşılaştırması yapılacak.
        son_dönem = dfsil4.index.max()
        son_ürt = dfsil4[hat][-1:].iloc[0]
        bir_ürt = dfsil4[hat][-2:-1].iloc[0]
        tüm_ort = dfsil4[hat][:-2].mean()

        if son_ürt > bir_ürt:
            metin4 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile bir önceki üretim miktarından {bir_ürt:,.0f} tondan %{np.abs(100-(100*(son_ürt/bir_ürt))):,.2f} yüksek gerçekleşmiştir."),metin4)
        else:
            metin4 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile bir önceki üretim miktarı olan {bir_ürt:,.0f} tondan %{100*(son_ürt/bir_ürt):,.2f} düşük gerçekleşmiştir."),metin4)    

        # haftalık raporda biten hafta ile yıl başından bu yana tüm haftaların ortalamalarının karşılaştırması yapılacak.
        if son_ürt > tüm_ort:
            metin4 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile diğer tüm önceki dönemlerin ortalaması olan {tüm_ort:,.0f} tondan %{np.abs(100-(100*(son_ürt/tüm_ort))):,.2f} yüksek gerçekleşmiştir."),metin4)
        else:
            metin4 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile diğer tüm önceki dönemlerin ortalaması olan {tüm_ort:,.0f} tondan %{100*(son_ürt/tüm_ort):,.2f} düşük gerçekleşmiştir."),metin4)
    
    metin4 = np.flip(metin4)

trace_solort = np.append(fig,trace_solort)
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#sağüst
#seçili dönemdeki, (gün, ay, hafta, çeyrek,yıl) ürünlerin üretim miktarlarının bir önceki döneme göre artış azalış grafiği
fig = go.Figure()
trace_sağüst = []

dönem='hafta'
toplam = 0
if dönem=='gün':
    roll=30
    bayram = kurban_bayG
elif dönem=='hafta':
    roll=4
    bayram = kurban_bayH
elif dönem=='ay':
    roll=3
    bayram = kurban_bayA
else:
    roll=1
    bayram = kurban_bayÇ

global dfsil3
indeks = dfürt[dönem].unique()
dfsil3 = pd.DataFrame(index = indeks, columns=['üretim_ton','artış_eksiliş','arka_arkaya'])
say = 0

for idx,i in enumerate (dfürt[dönem].unique()):
    a = dfürt.loc[dfürt[dönem]==i]
    sonuç = a[['pr1_miktar','pr2_miktar','pr3_miktar','pr4_miktar']].sum()
    toplam = sonuç.sum()
    dfsil3['üretim_ton'].iloc[idx] = round(toplam/1000,0)
    dene = dfsil3['üretim_ton'].iloc[idx] - dfsil3['üretim_ton'].iloc[idx-1]
    if dene <=0:
        say -=1
        dfsil3['artış_eksiliş'].iloc[idx] = say
    elif dene>0:
        say +=1
        dfsil3['artış_eksiliş'].iloc[idx] = say
        
    if dene<=dfsil3['artış_eksiliş'].iloc[idx]:
        dfsil3['arka_arkaya'].iloc[idx] = -1
    else:
        dfsil3['arka_arkaya'].iloc[idx] = 1
        
            
#grafikleştirme
fig.add_trace(go.Scatter(
                 x = dfsil3.index,
                 y = dfsil3['artış_eksiliş'],
                 mode = 'lines',
                 marker = dict(color='orange', opacity=0.5),
                 hoverlabel = dict(font=dict(color='black')),
                 showlegend=False))
                 
#mevsimler ve kurban bayramı için
if dönem =='hafta':
    for i in range(0,len(mevsim_hafta)):
        fig.add_vrect(x0=mevsim_hafta[i], x1= mevsim_hafta[i], line_dash = 'dash',line_color = 'darkgrey',opacity=1,
                     annotation_text = (f'{mevsim_isim[i]}'),
                     annotation_position = 'top right')
        
        fig.add_shape(type="rect",
                      x0=kurban_bayH[0], y0=dfsil3['artış_eksiliş'].min(), x1=kurban_bayH[1], y1=dfsil3['artış_eksiliş'].max(),
                      line=dict(
                      color="LightSeaGreen",
                      width=1),
                      fillcolor = 'LightSeaGreen', 
                      opacity=0.1,
                      label=dict(text="Kurban Bayramı"))
                    
elif dönem== 'ay':
    for i in range(0,len(mevsim_ay)):
        fig.add_vrect(x0=mevsim_ay[i], x1= mevsim_ay[i], line_dash = 'dash',line_color = 'darkgrey',opacity=1,
                     annotation_text = (f'{mevsim_isim[i]}'),
                     annotation_position = 'top right')
        
        fig.add_shape(type="rect",
                      x0=kurban_bayA[0], y0=dfsil3['artış_eksiliş'].min(), x1=kurban_bayA[1], y1=dfsil3['artış_eksiliş'].max(),
                      line=dict(
                      color="LightSeaGreen",
                      width=1),
                      fillcolor = 'LightSeaGreen', 
                      opacity=0.1,
                      label=dict(text="Kurban Bayramı"))       
        
elif dönem=='gün':
    for i in range(0,len(mevsim_gün)):
        fig.add_vrect(x0=mevsim_gün[i], x1= mevsim_gün[i], line_dash = 'dash',line_color = 'darkgrey',opacity=1,
                     annotation_text = (f'{mevsim_isim[i]}'),
                     annotation_position = 'top right')
        
        fig.add_shape(type="rect",
                      x0=kurban_bayG[0], y0=dfsil3['artış_eksiliş'].min(), x1=kurban_bayG[1], y1=dfsil3['artış_eksiliş'].max(),
                      line=dict(
                      color="LightSeaGreen",
                      width=1),
                      fillcolor = 'LightSeaGreen', 
                      opacity=0.1,
                      label=dict(text= 'Kurban Bayramı'))

fig.update_layout(barmode='stack',
                  xaxis = dict(tickmode = 'auto'),
                  yaxis = dict(gridcolor='lightgrey'),                          
                  paper_bgcolor = 'white',
                  plot_bgcolor = 'white',
                  showlegend = False
                  )
#fig.show()

#dfsil3 anomali kodlaması
if dönem == 'çeyrek':
    pass
else:
    say = 0
    süre = []
    indeks = []
    artış = []

    for idx,i in enumerate(dfsil3.index):
        if idx == len(dfsil3)-1:
            break
        a = dfsil3.arka_arkaya.iloc[idx]
        b = dfsil3.arka_arkaya.iloc[idx+1]
        if a==b:
            say +=1
            indeks = np.append(dfsil3.index[idx],indeks)
            süre = np.append(say,süre)
            artış = np.append(dfsil3.arka_arkaya.iloc[idx],artış)
        else:
            say = 0
        
    süre=np.flip(süre) 
    indeks = np.flip(indeks)
    artış = np.flip(artış)

    a = int(np.max(süre))# en uzun süre artış/eksiliş olan dönem
    b = int(np.argmax(süre)+1) # bu sürenin hangi zaman dilimine denk geldiği
    c = indeks[(b-a):b]
    if artış[b-1]== 1.0:
        durum = 'artış'
    elif artış[b-1] == -1.0:
        durum = 'azalma'

    metin31_ano = (f"{dönem.capitalize()} Bazında Üretim Artış/Azalış Grafiği")
    #metin3_ano = (f'{str(c)[1:-1]} haftalarda üretim miktarı üst üste {a} {dönem} {durum} göstermiştir. ')
    metin3_ano = (f'Yıllık {dönem} bazında ortalama {dfsil3.üretim_ton.mean():,.0f} ton üretim yapılmışken, Kurban Bayramından önceki {bayram[1]-bayram[0]} {dönem} ortalama üretim {dfsil3[bayram[0]:bayram[1]].üretim_ton.mean():,.0f} ton olarak gerçekleşmiştir. ')
    metin3_ano = metin3_ano + (f'Kurban Bayramı hariç yıllık ortalama ise {(dfsil3[:bayram[0]].üretim_ton.mean()+dfsil3[bayram[1]:].üretim_ton.mean())/2:,.0f} ton seviyesindedir. ')
    if dfsil3.üretim_ton.mean()>= dfsil3[bayram[0]:bayram[1]].üretim_ton.mean():
        metin = 'hiç bir etkisi olduğundan bahsedilemez.'
    elif dfsil3.üretim_ton.mean()<= dfsil3[bayram[0]:bayram[1]].üretim_ton.mean():
        metin = 'sınırlı bir etkisi olduğundan bahsedebiliriz.'
    elif dfsil3.üretim_ton.mean()*1.2<= dfsil3[bayram[0]:bayram[1]].üretim_ton.mean():
        metin = 'ciddi bir etkisi olduğundan bahsedebiliriz.'
    metin3_ano = metin3_ano + (f'Bu durumda Kurban Bayramının üretim miktarları üzerinde {metin} ')

trace_sağüst = np.append(fig,trace_sağüst)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#sağort
# Yıllık Üretim Miktarı En Yüksek Olan 25 Ürünün Üretim Miktarları 
trace_sağort = []
fig = go.Figure()
toplam = 0
kolon = ürün_list

global dfsil6, dfsil61
dfsil6 = pd.DataFrame(index = kolon, columns= ['üretim_ton'])
say = 0

for i in kolon:
    h1 = dfürt.loc[dfürt['pr1_ürün']==i]
    h2 = dfürt.loc[dfürt['pr2_ürün']==i]
    h3 = dfürt.loc[dfürt['pr3_ürün']==i]
    h4 = dfürt.loc[dfürt['pr4_ürün']==i]
    
    toplam =h1['pr1_miktar'].sum()+h2['pr2_miktar'].sum()+h3['pr3_miktar'].sum()+h4['pr4_miktar'].sum()
    dfsil6['üretim_ton'].iloc[say] = round(toplam/1000,2)
    say +=1

dfsil6 = dfsil6.sort_values('üretim_ton', ascending = False)
dfsil61 = dfsil6[:25]
kolon = dfsil61.index

#grafikleştirme
for idx,i in enumerate(kolon):
    fig.add_trace(go.Bar(
                name = kolon[idx],
                x = [dfsil61.index[idx]],
                y = [dfsil61['üretim_ton'].iloc[idx]],
                marker = dict(color=kol_renk.get(kolon[idx])), opacity=.8,
                hovertemplate = (f'<i>Ürün: </i>')+'%{x}'+
                '<br><i>Üretim:</i> %{y:,.02f} (ton)<br>'+ '<extra></extra>',
                  showlegend = False
                 ))

fig.update_layout(showlegend = False,
                  xaxis = dict(tickmode = 'linear'),
                  yaxis = dict(gridcolor='lightgrey'),                          
                  paper_bgcolor = 'white',
                  plot_bgcolor = 'white',                  
                  #title=dict(text=(f"Yıllık Üretim Miktarı En Yüksek Olan 25 Ürünün Üretim Miktarları (ton)")),
                  hoverlabel = dict(font=dict(color='white'),bgcolor='grey'))

#fig.show()

trace_sağort = np.append(fig,trace_sağort)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#solalt
#seçili ürünün seçili dönemdeki, (gün, ay, hafta, çeyrek,yıl) ürünlerin üretim miktarları (ton)
trace_solalt = []
fig = go.Figure()
dönem='hafta'
ürün = '20 A'
toplam = 0
tick = 'linear'

if dönem=='gün':
    roll=30
    mevsim = [60,152,244,335]
    çeyrek = [91,182,273]
    tick = 'auto'
elif dönem=='hafta':
    roll=4
    mevsim = [9,22,35,48]
    çeyrek = [14,27,40]
elif dönem=='ay':
    roll=3
    mevsim = [2,5,8,11]
    çeyrek = [3,6,9]
elif dönem=='çeyrek':
    roll=1
    mevsim = [1,2,3,4]
    çeyrek = [1,2,3,4]


global dfsil7
indeks = dfürt[dönem].unique()
dfsil7 = pd.DataFrame(index = indeks, columns= ['üretim_ton'])

for idx,i in enumerate (dfürt[dönem].unique()):
    a = dfürt.loc[dfürt[dönem]==i] 
    
    h1= a.loc[a['pr1_ürün']==ürün]
    h2= a.loc[a['pr2_ürün']==ürün]
    h3= a.loc[a['pr3_ürün']==ürün]
    h4= a.loc[a['pr4_ürün']==ürün]
                
    toplam = h1['pr1_miktar'].sum()+h2['pr2_miktar'].sum()+h3['pr3_miktar'].sum()+h4['pr4_miktar'].sum()        
    dfsil7['üretim_ton'].iloc[idx] = round(toplam/1000,2) 
    
if dönem == 'hafta':
    dfsil7 = dfsil7.drop(52, axis=0)
else:
    pass    
    
#grafikleştirme
fig.add_trace(go.Scatter(
                x = dfsil7.index,
                y = dfsil7['üretim_ton'],
                mode = 'lines',
                marker=dict(color=(kol_renk.get(ürün)))))

fig.update_layout(
    xaxis = dict(tickmode = tick),
    yaxis = dict(range = [(dfsil7['üretim_ton'].min()-20),(dfsil7['üretim_ton'].max()+20)],gridcolor='lightgrey'),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',                  
    title = dict(text=(f"Seçili ürün: {ürün}"))
    )
#fig.show()

# dfsil7 anomali kodlaması
if dönem == 'çeyrek':
    pass
else:
    dfsil7_kışA = dfsil7[:mevsim[0]]
    dfsil7_kışB = dfsil7[mevsim[3]:]
    dfsil7_kış = pd.concat([dfsil7_kışA,dfsil7_kışB], axis=0)

    ort_list = [dfsil7_kış.üretim_ton.mean(),(dfsil7[mevsim[0]:mevsim[1]]).üretim_ton.mean(),dfsil7[mevsim[1]:mevsim[2]].üretim_ton.mean(),
                dfsil7[mevsim[2]:mevsim[3]].üretim_ton.mean()]
    std_list = [dfsil7_kış.üretim_ton.std(), (dfsil7[mevsim[0]:mevsim[1]]).üretim_ton.std(), dfsil7[mevsim[1]:mevsim[2]].üretim_ton.std(),
               dfsil7[mevsim[2]:mevsim[3]].üretim_ton.std()]
    min_list = [dfsil7_kış.üretim_ton.min(), (dfsil7[mevsim[0]:mevsim[1]]).üretim_ton.min(), dfsil7[mevsim[1]:mevsim[2]].üretim_ton.min(),
               dfsil7[mevsim[2]:mevsim[3]].üretim_ton.min()]

    metin7_ano = (f"{dönem.capitalize()}lık {ürün} Üretim Miktarı (ton)")
    metin71_ano = (f'{mevsim_dict.get(np.argmax(ort_list))} mevsiminde {np.max(ort_list):,.0f} ton ile {dönem} bazında en yüksek ortalama üretim miktarına ulaşılmıştır.')
    metin71_ano = metin71_ano + (f'{mevsim_dict.get(np.argmin(ort_list))} mevsiminde {ürün} talebi azalarak {dönem} bazında {np.min(ort_list):,.0f} ton seviyelerine düşmüştür.')
    metin71_ano = metin71_ano + (f'{dönem.capitalize()} bazında en istikrarlı ortalama üretim seviyeleri {mevsim_dict.get(np.argmin(std_list))} aylarında gözlenmektedir.')
    metin71_ano = metin71_ano + (f'{dönem.capitalize()} bazında en düşük ortalama üretim miktarı {np.min(min_list):,.0f} ton ile  {mevsim_dict.get(np.argmin(min_list))} mevsiminde kaydedilmiştir.\n')

    #rapor kodlaması
    metin7 = []
    metin7 = np.append((f'Seçili ürün bazında üretim istatistikleri: '),metin7)
    metin7 = np.append(f'                                                                                  ',metin7)
    metin7 = np.append((f'Seçili ürün: {ürün}'),metin7)
    metin7 = np.append(f'                                                                                  ',metin7)
    if dönem == 'gün':
        dfsil7 = dfsil7.loc[dfsil7.üretim_ton>0]
    #1. Ortalamanın standart sapma kadar üstündeki ve altındaki haftaların listesi ve metin
    üst_dönem = dfsil7.loc[dfsil7.üretim_ton>= (dfsil7.üretim_ton.mean() + dfsil7.üretim_ton.std())]
    alt_dönem = dfsil7.loc[dfsil7.üretim_ton<= (dfsil7.üretim_ton.mean() - dfsil7.üretim_ton.std())]

    metin7 = np.append((f'Üst eşik sınırı olan {(dfsil7.üretim_ton.mean() + dfsil7.üretim_ton.std()):,.0f} tondan yüksek olan dönemler: '),metin7)
    metin7 = np.append((f'{str(list(üst_dönem.index))[1:-1]}'),metin7)
    metin7 = np.append((f'Alt eşik sınırı olan {(dfsil7.üretim_ton.mean() - dfsil7.üretim_ton.std()):,.0f} tondan düşük olan dönemler: '),metin7)
    metin7 = np.append((f'{str(list(alt_dönem.index))[1:-1]}'),metin7)

    y1 = len(üst_dönem.loc[üst_dönem.index<çeyrek[1]])
    y2 = len(üst_dönem.loc[üst_dönem.index>çeyrek[1]])

    metin7 = np.append((f'Üst eşik miktarını aşan dönemlerin %{100*(y1/len(üst_dönem)):,.2f} yılın ilk yarısında;'),metin7)
    metin7 = np.append((f'Üst eşik miktarını aşan dönemlerin %{100*(y2/len(üst_dönem)):,.2f} yılın ikinci yarısında meydana gelmiştir.'),metin7)

    ç1 = len(alt_dönem.loc[alt_dönem.index<çeyrek[1]])
    ç4 = len(alt_dönem.loc[alt_dönem.index>çeyrek[1]])

    metin7 = np.append((f'Alt eşik miktarından düşük dönemlerin %{100*(ç1/len(alt_dönem)):,.2f} yılın ilk yarısında;'),metin7)
    metin7 = np.append((f'Alt eşik miktarından düşük dönemlerin %{100*(ç4/len(alt_dönem)):,.2f} yılın ikinci yarısında meydana gelmiştir.'),metin7)

    #2. Min ve max dönemlerin listesi ve metin ve her dönem değerinin bütün içindeki oranı
    min_dönem = np.argmin(dfsil7.üretim_ton)
    max_dönem = np.argmax(dfsil7.üretim_ton)
    min_oran = np.min(dfsil7.üretim_ton)/dfsil7.üretim_ton.sum()
    max_oran = np.max(dfsil7.üretim_ton)/dfsil7.üretim_ton.sum()
    metin7 = np.append((f'En düşük üretim yapılan {dönem} {dfsil7.üretim_ton.min():,.0f} ton ile {min_dönem+1}. {dönem} olmuştur.'),metin7)
    metin7 = np.append((f'Bu miktar bugüne kadar yapılan tüm üretimin %{100*min_oran:,.2f} denk gelmektedir.'),metin7)
    metin7 = np.append((f'En yüksek üretim yapılan {dönem} {dfsil7.üretim_ton.max():,.0f} ton ile {max_dönem+1}. {dönem} olmuştur.'),metin7)
    metin7 = np.append((f'Bu miktar bugüne kadar yapılan tüm üretimin %{100*max_oran:,.2f} denk gelmektedir.'),metin7)

    #çeyrek ortalamaları
    df_kış = dfsil7.üretim_ton[:çeyrek[0]].mean()
    df_ilk = dfsil7.üretim_ton[çeyrek[0]:çeyrek[1]].mean()
    df_yaz = dfsil7.üretim_ton[çeyrek[1]:çeyrek[2]].mean()
    df_son = dfsil7.üretim_ton[çeyrek[2]:].mean()
    metin7 = np.append((f'İlk çeyrek üretim ortalaması {df_kış:,.0f} tondur.'),metin7)
    metin7 = np.append((f'İkinci çeyrek üretim ortalaması {df_ilk:,.0f} tondur.'),metin7)
    metin7 = np.append((f'Üçüncü çeyrek üretim ortalaması {df_yaz:,.0f} tondur.'),metin7)
    metin7 = np.append((f'Dördüncü çeyrek üretim ortalaması {df_son:,.0f} tondur.'),metin7)

    # haftalık raporda biten hafta ile bir önceki haftanın karşılaştırması yapılacak.
    son_dönem = dfsil7.index.max()
    son_ürt = dfsil7.üretim_ton[-1:].iloc[0]
    bir_ürt = dfsil7.üretim_ton[-2:-1].iloc[0]
    tüm_ort = dfsil7.üretim_ton[:-2].mean()

    if son_ürt > bir_ürt:
        metin7 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile bir önceki üretim miktarından {bir_ürt:,.0f} tondan %{np.abs(100-(100*(son_ürt/bir_ürt))):,.2f} yüksek gerçekleşmiştir."),metin7)
    else:
        metin7 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile bir önceki üretim miktarı olan {bir_ürt:,.0f} tondan %{100*(son_ürt/bir_ürt):,.2f} düşük gerçekleşmiştir."),metin7)    

    # haftalık raporda biten hafta ile yıl başından bu yana tüm haftaların ortalamalarının karşılaştırması yapılacak.
    if son_ürt > tüm_ort:
        metin7 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile diğer tüm önceki dönemlerin ortalaması olan {tüm_ort:,.0f} tondan %{np.abs(100-(100*(son_ürt/tüm_ort))):,.2f} yüksek gerçekleşmiştir."),metin7)
    else:
        metin7 = np.append((f"{son_dönem}. {dönem.capitalize()} üretim miktarı {son_ürt:,.0f} ton ile diğer tüm önceki dönemlerin ortalaması olan {tüm_ort:,.0f} tondan %{100*(son_ürt/tüm_ort):,.2f} düşük gerçekleşmiştir."),metin7)
    
    metin7 = np.flip(metin7)

trace_solalt = np.append(fig,trace_solalt)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#günlük rapor
#hat bazında seçilen yemin toplam günlük üretim miktarı ve toplam çalışma zamanı ve harcanan enerji (1.hat, 2,hat vb.)
h1_ısk_yüzde = np.random.uniform(0,0.0002)
h2_ısk_yüzde = np.random.uniform(0,0.0001)
h3_ısk_yüzde = np.random.uniform(0,0.00015)
h4_ısk_yüzde = np.random.uniform(0,0.00025)

global metin10_gün, metin11_gün
metin10_gün = []
metin11_gün = []

date = dfürt.date_pick.max()
dftarih = dfürt.loc[(dfürt['tarih']==date)]

metin10_gün = np.append(f'{date} tarihindeki genel üretim istatistikleri', metin10_gün)

h1_süre = len(dftarih.loc[dftarih.pr1_miktar!=0])
h1_miktar = round(dftarih['pr1_miktar'].sum()/1000)
if h1_miktar == 0:
    metin10_gün = np.append(f'{date} tarihinde 1. Hatta üretim yapılamamıştır.',metin10_gün)
else:
    h1_hız = h1_miktar*1000/h1_süre
    h1_ıskarta = round(h1_miktar*h1_ısk_yüzde*1000,2) #kg tekrar çevirmek için
    metin10_gün = np.append(f'Hat 1, üretim miktarı {h1_miktar:,.0f} ton, süre {h1_süre:,.0f} dakika, ıskarta miktarı {h1_ıskarta:,.2f} kg, hız {h1_hız:,.0f} kg/dk',metin10_gün)

h2_süre = len(dftarih.loc[dftarih.pr2_miktar!=0])
h2_miktar = round(dftarih['pr2_miktar'].sum()/1000)
if h2_miktar == 0:
    metin10_gün = np.append(f'{date} tarihinde 2. Hatta üretim yapılamamıştır.',metin10_gün)
else:
    h2_hız = h2_miktar*1000/h2_süre
    h2_ıskarta = round(h2_miktar*h2_ısk_yüzde*1000,2) #kg tekrar çevirmek için
    metin10_gün = np.append(f'Hat 2, üretim miktarı {h2_miktar:,.0f} ton, süre {h2_süre:,.0f} dakika, ıskarta miktarı {h2_ıskarta:,.2f} kg, hız {h2_hız:,.0f} kg/dk',metin10_gün)

h3_süre = len(dftarih.loc[dftarih.pr3_miktar!=0])
h3_miktar = round(dftarih['pr3_miktar'].sum()/1000)
if h3_miktar == 0:
    metin10_gün = np.append(f'{date} tarihinde 3. Hatta üretim yapılamamıştır.',metin10_gün)
else:
    h3_hız = h3_miktar*1000/h3_süre
    h3_ıskarta = round(h3_miktar*h3_ısk_yüzde*1000,2) #kg tekrar çevirmek için
    metin10_gün = np.append(f'Hat 3, üretim miktarı {h3_miktar:,.0f} ton, süre {h3_süre:,.0f} dakika, ıskarta miktarı {h3_ıskarta:,.2f} kg, hız {h3_hız:,.0f} kg/dk',metin10_gün)

h4_süre = len(dftarih.loc[dftarih.pr4_miktar!=0])
h4_miktar = round(dftarih['pr4_miktar'].sum()/1000)
if h4_miktar == 0:
    metin10_gün = np.append(f'{date} tarihinde 4. Hatta üretim yapılamamıştır.',metin10_gün)
else:
    h4_hız = h4_miktar*1000/h4_süre
    h4_ıskarta = round(h4_miktar*h4_ısk_yüzde*1000,2) #kg tekrar çevirmek için
    metin10_gün = np.append(f'Hat 4, üretim miktarı {h4_miktar:,.0f} ton, süre {h4_süre:,.0f} dakika, ıskarta miktarı {h4_ıskarta:,.2f} kg, hız {h4_hız:,.0f} kg/dk',metin10_gün)

metin10_gün = np.flip(metin10_gün)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

#hat ve en çok üretilen 3 ürün üretim istatistikleri
metin11_gün = np.append((f'{date} tarihindeki hat ve ürün bazındaki üretim istatistikleri'),metin11_gün)    

ürün1 = (dftarih.pr1_ürün.value_counts()[1:])
ürün2 = (dftarih.pr2_ürün.value_counts()[1:])
ürün3 = (dftarih.pr3_ürün.value_counts()[1:])
ürün4 = (dftarih.pr4_ürün.value_counts()[1:])

if len(ürün1)== 0:
    metin11_gün = np.append(f'{date} tarihinde 1. hatta üretim yapılmamıştır.',metin11_gün)
else:
    for i in range(0,len(ürün1)):
        dfür1 = dftarih.loc[dftarih['pr1_ürün'] == ürün1.index[i]]    
        h1_süre = len(dfür1)
        h1_miktar = round(dfür1['pr1_miktar'].sum()/1000)
        if h1_süre!=0:
            h1_hız = h1_miktar*1000/h1_süre
        elif h1_süre == 0:
            h1_hız=0
        h1_ıskarta = round(h1_miktar*h1_ısk_yüzde*1000,2) #kg tekrar çevirmek için    
        metin11_gün = np.append((f'Hat 1, {ürün1.index[i]} üretim miktarı {h1_miktar:,.0f} ton, süre {h1_süre:,.0f} dakika, ıskarta miktarı {h1_ıskarta:,.2f} kg, hız {h1_hız:,.0f} kg/dk'),metin11_gün)
    
if len(ürün2) == 0:
    metin11_gün = np.append(f'{date} tarihinde 2. hatta üretim yapılmamıştır.',metin11_gün)
else:
    for i in range(0,len(ürün2)):
        dfür2 = dftarih.loc[dftarih['pr2_ürün'] == ürün2.index[i]]   
        h2_süre = len(dfür2)
        h2_miktar = round(dfür2['pr2_miktar'].sum()/1000)
        if h2_süre!=0:
            h2_hız = h2_miktar*1000/h2_süre    
        else:
            h2_hız=0
        h2_ıskarta = h2_miktar*h2_ısk_yüzde*1000 #kg tekrar çevirmek için
        metin11_gün = np.append((f'Hat 2, {ürün2.index[i]} üretim miktarı {h2_miktar:,.0f} ton, süre {h2_süre:,.0f} dakika, ıskarta miktarı {h2_ıskarta:,.2f} kg, hız {h2_hız:,.0f} kg/dk'),metin11_gün)

if len(ürün3) == 0:
    metin11_gün = np.append(f'{date} tarihinde 3. hatta üretim yapılmamıştır.',metin11_gün) 
else:
    for i in range(0,len(ürün3)):
        dfür3 = dftarih.loc[dftarih['pr3_ürün'] == ürün3.index[i]]
        h3_süre = len(dfür3)
        h3_miktar = round(dfür3['pr3_miktar'].sum()/1000)
        if h3_süre!=0:
            h3_hız = h3_miktar*1000/h3_süre
        else:
            h3_hız =0
        h3_ıskarta = h3_miktar*h3_ısk_yüzde*1000 #kg tekrar çevirmek için
        metin11_gün = np.append((f'Hat 3, {ürün3.index[i]} üretim miktarı {h3_miktar:,.0f} ton, süre {h3_süre:,.0f} dakika, ıskarta miktarı {h3_ıskarta:,.2f} kg, hız {h3_hız:,.0f} kg/dk'),metin11_gün)
    
if len(ürün4) == 0:
    metin11_gün = np.append(f'{date} tarihinde 4. hatta üretim yapılmamıştır.',metin11_gün)
else:
    for i in range(0,len(ürün4)):
        dfür4 = dftarih.loc[dftarih['pr4_ürün'] == ürün4.index[i]] 
        h4_süre = len(dfür4)
        h4_miktar = dfür4['pr4_miktar'].sum()/1000
        if h4_süre!=0:
            h4_hız = round(h4_miktar*1000/h4_süre)
        else:
            h4_hız=0
        h4_ıskarta = h4_miktar*h4_ısk_yüzde*1000 #kg tekrar çevirmek için
        metin11_gün = np.append((f'Hat 4, {ürün4.index[i]} üretim miktarı {h4_miktar:,.0f} ton, süre {h4_süre:,.0f} dakika, ıskarta miktarı {h4_ıskarta:,.2f} kg, hız {h4_hız:,.0f} kg/dk'),metin11_gün)

metin11_gün = np.flip(metin11_gün)

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
# 5 parça bilgi
# üretim miktarı, datepickerrange ile paralel
start_date = dfürt.date_pick.min()
end_date = dfürt.date_pick.max()
df_ = dfürt.loc[(dfürt.date_pick>=start_date)&(dfürt.date_pick<=end_date)]
kart_1 = f"{df_[['pr1_miktar','pr2_miktar','pr3_miktar','pr4_miktar']].sum().sum()/1000:,.0f} ton"

# kapasite kullanım oranı
liste = []
for idx,i in enumerate (dfürt.gün.unique()):
    dfgün = dfürt.loc[dfürt.gün==i]
    liste = np.append(round(dfgün[['pr1_miktar','pr2_miktar','pr3_miktar','pr4_miktar']].sum().sum()/1000,0),liste)
gün_max = np.max(liste)
kart_2 = f'%{100*(df_[["pr1_miktar","pr2_miktar","pr3_miktar","pr4_miktar"]].sum().sum()/1000)/(gün_max*(end_date-start_date).days):,.2f}'

# en çok üretilen ürün ve yüzdesi
kolon = ürün_list
dfürt_max = pd.DataFrame(index = kolon, columns= ['üretim_ton'])
say = 0
for i in kolon:
    h1 = df_.loc[df_['pr1_ürün']==i]
    h2 = df_.loc[df_['pr2_ürün']==i]
    h3 = df_.loc[df_['pr3_ürün']==i]
    h4 = df_.loc[df_['pr4_ürün']==i]    
    toplam =h1['pr1_miktar'].sum()+h2['pr2_miktar'].sum()+h3['pr3_miktar'].sum()+h4['pr4_miktar'].sum()
    dfürt_max['üretim_ton'].iloc[say] = round(toplam/1000,2)
    say +=1
dfürt_max = dfürt_max.sort_values('üretim_ton', ascending = False)
dfürt_max = dfürt_max[:1]
kart_3 = f'{dfürt_max.index[0]}, {dfürt_max.üretim_ton.iloc[0]:,.0f} ton'

# hat bazında üretim dağılımı
hat1_ürt = df_['pr1_miktar'].sum()/1000
hat2_ürt = df_['pr2_miktar'].sum()/1000
hat3_ürt = df_['pr3_miktar'].sum()/1000
hat4_ürt = df_['pr4_miktar'].sum()/1000
hat1_oran = hat1_ürt/(hat1_ürt+hat2_ürt+hat3_ürt+hat4_ürt)
hat2_oran = hat2_ürt/(hat1_ürt+hat2_ürt+hat3_ürt+hat4_ürt)
hat3_oran = hat3_ürt/(hat1_ürt+hat2_ürt+hat3_ürt+hat4_ürt)
hat4_oran = hat4_ürt/(hat1_ürt+hat2_ürt+hat3_ürt+hat4_ürt)
kart_4 = f'%{100*hat1_oran:,.2f}, %{100*hat2_oran:,.2f}, %{100*hat3_oran:,.2f}, %{100*hat4_oran:,.2f}'

# hat bazında ort hız dağılımları
hat1_hız = df_.pr1_miktar.sum()/len(df_.loc[df_.pr1_ürün!='0'])
hat2_hız = df_.pr2_miktar.sum()/len(df_.loc[df_.pr2_ürün!='0'])
hat3_hız = df_.pr3_miktar.sum()/len(df_.loc[df_.pr3_ürün!='0'])
hat4_hız = df_.pr4_miktar.sum()/len(df_.loc[df_.pr4_ürün!='0'])
kart_5 = f'{hat1_hız:,.2f}kg/dk, {hat2_hız:,.2f}kg/dk, {hat3_hız:,.2f}kg/dk, {hat4_hız:,.2f}kg/dk'

gr_df = [dfsil1, dfsil4, dfsil7, dfsil3, dfsil61]
gr_dict = dict(zip(gr_list,gr_df))

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#grafik yorumlama aracı
    

#response_solüst = text_model.predict(prompt= f
"""General introduction:
This is a cattle feed production facility. Factory has produced a little more than approximately
275000 tons of almost 60 different variety of cattle feed in 2022. 
There are 4 production lines in factory.

Examples :
Periods higher than the upper threshold limit of 6,569 tons: 1, 8, 9, 17, 21, 40, 44, 50
Periods lower than the lower threshold limit of 4,034 tons: 4, 25, 28, 39, 48
62% of the periods exceeding the upper threshold amount are in the first half of the year;
38% of the periods exceeding the upper threshold amount occurred in the second half of the year.
40% of periods lower than the lower threshold amount are in the first half of the year;

Task:
Write me an interpretation of the graph {dfsil1}, where index is the {dönem_dict.get(dönem)}of the year and 
üretim/ton column is the production amount in tons'
"""#, max_output_tokens=2048, temperature=0.3)

#metin_solüst = str(response_solüst)
#translate_client = translate.Client()
#metin_solüst = translate_client.translate(metin_solüst, target_language='tr')
#m_solüst = re.search('text=(.+?)&#39;citationMetadata', str(metin_solüst))
#if m_solüst:
#    yz_solüst = m_solüst.group(1)  


#response_solort = text_model.predict(prompt= 
"""General introduction:
This is a cattle feed production facility. Factory has produced a little more than approximately
275000 tons of almost 60 different variety of cattle feed in 2022. 
There are 4 production lines in factory.

Example:
General production statistics by line&#39; &#39;
Line no: Line1&
Periods with an upper threshold limit of 1,941 tons: 
1, 6, 7, 8, 9, 21, 30, 40, 50;
Lower threshold limit Periods with less than 966 tonnes: 
25, 26, 27, 28, 43, 48&#39; &#39;
67% of periods exceeding the upper threshold amount are in the first half of the year;
33% of the periods exceeding the upper threshold amount occurred in the second half of the year.
33% of periods lower than the lower threshold amount are in the first half of the year;
50% of the periods below the lower threshold amount occurred in the second half of the year.
The week with the lowest production was the 28th week with 285 tons.
This amount corresponds to 0.38% of all production made to date.

Task:
Write me a comprehensive interpretation of the graph {dfsil4}, 
where index is the {dönem_dict.get(dönem)} of the year.
column named hat1 is the production amount in tons in line 1 and column name hat1_ort is the rolling mean of hat1""",
#max_output_tokens=2048, temperature=0.5)

#metin_solort = str(response_solort)
#translate_client = translate.Client()
#metin_solort = translate_client.translate(metin_solort, target_language='tr')

#m_solort = re.search('text=(.+?)&#39;citationMetadata', str(metin_solort))
#if m_solort:
#    yz_solort = m_solort.group(1)

#response_solalt = text_model.predict(prompt= f
"""General introduction:
This is a cattle feed production facility. Factory has produced a little more than approximately
275000 tons of almost 60 different variety of cattle feed in 2022. 
There are 4 production lines in factory.

Task:
Write me an interpretation of the graph {dfsil7}, where index is the {dönem_dict.get(dönem)} of the year and
üretim_ton column is the production amount of selected product {ürün} in tons""",
#max_output_tokens=2048, temperature=0.5)
#metin_solalt = str(response_solalt)
#translate_client = translate.Client()
#metin_solalt = translate_client.translate(metin_solalt, target_language='tr')

#m_solalt = re.search('text=(.+?)&#39', str(metin_solalt))
#if m_solalt:
#    yz_solalt = m_solalt.group(1)

#response_sağüst = text_model.predict(prompt= f
    
"""General introduction: 
This is a cattle feed production facility. Factory has produced a little more than approximately
275000 tons of almost 60 different variety of cattle feed in 2022. 
There are 4 production lines in factory.

Task: 
Write me an interpretation of the graph {dfsil3}, where index is the {dönem_dict.get(dönem)} of the year.
artış_eksiliş column indicates wheter or not the production amount in the previous {dönem_dict.get(dönem)} has increased. 
0 indicates a decrease, 1 indicates an increase.
arka_arkaya column indicates whether or not increasing or decreasing {dönem_dict.get(dönem)} come one after the other,
in other words if they are consecutive {dönem_dict.get(dönem)} or not. 
1 indicates that previous period is also a continuation of increase or decrease whatever the case maybe.    
"""
#max_output_tokens=2048, temperature=0.5)

#metin_sağüst = str(response_sağüst)
#translate_client = translate.Client()
#metin_sağüst = translate_client.translate(metin_sağüst, target_language='tr')

#m_sağüst = re.search('text=(.+?)&#39;citationMetadata', str(metin_sağüst))
#if m_sağüst:
#    yz_sağüst = m_sağüst.group(1)

#response_sağort = text_model.predict(prompt= f
"""General introduction: This is a cattle feed production facility. Factory has produced a little more than approximately
275000 tons of almost 60 different variety of cattle feed in 2022. 
There are 4 production lines in factory.

Task:Write me an interpretation of the graph {dfsil61}, where index is the names of the products produced in the factory
and üretim_ton column is the production amount in tons"""#, max_output_tokens=2048, temperature=0.5)
#metin_sağort = str(response_sağort)
#translate_client = translate.Client()
#metin_sağort = translate_client.translate(metin_sağort, target_language='tr')

#m_sağort = re.search('text=(.+?)&#39', str(metin_sağort))
#if m_sağort:
#    yz_sağort = m_sağort.group(1)

yz_sonuç = ''

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#--------------- alt kısımdaki kod sabit kalacak-----------------------------------------------------

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
                        start_date = min(dfürt.date_pick),
                        end_date = max(dfürt.date_pick),
                        min_date_allowed = dfürt.date_pick.min(),
                        max_date_allowed = dfürt.date_pick.max(),
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

hat_seç = html.Div([#dropdown div
    dbc.Label('Hat seçimi',style = seçkont_lab_sty),
    dcc.Dropdown(hat_kısalist, value= hat_kısalist[0], multi = False, id= 'hat_ismi', clearable = False,
                 style = seçkont_gr_sty),
        ],className = seçkont_div_cls    
)#dropdown div   

#yz_solüst = html.Div([#modal div
#    dbc.Button("YZ Asistan Grafik Yorum", id="open_modal_solüst", n_clicks=0, style = seçkont_gr_sty,
#            className = seçkont_div_cls),
#    dbc.Modal([
#        dbc.ModalHeader(dbc.ModalTitle(f"Üretim Miktarları Grafiğinin Yapay Zeka Yorumlaması")),
#        dbc.ModalBody(yz_solüst),
#        dbc.ModalFooter(
#            dbc.Button("Kapat", id="close_modal_solüst", style= seçkont_gr_sty, n_clicks=0)),
#            ],
#            id="modal_solüst", scrollable=True, is_open=False, style = seçkont_gr_sty)
#        ],className=seçkont_div_cls
#)#modal div

#yz_solort = html.Div([#modal div
#    dbc.Button("YZ Asistan Grafik Yorum", id="open_modal_solort", n_clicks=0, style = seçkont_gr_sty,
#            className = seçkont_div_cls),
#    dbc.Modal([
#        dbc.ModalHeader(dbc.ModalTitle(f"Hat Bazında Üretim Miktarı Grafiğinin Yapay Zeka Yorumlaması")),
#        dbc.ModalBody(yz_solort),
#        dbc.ModalFooter(
#            dbc.Button("Kapat", id="close_modal_solort", style= seçkont_gr_sty, n_clicks=0)),
#            ],
#            id="modal_solort", scrollable=True, is_open=False, style = seçkont_gr_sty)
#        ],className=seçkont_div_cls
#)#modal div

#yz_solalt = html.Div([#modal div
#    dbc.Button("YZ Asistan Grafik Yorum", id="open_modal_solalt", n_clicks=0, style = seçkont_gr_sty,
#            className = seçkont_div_cls),
#    dbc.Modal([
#        dbc.ModalHeader(dbc.ModalTitle(f"Ürün Bazında Üretim Miktarı Grafiğinin Yapay Zeka Yorumlaması")),
#        dbc.ModalBody(yz_solalt),
#        dbc.ModalFooter(
#            dbc.Button("Kapat", id="close_modal_solalt", style= seçkont_gr_sty, n_clicks=0)),
#            ],
#            id="modal_solalt", scrollable=True, is_open=False, style = seçkont_gr_sty)
#        ],className=seçkont_div_cls
#)#modal div

#yz_sağüst = html.Div([#modal div
#    dbc.Button("YZ Asistan Grafik Yorum", id="open_modal_sağüst", n_clicks=0, style = seçkont_gr_sty,
#            className = seçkont_div_cls),
#    dbc.Modal([
#        dbc.ModalHeader(dbc.ModalTitle(f"Üretim Artış/Azalış Grafiğinin Yapay Zeka Yorumlaması")),
#        dbc.ModalBody(yz_sağüst),
#        dbc.ModalFooter(
#            dbc.Button("Kapat", id="close_modal_sağüst", style= seçkont_gr_sty, n_clicks=0)),
#            ],
#            id="modal_sağüst", scrollable=True, is_open=False, style = seçkont_gr_sty)
#        ],className=seçkont_div_cls
#)#modal div

#yz_sağort = html.Div([#modal div
#    dbc.Button("YZ Asistan Grafik Yorum", id="open_modal_sağort", n_clicks=0, style = seçkont_gr_sty,
#            className = seçkont_div_cls),
#    dbc.Modal([
#        dbc.ModalHeader(dbc.ModalTitle(f"Yıllık Üretim Miktarı En Yüksek Olan 25 Ürünün Üretim Miktarları Grafiğinin Yapay Zeka Yorumlaması")),
#        dbc.ModalBody(yz_sağort),
#        dbc.ModalFooter(
#            dbc.Button("Kapat", id="close_modal_sağort", style= seçkont_gr_sty, n_clicks=0)),
#            ],
#            id="modal_sağort", scrollable=True, is_open=False, style = seçkont_gr_sty)
#        ],className=seçkont_div_cls
#)#modal div


#soru_kutusu = dbc.InputGroup(
#    children=[
#        dbc.Input(id="user-input", placeholder="Merhaba, bana Üretim Üretim veri tabanıyla ilgili bir soru sorun...", 
#                  type="text", 
#                  style=seçkont_gr_sty1),
#        dbc.InputGroup(dbc.Button("Gönder", id="gönder", style=seçkont_gr_sty1)),
#    ],className=seçkont_div_cls
#)

#yanıt_kutusu = dbc.InputGroup(
#    children = [
#        dbc.Label('Sorunuzun yanıtı:', id='başlık', style=seçkont_gr_sty1),
#        dbc.Textarea(value = yz_sonuç, id='gövde', style=seçkont_gr_sty1),
#    ],className=seçkont_div_cls
#)

#yz_navbar = html.Div([#modal div
#    dbc.Button("SC YZ Soru Sor!!!", id="open_modal_soru", n_clicks=0, style = seçkont_gr_sty,
#            className = seçkont_div_cls),
#    dbc.Modal([ 
#        dbc.ModalHeader(dbc.ModalTitle(f"Solution Cube Yapay Zeka Yardımcısı")),
#        soru_kutusu,
#        yanıt_kutusu,
#        dbc.ModalFooter(
#            dbc.Button("Kapat", id="close_modal_soru", style= seçkont_gr_sty , n_clicks=0)),
#            ],
#            id="modal_soru", scrollable=True, is_open=False, size='lg', style = seçkont_gr_sty)
#        ],className=seçkont_div_cls
#)#modal div


sayfa_seç = html.Div([
    dbc.Label('Sayfa seçimi',style = sayseç_lab_sty),
    dbc.Nav([    
        dbc.NavItem(dbc.NavLink("Üretim Paneli", active=True, href="http://127.0.0.1:8072", className = sayseç_nav_cls),
                   style = sayseç_nav_sty),
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

seçim_kontrol2 = dbc.Card([tarih_seç, dönem_seç, ürün_seç, hat_seç, sayfa_seç], style = {'height':1030}, 
                         className = graf_div_cls)#, yz_navbar

#--------------------------------
#fonksiyonlar

#kart şeklindeki 4 adet metin alanı

kart_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Toplam Üretim Miktarı'], className="text-nowrap"),
            html.H1(kart_1, id = 'kart_1', className="fs-2 text"),
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls
)


kart_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Kapasite Kullanım Oranı'], className="text-nowrap"),
            html.H1(kart_2, id = 'kart_2', className="fs-2 text"),           
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)


kart_3 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['En Çok Üretilen Ürün'], className="text-nowrap"),
            html.H1(kart_3, id = 'kart_3', className="fs-2 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_4 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Hatlar Üretim Dağılımı'], className="text-nowrap"),
            html.H1(kart_4, id = 'kart_4', className="fs-5 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

kart_5 = dbc.Card(
    dbc.CardBody(
        [
            html.H3(['Hatlar Ort.Hız Dağılımı'], className="text-nowrap"),
            html.H1(kart_5, id = 'kart_5', className="fs-5 text"), 
        ], className = kart_lab_cls
    ),
    style = {'width':380,'height':130}, className = kart_göv_cls,
)

solüst = html.Div([#solüst(1.grafik)
    dbc.Label(f'Seçili Dönem Bazında Üretim Miktarları Grafiği (ton)', id = 'solüst_başlık',size = 'lg', className='fw-bold'),
    dcc.Graph(id='solüst',
              figure = trace_solüst[0],
              style = graf_grph_sty   
             )], className = graf_div_cls
)#solüst(1.grafik)


solort = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Dönem ve Hat Bazında Üretim Miktarı (ton)", id = 'solort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='solort',
              figure = trace_solort[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)

solalt = html.Div([#solalt(2.grafik)
    dbc.Label( f"Seçili Dönem ve Ürün Bazında Üretim Miktarı (ton)", id='solalt_başlık', size = 'lg',className='fw-bold'),
    dcc.Graph(id='solalt',
              figure = trace_solalt[0],
              style = graf_grph_sty
             )], className = graf_div_cls
)#solort(2.grafik)


sağüst = html.Div([#sağüst(3.grafik)
    dbc.Label(f"Seçili Dönem Bazında Üretim Artış/Azalış Grafiği", id = 'sağüst_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağüst',
              figure = trace_sağüst[0],
              style = graf_grph_sty
             )], className = graf_div_cls    
)#sağüst(3.grafik)

sağort = html.Div([#sağalt(4.grafik)
    dbc.Label( f"Yıllık Üretim Miktarı En Yüksek Olan 25 Ürünün Üretim Miktarları (ton)", id = 'sağort_başlık', size = 'lg', className='fw-bold'),
    dcc.Graph(id='sağort',
              figure = trace_sağort[0],
              style = graf_grph_sty
             )],  className = graf_div_cls
)#sağalt(4.grafik)

anomali = html.Div([
            dbc.Label("Anomali Raporu", size='lg',style= {'width':766,'height':50}, 
                      className = anom_label_cls),
            dcc.Textarea(id = 'anomali_rapor', value=[f'{metin11_ano}\n{metin1_ano}\n\n{metin31_ano}\n{metin3_ano}\n\n{metin4_ano}\n{metin41_ano}\n\n{metin7_ano}\n{metin71_ano}'], 
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
    html.Button("Raporla", id="rap_düğme", style = {'font-size':'20px','width':172,'height':50},
                    className = "bg-warning text-dark border-secondary rounded-pill shadow rounded"),
    ], className = seçkont_div_cls
)#raporlama düğmesi alanı

seçim_kontrol3 = dbc.Card([gün_seç,rapdönem_seç,rap_düğme], style = {'width':172,'height':500}, 
                         className = graf_div_cls)
#---------------------------------------------------

günlük_rap = html.Div([
    dbc.Label('Günlük Rapor', size='lg',style= {'width':566,'height':50}, 
                      className = anom_label_cls),
    dcc.Textarea(id = 'günlük_rap', value=[f'{metin10_gün}\n\n{metin11_gün}\n'], 
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
                     dbc.Col([solüst,solort],width =6),#yz_solüst,yz_solort
                     dbc.Col([sağüst,sağort],width =5)]),#yz_sağüst, yz_sağort
            
            dbc.Row([dbc.Col([solalt],width =4),#, yz_solalt
                     dbc.Col([anomali],width =4),
                     dbc.Col([seçim_kontrol3],width =1),
                     dbc.Col([günlük_rap],width =3)
                    ]), 
            
        ], fluid = True, className = applayout_gövde_cls)#container
    
])#div
