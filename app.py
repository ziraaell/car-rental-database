import urllib.parse as up
import psycopg2
from flask import Flask, render_template, url_for, request, redirect, flash
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import CheckConstraint
from flask_migrate import Migrate, migrate
from sqlalchemy.sql import text
import os
from flask import jsonify
from sqlalchemy import func
import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings("ignore", category=SAWarning)

load_dotenv()
DB_URL = os.getenv('DATABASE_URL') 
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL2')
conn = psycopg2.connect(DB_URL)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Brand(db.Model):
    """
    Reprezentuje markę pojazdu w bazie danych.

    Attributes:
        id_marka (int): Klucz główny, identyfikator marki.
        nazwa_marki (str): Nazwa marki pojazdu.
    :no-index:
    """
    __tablename__ = 'marki'
    __table_args__ = (
    {'schema': 'wypozyczalnia'},
)

    id_marka = db.Column(db.Integer, primary_key = True)
    nazwa_marki = db.Column(db.String(64), nullable=False, unique=True)
    model_b = db.relationship('Model', back_populates='marka')


class Model(db.Model):
    """
    Reprezentuje model samochodu dostępny w systemie wypożyczalni.

    Attributes:
        id_model (int): Klucz główny, unikalny identyfikator modelu samochodu.
        nazwa_modelu (str): Nazwa modelu samochodu (np. "Mustang", "Civic"), wartość obowiązkowa.
        id_marka (int): Klucz obcy odnoszący się do tabeli 'Brand', określa markę pojazdu.
        id_klasa (int): Klucz obcy odnoszący się do tabeli 'CarClass', określa klasę pojazdu (np. "A", "B").
    
    Relationships:
        marka (relationship): Relacja do tabeli 'Brand', określająca markę, do której należy dany model.
        auta (relationship): Relacja do tabeli 'Car', reprezentująca wszystkie samochody należące do tego modelu.
        klasa (relationship): Relacja do tabeli 'CarClass', określająca klasę, do której przypisany jest model.
        zamowienia (relationship): Relacja do tabeli 'Order', reprezentująca zamówienia, w których wskazano dany model samochodu.
    :no-index:
    """
    __tablename__ = 'modele'
    __table_args__ = (
    {'schema': 'wypozyczalnia'},
)

    id_model = db.Column(db.Integer, primary_key = True)
    nazwa_modelu = db.Column(db.String(64), nullable=False)
    id_marka = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.marki.id_marka'), nullable=False)
    id_klasa = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.klasa.id_klasa'), nullable=False) 
    marka = db.relationship('Brand', back_populates="model_b")
    auta = db.relationship('Car', back_populates='model_a')
    klasa = db.relationship('CarClass', back_populates='model_k')
    zamowienia = db.relationship('Order', back_populates='model')


class CarClass(db.Model):
    """
    Model tabeli 'klasa', reprezentujący klasy samochodów w systemie wypożyczalni.

    Attributes:
        id_klasa (int): Klucz główny, unikalny identyfikator klasy samochodu.
        nazwa (str): Nazwa klasy samochodu (np. "B", "C", "SUV").
        opis (str): Opcjonalny opis klasy samochodu, zawierający szczegóły dotyczące jej charakterystyki.
        model_k (list[Model]): Relacja do modeli samochodów (Model) powiązanych z daną klasą.
        cennik (list[PriceList]): Relacja do tabeli 'cennik', zawierająca informacje o stawkach za wynajem dla danej klasy samochodów.
    :no-index:
    """
    __tablename__ = 'klasa'
    __table_args__ = (
    {'schema': 'wypozyczalnia'},
    )
    id_klasa = db.Column(db.Integer, primary_key = True)				
    nazwa = db.Column(db.String(32), nullable=False, unique=True)
    opis = db.Column(db.Text, nullable=True)
    model_k = db.relationship('Model', back_populates='klasa')
    cennik = db.relationship('PriceList', back_populates='klasa_p')

    

class Car(db.Model):
    """
    Reprezentuje samochód dostępny w wypożyczalni.

    Attributes:
        id_auto (int): Klucz główny, unikalny identyfikator samochodu.
        id_model (int): Klucz obcy odnoszący się do tabeli 'Model', określa model pojazdu.
        numer_rejestracyjny (str): Unikalny numer rejestracyjny samochodu.
        rok (int): Rok produkcji pojazdu.

    Relationships:
        model_a (relationship): Relacja do tabeli 'Model', określająca model pojazdu.
        wypozyczenia (relationship): Relacja do tabeli 'Rental', reprezentująca wypożyczenia, w których uczestniczy ten samochód.
    :no-index:
    """
    __tablename__ = 'auta'
    __table_args__ = (
    {'schema': 'wypozyczalnia'},
    )

    id_auto = db.Column(db.Integer, primary_key = True)
    id_model = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.modele.id_model'), nullable=False)
    numer_rejestracyjny = db.Column(db.String(50), nullable=False, unique=True)
    rok = db.Column(db.Integer, nullable=False)
    model_a  = db.relationship('Model', back_populates="auta")
    wypozyczenia = db.relationship('Rental', back_populates = 'auto')

class Client(db.Model):
    """
    Reprezentuje klienta w systemie wypożyczalni samochodowej.

    Attributes:
        id_klient (int): Klucz główny, unikalny identyfikator klienta.
        imie (str): Imię klienta, wartość obowiązkowa.
        nazwisko (str): Nazwisko klienta, wartość obowiązkowa.
        telefon (str): Unikalny numer telefonu klienta, wartość obowiązkowa.

    Relationships:
        wypozyczenia (relationship): Relacja do tabeli 'Rental', reprezentująca wypożyczenia wykonane przez klienta.
        zamowienia (relationship): Relacja do tabeli 'Order', reprezentująca zamówienia klienta.
    :no-index:
    """
    __tablename__ = 'klienci'
    __table_args__ = (
    {'schema': 'wypozyczalnia'},
)

    id_klient = db.Column(db.Integer, primary_key = True)
    imie = db.Column(db.String(64), nullable=False)
    nazwisko = db.Column(db.String(64), nullable=False)
    telefon = db.Column(db.String(20), nullable=False, unique=True)
    wypozyczenia = db.relationship('Rental', back_populates='klient')
    zamowienia = db.relationship('Order', back_populates='klient')

    
class Job(db.Model):
    """
    Reprezentuje stanowisko pracy w systemie wypożyczalni.

    Attributes:
        id_rola (int): Klucz główny, unikalny identyfikator stanowiska.
        nazwa (str): Nazwa stanowiska (np. 'Kierownik', 'Konsultant').
        wyplata (Decimal): Wynagrodzenie przypisane do stanowiska, musi być większe od 0.
        czy_moze_wynajmowac (bool): Flaga wskazująca, czy osoba na tym stanowisku może wynajmować pojazdy.

    Relationships:
        stanowisko (relationship): Relacja do tabeli 'Employee', reprezentująca pracowników na tym stanowisku.
    :no-index:
    """
    __tablename__ = 'role'
    __table_args__ = (
        CheckConstraint('wyplata > 0', name='check_wyplata_positive'), 
        {'schema': 'wypozyczalnia'}  
    )
    id_rola = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(64), nullable=False)
    wyplata = db.Column(db.Numeric(10, 2), nullable=False)
    czy_moze_wynajmowac = db.Column(db.Boolean, nullable=False, default=False)
    stanowisko = db.relationship('Employee', back_populates = 'rola')

class Employee(db.Model):
    """
    Reprezentuje pracownika w systemie wypożyczalni.

    Attributes:
        id_pracownik (int): Klucz główny, unikalny identyfikator pracownika.
        imie (str): Imię pracownika.
        nazwisko (str): Nazwisko pracownika.
        telefon (str): Unikalny numer telefonu pracownika.
        id_rola (int): Klucz obcy do tabeli 'role', identyfikujący stanowisko pracownika.

    Relationships:
        rola (relationship): Relacja do tabeli 'Job', reprezentująca stanowisko pracownika.
        wypozyczenia (relationship): Relacja do tabeli 'Rental', reprezentująca wypożyczenia obsługiwane przez pracownika.
    :no-index:
    """
    __tablename__ = 'pracownicy'
    __table_args__ = (
    {'schema': 'wypozyczalnia'},
    )

    id_pracownik = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(64), nullable=False)
    nazwisko = db.Column(db.String(64), nullable=False)
    telefon = db.Column(db.String(20), nullable=False, unique=True)
    id_rola = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.role.id_rola'), nullable=False) 
    rola  = db.relationship('Job', back_populates="stanowisko")
    wypozyczenia = db.relationship('Rental', back_populates='pracownik')


class PriceList(db.Model):
    """
    Reprezentuje cennik wynajmu pojazdów.

    Attributes:
        id_cennik (int): Klucz główny, unikalny identyfikator cennika.
        id_klasa (int): Klucz obcy do tabeli 'klasa', identyfikujący klasę pojazdu.
        stawka_za_dzien (Decimal): Stawka dzienna za wynajem pojazdu danej klasy.

    Relationships:
        klasa_p (relationship): Relacja do tabeli 'CarClass', reprezentująca klasę pojazdu.
    :no-index:
    """
    __tablename__ = 'cennik'
    __table_args__ = (
    {'schema': 'wypozyczalnia'},
)

    id_cennik = db.Column(db.Integer, primary_key=True)
    id_klasa = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.klasa.id_klasa'), nullable=False)
    stawka_za_dzien = db.Column(db.Numeric(10, 2), nullable=False)
    klasa_p = db.relationship('CarClass', back_populates='cennik')

class Rental(db.Model):
    """
    Reprezentuje wypożyczenie w bazie danych.

    Attributes:
        id_wypozyczenia (int): Klucz główny, identyfikator wypożyczenia.
        data_wypozyczenia (date): Data rozpoczęcia wypożyczenia.
        data_oddania (date): Data zakończenia wypożyczenia.
        id_klient (int): Identyfikator klienta, klucz obcy do tabeli `klienci`.
        id_auto (int): Identyfikator auta, klucz obcy do tabeli `auta`.
        id_pracownik (int): Identyfikator pracownika, klucz obcy do tabeli `pracownicy`.
        klient (relationship): Relacja do tabeli `klienci`, określająca klienta.
        auto (relationship): Relacja do tabeli `auta`, określająca wypożyczone auto.
        pracownik (relationship): Relacja do tabeli `pracownicy`, określająca pracownika obsługującego wypożyczenie.
    :no-index:
    """
    __tablename__ = 'wypozyczenia'
    __table_args__ = (
        CheckConstraint('data_oddania > data_wypozyczenia', name='check_data_oddania'),
        {'schema': 'wypozyczalnia'},
    )

    id_wypozyczenia = db.Column(db.Integer, primary_key=True)
    data_wypozyczenia = db.Column(db.Date, nullable=False)
    data_oddania = db.Column(db.Date, nullable=False)
    
    id_klient = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.klienci.id_klient'), nullable=False)
    id_auto = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.auta.id_auto'), nullable=False)
    id_pracownik = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.pracownicy.id_pracownik'), nullable=False)
    
    klient = db.relationship('Client', back_populates='wypozyczenia')
    auto = db.relationship('Car', back_populates='wypozyczenia')
    pracownik = db.relationship('Employee', back_populates='wypozyczenia')
    platnosc = db.relationship('Payment', back_populates='wypozyczenia')


status_enum = ENUM('udane', 'nieudane', 'oczekujące', name='status_enum', schema='wypozyczalnia')

class Order(db.Model):
    """
    Reprezentuje zamówienie na wynajem samochodu w wypożyczalni.

    Attributes:
        id_zamowienia (int): Klucz główny, unikalny identyfikator zamówienia.
        id_klient (int): Klucz obcy odnoszący się do tabeli 'Client', określa klienta składającego zamówienie.
        id_model (int): Klucz obcy odnoszący się do tabeli 'Model', określa model pojazdu zamawianego przez klienta.
        data_rozpoczecia (date): Data rozpoczęcia zamówienia.
        data_zakonczenia (date): Data zakończenia zamówienia.
        status (str): Status zamówienia ('udane', 'nieudane', 'oczekujące').

    Relationships:
        klient (relationship): Relacja do tabeli 'Client', określająca klienta składającego zamówienie.
        model (relationship): Relacja do tabeli 'Model', określająca model zamawianego pojazdu.
    :no-index:
    """
    __tablename__ = 'zamowienia'
    __table_args__ = (
        CheckConstraint('data_zakonczenia > data_rozpoczecia', name='check_data_zakonczenia'),
        {'schema': 'wypozyczalnia'},
    )

    id_zamowienia = db.Column(db.Integer, primary_key=True)
    id_klient = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.klienci.id_klient'), nullable=False)
    id_model = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.modele.id_model'), nullable=False)
    data_rozpoczecia = db.Column(db.Date, nullable=False)
    data_zakonczenia = db.Column(db.Date, nullable=False)
    status = db.Column(status_enum, nullable=False, default='oczekujące')
    klient = db.relationship('Client', back_populates='zamowienia')
    model = db.relationship('Model', back_populates='zamowienia')

class CarDetails(db.Model):
    """
    Widok szczegółowy samochodów, używany do prezentacji danych.

    Attributes:
        id_auto (int): Klucz główny, identyfikator samochodu.
        nazwa_modelu (str): Nazwa modelu samochodu.
        nazwa_marki (str): Nazwa marki samochodu.
        numer_rejestracyjny (str): Numer rejestracyjny samochodu.
        id_klasa (int): Identyfikator klasy pojazdu.
        nazwa_klasy (str): Nazwa klasy pojazdu.
    :no-index:
    """
    __tablename__ = 'szczegoly_aut'
    __table_args__ = (
        {'schema': 'wypozyczalnia'}, 
    )

    id_auto = db.Column(db.Integer, primary_key=True)
    nazwa_modelu = db.Column(db.String(64))
    nazwa_marki = db.Column(db.String(64))
    numer_rejestracyjny = db.Column(db.String(50))
    id_klasa = db.Column(db.Integer)
    nazwa_klasy = db.Column(db.String(32)) 

class RentalDetails(db.Model):
    """
    Widok szczegółowy wypożyczeń, używany do prezentacji danych.

    Attributes:
        id_wypozyczenia (int): Klucz główny, identyfikator wypożyczenia.
        id_klient (int): Identyfikator klienta.
        klient (str): Imię i nazwisko klienta.
        id_auto (int): Identyfikator samochodu.
        nazwa_marki (str): Marka wypożyczonego samochodu.
        nazwa_modelu (str): Model wypożyczonego samochodu.
        numer_rejestracyjny (str): Numer rejestracyjny samochodu.
        data_wypozyczenia (date): Data rozpoczęcia wypożyczenia.
        data_oddania (date): Data zakończenia wypożyczenia.
        id_pracownik (int): Identyfikator pracownika realizującego wypożyczenie.
        pracownik (str): Imię i nazwisko pracownika.
    :no-index:
    """
    __tablename__ = 'szczegoly_wypozyczenia'
    __table_args__ = {'schema': 'wypozyczalnia'}
    
    id_wypozyczenia = db.Column(db.Integer, primary_key=True)
    id_klient = db.Column(db.Integer)
    klient = db.Column(db.String(128))
    id_auto = db.Column(db.Integer)
    nazwa_marki = db.Column(db.String(64))
    nazwa_modelu = db.Column(db.String(64))
    numer_rejestracyjny = db.Column(db.String(50))
    data_wypozyczenia = db.Column(db.Date)
    data_oddania = db.Column(db.Date)
    id_pracownik = db.Column(db.Integer)
    pracownik = db.Column(db.String(128))

class Payment(db.Model):
    """
    Model tabeli 'platnosci', reprezentujący dane dotyczące płatności w systemie wypożyczalni.

    Attributes:
        id_platnosc (int): Klucz główny, identyfikator płatności.
        id_wypozyczenia (int): Identyfikator powiązanego wypożyczenia.
        kwota (decimal): Kwota płatności za dane wypożyczenie.
        wypozyczenia (Rental): Relacja do modelu 'Rental', reprezentująca powiązanie płatności z wypożyczeniem.
    :no-index:
    """
    __tablename__ = 'platnosci'
    __table_args__ = {'schema': 'wypozyczalnia'}

    id_platnosc = db.Column(db.Integer, primary_key=True)
    id_wypozyczenia = db.Column(db.Integer, db.ForeignKey('wypozyczalnia.wypozyczenia.id_wypozyczenia'),nullable=False)
    kwota = db.Column(db.Numeric(10,2), nullable=False)
    wypozyczenia = db.relationship('Rental', back_populates='platnosc')

context_data = {
    "cars": {'data': [Model, Brand]},
    "models": { 'data' : [Brand, CarClass]},
    "brands" : { 'data' : []},
    "classes" : { 'data' : []},
    "clients" : { 'data' : []},
    'jobs' : {'data' : []},
    'workers' : {'data' : [Job]},
    'pricelist' : {'data' : []},
    'rentals' : {'data' : [Client, Model, Brand]},
    'rentals_cost' : {},
    'payments' : {'data' : []}
}

labels = {
    'cars' : ['ID', 'Model', 'Marka', 'Numer rejestracyjny', 'Klasa'],
    'models' : ['ID', 'Marka', 'Model'],
    'brands' : ['ID', 'Marka'],
    'classes' : ['ID', 'Klasa', 'Opis'],
    'clients' : ['ID', 'Imie', 'Nazwisko', 'Telefon'],
    'jobs' : ['ID', 'Nazwa stanowiska', 'Wypłata', "Może wynajmować auta"],
    'workers' : ['ID', 'Imie', 'Nazwisko', 'Telefon', 'Stanowisko'],
    'pricelist' : ['ID', "Klasa", "Stawka za dzień"],
    'rentals' : ['ID', 'Klient', 'Numer rejestracyjny', 'Marka', 'Model', 'Początek', 'Koniec', 'Pracownik wynajmujący'],
    'orders' : ['ID' , 'Klient', 'Model', 'Początek', 'Koniec', 'Status'],
    'payments' : ['ID', 'ID wypozyczenia', 'Kwota']
}
  
@app.route('/')
def home():
    """
    Główna strona aplikacji.

    Returns:
        str: Renderowany szablon HTML dla strony głównej.
    """
    return render_template('index.html')

@app.template_filter('getattr')
def getattr_filter(obj, attr):
    """
    Filtr Flask używany do dynamicznego dostępu do atrybutów obiektów w szablonach.

    Args:
        obj (object): Obiekt, z którego atrybut ma być pobrany.
        attr (str): Nazwa atrybutu.

    Returns:
        any: Wartość atrybutu lub None, jeśli atrybut nie istnieje.
    """
    return getattr(obj, attr, None)

@app.route('/models')
def models():
    """
    Widok listy modeli pojazdów.

    Zwraca dane o modelach, w tym ich ID, nazwę modelu oraz markę, z połączeniem relacyjnym do tabeli 'Brand'.

    Returns:
        str: Renderowany szablon HTML z listą modeli pojazdów.
    """
    data = Model.query.with_entities(Model.id_model, Model.nazwa_modelu).all()
    data = db.session.query(Model.id_model, Brand.nazwa_marki, Model.nazwa_modelu).join(Brand, Model.id_marka == Brand.id_marka).all()
    return render_template('models.html', title="Modele", labels=labels['models'], data=data, context="models")

@app.route('/cars')
def car_details():
    """
    Widok szczegółów samochodów.

    Pobiera dane o samochodach, w tym ich ID, model, markę, numer rejestracyjny oraz klasę.

    Returns:
        str: Renderowany szablon HTML z listą szczegółów samochodów.
    """
    data = CarDetails.query.with_entities(CarDetails.id_auto, CarDetails.nazwa_modelu, CarDetails.nazwa_marki, CarDetails.numer_rejestracyjny,
                                        CarDetails.nazwa_klasy).all()
    return render_template('cars.html', title="Auta", labels=labels['cars'], data=data, context="cars")

@app.route('/brands')
def brand_details():
    """
    Widok listy marek.

    Pobiera dane o markach, w tym ich ID i nazwę.

    Returns:
        str: Renderowany szablon HTML z listą marek.
    """
    data = Brand.query.with_entities(Brand.id_marka, Brand.nazwa_marki).all()
    return render_template('brands.html', title="Marki", labels=labels['brands'], data=data, context="brands")

@app.route('/classes')
def classes_details():
    """
    Widok listy klas pojazdów.

    Pobiera dane o klasach, w tym ich ID, nazwę i opis.

    Returns:
        str: Renderowany szablon HTML z listą klas pojazdów.
    """
    data = CarClass.query.with_entities(CarClass.id_klasa, CarClass.nazwa, CarClass.opis).all()
    return render_template('classes.html', title="Klasy aut", labels=labels['classes'], data=data, context="classes")

@app.route('/clients')
def clients_details():
    """
    Widok listy klientów.

    Pobiera dane o klientach, w tym ich ID, imię, nazwisko i numer telefonu.

    Returns:
        str: Renderowany szablon HTML z listą klientów.
    """
    data = Client.query.with_entities(Client.id_klient, Client.imie, Client.nazwisko, Client.telefon).all()
    return render_template('clients.html', title="Klienci", labels=labels['clients'], data=data, context="clients")

@app.route('/jobs')
def jobs_details():
    """
    Widok listy stanowisk pracy.

    Pobiera dane o stanowiskach, w tym ich ID, nazwę, wypłatę i informację, czy mogą wynajmować auta.

    Returns:
        str: Renderowany szablon HTML z listą stanowisk pracy.
    """
    data = Job.query.with_entities(Job.id_rola, Job.nazwa, Job.wyplata, Job.czy_moze_wynajmowac).all()
    data = [(id_rola, nazwa, wyplata, "Tak" if czy_moze_wynajmowac else "Nie") for id_rola, nazwa, wyplata, czy_moze_wynajmowac in data]
    return render_template('jobs.html', title="Stanowiska", labels=labels['jobs'], data=data, context="jobs")

@app.route('/workers')
def workers_details():
    print("ELO")
    """
    Widok listy pracowników.

    Pobiera dane o pracownikach, w tym ich ID, imię, nazwisko, telefon i nazwę stanowiska.

    Returns:
        str: Renderowany szablon HTML z listą pracowników.
    """
    data = db.session.query(Employee.id_pracownik, Employee.imie, Employee.nazwisko, Employee.telefon, Job.nazwa.label('stanowisko')).join(Job, Employee.id_rola == Job.id_rola).all()
    return render_template('workers.html', title="Pracownicy", labels=labels['workers'], data=data, context="workers")

@app.route('/rentals')
def rentals_details():
    """
    Widok szczegółów wypożyczeń.

    Pobiera dane o wypożyczeniach, w tym ID, klienta, numer rejestracyjny pojazdu, markę, model, daty wynajmu i pracownika.

    Returns:
        str: Renderowany szablon HTML z listą wypożyczeń.
    """
    data = RentalDetails.query.with_entities(RentalDetails.id_wypozyczenia , RentalDetails.klient, RentalDetails.numer_rejestracyjny,
                            RentalDetails.nazwa_marki, RentalDetails.nazwa_modelu, RentalDetails.data_wypozyczenia, RentalDetails.data_oddania, RentalDetails.pracownik).all()
    return render_template('rentals.html', title="Wypożyczenia", labels=labels['rentals'], data=data, context="rentals")

@app.route('/orders')
def orders_details():
    """
    Widok listy zamówień.

    Pobiera dane o zamówieniach, w tym ich ID, klienta, model pojazdu, daty i status zamówienia.

    Returns:
        str: Renderowany szablon HTML z listą zamówień.
    """
    data = (
        db.session.query(Order.id_zamowienia, func.concat(Client.imie, ' ', Client.nazwisko), Model.nazwa_modelu, Order.data_rozpoczecia,
        Order.data_zakonczenia,Order.status).join(Client, Order.id_klient == Client.id_klient).join(Model, Order.id_model == Model.id_model))
    return render_template('orders.html',title="Zamówienia",labels=labels['orders'], data=data, context="orders")


@app.route('/pricelist')
def price_list():
    """
    Widok cennika.

    Pobiera dane o cenniku, w tym ID, klasę pojazdu i stawkę dzienną za wynajem.

    Returns:
        str: Renderowany szablon HTML z listą cenników.
    """
    data = db.session.query(PriceList.id_cennik, CarClass.nazwa, PriceList.stawka_za_dzien).join(PriceList, PriceList.id_klasa == CarClass.id_klasa).all()
    return render_template('pricelist.html', title="Cennik", labels=labels['pricelist'], data=data, context="pricelist")

@app.route('/payments', methods= ['GET', 'POST'])
def payment_details():
    """
    Widok szczegółów płatności.

    Pobiera dane o płatnościach, w tym ID płatności, ID wypożyczenia oraz kwotę.

    Returns:
        str: Renderowany szablon HTML z listą płatności.
    """
    data = db.session.query(Payment.id_platnosc, Payment.id_wypozyczenia, Payment.kwota).all()
    return render_template('payments.html', title="Płatności", labels=labels['payments'], data = data, context="payments")

@app.route('/incomes', methods =['GET', 'POST'])
def income():
    """
    Widok przychodów.

    Wyświetla dane dotyczące całkowitych i średnich przychodów.

    Returns:
        str: Renderowany szablon HTML z podsumowaniem przychodów.
    """
    return render_template('incomes.html', title="Przychody", context="incomes")


@app.route('/data', methods=['GET', 'POST'])
def data_view():
    """
    Widok dynamicznych danych kontekstowych.

    Pozwala na przeglądanie i dodawanie danych w zależności od wybranego kontekstu.

    Args:
        context (str): Nazwa kontekstu danych, domyślnie ustawiona na 'index'.

    Returns:
        str: Renderowany szablon HTML odpowiadający wybranemu kontekstowi.
    """
    context = request.form.get('context') or request.args.get('context', 'index')
    data = [elem.query.all() for elem in context_data[context]['data']]
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
                return render_template(
                f'{context}.html', 
                title="Dodawanie", 
                mode="add", 
                context=context, 
                data_set=data)
    return render_template(f'{context}.html', title="Dane", mode=None, context=context)

@app.route('/get_models/<int:brand_id>', methods=['GET'])
def get_brands(brand_id):
    """
    Pobiera listę modeli dla określonej marki.

    Args:
        brand_id (int): ID marki, dla której mają być pobrane modele.

    Returns:
        Response: JSON z listą modeli zawierającą 'id_model' i 'nazwa_model'.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wypozyczalnia.wyszukaj_modele(%s)", (brand_id,))
    rows = cursor.fetchall()
    model_list = [{'id_model': row[0], 'nazwa_model': row[1]} for row in rows]
    cursor.close()
    return jsonify(model_list)

@app.route('/incomes/all')
def get_raport():
    """
    Wyświetla raport finansowy.

    Pobiera dane o całkowitych i średnich przychodach oraz przychodach na klasy aut.

    Returns:
        str: Renderowany szablon HTML z raportem finansowym.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wypozyczalnia.raport_finansowy;")
    report = [cursor.fetchone()]

    query = "SELECT * FROM wypozyczalnia.przychody_na_klasy_aut();"
    cursor.execute(query)
    class_report = cursor.fetchall()
    cursor.close()
    
    cursor.close()
    return render_template('incomes.html', title = "Podsumowanie finansowe", labels=['Klasa', 'Liczba wypożyczeń', 'Całkowity przychód'],labels2=['Całkowity przychód' , 'Średni przychód'], data=class_report, report=report)
    
@app.route('/available_cars')
def available_cars():
    """
    Wyświetla widok dla wyszukiwania dostępnych aut.

    Returns:
        str: Renderowany szablon HTML dla wyszukiwania dostępnych samochodów.
    """  
    return render_template('available_cars.html', title = "Dostępność aut")

@app.route('/popular_cars')
def popular_cars():
    """
    Wyświetla widok dla wyszukiwania najpopularniejszych modeli.

    Returns:
        str: Renderowany szablon HTML dla wyszukiwania najpopularniejszych modeli samochodów.
    """  
    return render_template('popular_cars.html', title = "Wyszukaj najpopularniejsze modele")



@app.route("/available_cars/search", methods=['GET', 'POST'])
def available_cars_search():
    """
    Przeszukuje dostępne samochody w podanym przedziale czasowym.

    Args:
        data_rozpoczecia (str): Data rozpoczęcia wynajmu.
        data_zakonczenia (str): Data zakończenia wynajmu.

    Returns:
        str: Renderowany szablon HTML z wynikami wyszukiwania, liczbą dostępnych aut, modeli i marek.
    """
    data_rozpoczecia = request.form.get("search_start_date")
    data_zakonczenia = request.form.get("search_end_date")
    cursor = conn.cursor()

    query_cars = "SELECT * FROM wypozyczalnia.dostepne_auta_w_danym_terminie(%s, %s);"
    cursor.execute(query_cars, (data_rozpoczecia, data_zakonczenia))
    cars = cursor.fetchall()
    labels = ["ID", "Model", "Marka", "Numer rejestracyjny", "Klasa"]

    query_amount = "SELECT * FROM wypozyczalnia.policz_auta_dostepne_w_danym_terminie(%s, %s);"
    cursor.execute(query_amount, (data_rozpoczecia, data_zakonczenia))
    amount = cursor.fetchone()

    query_models_amount = "SELECT * FROM wypozyczalnia.policz_modele_auta_dostepne_w_danym_terminie(%s, %s);"
    cursor.execute(query_models_amount, (data_rozpoczecia, data_zakonczenia))
    models_amount = cursor.fetchall()
    labels2 = ['Marka', 'Ilość']

    query_brands_amount = "SELECT * FROM wypozyczalnia.policz_marki_auta_dostepne_w_danym_terminie(%s, %s);"
    cursor.execute(query_brands_amount, (data_rozpoczecia, data_zakonczenia))
    brands_amount = cursor.fetchall()
    labels3 = ['Marka', 'Model', 'Ilość']

    return render_template('available_cars.html', title = "Dostępność aut", labels=labels, data=cars, amount=amount, models=models_amount, labels2=labels2, brands=brands_amount, labels3=labels3)

@app.route("/popular_cars/search", methods=['GET', 'POST'])
def popular_cars_search():
    """
    Wyszukuje najpopularniejsze modele samochodów.

    Args:
        rental_amount (int): Minimalna liczba wypożyczeń modelu, aby został uwzględniony w wynikach.

    Returns:
        str: Renderowany szablon HTML z listą najpopularniejszych modeli samochodów.
    """
    rental_amount = request.form.get("rental_amount")
    cursor = conn.cursor()
    query = "SELECT * FROM wypozyczalnia.najpopularniejsze_modele(%s);"
    cursor.execute(query, rental_amount)
    cars = cursor.fetchall()

    return render_template('popular_cars.html', title = "Dostępność aut", labels=['Model', 'Marka', 'Liczba wypożyczeń'], data=cars)
     


@app.route('/cars/add', methods=['POST'])
def add_car():
    """
    Dodaje nowy samochód do bazy danych.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę z listą samochodów z odpowiednim komunikatem.
    """
    numer_rejestracyjny = request.form.get('registration')
    rok = request.form.get('rok')
    id_model = request.form.get('model_id')

    if not numer_rejestracyjny or not rok or not id_model:
        flash("Błąd: Wprowadź wszystkie wymagane dane", "error")
        return redirect('/cars')
    try:
        new_car = Car(
            numer_rejestracyjny=numer_rejestracyjny.strip(),
            rok=int(rok),
            id_model=int(id_model),
        )
        db.session.add(new_car)
        db.session.commit()
        flash("Samochód został pomyślnie dodany!", "success")
        return redirect('/cars')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if "Niepoprawny numer rejestracyjny" in error_message:
            flash("Podano niepoprawny numer rejestracyjny. Poprawny format to [TRZY_LITERY][TRZY_CYFRY][2-5_ZNAKÓW_LUB_SPACJI]", "error")
        elif "duplicate key value violates unique constraint" in error_message:
            flash(f"Numer rejestracyjny '{numer_rejestracyjny}' już istnieje w bazie danych. Proszę podać unikalny numer.", "error")
        else:
            display_error(error_message)
        return redirect('/cars')
    

@app.route('/models/add', methods=['POST'])
def add_model():
    """
    Dodaje nowy model samochodu do bazy danych.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę z listą modeli z odpowiednim komunikatem.
    """
    nazwa_modelu = request.form.get('models_model_name')
    id_marka = request.form.get('model_brand_id')
    id_klasa = request.form.get('class_id')

    try:
        new_model = Model(
            nazwa_modelu=nazwa_modelu.strip(),
            id_marka=int(id_marka),
            id_klasa=int(id_klasa),
        )
        db.session.add(new_model)
        db.session.commit()
        flash("Model został pomyślnie dodany!", "success")
        return redirect('/models')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if "Niepoprawny numer rejestracyjny" in error_message:
            flash("Podano niepoprawny numer rejestracyjny. Poprawny format to [TRZY_LITERY][TRZY_CYFRY][2-5_ZNAKÓW_LUB_SPACJI]", "error")
        else:
            display_error(error_message=error_message)
        return redirect('/models')
    

@app.route('/brands/add', methods=['POST'])
def add_brand():
    """
    Dodaje nową markę do bazy danych.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę z listą marek z odpowiednim komunikatem.
    """
    nazwa_marki = request.form.get('brands_brand_name')
    try:
        new_brand = Brand(
            nazwa_marki=nazwa_marki
        )
        db.session.add(new_brand)
        db.session.commit()
        flash(f"Marka {nazwa_marki} została pomyślnie dodana!", "success")
        return redirect('/brands')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if "duplicate key value violates unique constraint" in error_message:
            flash(f"Marka {nazwa_marki} istnieje już w bazie. Proszę podać unikalną nazwę.", "error")
        else:
            display_error(error_message=error_message)
        return redirect('/brands')
    
@app.route('/classes/add', methods=['POST'])
def add_class():
    """
    Dodaje nową klasę samochodów do bazy danych.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę listy klas z komunikatem sukcesu lub błędu.
    """
    
    nazwa_klasy = request.form.get('classes_class_name')
    opis = request.form.get('description')

    try:
        new_class= CarClass(
            nazwa=nazwa_klasy,
            opis = opis
        )
        db.session.add(new_class)
        db.session.commit()
        flash(f"Klasa {nazwa_klasy} została pomyślnie dodana!", "success")
        return redirect('/classes')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if "duplicate key value violates unique constraint" in error_message:
            flash(f"Klasa {nazwa_klasy} istnieje już w bazie. Proszę podać unikalną nazwę.", "error")
        else:
            display_error(error_message=error_message)
        return redirect('/classes')
    
@app.route('/clients/add', methods=['POST'])
def add_client():
    """
    Dodaje nowego klienta do bazy danych.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę z listą klientów z odpowiednim komunikatem.
    """
    imie = request.form.get('clients_name')
    nazwisko = request.form.get('clients_surname')
    telefon = request.form.get('clients_phone')

    try:
        new_client= Client(
            imie = imie,
            nazwisko = nazwisko,
            telefon = telefon
        )
        db.session.add(new_client)
        db.session.commit()
        flash(f"Klient/ka {imie} {nazwisko} został/a pomyślnie dodany/a!", "success")
        return redirect('/clients')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if "duplicate key value violates unique constraint" in error_message:
            flash(f"Numer {telefon} istnieje już w bazie. Proszę podać unikalny numer telefonu.", "error")
        elif 'Niepoprawny numer telefonu' in error_message:
            flash(f"Podano niepoprawny numer {telefon}. Poprawny format to [9 CYFR].", "error")
        else:
            display_error(error_message=error_message)
        return redirect('/clients')
    

    
@app.route('/jobs/add', methods=['POST'])
def add_job():
    """
    Dodaje nowe stanowisko do bazy danych.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę z listą stanowisk z odpowiednim komunikatem.
    """
    stanowisko = request.form.get('role_name')
    wyplata = request.form.get('role_salary')
    czy_moze_wynajmowac = True if request.form.get('can_rent_id') == "True" else False

    try:
        new_job = Job(
            nazwa = stanowisko,
            wyplata = wyplata,
            czy_moze_wynajmowac = czy_moze_wynajmowac
        )
        db.session.add(new_job)
        db.session.commit()
        flash(f"Stanowisko {stanowisko} zostało pomyślnie dodane", "success")
        return redirect('/jobs')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if "duplicate key value violates unique constraint" in error_message:
            flash(f"Stanowisko {stanowisko} istnieje już w bazie. Proszę podać unikalną nazwę.", "error")
        elif 'check constraint' in error_message:
            flash(f"Wypłata {wyplata} musi byc wieksza od zera.", "error")
        else:
            display_error(error_message=error_message)
        return redirect('/jobs')
    
@app.route('/workers/add', methods=['POST'])
def add_employee():
    """
    Dodaje nowego pracownika do bazy danych.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę z listą pracowników z odpowiednim komunikatem.
    """
    imie = request.form.get('workers_name')
    nazwisko = request.form.get('workers_surname')
    telefon = request.form.get('workers_phone')
    id_rola = request.form.get('role_id')

    try:
        new_job = Employee(
            imie = imie,
            nazwisko = nazwisko,
            telefon = telefon,
            id_rola = id_rola
        )
        db.session.add(new_job)
        db.session.commit()
        flash(f"Pracownik {imie} {nazwisko} został/a pomyślnie dodany/a", "success")
        return redirect('/workers')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if "duplicate key value violates unique constraint" in error_message:
            flash(f"Pracownik {imie} {nazwisko} o numerze {telefon} istnieje już w bazie.", "error")
        elif 'Niepoprawny numer telefonu' in error_message:
            flash(f"Podano niepoprawny numer {telefon}. Poprawny format to [9 CYFR].", "error")
        else:
            display_error(error_message=error_message)
        return redirect('/workers')
    

@app.route('/rentals/add', methods=['POST'])
def add_rental():
    """
    Dodaje nowe zamówienie na wynajem pojazdu.

    Dane pobierane są z formularza HTTP POST.

    Returns:
        Response: Przekierowanie na stronę z listą wypożyczeń z odpowiednim komunikatem.
    """
    id_klient = request.form.get('client_id')
    id_model = request.form.get('rental_model_id')
    start = request.form.get('start_rental_date')
    koniec = request.form.get('end_rental_date')
    try:
        new_order = Order(
            id_klient = int(id_klient),
            id_model = int(id_model),
            data_rozpoczecia = start,
            data_zakonczenia = koniec,
        )
        db.session.add(new_order)
        db.session.commit()
        if new_order.status == 'nieudane':
            flash(f"Brak dostępnych aut w podanym terminie. Spróbuj inny model lub zmień termin zamówienia.", "error")
        else:
            flash(f"Zamówienie zostało pomyślnie dodane", "success")
        return redirect('/rentals')

    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        if 'check constraint' in error_message:
            flash(f"Wygląda na to, że próbujesz zakończyć wypożyczenie, zanim się zacznie. Proszę wprowadzić poprawne daty.", "error")
        else:
            display_error(error_message=error_message)
        return redirect('/rentals')

def delete_record(model, record_id, identifier_field):
    """
    Usuwa rekord z podanej tabeli na podstawie identyfikatora.

    Args:
        model (db.Model): Model bazy danych, z którego ma zostać usunięty rekord.
        record_id (int): ID rekordu, który ma zostać usunięty.
        identifier_field (str): Nazwa pola identyfikatora w tabeli.

    Returns:
        bool: True, jeśli usunięcie zakończyło się sukcesem; False w przypadku błędu.
    """
    try:
        record = db.session.query(model).filter(getattr(model, identifier_field) == record_id).first()     
        if not record:
            return False
        db.session.delete(record)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        error_message = getattr(e, 'pgerror', str(e))
        flash(f"Wystąpił nieoczekiwany błąd: {error_message}", "error")
        return False
    

@app.route('/cars/delete/<int:id>', methods=['POST'])
def delete_car(id):
    """
    Usuwa rekord samochodu z tabeli `auta`.

    Args:
        id (int): ID samochodu do usunięcia.

    Returns:
        Response: Przekierowanie na listę samochodów z odpowiednim komunikatem.
    """
    if delete_record(Car, id, 'id_auto'):
        flash(f"Auto {id} zostało pomyślnie usunięte.", "success")  
    return redirect('/cars')

@app.route('/models/delete/<int:id>', methods=['POST'])
def delete_model(id):
    """
    Usuwa rekord modelu z tabeli `modele`.

    Args:
        id (int): ID modelu do usunięcia.

    Returns:
        Response: Przekierowanie na listę modeli z odpowiednim komunikatem.
    """
    if delete_record(Model, id, 'id_model'):
        flash(f"Model {id} został pomyślnie usunięty.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/models')

@app.route('/brands/delete/<int:id>', methods=['POST'])
def delete_brand(id):
    """
    Usuwa rekord marki z tabeli `marki`.

    Args:
        id (int): ID marki do usunięcia.

    Returns:
        Response: Przekierowanie na listę marek z odpowiednim komunikatem.
    """
    if delete_record(Brand, id, 'id_marka'):
        flash(f"Marka {id} została pomyślnie usunięta.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/brands')

@app.route('/classes/delete/<int:id>', methods=['POST'])
def delete_class(id):
    """
    Usuwa rekord klasy pojazdu z tabeli `klasa`.

    Args:
        id (int): ID klasy do usunięcia.

    Returns:
        Response: Przekierowanie na listę klas z odpowiednim komunikatem.
    """
    if delete_record(CarClass, id, 'id_klasa'):
        flash(f"Klasa {id} została pomyślnie usunięta.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/classes')

@app.route('/clients/delete/<int:id>', methods=['POST'])
def delete_client(id):
    """
    Usuwa rekord klienta z tabeli `klienci`.

    Args:
        id (int): ID klienta do usunięcia.

    Returns:
        Response: Przekierowanie na listę klientów z odpowiednim komunikatem.
    """
    if delete_record(Client, id, 'id_klient'):
        flash(f"Klient {id} został pomyślnie usunięty.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/clients')

@app.route('/jobs/delete/<int:id>', methods=['POST'])
def delete_job(id):
    """
    Usuwa rekord stanowiska z tabeli `role`.

    Args:
        id (int): ID stanowiska do usunięcia.

    Returns:
        Response: Przekierowanie na listę stanowisk z odpowiednim komunikatem.
    """
    if delete_record(Job, id, 'id_rola'):
        flash(f"Stanowisko {id} zostało pomyślnie usunięte.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/jobs')

@app.route('/workers/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    """
    Usuwa rekord pracownika z tabeli `pracownicy`.

    Args:
        id (int): ID pracownika do usunięcia.

    Returns:
        Response: Przekierowanie na listę pracowników z odpowiednim komunikatem.
    """
    if delete_record(Employee, id, 'id_pracownik'):
        flash(f"Pracownik {id} został pomyślnie usunięty.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/workers')

@app.route('/pricelist/delete/<int:id>', methods=['POST'])
def delete_pricelist(id):
    """
    Usuwa rekord z tabeli `cennik`.

    Args:
        id (int): ID rekordu do usunięcia.

    Returns:
        Response: Przekierowanie na listę cenników z odpowiednim komunikatem.
    """
    if delete_record(PriceList, id, 'id_cennik'):
        flash(f"Rekord {id} został pomyślnie usunięty.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/pricelist')

@app.route('/orders/delete/<int:id>', methods=['POST'])
def delete_order(id):
    """
    Usuwa rekord zamówienia z tabeli `zamowienia`.

    Args:
        id (int): ID zamówienia do usunięcia.

    Returns:
        Response: Przekierowanie na listę zamówień z odpowiednim komunikatem.
    """
    if delete_record(Order, id, 'id_zamowienia'):
        flash(f"Wypożyczenie {id} zostało pomyślnie usunięte.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/orders')

@app.route('/rentals/delete/<int:id>', methods=['POST'])
def delete_rental(id):
    """
    Usuwa rekord wypożyczenia z tabeli `wypozyczenia`.

    Args:
        id (int): ID wypożyczenia do usunięcia.

    Returns:
        Response: Przekierowanie na listę wypożyczeń z odpowiednim komunikatem.
    """
    if delete_record(Rental, id, 'id_wypozyczenia'):
        flash(f"Zamówienie {id} zostało pomyślnie usunięte.", "success")
    else:
        flash(f"Wystąpił nieoczekiwany błąd podczas usuwania rekordu", "error")   
    return redirect('/rentals')

def display_error(error_message):
    """
    Obsługuje błędy bazy danych, wyświetlając odpowiednie komunikaty użytkownikowi.

    Args:
        error_message (str): Treść błędu.

    Returns:
        None: Wyświetla komunikaty za pomocą `flash`.
    """

    if "null value in column" in error_message:
        flash(f'Wystąpił bląd po stronie bazy {error_message}', "error")
    elif "value too long for type character varying" in error_message:
        flash("Błąd: Wartość przekracza maksymalną liczbę znaków.", "error")
    elif "invalid input syntax" in error_message:
        flash("Nieprawidłowy typ danych wstawiony do kolumny.", "error")
    elif "invalid literal for int()" in error_message:
        flash("Błąd: Podano nieprawidłowe dane. Oczekiwano liczby całkowitej.", "error")
    else:
        flash(f'Wystąpił bląd po stronie bazy {error_message}', "error")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))