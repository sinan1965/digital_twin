
/*
==========================================
Veri tabanı ve şemaların oluşturulması
==========================================
Amaç:
	Bu betik oluşturmak istediğimiz veritabanının halihazırda olup olmadığına bakar,
	eğer varsa silinir ve yeniden oluşturulur. Buna ek olarak veri tabanı içinde 
	üç adet 'bronz','gümüş' ve 'altın' isminde üç adet şema oluşturur.

Uyarı:
Bu betik çalıştırıldığında eğer var ise tüm Sayısalİkiz veritabanını siler ve 
tüm veriler de silinömiş olur. Bunu çalıştırmadan önce dikkale inceleyin ve gerekli 
veri yedeklemelerini aldığınızdan emin olun lütfen...
*/

use master
go

-- Olası eski Sayısalİkiz veritabanını silip yeniden oluşturmak için
if exists (select 1 from sys.databases where name = 'Sayısalİkiz')
begin
	alter database Sayısalİkiz set single_user with rollback immediate;
	drop database Sayısalİkiz;
end;
go

--Sayısalİkiz veri tabanının oluşturulması
create database Sayısalİkiz;
go
use Sayısalİkiz;
go
create schema bronz;
go
create schema gümüş;
go
create schema altın;
go
