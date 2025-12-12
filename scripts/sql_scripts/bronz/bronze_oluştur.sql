/*
============================================
DDL Betik: Bronz tablolarının oluşturulması
============================================
Betik amacı:
  Bu betik bronz katmanındaki tabloları 
  oluşturur ev varsa eskileri siler.
Bronz tablolarındaki DDL yapısını tekrar 
  tanımlamak için bu betiği çalıştırın.
===========================================
*/

if object_id ('bronz.üretim_veri', 'U') is not null
	drop table bronz.üretim_veri;
create table bronz.üretim_veri(
	tarih_saat datetime,
	pr1_urun nvarchar(50), 
	pr1_miktar float, 
	pr2_urun nvarchar(50), 
	pr2_miktar float, 
	pr3_urun nvarchar(50), 
	pr3_miktar float, 
	pr4_urun nvarchar(50), 
	pr4_miktar float
);


if object_id ('bronz.enerji_veri', 'U') is not null
	drop table bronz.enerji_veri;
create table bronz.enerji_veri(
	tarih_saat datetime,
	hat1 nvarchar(50), 
	hat2 nvarchar(50),
	hat3 nvarchar(50),
	hat4 nvarchar(50),
	hat1_pr_en float,
	hat1_ex_en float,
	hat1_kd_en float,
	hat2_pr_en float,
	hat2_ex_en float,
	hat2_kd_en float,
	hat3_pr_en float,
	hat3_ex_en float,
	hat3_kd_en float,
	hat4_pr_en float,
	hat4_ex_en float,
	hat4_kd_en float
)


if object_id ('bronz.otomasyon_veri', 'U') is not null
	drop table bronz.otomasyon_veri;
create table bronz.otomasyon_veri(
	tarih_saat datetime,
	hat1 nvarchar(50),
	hat2 nvarchar(50),
	hat3 nvarchar(50),
	hat4 nvarchar(50),
	hat1bsl_malz float,
	hat1ml_akım float,
	hat1kd_çsıcak float,
	hat1ex_akım float,
	hat1ex_çsıcak float,
	hat1ex_rsıcak float,
	hat1ex_hidbas float,
	hat1pr_akım float,
	hat2bsl_malz float,
	hat2ml_akım float,
	hat2kd_çsıcak float,
	hat2ex_akım float,
	hat2ex_çsıcak float,
	hat2ex_rsıcak float,
	hat2ex_hidbas float,
	hat2pr_akım float,
	hat3bsl_malz float,
	hat3ml_akım float,
	hat3kd_çsıcak float,
	hat3ex_akım float,
	hat3ex_çsıcak float, 
	hat3ex_rsıcak float, 
	hat3ex_hidbas float,
	hat3pr_akım float,
	hat4bsl_malz float,
	hat4ml_akım float,
	hat4kd_çsıcak float,
	hat4ex_akım float,
	hat4ex_çsıcak float,
	hat4ex_rsıcak float,
	hat4ex_hidbas float,
	hat4pr_akım float
)

if object_id ('bronz.personel_veri', 'U') is not null
	drop table bronz.personel_veri;
create table bronz.personel_veri(
	tarih_saat datetime,
	_id nvarchar(50),
	floorPlan_id nvarchar(50),
	floorPlan_label nvarchar(50),
	presence_duration int,
	presence_startedAt nvarchar(50),
	tracker_id nvarchar(50), 
	tracker_label nvarchar(50),
	zone_id nvarchar(50),
	zone_label nvarchar(50),
	ay int,
	hafta int,
	gün int,
	tarih_n nvarchar(50),
	zaman nvarchar(50),
	dept_ismi nvarchar(50),
	kat_ismi nvarchar(50),
	hafta_günü int,
	gün_saati int,
	çeyrek int,
	gün_ismi nvarchar(50),
	kısa_isim nvarchar(50),
	vardiya int
)

if object_id ('bronz.forklift_zph', 'U') is not null
	drop table bronz.forklift_zph;
create table bronz.forklift_zph(
	tarih date,
	tracker nvarchar(50),
	zone nvarchar(50),
	start_date1 date,
	start_time time,
	end_date date,
	end_time time,
	duration_sec int,
	ay int,
	hafta int,
	gün int,
	hafta_günü int,
	gün_saati int,
	çeyrek int
)

if object_id ('bronz.forklift_osh', 'U') is not null
	drop table bronz.forklift_osh;
create table bronz.forklift_osh(
	row_no int,
	device nvarchar(50),
	start_date datetime,
	end_date datetime,
	off_site_time nvarchar(50),
	off_site_seconds float,
	ay int,
	hafta int,
	gün int,
	hafta_günü int,
	çeyrek int
);

if object_id ('bronz.forklift_whh', 'U') is not null
	drop table bronz.forklift_whh;
create table bronz.forklift_whh(
	row_no int,
	tracker nvarchar(50),
	work_start_date date,
	work_start_hour datetime,
	work_finish_date date,
	work_finish_hour datetime,
	duration nvarchar(50),
	duration_seconds float,
	ay int,
	hafta int,
	gün int,
	hafta_günü int,
	çeyrek int,
	gün_saati int
)

if object_id ('bronz.sipariş_veri', 'U') is not null
	drop table bronz.sipariş_veri;
create table bronz.sipariş_veri(
	tarih datetime,
	bayii nvarchar(50),
	sipariş_miktarı float,
	irsaliye_miktarı int,
	fatura_miktarı int,
	ürün_adı nvarchar(50),
	birim_fiyat int,
	alt_top int,
	kdv float, 
	genel_toplam float,
	kayıt_tarihi datetime,
	onay_tarihi datetime,
	istenen_teslimT datetime,
	son_irsaliyeT datetime,
	sevk_performansı int,
	zamanında int,
	kayıt_eden nvarchar(50)
)

if object_id ('bronz.bakım_veri', 'U') is not null
	drop table bronz.bakım_veri;
create table bronz.bakım_veri(
	Arıza_Bakım nvarchar(50),
	Bildirim_Tarihi nvarchar(50),
	Ekipman_Adı nvarchar(50),
	ArızaBakım_Grubu nvarchar(50),
	ArızaBakım_Türü nvarchar(50),
	ArızaBakım_Detayı nvarchar(50),
	Parça_Adedi float,
	MüdahaleBaşl_Tarihi nvarchar(50),
	MüdahaleBitiş_Tarihi nvarchar(50),
	MüdahaleBaşl_Saati nvarchar(50),
	MüdahaleBitiş_Saati nvarchar(50),
	MüdahaleSüresi_Dk float,
	Açıklama nvarchar(300)
)
