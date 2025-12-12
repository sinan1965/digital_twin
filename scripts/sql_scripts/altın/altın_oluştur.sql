----------------------------------------------------
---------------Altın katman oluşturma---------------
----------------------------------------------------

if object_id ('altın.üretim_veri', 'U') is not null
	drop table altın.üretim_veri;
create table altın.üretim_veri(
	tarih_saat datetime,
	hat1_urun nvarchar(50), 
	hat1_miktar float, 
	hat2_urun nvarchar(50), 
	hat2_miktar float, 
	hat3_urun nvarchar(50), 
	hat3_miktar float, 
	hat4_urun nvarchar(50), 
	hat4_miktar float,
	ay int,
	hafta int,
	gün int,
	sayısalikiz_create_date datetime2 default getdate()
);


if object_id ('altın.enerji_veri', 'U') is not null
	drop table altın.enerji_veri;
create table altın.enerji_veri(
	tarih_saat datetime,
	hat1_urun nvarchar(50),	
	hat1_pres float,
	hat1_expander float,
	hat1_kondüsyonel float,
	hat2_urun nvarchar(50),
	hat2_pres float,
	hat2_expander float,
	hat2_kondüsyonel float,
	hat3_urun nvarchar(50),
	hat3_pres float,
	hat3_expander float,
	hat3_kondüsyonel float,
	hat4_urun nvarchar(50),
	hat4_pres float,
	hat4_expander float,
	hat4_kondüsyonel float,
	ay int,
	hafta int,
	gün int,
	sayısalikiz_create_date datetime2 default getdate()
)


if object_id ('altın.otomasyon_veri', 'U') is not null
	drop table altın.otomasyon_veri;
create table altın.otomasyon_veri(
	tarih_saat datetime,
	hat1_urun nvarchar(50),	
	hat1_beslemeMalzeme float,
	hat1_melasiyerAkım float,
	hat1_kondüsyonelÇıkışSıcaklık float,
	hat1_expanderAkım float,
	hat1_expanderÇıkışSıcaklık float,
	hat1_expanderRedüktörSıcaklık float,
	hat1_expanderHidrolikBasınç float,
	hat1_presAkım float,
	hat2_urun nvarchar(50),	
	hat2_beslemeMalzeme float,
	hat2_melasiyerAkım float,
	hat2_kondüsyonelÇıkışSıcaklık float,
	hat2_expanderAkım float,
	hat2_expanderÇıkışSıcaklık float,
	hat2_expanderRedüktörSıcaklık float,
	hat2_expanderHidrolikBasınç float,
	hat2_presAkım float,
	hat3_urun nvarchar(50),	
	hat3_beslemeMalzeme float,
	hat3_melasiyerAkım float,
	hat3_kondüsyonelÇıkışSıcaklık float,
	hat3_expanderAkım float,
	hat3_expanderÇıkışSıcaklık float,
	hat3_expanderRedüktörSıcaklık float,
	hat3_expanderHidrolikBasınç float,
	hat3_presAkım float,
	hat4_urun nvarchar(50),	
	hat4_beslemeMalzeme float,
	hat4_melasiyerAkım float,
	hat4_kondüsyonelÇıkışSıcaklık float,
	hat4_expanderAkım float,
	hat4_expanderÇıkışSıcaklık float,
	hat4_expanderRedüktörSıcaklık float,
	hat4_expanderHidrolikBasınç float,
	hat4_presAkım float,	
	ay int,
	hafta int,
	gün int,
	sayısalikiz_create_date datetime2 default getdate()
)

if object_id ('altın.personel_veri', 'U') is not null
	drop table altın.personel_veri;
create table altın.personel_veri(
	tarih_saat datetime,
	_id nvarchar(50),
	katPlan_anahtarı nvarchar(50),
	katPlan_etiketi nvarchar(50),
	bulunma_süresi int,
	bulunma_başlangıcı nvarchar(50),
	forklift_anahtarı nvarchar(50), 
	forklift_etiketi nvarchar(50),
	bölge_anahtarı nvarchar(50),
	bölge_etiketi nvarchar(50),
	ay int,
	hafta int,
	gün int,
	tarih_normal nvarchar(50),
	zaman nvarchar(50),
	departman_ismi nvarchar(50),
	kat_ismi nvarchar(50),		
	hafta_günü int,
	gün_saati int,
	çeyrek int,
	gün_ismi nvarchar(50),
	kısa_isim nvarchar(50),
	vardiya int,
	sayısalikiz_create_date datetime2 default getdate()
)

if object_id ('altın.forklift_zph', 'U') is not null
	drop table altın.forklift_zph;
create table altın.forklift_zph(
	tarih date,
	forklift_anahtarı nvarchar(50),
	bölge nvarchar(50),
	başlangıç_tarihi date,
	başlangıç_saati time,
	bitiş_tarihi time,
	bitiş_saati time,
	süre_saniye int,
	başlangıç_zamanDamgası datetime,
	bitiş_zamanDamgası datetime,
	ay int,
	hafta int,
	gün int,
	hafta_günü int,
	gün_saati int,
	çeyrek int,
	sayısalikiz_create_date datetime2 default getdate()
)

if object_id ('altın.forklift_osh', 'U') is not null
	drop table altın.forklift_osh;
create table altın.forklift_osh(
	sıra_no int,
	forklift_anahtarı nvarchar(50),
	başlangıç_tarihi datetime,
	bitiş_saati datetime,
	bölge_dışıSüre nvarchar(50),
	bölge_dışıSaniye float,
	ay int,
	hafta int,
	gün int,
	hafta_günü int,
	çeyrek int,
	sayısalikiz_create_date datetime2 default getdate()
);

if object_id ('altın.forklift_whh', 'U') is not null
	drop table altın.forklift_whh;
create table altın.forklift_whh(
	sıra_no int,
	forklift_anahtarı nvarchar(50),
	iş_başlangıçTarihi date,
	iş_başlangıçSaati datetime,
	iş_bitişTarihi date,
	iş_bitişSaati datetime,
	süre nvarchar(50),
	süre_saniye float,
	başlangıç_zamanDamgası datetime,
	bitiş_zamanDamgası datetime,
	ay int,
	hafta int,
	gün int,
	hafta_günü int,
	çeyrek int,
	gün_saati int,
	sayısalikiz_create_date datetime2 default getdate()
)

if object_id ('altın.sipariş_veri', 'U') is not null
	drop table altın.sipariş_veri;
create table altın.sipariş_veri(
	tarih datetime,
	bayii nvarchar(50),
	sipariş_miktarı float,
	irsaliye_miktarı int,
	fatura_miktarı int,
	ürün_adı nvarchar(50),
	birim_fiyat int,
	alt_toplam int,
	kdv float, 
	genel_toplam float,
	kayıt_tarihi datetime,
	onay_tarihi datetime,
	istenen_teslimTarihi datetime,
	son_irsaliyeTarihi datetime,
	sevk_performansı int,
	zamanında int,
	kayıt_eden nvarchar(50),
	başlangıç_zamanDamgası datetime,
	bitiş_zamanDamgası datetime,
	sayısalikiz_create_date datetime2 default getdate()
)

if object_id ('altın.bakım_veri', 'U') is not null
	drop table altın.bakım_veri;
create table altın.bakım_veri(
	arıza_bakım nvarchar(50),
	bildirim_tarihi nvarchar(50),
	ekipman_ismi nvarchar(50),
	arıza_bakımGrubu nvarchar(50),
	arıza_bakımTürü nvarchar(50),
	arıza_bakımDetayı nvarchar(50),
	parça_adedi float,
	müdahale_başlTarihi nvarchar(50),
	müdahale_başlSaati nvarchar(50),
	müdahale_bitişTarihi nvarchar(50),	
	müdahale_bitişSaati nvarchar(50),
	müdahale_süresiDk float,
	açıklama nvarchar(300),
	baş_saati datetime,
	bit_saati datetime,
	ay int,
	hafta int,
	gün int,
	sayısalikiz_create_date datetime2 default getdate()
)


