/*
=======================================================================
Saklı Yordam: Gümüş katmanın yüklenmesi
=======================================================================
Betik amacı: 
  Bu saklı yordam tabloları Bronz katmandan dönüştürerek yükler.
  Aşağıdaki işleri yapar:
    -Varsa varolan tabloları yükleme işleminden önce siler.
    -Yeni kolon oluşturma ve türetilniş kolon oluşturma, veri tipi değiştirme vb. 
    dönüşüm işlemlerini yapar.
    -INSERT INTO komutunu kullanarak Bronz katman tablolarından verileri gümüş
    tablolarına yükler. 

Örnek kullanım:
  EXEC bronz.yükle_bronz;
=======================================================================
*/
---------------------------------------------------
------CREATE PROCEDURE-----------------------------
---------------------------------------------------
create or alter procedure gümüş.load_gümüş as
begin
	declare @start_time datetime, @end_time datetime, @batch_start_time datetime, @batch_end_time datetime;
	begin try
		set @batch_start_time = GETDATE();
		print '=====================================================';
		print 'Gümüş Katman Yükleniyor...';
		print '=====================================================';

		print '-----------------------------------------------------';
		print 'Üretim verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();		
		truncate table gümüş.üretim_veri;
		insert into gümüş.üretim_veri(
			tarih_saat,
			pr1_urun,
			pr1_miktar,
			pr2_urun,
			pr2_miktar,
			pr3_urun,
			pr3_miktar,
			pr4_urun,
			pr4_miktar,
			ay,
			hafta,
			gün
			)
			select
			tarih_saat,
			pr1_urun,
			pr1_miktar,
			pr2_urun,
			pr2_miktar,
			pr3_urun,
			pr3_miktar,
			pr4_urun,
			pr4_miktar,
			month(tarih_saat) as ay,
			datepart(week, tarih_saat) as hafta,
			day(tarih_saat) as gün
			from bronz.üretim_veri		
				
		set @end_time = getdate();

		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Otomasyon verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table gümüş.otomasyon_veri;
		insert into gümüş.otomasyon_veri(
			tarih_saat,
			hat1,
			hat2,
			hat3,
			hat4,
			hat1bsl_malz,
			hat1ml_akım,
			hat1kd_çsıcak,
			hat1ex_akım,
			hat1ex_çsıcak,
			hat1ex_rsıcak,
			hat1ex_hidbas,
			hat1pr_akım,
			hat2bsl_malz,
			hat2ml_akım,
			hat2kd_çsıcak,
			hat2ex_akım,
			hat2ex_çsıcak,
			hat2ex_rsıcak,
			hat2ex_hidbas,
			hat2pr_akım,
			hat3bsl_malz,
			hat3ml_akım,
			hat3kd_çsıcak,
			hat3ex_akım,
			hat3ex_çsıcak,
			hat3ex_rsıcak,
			hat3ex_hidbas,
			hat3pr_akım,
			hat4bsl_malz,
			hat4ml_akım,
			hat4kd_çsıcak,
			hat4ex_akım,
			hat4ex_çsıcak,
			hat4ex_rsıcak,
			hat4ex_hidbas,
			hat4pr_akım,
			ay,
			hafta,
			gün
			)
			select
			tarih_saat,
			hat1,
			hat2,
			hat3,
			hat4,
			hat1bsl_malz,
			hat1ml_akım,
			hat1kd_çsıcak,
			hat1ex_akım,
			hat1ex_çsıcak,
			hat1ex_rsıcak,
			hat1ex_hidbas,
			hat1pr_akım,
			hat2bsl_malz,
			hat2ml_akım,
			hat2kd_çsıcak,
			hat2ex_akım,
			hat2ex_çsıcak,
			hat2ex_rsıcak,
			hat2ex_hidbas,
			hat2pr_akım,
			hat3bsl_malz,
			hat3ml_akım,
			hat3kd_çsıcak,
			hat3ex_akım,
			hat3ex_çsıcak,
			hat3ex_rsıcak,
			hat3ex_hidbas,
			hat3pr_akım,
			hat4bsl_malz,
			hat4ml_akım,
			hat4kd_çsıcak,
			hat4ex_akım,
			hat4ex_çsıcak,
			hat4ex_rsıcak,
			hat4ex_hidbas,
			hat4pr_akım,
			month(tarih_saat) as ay,
			datepart(week, tarih_saat) as hafta,
			day(tarih_saat) as gün
		from bronz.otomasyon_veri

		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Enerji verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table gümüş.enerji_veri;
		insert into gümüş.enerji_veri(
			tarih_saat,
			hat1,
			hat2,
			hat3,
			hat4,
			hat1_pr_en,
			hat1_ex_en,
			hat1_kd_en,
			hat2_pr_en,
			hat2_ex_en,
			hat2_kd_en,
			hat3_pr_en,
			hat3_ex_en,
			hat3_kd_en,
			hat4_pr_en,
			hat4_ex_en,
			hat4_kd_en,
			ay,
			hafta,
			gün
			)
			select
			tarih_saat,
			hat1,
			hat2,
			hat3,
			hat4,
			hat1_pr_en,
			hat1_ex_en,
			hat1_kd_en,
			hat2_pr_en,
			hat2_ex_en,
			hat2_kd_en,
			hat3_pr_en,
			hat3_ex_en,
			hat3_kd_en,
			hat4_pr_en,
			hat4_ex_en,
			hat4_kd_en,
			month(tarih_saat) as ay,
			datepart(week, tarih_saat) as hafta,
			day(tarih_saat) as gün
		from bronz.enerji_veri

		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Forklift off-site-history verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table gümüş.forklift_osh;
		insert into gümüş.forklift_osh(
			row_no,
			device,
			start_date,
			end_date,
			off_site_time,
			off_site_seconds,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek
			)
			select
			row_no,
			device,
			start_date,
			end_date,
			off_site_time,
			off_site_seconds,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek
		from bronz.forklift_osh

		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Forklift working-hours-history verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table gümüş.forklift_whh;
		insert into gümüş.forklift_whh(
			row_no,
			tracker,
			work_start_date,
			work_start_hour,
			work_finish_date,
			work_finish_hour,
			duration,
			duration_seconds,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek,
			gün_saati,
			start_ts,
			finish_ts
			)
			select
			row_no,
			tracker,
			work_start_date,
			work_start_hour,
			work_finish_date,
			work_finish_hour,
			duration,
			duration_seconds,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek,
			gün_saati,
			cast(convert(datetime,work_start_date) + work_start_hour as datetime) as start_ts,
			cast(convert(datetime,work_finish_date) + work_finish_hour as datetime) as finish_ts
			from bronz.forklift_whh
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Forklift zone-presence-history verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table gümüş.forklift_zph;
		insert into gümüş.forklift_zph(
			tarih,
			tracker,
			zone,
			start_date1,
			start_time,
			end_date,
			end_time,
			ay,
			hafta,
			gün,
			hafta_günü,
			gün_saati,
			çeyrek,
			start_ts,
			finish_ts,
			duration_sec
			)
			select 
			tarih,
			tracker,
			zone,
			start_date1,
			start_time,
			end_date,
			end_time,
			ay,
			hafta,
			gün,
			hafta_günü,
			gün_saati,
			çeyrek,
			cast(convert(datetime,start_date1) + convert(datetime,start_time) as datetime) as start_ts,
			cast(convert(datetime,end_date) + convert(datetime,end_time) as datetime) as finish_ts,
			datediff(second,start_time, end_time) as duration_sec
	from bronz.forklift_zph
	set @end_time = getdate();
	print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
	print '---------------';

	print '-----------------------------------------------------';
	print 'Personel konum verileri yükleniyor...';
	print '-----------------------------------------------------';
	set @start_time = getdate();
	truncate table gümüş.personel_veri;
	insert into gümüş.personel_veri(
		tarih_saat,
		_id,
		floorPlan_id,
		floorPlan_label,
		presence_duration,
		presence_startedAt,
		tracker_id,
		tracker_label,
		zone_id,
		zone_label,
		ay,
		hafta,
		gün,
		tarih_n,
		zaman,
		dept_ismi,
		kat_ismi,
		hafta_günü,
		gün_saati,
		çeyrek,
		gün_ismi,
		kısa_isim,
		vardiya
		)
		select
		tarih_saat,
		_id,
		floorPlan_id,
		floorPlan_label,
		presence_duration,
		presence_startedAt,
		tracker_id,
		tracker_label,
		zone_id,
		zone_label,
		ay,
		hafta,
		gün,
		tarih_n,
		zaman,
		dept_ismi,
		kat_ismi,
		hafta_günü,
		gün_saati,
		çeyrek,
		gün_ismi,
		kısa_isim,
		vardiya
		from bronz.personel_veri
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Sipariş verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table gümüş.sipariş_veri;
		insert into gümüş.sipariş_veri(
			tarih,
			bayii,
			sipariş_miktarı,
			irsaliye_miktarı,
			fatura_miktarı,
			ürün_adı,
			birim_fiyat,
			alt_top,
			kdv,
			genel_toplam,
			kayıt_tarihi,
			onay_tarihi,
			istenen_teslimT,
			son_irsaliyeT,
			sevk_performansı,
			zamanında,
			kayıt_eden
			)
			select
			tarih,
			bayii,
			sipariş_miktarı,
			irsaliye_miktarı,
			fatura_miktarı,
			ürün_adı,
			birim_fiyat,
			alt_top,
			kdv,
			genel_toplam,
			kayıt_tarihi,
			onay_tarihi,
			istenen_teslimT,
			son_irsaliyeT,
			sevk_performansı,
			zamanında,
			kayıt_eden
		from bronz.sipariş_veri
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Bakım verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table gümüş.bakım_veri;
		insert into gümüş.bakım_veri(
			Arıza_Bakım,
			Bildirim_Tarihi,
			Ekipman_Adı,
			ArızaBakım_Grubu,
			ArızaBakım_Türü,
			ArızaBakım_Detayı,
			Parça_Adedi,
			MüdahaleBaşl_Tarihi,
			MüdahaleBitiş_Tarihi,
			MüdahaleBaşl_Saati,
			MüdahaleBitiş_Saati,
			MüdahaleSüresi_Dk,
			Açıklama,
			baş_saati,
			bit_saati,
			ay,
			hafta,
			gün
			)
			select
			Arıza_Bakım,
			Bildirim_Tarihi,
			Ekipman_Adı,
			ArızaBakım_Grubu,
			ArızaBakım_Türü,
			ArızaBakım_Detayı,
			Parça_Adedi,
			MüdahaleBaşl_Tarihi,
			MüdahaleBitiş_Tarihi,
			MüdahaleBaşl_Saati,
			MüdahaleBitiş_Saati,
			MüdahaleSüresi_Dk,
			Açıklama,
			convert(datetime,(MüdahaleBaşl_Tarihi + ' ' + MüdahaleBaşl_Saati + ':00'),105) as baş_saati,
			convert(datetime,(MüdahaleBitiş_Tarihi + ' ' + MüdahaleBitiş_Saati + ':00'),105) as bit_saati,
			month(convert(date,MüdahaleBaşl_Tarihi,105)) as ay,
			datepart(week, convert(date,MüdahaleBaşl_Tarihi, 105)) as hafta,
			day(convert(date, MüdahaleBaşl_Tarihi, 105)) as gün
			from bronz.bakım_veri

		set @end_time = GETDATE();
		print '>> Yükleme süresi: ' + CAST(DATEDIFF(SECOND, @start_time, @end_time) AS NVARCHAR) + ' saniye';
        PRINT '>> -------------';

		SET @batch_end_time = GETDATE();
		PRINT '=========================================='
		PRINT 'Gümüş katmanın yüklemesi tamamlandı...';
        PRINT '   - Toplam Yükleme Süresi: ' + CAST(DATEDIFF(SECOND, @batch_start_time, @batch_end_time) AS NVARCHAR) + ' saniye';
		PRINT '=========================================='
		
	END TRY
	BEGIN CATCH
		PRINT '=========================================='
		PRINT 'Gümüş Katman yüklenirken bir hata oluştu...'
		PRINT 'Hata Mesajı' + ERROR_MESSAGE();
		PRINT 'Hata Mesajı' + CAST (ERROR_NUMBER() AS NVARCHAR);
		PRINT 'Hata Mesajı' + CAST (ERROR_STATE() AS NVARCHAR);
		PRINT '=========================================='
	END CATCH
END

