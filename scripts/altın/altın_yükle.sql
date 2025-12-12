--------------------------------------------------
------Altın katman prosedür oluşturma--------------
---------------------------------------------------

create or alter procedure altın.yükle_altın as
begin
	declare @start_time datetime, @end_time datetime, @batch_start_time datetime, @batch_end_time datetime;
	begin try
		set @batch_start_time = GETDATE();
		print '=====================================================';
		print 'Altın Katman Yükleniyor...';
		print '=====================================================';

		print '-----------------------------------------------------';
		print 'Üretim verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();		
		truncate table altın.üretim_veri;
		insert into altın.üretim_veri(
			tarih_saat,
			hat1_urun, 
			hat1_miktar, 
			hat2_urun, 
			hat2_miktar, 
			hat3_urun, 
			hat3_miktar, 
			hat4_urun, 
			hat4_miktar,
			ay,
			hafta,
			gün
			)
			select
			tarih_saat,
			pr1_urun as hat1_urun,
			pr1_miktar as hat1_miktar,
			pr2_urun as hat2_urun,
			pr2_miktar as hat2_miktar,
			pr3_urun as hat3_urun,
			pr3_miktar as hat3_miktar,
			pr4_urun as hat4_urun,
			pr4_miktar as hat4_miktar,
			ay,
			hafta,
			gün
			from gümüş.üretim_veri	
			set @end_time = getdate();

		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' saniye';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Otomasyon verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table altın.otomasyon_veri;
		insert into altın.otomasyon_veri(
			tarih_saat,
			hat1_urun,	
			hat1_beslemeMalzeme,
			hat1_melasiyerAkım,
			hat1_kondüsyonelÇıkışSıcaklık,
			hat1_expanderAkım,
			hat1_expanderÇıkışSıcaklık,
			hat1_expanderRedüktörSıcaklık,
			hat1_expanderHidrolikBasınç,
			hat1_presAkım,
			hat2_urun,	
			hat2_beslemeMalzeme,
			hat2_melasiyerAkım,
			hat2_kondüsyonelÇıkışSıcaklık,
			hat2_expanderAkım,
			hat2_expanderÇıkışSıcaklık,
			hat2_expanderRedüktörSıcaklık,
			hat2_expanderHidrolikBasınç,
			hat2_presAkım,
			hat3_urun,	
			hat3_beslemeMalzeme,
			hat3_melasiyerAkım,
			hat3_kondüsyonelÇıkışSıcaklık,
			hat3_expanderAkım,
			hat3_expanderÇıkışSıcaklık,
			hat3_expanderRedüktörSıcaklık,
			hat3_expanderHidrolikBasınç,
			hat3_presAkım,
			hat4_urun,	
			hat4_beslemeMalzeme,
			hat4_melasiyerAkım,
			hat4_kondüsyonelÇıkışSıcaklık,
			hat4_expanderAkım,
			hat4_expanderÇıkışSıcaklık,
			hat4_expanderRedüktörSıcaklık,
			hat4_expanderHidrolikBasınç,
			hat4_presAkım,
			ay,
			hafta,
			gün
			)
			select
			tarih_saat,
			hat1 as hat1_urun,			
			hat1bsl_malz as hat1_beslemeMalzeme,
			hat1ml_akım as hat1_melasiyerAkım,
			hat1kd_çsıcak as hat2_kondüsyonelÇıkışSıcaklık,
			hat1ex_akım as hat1_expanderAkım,
			hat1ex_çsıcak as hat1_expanderÇıkışSıcaklık,
			hat1ex_rsıcak as hat1_expanderRedüktörSıcaklık,
			hat1ex_hidbas as hat1_expanderHidrolikBasınç,
			hat1pr_akım as hat1_presAkım,
			hat2 as hat2_urun,
			hat2bsl_malz as hat2_beslemeMalzeme,
			hat2ml_akım as hat2_melasiyerAkım,
			hat2kd_çsıcak as hat2_kondüsyonelÇıkışSıcaklık,
			hat2ex_akım as hat2_expanderAkım,
			hat2ex_çsıcak as hat2_expanderÇıkışSıcaklık,
			hat2ex_rsıcak as hat2_expanderRedüktörSıcaklık,
			hat2ex_hidbas as hat1_expanderHidrolikBasınç,
			hat2pr_akım as hat2_presAkım,
			hat3 as hat3_urun,
			hat3bsl_malz as hat3_beslemeMalzeme,
			hat3ml_akım as hat3_melasiyerAkım,
			hat3kd_çsıcak as hat3_kondüsyonelÇıkışSıcaklık,
			hat3ex_akım as hat3_expanderAkım,
			hat3ex_çsıcak as hat3_expanderÇıkışSıcaklık,
			hat3ex_rsıcak as hat3_expanderRedüktörSıcaklık,
			hat3ex_hidbas as hat3_expanderHidrolikBasınç,
			hat3pr_akım as hat3_presAkım,
			hat4 as hat4_urun,
			hat4bsl_malz as hat4_beslemeMalzeme,
			hat4ml_akım as hat4_melasiyerAkım,
			hat4kd_çsıcak as hat4_kondüsyonelÇıkışSıcaklık,
			hat4ex_akım as hat4_expanderAkım,
			hat4ex_çsıcak as hat4_expanderÇıkışSıcaklık,
			hat4ex_rsıcak as hat4_expanderRedüktörSıcaklık,
			hat4ex_hidbas as hat4_expanderHidrolikBasınç,
			hat4pr_akım as hat4_presAkım,
			ay,
			hafta,
			gün
		from gümüş.otomasyon_veri

		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Enerji verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table altın.enerji_veri;
		insert into altın.enerji_veri(
			tarih_saat,
			hat1_urun,	
			hat1_pres,
			hat1_expander,
			hat1_kondüsyonel,
			hat2_urun,
			hat2_pres,
			hat2_expander,
			hat2_kondüsyonel,
			hat3_urun,
			hat3_pres,
			hat3_expander,
			hat3_kondüsyonel,
			hat4_urun,
			hat4_pres,
			hat4_expander,
			hat4_kondüsyonel,
			ay,
			hafta,
			gün
			)
			select
			tarih_saat,
			hat1 as hat1_urun,			
			hat1_pr_en as hat1_pres,
			hat1_ex_en as hat1_expander,
			hat1_kd_en as hat1_kondüsyonel,
			hat2 as hat2_urun,
			hat2_pr_en as hat2_pres,
			hat2_ex_en as hat2_expander,
			hat2_kd_en as hat2_kondüsyonel,
			hat3 as hat3_urun,
			hat3_pr_en as hat3_pres,
			hat3_ex_en as hat3_expander,
			hat3_kd_en as hat3_kondüsyonel,
			hat4 as hat4_urun,
			hat4_pr_en as hat4_pres,
			hat4_ex_en as hat4_expander,
			hat4_kd_en as hat4_kondüsyonel,
			ay,
			hafta,
			gün
		from gümüş.enerji_veri

		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Forklift off-site-history verileri yükleniyor...';
		print '-----------------------------------------------------';

		set @start_time = getdate();
		truncate table altın.forklift_osh;
		insert into altın.forklift_osh(
			sıra_no,
			forklift_anahtarı,
			başlangıç_tarihi,
			bitiş_saati,
			bölge_dışıSüre,
			bölge_dışıSaniye,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek
			)
			select
			row_no as sıra_no ,
			device as forklift_anahtarı,
			start_date as başlangıç_tarihi,
			end_date as bitiş_saati,
			off_site_time as bölge_dışıSüre,
			off_site_seconds as bölge_dışıSaniye,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek
		from gümüş.forklift_osh

		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Forklift working-hours-history verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table altın.forklift_whh;
		insert into altın.forklift_whh(
			sıra_no,
			forklift_anahtarı,
			iş_başlangıçTarihi,
			iş_başlangıçSaati,
			iş_bitişTarihi,
			iş_bitişSaati,
			süre,
			süre_saniye,
			başlangıç_zamanDamgası,
			bitiş_zamanDamgası,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek,
			gün_saati
			)
			select
			row_no as sıra_no,
			tracker as forklift_anahtarı,
			work_start_date as iş_başlangıçTarihi,
			work_start_hour as iş_başlangıçSaati,
			work_finish_date as iş_bitişTarihi,
			work_finish_hour as iş_bitişSaati,
			duration as süre,
			duration_seconds as süre_saniye,
			start_ts as başlangıç_zamanDamgası,
			finish_ts as bitiş_zamanDamgası,
			ay,
			hafta,
			gün,
			hafta_günü,
			çeyrek,
			gün_saati			
			from gümüş.forklift_whh
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Forklift zone-presence-history verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table altın.forklift_zph;
		insert into altın.forklift_zph(
			tarih,
			forklift_anahtarı,
			bölge,
			başlangıç_tarihi,
			başlangıç_saati,
			bitiş_tarihi,
			bitiş_saati,
			süre_saniye,
			başlangıç_zamanDamgası,
			bitiş_zamanDamgası,
			ay,
			hafta,
			gün,
			hafta_günü,
			gün_saati,
			çeyrek
			)
			select 
			tarih,
			tracker as forklift_anahtarı,
			zone as bölge,
			start_date1 as başlangıç_tarihi,
			start_time as başlangıç_saati,
			end_date as bitiş_tarihi,
			end_time as bitiş_saati,
			duration_sec as süre_saniye,
			start_ts as başlangıç_zamanDamgası,
			finish_ts as bitiş_zamanDamgası,			
			ay,
			hafta,
			gün,
			hafta_günü,
			gün_saati,
			çeyrek			
	from gümüş.forklift_zph
	set @end_time = getdate();
	print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
	print '---------------';

	print '-----------------------------------------------------';
	print 'Personel konum verileri yükleniyor...';
	print '-----------------------------------------------------';
	set @start_time = getdate();
	truncate table altın.personel_veri;
	insert into altın.personel_veri(
		tarih_saat,
		_id,
		katPlan_anahtarı,
		katPlan_etiketi,
		bulunma_süresi,
		bulunma_başlangıcı,
		forklift_anahtarı, 
		forklift_etiketi,
		bölge_anahtarı,
		bölge_etiketi,
		ay,
		hafta,
		gün,
		tarih_normal,
		zaman,
		departman_ismi,
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
		floorPlan_id as katPlan_anahtarı,
		floorPlan_label as katPlan_etiketi,
		presence_duration as bulunma_süresi,
		presence_startedAt as bulunma_başlangıcı,
		tracker_id as forklift_anahtarı,
		tracker_label as forklift_etiketi,
		zone_id as bölge_anahtarı,
		zone_label as bölge_etiketi,
		ay,
		hafta,
		gün,
		tarih_n as tarih_normal,
		zaman,
		dept_ismi as departman_ismi,
		vardiya
		hafta_günü,
		gün_saati,
		çeyrek,
		gün_ismi,
		kat_ismi,
		kısa_isim
		from gümüş.personel_veri
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Sipariş verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table altın.sipariş_veri;
		insert into altın.sipariş_veri(
			tarih,
			bayii,
			sipariş_miktarı,
			irsaliye_miktarı,
			fatura_miktarı,
			ürün_adı,
			birim_fiyat,
			alt_toplam,
			kdv,
			genel_toplam,
			kayıt_tarihi,
			onay_tarihi,
			istenen_teslimTarihi,
			son_irsaliyeTarihi,
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
			alt_top as alt_toplam,
			kdv,
			genel_toplam,
			kayıt_tarihi,
			onay_tarihi,
			istenen_teslimT as istenen_teslimTarihi,
			son_irsaliyeT as son_irsaliyeTarihi,
			sevk_performansı,
			zamanında,
			kayıt_eden
		from gümüş.sipariş_veri
		set @end_time = getdate();
		print '>> Yükleme süresi: ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '---------------';

		print '-----------------------------------------------------';
		print 'Bakım verileri yükleniyor...';
		print '-----------------------------------------------------';
		set @start_time = getdate();
		truncate table altın.bakım_veri;
		insert into altın.bakım_veri(
			arıza_bakım,
			bildirim_tarihi,
			ekipman_ismi,
			arıza_bakımGrubu,
			arıza_bakımTürü,
			arıza_bakımDetayı,
			parça_adedi,
			müdahale_başlTarihi,
			müdahale_başlSaati,
			müdahale_bitişTarihi,			
			müdahale_bitişSaati,
			müdahale_süresiDk,
			açıklama,
			baş_saati,
			bit_saati,
			ay,
			hafta,
			gün
			)
			select
			Arıza_Bakım as arıza_bakım,
			Bildirim_Tarihi as bildirim_tarihi,
			Ekipman_Adı as ekipman_ismi,
			ArızaBakım_Grubu as arıza_bakımGrubu,
			ArızaBakım_Türü as arıza_bakımTürü,
			ArızaBakım_Detayı as arıza_bakımDetayı,
			Parça_Adedi as parça_adedi,
			MüdahaleBaşl_Tarihi as müdahale_başlTarihi,
			MüdahaleBaşl_Saati as müdahale_başlSaati,
			MüdahaleBitiş_Tarihi as müdahale_bitişTarihi,			
			MüdahaleBitiş_Saati as müdahale_bitişSaati,
			MüdahaleSüresi_Dk as müdahale_süresiDk,
			Açıklama as açıklama,
			baş_saati,
			bit_saati,
			ay,
			hafta,
			gün
			from gümüş.bakım_veri

		set @end_time = GETDATE();
		print '>> Yükleme süresi: ' + CAST(DATEDIFF(SECOND, @start_time, @end_time) AS NVARCHAR) + ' saniye';
        PRINT '>> -------------';

		SET @batch_end_time = GETDATE();
		PRINT '=========================================='
		PRINT 'Altın katmanın yüklemesi tamamlandı...';
        PRINT '   - Toplam Yükleme Süresi: ' + CAST(DATEDIFF(SECOND, @batch_start_time, @batch_end_time) AS NVARCHAR) + ' saniye';
		PRINT '=========================================='
		
	END TRY
	BEGIN CATCH
		PRINT '=========================================='
		PRINT 'Altın Katman yüklenirken bir hata oluştu...'
		PRINT 'Hata Mesajı' + ERROR_MESSAGE();
		PRINT 'Hata Mesajı' + CAST (ERROR_NUMBER() AS NVARCHAR);
		PRINT 'Hata Mesajı' + CAST (ERROR_STATE() AS NVARCHAR);
		PRINT '=========================================='
	END CATCH
END

