drop schema wypozyczalnia cascade;
create schema wypozyczalnia;

SET datestyle = 'European, DMY';

create table wypozyczalnia.marki (
    id_marka 		SERIAL 			primary key,
    nazwa_marki 	VARCHAR(64) 	not null unique
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.klasa(
id_klasa 				serial 			primary key,
nazwa 					varchar(32)		not null unique,
opis 					text
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.modele(
id_model 				serial 			primary key,
nazwa_modelu 			varchar(64) 	not null,
id_marka 				int				not null,

constraint fk_model_marka foreign key (id_marka) references wypozyczalnia.marki (id_marka)
);

--------------------------------------------------------------------------------------------------------------------------------------

create table wypozyczalnia.auta(
id_auto 				serial 			primary key,
id_model 				int			 	not null,
numer_rejestracyjny 	varchar(50) 	not null unique,
rok 					int 			not null,

constraint fk_auto_model foreign key (id_model) references wypozyczalnia.modele (id_model)
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.klienci(
id_klient 				serial 			primary key,
imie 					varchar(64) 	not null,
nazwisko 				varchar(64) 	not null,
telefon 				varchar(9) 		not null unique
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.role(
id_rola 				serial 			primary key,
nazwa 					varchar(64) 	not null unique,
wyplata 				numeric(10,2)	not null check (wyplata > 0),
czy_moze_wynajmowac 	boolean 		not null default false
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.pracownicy(
id_pracownik 			serial 			primary key,
imie 					varchar(64) 	not null,
nazwisko 				varchar(64) 	not null,
telefon 				varchar(9) 		not null unique,
id_rola 				int 			not null,

constraint fk_pracownicy_rola foreign key (id_rola) references wypozyczalnia.role (id_rola)
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.wypozyczenia(
id_wypozyczenia 		serial 			primary key,
data_wypozyczenia 		date 			not null,
data_oddania 			date 			not null check (data_oddania > data_wypozyczenia),
id_klient 				int 			not null,
id_auto 				int 			not null,
id_pracownik 			int 			not null,

constraint fk_wypozyczenia_id_klient foreign key (id_klient) references wypozyczalnia.klienci (id_klient),
constraint fk_wypozyczenia_id_auto foreign key (id_auto) references wypozyczalnia.auta (id_auto),
constraint fk_wypozyczenia_id_pracownik foreign key (id_pracownik) references wypozyczalnia.pracownicy(id_pracownik)
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.cennik(
id_cennik 				serial 			primary key,
id_klasa 				int 			not null unique,
stawka_za_dzien 		numeric(10,2) 	not null check (stawka_za_dzien > 0),

constraint fk_cennik_id_klasa foreign key (id_klasa) references wypozyczalnia.klasa (id_klasa)
);
--------------------------------------------------------------------------------------------------------------------------------------
create table wypozyczalnia.platnosci(
id_platnosc serial primary key,
id_wypozyczenia int not null,
kwota numeric(10,2),

constraint fk_platnosci_id_wypozyczenia foreign key (id_wypozyczenia) references wypozyczalnia.wypozyczenia(id_wypozyczenia)
);
--------------------------------------------------------------------------------------------------------------------------------------
create type wypozyczalnia.status_enum as enum ('udane', 'nieudane', 'oczekujące');

create table wypozyczalnia.zamowienia(
id_zamowienia serial primary key,
id_klient int not null,
id_model int not null,
data_rozpoczecia date not null,
data_zakonczenia date not null check (data_zakonczenia > data_rozpoczecia),
status wypozyczalnia.status_enum not null,

constraint fk_zamowienia_id_klient foreign key (id_klient) references wypozyczalnia.klienci(id_klient),
constraint fk_zamowienia_id_model foreign key (id_model) references wypozyczalnia.modele(id_model)
);
--------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.marki(nazwa_marki) values
('Toyota'),
('Peugot'),
('BMW'),
('Mercedes'),
('Audi'),
('Volvo'),
('Opel');
--------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.modele(nazwa_modelu, id_marka) values
('Corolla', 1), ('Yaris', 1), ('RAV4', 1), ('Camry', 1), ('Highlander', 1),
('607', 2), ('208', 2), ('308', 2), ('2008', 2), ('3008', 2),
('X1', 3), ('X5', 3), ('Z4', 3), ('5 Series', 3), ('i8', 3),
('B-Class', 4), ('C-Class', 4), ('GLA', 4), ('GLE', 4), ('AMG GT', 4),
('RS7', 5), ('A4', 5), ('Q5', 5), ('TT', 5), ('e-tron', 5),
('XC40', 6), ('XC60', 6), ('XC90', 6), ('S60', 6), ('V90', 6),
('Astra', 7), ('Corsa', 7), ('Insignia', 7), ('Mokka', 7), ('Grandland', 7);
--------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.klasa(nazwa, opis) values
('B', 'Małe auta miejskie – kompaktowe samochody zapewniające większy komfort niż mikroauta'),
('C', 'Kompaktowe auta rodzinne – hatchbacki i mniejsze sedany lub kombi, idealne na codzienne użytkowanie'),
('D', 'Klasa średnia – większe sedany i kombi, oferujące więcej miejsca i wygody na dłuższe trasy'),
('E', 'Klasa wyższa – luksusowe sedany i kombi, łączące komfort, moc i zaawansowane technologie'),
('F', 'Luksusowe limuzyny – najbardziej prestiżowe auta, zapewniające najwyższy poziom luksusu i przestronności'),
('G', 'Sportowe auta i coupe – samochody o wysokich osiągach i dynamicznym wyglądzie, stworzone do emocjonującej jazdy'),
('J', 'SUV-y i crossovery – przestronne auta o wyższej pozycji siedzenia, idealne na różne rodzaje dróg i warunki terenowe');
--------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.auta (id_model, numer_rejestracyjny, rok) values
(1, 'DW45231A', 2019),
(1, 'DW98765B', 2020),
(2, 'KR54312C', 2021),
(2, 'KR87654D', 2018),
(2, 'KR11234E', 2012),
(3, 'WA78901F', 2022),
(3, 'WA23456G', 2021),
(4, 'PO67890H', 2014),
(4, 'PO12345I', 2019),
(4, 'PO98765J', 2021),
(4, 'PO45678K', 2022),
(5, 'GD12345L', 2020),
(5, 'GD98765M', 2015),
(5, 'GD87654N', 2023),
(5, 'GD54321O', 2017),
(5, 'GD67890P', 2021),
(6, 'DW60701A', 2013),
(6, 'DW60702B', 2019),
(6, 'DW60703C', 2020),
(6, 'DW60704D', 2021),
(7, 'KR20801E', 2012),
(7, 'KR20802F', 2021),
(7, 'KR20803G', 2019),
(8, 'WA30801H', 2017),
(8, 'WA30802I', 2018),
(8, 'WA30804J', 2010),
(9, 'PO200801K', 2021),
(9, 'PO200802L', 2016),
(10, 'GD300801M', 2020),
(10, 'GD300802N', 2019),
(10, 'GD300803O', 2021),
(10, 'GD300804P', 2020),
(10, 'GD300805Q', 2014),
(11, 'KR32001A', 2018),
(11, 'KR32002B', 2020),
(12, 'KR32003C', 2019),
(12, 'KR32004D', 2021),
(12, 'WA52001E', 2017),
(12, 'WA52002F', 2022),
(13, 'WA52003G', 2020),
(13, 'POX501H', 2019),
(12, 'POX502I', 2021),
(14, 'POX503J', 2020),
(14, 'GDZ401K', 2022),
(15, 'GDZ402L', 2021),
(13, 'GDi301M', 2020),
(15, 'GDi302N', 2023),
(14, 'GDi303O', 2022),
(16, 'DW12456A', 2018), 
(16, 'DW67891B', 2020),
(17, 'DW54321C', 2017), 
(17, 'KR67890D', 2019),
(16, 'KR98765E', 2021),
(18, 'KR87654F', 2020),
(16, 'WA34567G', 2021),
(20, 'WA23456H', 2019), 
(19, 'WA56789I', 2022), 
(19, 'PO12345J', 2020), 
(19, 'PO67890K', 2021), 
(20, 'GD54321L', 2021), 
(20, 'GD87654M', 2020), 
(16, 'GD23456N', 2022), 
(18, 'GD98765O', 2023), 
(19, 'GD34567P', 2021), 
(21, 'DW12345A', 2019), 
(21, 'DW56789B', 2020), 
(22, 'DW98765C', 2021), 
(23, 'KR12345A', 2021), 
(24, 'KR67890B', 2018), 
(23, 'KR54321C', 2020), 
(23, 'WA12345A', 2020), 
(22, 'WA67890B', 2021), 
(21, 'PO12345A', 2022), 
(22, 'PO56789B', 2023), 
(25, 'PO54321C', 2021), 
(25, 'PO67890D', 2020), 
(25, 'GD12345A', 2021), 
(25, 'GD67890B', 2022), 
(24, 'GD54321C', 2023), 
(22, 'GD98765D', 2021), 
(22, 'GD87654E', 2022), 
(26, 'KRXC401A', 2019), 
(26, 'KRXC402B', 2020), 
(26, 'KRXC403C', 2021), 
(26, 'POXC601D', 2018), 
(27, 'POXC602E', 2021), 
(27, 'POXC603F', 2020), 
(27, 'GDXC901G', 2017), 
(28, 'GDXC902H', 2019), 
(29, 'GDXC903I', 2021), 
(30, 'WAV601J', 2018), 
(30, 'WAV602K', 2020), 
(29, 'DWV901L', 2022), 
(31, 'DWAST01A', 2019), 
(32, 'DWAST02B', 2020), 
(32, 'DWAST03C', 2021), 
(33, 'KRCO101D', 2018), 
(34, 'KRCO102E', 2021),
(35, 'POINS01F', 2020),
(32, 'POINS02G', 2021),
(33, 'POINS03H', 2022),
(34, 'GDMOK01I', 2019),
(35, 'GDMOK02J', 2021),
(33, 'DWGRA01K', 2023),
(32, 'DWGRA02L', 2022),
(31, 'DWGRA03M', 2021);
--------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.klienci (imie, nazwisko, telefon) values
('Jan', 'Bartyzel', '600123456'),
('Anna', 'Witelska', '600234567'),
('Piotr', 'Wójcikowski', '600345678'),
('Katarzyna', 'Wójcik', '600456789'),
('Michał', 'Piątek', '600567890'),
('Agnieszka', 'Lewandowska', '600678901'),
('Antoni', 'Dąbrowski', '600789012'),
('Kamila', 'Kowalczyk', '600890123'),
('Maciej', 'Zieliński', '600901234'),
('Alina', 'Szymańska', '600012345'),
('Kacper', 'Woźniak', '600543210'),
('Aleksandra', 'Jankowska', '600432109'),
('Adam', 'Mazur', '600321098'),
('Ewa', 'Krawczyk', '600210987'),
('Rafał', 'Sikora', '600109876'),
('Natalia', 'Olszewska', '600098765'),
('Marcin', 'Sobczak', '600987654'),
('Magdalena', 'Kozłowska', '600876543'),
('Grzegorz', 'Czarnecki', '600765432'),
('Karolina', 'Pawlak', '600654321'),
('Łucja', 'Król', '600543219'),
('Amelia', 'Nowicka', '600432198'),
('Patryk', 'Wieczorek', '600321987'),
('Alicja', 'Kubiak', '600210976'),
('Marek', 'Lis', '600109865'),
('Beata', 'Wasilewska', '600098754'),
('Mateusz', 'Chmielewski', '600987643'),
('Olga', 'Górska', '600876532'),
('Kamil', 'Adamski', '600765421'),
('Julia', 'Michalska', '600654310');
--------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.role (nazwa, wyplata, czy_moze_wynajmowac) values
('Kierownik', 8000.00, true),
('Mechanik', 4500.00, false),
('Specjalista ds. obsługi klienta', 4000.00, true),
('Magazynier', 3500.00, false),
('Sprzątacz', 3000.00, false),
('Asystent biurowy', 3200.00, false);
--------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.pracownicy (imie, nazwisko, telefon, id_rola) values
('Jan', 'Kowalski', '501123456', 1),
('Piotr', 'Wiśniewski', '502123457', 2),
('Michał', 'Kamiński', '503123458', 2),
('Agnieszka', 'Nowak', '504123459', 3),
('Katarzyna', 'Wójcik', '505123460', 3),
('Tomasz', 'Dąbrowski', '506123461', 3),
('Joanna', 'Kowalczyk', '507123462', 3),
('Paweł', 'Zieliński', '508123463', 3),
('Monika', 'Szymańska', '509123464', 3),
('Krzysztof', 'Woźniak', '510123465', 3),
('Maria', 'Jankowska', '511123466', 3),
('Natalia', 'Olszewska', '512123467', 3),
('Łukasz', 'Król', '513123468', 3),
('Grzegorz', 'Czarnecki', '514123469', 4),
('Beata', 'Wasilewska', '515123470', 4),
('Ewa', 'Krawczyk', '516123471', 5),
('Magdalena', 'Kozłowska', '517123472', 5),
('Rafał', 'Sikora', '518123473', 6),
('Karolina', 'Pawlak', '519123474', 6),
('Zuzanna', 'Nowicka', '520123475', 6);
--------------------------------------------------------------------------------------------------------------------------------------
INSERT INTO wypozyczalnia.cennik (id_klasa, stawka_za_dzien) VALUES
(1, 50.00),
(2, 70.00), 
(3, 100.00), 
(4, 150.00), 
(5, 200.00), 
(6, 180.00), 
(7, 120.00); 
--------------------------------------------------------------------------------------------------------------------------------------
alter table wypozyczalnia.modele add column id_klasa int;
alter table wypozyczalnia.modele add constraint fk_model_id_klasa foreign key (id_klasa) references wypozyczalnia.klasa(id_klasa);

update wypozyczalnia.modele m
set id_klasa = case
	when m.nazwa_modelu in ('Yaris', '208', 'Corsa') then 1
    when m.nazwa_modelu in ('Corolla', '308', 'Astra', 'A4', 'B-Class') then 2 
    when m.nazwa_modelu in ('Camry', 'Insignia', 'S60', 'C-Class', '5 Series') then 3 
    when m.nazwa_modelu in ('607', 'V90', 'GLE') then 4 
    when m.nazwa_modelu in ('RS7', 'S-Class') then 5 
    when m.nazwa_modelu in ('Z4', 'AMG GT', 'TT', 'i8') then 6 
    when m.nazwa_modelu in ('RAV4', 'Highlander', '2008', '3008', 'X1', 'X5', 'Q5', 'e-tron', 'XC40', 'XC60', 'XC90', 'Mokka', 'Grandland', 'GLA') then 7
end;

alter table wypozyczalnia.modele alter column id_klasa set not null;
--------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------
create or replace view wypozyczalnia.modele_marki_klasy as
select mo.id_model, mo.nazwa_modelu, ma.id_marka, ma.nazwa_marki, k.id_klasa, k.nazwa
from wypozyczalnia.modele mo
join wypozyczalnia.marki ma on ma.id_marka = mo.id_marka
join wypozyczalnia.klasa k on k.id_klasa = mo.id_klasa;
--------------------------------------------------------------------------------------------------------------------------------------

create or replace view wypozyczalnia.szczegoly_aut as
select a.id_auto, m.id_model, ma.id_marka, m.nazwa_modelu, ma.nazwa_marki, a.numer_rejestracyjny, k.id_klasa, k.nazwa as nazwa_klasy
from wypozyczalnia.auta a
join wypozyczalnia.modele m on a.id_model = m.id_model
join wypozyczalnia.marki ma on m.id_marka = ma.id_marka
join wypozyczalnia.klasa k on m.id_klasa = k.id_klasa;
-------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.dostepne_auta_w_danym_terminie(data_rozpoczecia date, data_zakonczenia date)
returns table(
	id_auto int,
	nazwa_modelu varchar(64),
	nazwa_marki varchar(64),
	numer_rejestracyjny varchar(50),
	nazwa_klasy varchar(32)
	)
as $$
begin
	return query
	select sa.id_auto, sa.nazwa_modelu, sa.nazwa_marki, sa.numer_rejestracyjny, sa.nazwa_klasy
	from wypozyczalnia.szczegoly_aut sa
	where sa.id_auto not in (select w.id_auto from wypozyczalnia.wypozyczenia w 
	where (w.data_wypozyczenia <= data_zakonczenia and w.data_oddania >= data_rozpoczecia));
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.policz_auta_dostepne_w_danym_terminie(data_rozpoczecia date, data_zakonczenia date)
returns int as 
$$
declare 
	liczba_aut int;
begin
	select count(*) as liczba_aut into liczba_aut
	from wypozyczalnia.dostepne_auta_w_danym_terminie(data_rozpoczecia, data_zakonczenia);
	return liczba_aut;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.policz_modele_auta_dostepne_w_danym_terminie(data_rozpoczecia date, data_zakonczenia date)
returns table (
	nazwa_marki varchar(64),
	ilosc bigint
)
as $$
begin
	return query
	select auta.nazwa_marki, count(*) as ilosc
	from wypozyczalnia.dostepne_auta_w_danym_terminie(data_rozpoczecia, data_zakonczenia) as auta
	group by auta.nazwa_marki
	order by auta.nazwa_marki;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.policz_marki_auta_dostepne_w_danym_terminie(data_rozpoczecia date, data_zakonczenia date)
returns table (
	nazwa_marki varchar(64),
	nazwa_modelu varchar(64),
	ilosc bigint
)
as $$
begin
	return query
	select auta.nazwa_marki, auta.nazwa_modelu, count(*) as ilosc
	from wypozyczalnia.dostepne_auta_w_danym_terminie(data_rozpoczecia, data_zakonczenia) as auta
	group by auta.nazwa_marki, auta.nazwa_modelu
	order by auta.nazwa_marki, auta.nazwa_modelu;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.wyszukaj_modele(marka_id int)
	returns table(
	id_model int,
	nazwa_modelu varchar(64)
	)
as $$
begin
	return query
	select mm.id_model, mm.nazwa_modelu
	from wypozyczalnia.modele_marki_klasy mm
	where mm.id_marka = marka_id;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.wyszukaj_marki(model_id int)
	returns table(
	id_marka int,
	nazwa_marki varchar(64)
	)
as $$
begin
	return query
	select mm.id_marka, mm.nazwa_marki
	from wypozyczalnia.modele_marki_klasy mm
	where mm.id_model = model_id;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.sprawdz_numer_rejestracyjny()
returns trigger as $$
begin
    if new.numer_rejestracyjny !~ '^[A-Z]{2,3}[0-9]{2,3}[A-Z0-9 ]{2,5}$' then
        raise exception 'Niepoprawny numer rejestracyjny %s', new.numer_rejestracyjny;
		return null;
    end if;
    return new;
end;
$$ language plpgsql;

create trigger trigger_sprawdz_numer_rejestracyjny
before insert or update on wypozyczalnia.auta
for each row
execute function wypozyczalnia.sprawdz_numer_rejestracyjny();
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.sprawdz_numer_telefonu()
returns trigger as $$
begin 
	if new.telefon !~ '^\d{9}$' then
		raise exception 'Niepoprawny numer telefonu';
		return null;
	end if;
	return new;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create trigger trigger_sprawdz_numer_telefonu_klient
before insert or update on wypozyczalnia.klienci 
for each row 
execute function wypozyczalnia.sprawdz_numer_telefonu();

create trigger trigger_sprawdz_numer_telefonu_pracownik
before insert or update on wypozyczalnia.pracownicy 
for each row 
execute function wypozyczalnia.sprawdz_numer_telefonu();
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.wybierz_pracownika()
returns int as $$
declare
    id_pracownik int;
begin
    select p.id_pracownik into id_pracownik from wypozyczalnia.pracownicy p
    left join wypozyczalnia.wypozyczenia w on p.id_pracownik = w.id_pracownik
	join wypozyczalnia.role r on r.id_rola = p.id_rola
	where czy_moze_wynajmowac = True and r.id_rola != 1
    group by p.id_pracownik order by count(w.id_wypozyczenia) asc
    limit 1;

    if id_pracownik is null then
        raise exception 'brak dostępnych pracowników';
    end if;
    return id_pracownik;
end;
$$ language plpgsql;
---------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.zloz_zamowienie()
returns trigger as $$
declare 
    id_auto int;
    numer_rejestracyjny varchar(50);
    id_pracownik int;
begin
    select a.id_auto, a.numer_rejestracyjny
    into id_auto, numer_rejestracyjny
    from wypozyczalnia.auta a
    where a.id_model = new.id_model and not exists (select 1 from wypozyczalnia.wypozyczenia w 
	where w.id_auto = a.id_auto and (w.data_wypozyczenia <= new.data_zakonczenia and w.data_oddania >= new.data_rozpoczecia))
    limit 1;

    if id_auto is not null then
        id_pracownik := wypozyczalnia.wybierz_pracownika();
        insert into wypozyczalnia.wypozyczenia (data_wypozyczenia, data_oddania, id_klient, id_auto, id_pracownik)
        values (new.data_rozpoczecia, new.data_zakonczenia, new.id_klient, id_auto, id_pracownik);
        new.status := 'udane';
    else
        new.status := 'nieudane';
    end if;
    return new;
end; 
$$ language plpgsql;

create trigger trigger_zloz_zamowienie
before insert on wypozyczalnia.zamowienia
for each row
execute function wypozyczalnia.zloz_zamowienie();
---------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.dodaj_platnosc()
returns trigger as $$
declare
    kwota numeric(10,2);
    stawka_za_dzien numeric(10,2);
    czas_wypozyczenia int;
begin
    select c.stawka_za_dzien into stawka_za_dzien from wypozyczalnia.cennik c
    join wypozyczalnia.modele m on m.id_klasa = c.id_klasa
    join wypozyczalnia.auta a on a.id_model = m.id_model
    where a.id_auto = new.id_auto;

    czas_wypozyczenia := new.data_oddania - new.data_wypozyczenia;
    kwota := czas_wypozyczenia * stawka_za_dzien;

    insert into wypozyczalnia.platnosci (id_wypozyczenia, kwota) values (new.id_wypozyczenia, kwota);
    return new;
end;
$$ language plpgsql;

create trigger trigger_dodaj_platnosc
after insert on wypozyczalnia.wypozyczenia
for each row
execute function wypozyczalnia.dodaj_platnosc();
---------------------------------------------------------------------------------------------------------------------------------------
insert into wypozyczalnia.wypozyczenia (data_wypozyczenia, data_oddania, id_klient, id_auto, id_pracownik) values
('2024-11-15', '2025-03-15', 1, 4, 4), 
('2025-01-10', '2025-04-10', 13, 6, 5), 
('2024-10-25', '2025-05-12', 14, 10, 4), 
('2025-01-18', '2025-03-18', 20, 14, 5),
('2024-09-10', '2025-03-25', 2, 19, 6), 
('2024-11-22', '2025-05-20', 12, 21, 7), 
('2025-01-05', '2025-06-18', 15, 29, 8), 
('2024-08-20', '2025-04-12', 3, 36, 9), 
('2024-11-05', '2025-05-06', 11, 43, 10),
('2025-01-12', '2025-06-20', 16, 48, 11), 
('2024-12-01', '2025-04-08', 19, 39, 7), 
('2024-09-15', '2025-03-10', 4, 51, 12), 
('2025-01-18', '2025-05-20', 10, 57, 13), 
('2024-12-22', '2025-06-25', 17, 60, 12), 
('2024-08-06', '2025-03-18', 5, 66, 4), 
('2024-09-10', '2025-04-22', 9, 71, 5), 
('2025-01-15', '2025-05-30', 18, 78, 6),
('2024-10-14', '2025-06-18', 18, 75, 8), 
('2024-10-10', '2025-05-20', 6, 86, 7),
('2024-11-14', '2025-03-10', 7, 96, 8), 
('2025-01-10', '2025-06-28', 8, 101, 9), 
('2024-12-18', '2025-04-22', 19, 105, 10); 

insert into wypozyczalnia.wypozyczenia (data_wypozyczenia, data_oddania, id_klient, id_auto, id_pracownik) values
('2023-12-05', '2024-01-20', 21, 5, 4), 
('2024-09-08', '2025-01-18', 22, 11, 5), 
('2022-11-18', '2023-01-10', 23, 20, 6), 
('2024-12-15', '2025-01-05', 24, 22, 7), 
('2023-10-25', '2024-07-12', 25, 37, 9), 
('2024-09-20', '2024-12-25', 26, 41, 10), 
('2023-12-01', '2024-02-15', 27, 38, 11), 
('2022-08-15', '2023-05-28', 28, 52, 13),
('2024-01-01', '2024-06-15', 29, 58, 14), 
('2023-10-10', '2024-04-05', 30, 67, 4), 
('2024-11-20', '2025-01-12', 29, 76, 5), 
('2023-09-10', '2024-12-07', 1, 87, 7), 
('2024-05-12', '2025-01-10', 28, 88, 8), 
('2023-11-15', '2024-10-25', 28, 89, 9), 
('2024-12-01', '2025-01-08', 2, 102, 9), 
('2023-11-15', '2024-01-22', 30, 106, 10), 
('2025-01-10', '2025-01-15', 5, 104, 11); 
--------------------------------------------------------------------------------------------------------------------------------------
create or replace view wypozyczalnia.raport_finansowy as
select sum(p.kwota)::numeric(10,2) as całkowity_przychód, 
avg(p.kwota)::numeric(10,2) as średni_przychód_na_wypożyczenie
from wypozyczalnia.platnosci p;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace view wypozyczalnia.szczegoly_wypozyczenia as
select w.id_wypozyczenia, k.id_klient, CONCAT(k.imie, ' ', k.nazwisko) as klient, sa.nazwa_marki, sa.nazwa_modelu, sa.numer_rejestracyjny, w.data_wypozyczenia, w.data_oddania, w.id_pracownik, CONCAT(p.imie, ' ', p.nazwisko) as pracownik, sa.id_klasa
from wypozyczalnia.wypozyczenia w
join wypozyczalnia.klienci k on w.id_klient = k.id_klient
join wypozyczalnia.szczegoly_aut sa on w.id_auto = sa.id_auto
join wypozyczalnia.pracownicy p on p.id_pracownik = w.id_pracownik;
--------------------------------------------------------------------------------------------------------------------------------------

create or replace view wypozyczalnia.koszty_wypozyczenia as
select sw.id_wypozyczenia, sw.klient, sw.nazwa_modelu, sw.nazwa_marki, sw.numer_rejestracyjny, sw.data_oddania - sw.data_wypozyczenia as czas_wypozyczenia,
(sw.data_oddania - sw.data_wypozyczenia) * (select c.stawka_za_dzien from wypozyczalnia.cennik c where sw.id_klasa = c.id_klasa) as kwota
from wypozyczalnia.szczegoly_wypozyczenia sw;

--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.najpopularniejsze_modele(min_wypozyczenia int)
returns table(
    nazwa_modelu varchar(64),
    nazwa_marki varchar(64),
    liczba_wypozyczen bigint
) as $$
begin
    return query
    select sa.nazwa_modelu, sa.nazwa_marki, count(w.id_wypozyczenia) as liczba_wypozyczen
    from wypozyczalnia.wypozyczenia w
    join wypozyczalnia.szczegoly_aut sa on w.id_auto = sa.id_auto
    group by sa.nazwa_modelu, sa.nazwa_marki
    having count(w.id_wypozyczenia) >= min_wypozyczenia
    order by liczba_wypozyczen desc;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.przychody_na_klasy_aut()
returns table(
    nazwa_klasy varchar(32),
    liczba_wypozyczen bigint,
    calkowity_przychod numeric(10,2)
) as $$
begin
    return query
    select c.nazwa, count(w.id_wypozyczenia) as liczba_wypozyczen, sum(p.kwota) as calkowity_przychod
    from wypozyczalnia.wypozyczenia w
    join wypozyczalnia.platnosci p on w.id_wypozyczenia = p.id_wypozyczenia
    join wypozyczalnia.szczegoly_aut sa on w.id_auto = sa.id_auto
    join wypozyczalnia.klasa c on sa.id_klasa = c.id_klasa
    group by c.nazwa
    order by c.nazwa;
end;
$$ language plpgsql;
--------------------------------------------------------------------------------------------------------------------------------------
create or replace function wypozyczalnia.usun_powiazane_platnosci()
returns trigger as $$
begin
    delete from wypozyczalnia.platnosci
    where id_wypozyczenia = old.id_wypozyczenia;
    return old;
end;
$$ language plpgsql;

create trigger trigger_usun_powiazane_platnosci
after delete on wypozyczalnia.wypozyczenia
for each row
execute function wypozyczalnia.usun_powiazane_platnosci();