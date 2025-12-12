/*
=======================================================================
Saklı Yordam: Bronz katmanın yüklenmesi
=======================================================================
Betik amacı: 
  Bu saklı yordam csv dosyalarından bronz katmana verileri yükler.
  Aşağıdaki işleri yapar:
    -Varsa varolan tabloları yükleme işleminden önce siler.
    -BULK INSERT konutunu kullanarak csv dosyalarından verileri bronz
    tablolarına yükler. 

Örnek kullanım:
  EXEC bronz.yükle_bronz;
=======================================================================
*/

create or alter procedure bronz.yükle_bronz as
begin
	declare @start_time datetime, @end_time datetime, @batch_start_time datetime, @batch_end_time datetime;
	begin try
		set @batch_start_time = GETDATE();
		print '=====================================================';
		print 'Bronz katman yükleniyor...';
		print '=====================================================';

		print '-----------------------------------------------------';
		print 'Üretim verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
			
		truncate table bronz.üretim_veri;
		bulk insert bronz.üretim_veri
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\üretim\üretim_master_sample.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			codepage = '65001',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Enerji verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table bronz.enerji_veri;
		bulk insert bronz.enerji_veri
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\enerji\enerji_master_sample.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Otomasyon verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table bronz.otomasyon_veri;
		bulk insert bronz.otomasyon_veri
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\otomasyon\otomasyon_master_sample.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Personel konum verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table bronz.personel_veri;
		bulk insert bronz.personel_veri
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\personel\personel_master_sample.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);

		print '-----------------------------------------------------';
		print 'Forklift konum verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();truncate table bronz.forklift_zph;
		bulk insert bronz.forklift_zph
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\forklift\forklift_zone_presence.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';


		print '-----------------------------------------------------';
		print 'Forklift alan dışı süre verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();truncate table bronz.forklift_osh;
		bulk insert bronz.forklift_osh
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\forklift\forklift_off_site.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Forklift çalışma süreleri verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();truncate table bronz.forklift_whh;
		bulk insert bronz.forklift_whh
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\forklift\forklift_working_hours.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Sipariş verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();truncate table bronz.sipariş_veri;
		bulk insert bronz.sipariş_veri
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\sipariş\sipariş_master_veri.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		
		print '-----------------------------------------------------';
		print 'Bakım ve arıza verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();truncate table bronz.bakım_veri;
		bulk insert bronz.bakım_veri
		from 'C:\Users\Dell\Desktop\projeler\demo_proje\bakım_arıza\bakım_arıza_master_veri.csv'
		with (
			firstrow = 2,
			fieldterminator = ';',
			tablock
		);
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		set @batch_end_time = GETDATE();

		print '=====================================================';
		print 'Bronz katmanın yüklemesi tamamlandı...';
		print '  -Toplam yükleme süresi: ' + cast(datediff(second, @batch_start_time, @batch_end_time) as varchar) + ' saniye';
		print '=====================================================';

	end try
	begin catch
		print '=====================================================';
		print 'Bronz katman yüklenirken bir hata oluştu!';
		print 'Hata mesajı' + error_message();
		print 'Hata mesajı' + cast(error_number() as nvarchar);
		print 'Hata mesajı' + cast(error_state() as nvarchar);
		print '=====================================================';
	end catch
end
