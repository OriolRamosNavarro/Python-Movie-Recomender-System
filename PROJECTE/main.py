import os, time, logging, pickle
import numpy as np
import math, reprlib
from dataclasses import dataclass, field

## Importem 'Content_items()'
from Setup_Datasets.content_items import Content_Items

## Importem 'Ratings()'
from Setup_Datasets.ratings import Ratings

## Importem 'User()'
from user import User

## Importem 'Rec_Simple()'
from Procediments.rec_simple import Rec_simple

## Importem 'Rec_Colaborativa()'
from Procediments.rec_colaboratiu import Rec_colaborativa

## Importem 'Rec_Contingut()'
from Procediments.rec_contingut import Rec_contingut

## Importem 'Argparse_Options'
import argparse_options

## Importem 'Pickle_Utils'
import pickle_utils


def start_time() -> time.time:
    """
    Inicia el temporitzador per mesurar el temps d'execució.

    Parameters
    ----------
    None
    
    Return
    ------
    time.time
        La marca de temps actual en segons des de l'època (01/01/1970 00:00:00 UTC).
    """
    return time.time()
    
def stop_time(temps_inicial: time.time, classe: str) -> None:
    """
    Detura el temporitzador i registra el temps d'execució d'una classe específica.

    Parameters
    ----------
    temps_inicial : time.time
        La marca de temps inicial obtinguda de la funció `start_time`.
    
    classe : str
        El nom de la classe per a la qual es va iniciar el temporitzador.

    Return
    ------
    None
    """
    temps_final = time.time()
    logging.info(f"S'ha completat la execucció de {classe} en {round((temps_final - temps_inicial),5)} segons.")

def set_content_items(fitxer: str, pickle_file: str) -> None:
    """
    Carrega o crea el fitxer de contingut en format pickle.

    Parameters
    ----------
    fitxer : str
        El nom del fitxer de text que conté les dades.
    pickle_file : str
        El nom del fitxer pickle on es desaran o es carregaran les dades.

    Return
    ------
    None
    """
    ti = start_time()
    if os.path.exists(pickle_file):
        pickle_utils.load_content_items(pickle_file)
    else:
        pickle_utils.create_content_items(pickle_file, fitxer)
    stop_time(ti, 'Content_Items')
    
def set_ratings(fitxer: str, pickle_file: str) -> None:
    """
    Carrega o crea el fitxer de valoracions en format pickle.

    Parameters
    ----------
    fitxer : str
        El nom del fitxer de text que conté les dades de valoració.
    pickle_file : str
        El nom del fitxer pickle on es desaran o es carregaran les dades.

    Return
    ------
    None
    """
    ti = start_time()
    if os.path.exists(pickle_file):
        pickle_utils.load_ratings(pickle_file)
    else:
        pickle_utils.create_ratings(pickle_file, fitxer)
    stop_time(ti, 'Ratings')

def set_rec_simple() -> float:
    """
    Executa el sistema de recomanació simple.

    Parameters
    ----------
    None

    Return
    ------
    float
        Es retornen dos floats corresponents al mae i rmse.
    """
    usuari = set_parametres('usuari')
    min_vots = set_parametres('min_vots')

    ti = start_time()
    ## Guardem el usuari a User()
    User.set_user(usuari)

    rs = Rec_simple()
    rs.__main__(min_vots)
    stop_time(ti, 'Recomanacio Simple')
    rs.get_nom_items()
    return rs.calcular_metriques()

def set_rec_colab(pickle_file: str) -> float:
    """
    Executa el sistema de recomanació col·laboratiu.

    Parameters
    ----------
    pickle_file : str
        El nom del fitxer pickle on es troba la matriu de valoracions.

    Return
    ------
    float
        Es retornen dos floats corresponents al mae i rmse.
    """
    usuari = set_parametres('Usuari')
    k = set_parametres("valor de 'k'")

    if os.path.exists(pickle_file):
        rc = pickle_utils.load_matriu_valoracions(pickle_file)
    else:
        rc = pickle_utils.create_matriu_valoracions(pickle_file)

    User.set_user(usuari)
    ti = start_time()
    rc.__main__(k)
    stop_time(ti, 'Recomanacio Colaborativa')
    rc.get_nom_items()
    return rc.calcular_metriques()

def set_rec_contingut() -> float:
    """
    Executa el sistema de recomanació basat en contingut.

    Parameters
    ----------
    None
    
    Return
    ------
    float
        Es retornen dos floats corresponents al mae i rmse.
    """
    usuari = set_parametres('Usuari')

    User.set_user(usuari)

    ti = start_time()
    rco = Rec_contingut()
    rco.__main__()
    stop_time(ti, 'Recomanacio Colaborativa')
    rco.get_nom_items()
    return rco.calcular_metriques()

def set_parametres(parametres: str) -> int:
    """
    Solicita i valida un paràmetre inserit per l'usuari.

    Parameters
    ----------
    parametres: str
        El nom del paràmetre a sol·licitar.

    Return
    ------
    int
        El valor del paràmetre introduït per l'usuari.
    """
    valid = False
    while valid != True:
        os.system('cls')
        try:
            valor = int(input(f"Inserti el {parametres} a utilitzar (int): "))
            print(f"S'utilitzar el {parametres}: {valor}.")
            confirmat = str(input("Esteu segurs d'aquesta acció? (s/N): "))
            if confirmat.lower() == 's':
                valid = True
            else:
                print(f"S'ha cancelat l'operacio.")
                time.sleep(1)
        except ValueError:
            print(f"El parametre {parametres} indicat NO és un número.")
            time.sleep(2)
        except Exception as e:
            print(f'Ha saltat un error inesperat: {str(e)}')
            time.sleep(2)
    return valor

def set_accio() -> int:
    """
    Solicita i valida l'acció que desitja realitzar l'usuari.

    Parameters
    ----------
    None

    Return
    ------
    int
        El número d'acció seleccionada per l'usuari.
    """
    valid = False
    while valid != True:
        os.system('cls')
        try:
            accions_valides = [1, 2, 3]
            print(f"(1).  Sistema de Recomenació.")
            print(f"(2).  Sistema d'Avaluació.")
            print(f"(3).  Sortir del Programa.")
            accio = int(input('Inserti una acció a realitzar (int): '))
            print(f"S'utilitzar l'acció nº: {accio}.")
            confirmat = str(input("Esteu segurs d'utilitzar aquesta acció? (s/N): "))

            if accio in accions_valides and confirmat.lower() == 's':
                valid = True
            else:
                if confirmat.lower() != 's':
                    print(f"S'ha cancelat l'operació.")
                elif accio not in accions_valides :
                    print(f"Acció fora de rang.")
                time.sleep(1)
        except ValueError:
            print(f"L'acció indicada NO és un número.")
            time.sleep(2)
        except Exception as e:
            print(f'Ha saltat un error inesperat: {str(e)}')
            time.sleep(2)
    return accio


def __main__():
    """
    Funció principal del programa.

    Executa el programa de recomanació segons els arguments seleccionats.

    Parameters
    ----------
    None

    Return
    ------
    None
    """
    args = argparse_options.set_arguments()
    dataset, metode = argparse_options.get_arguments(args)
    print(f"S'utilitzarà el dataset {dataset} i el mètode de recomneació {metode}")
    os.system('pause')

    if dataset == 'movies':
        fitxer_dataset = 'dataset/MoviesLens100k/movies.csv'
        pickle_dataset = 'dataset/MoviesLens100k/movies.pkl'
        fitxer_ratings = 'dataset/MoviesLens100k/ratings.csv'
        pickle_ratings = 'dataset/MoviesLens100k/ratings.pkl'

        if metode == 'rec_colaboratiu':
            pickle_matriu_valoracions = 'Procediments/movies-matriu_valoracions.pkl'  
    
    elif dataset == 'books':
        fitxer_dataset = 'dataset/Books/Books-small.csv'
        pickle_dataset = 'dataset/Books/Books-small.pkl'
        fitxer_ratings = 'dataset/Books/Ratings-small.csv'
        pickle_ratings = 'dataset/Books/Ratings-small.pkl'

        if metode == 'rec_colaboratiu':
            pickle_matriu_valoracions = 'Procediments/books-matriu_valoracions.pkl'  

    log_file_name = f"logs/log_{time.strftime('%Y%m%d-%H%M%S')}.txt"
    logging.basicConfig(filename=log_file_name,level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

    set_content_items(fitxer_dataset, pickle_dataset)
    set_ratings(fitxer_ratings, pickle_ratings)

    accio = 0
    while accio != 3:
        accio = set_accio()
        if accio == 1:
            if metode == 'rec_simple':    
                mae, rmse = set_rec_simple()
            elif metode == 'rec_colaboratiu':
                mae, rmse = set_rec_colab(pickle_matriu_valoracions)
            elif metode == 'rec_contingut':
                mae, rmse = set_rec_contingut()
        elif accio == 2:
            try:
                print('MAE:',mae)
                print('RMSE:',rmse)
            except:
                print("Primer s'ha d'executar el sistema recomanador per podre avaluar les mètriques.")
        elif accio == 3:
            print('Sortint del programa...')
            exit()
        os.system('pause')


__main__()


                
## per fer una mascara / intercecció np_zero = U() * V()
'''
def similiud(u,v):
    no_zero= ((u != 0) == (v != 0))
    numerador = (u[no_zero] == v[no_zero]).sum()
    norma_u = np.sqrt((u[no_zero]**2).sum())
    norma_v = np.sqrt((v[no_zero]**2).sum())
    return numerador/(norma_u * norma_v)

    ## S'han de considerar només aquells que els dos són diferents de 0    
'''
    


'''
MIN_VOTS=declarar

class pelicula ---> generar llista de pelicules a traves del fitxer
    atributs=> || RATINGS -->
                    - id_user: int
                    - movie_id: int
                    - rating: float
                    + __init__()
                    + llegeix_fitxer(nom_fitxer: str)
                    + get_movie_id() -> int
                    + get_rating() -> float
                    + get_llista_ratings() -> dict(movie_id: (list(ratings)))

               || MOVIES -->
                    - movie_id: int
                    - titol: str
                    - generes: list(str)
                    + __init__()
                    + llegeix_fitxer(nom_fitxer: str)
                    + get_movie_id() -> int
                    + get_llista_pelis() -> dict(movie_id: (titol, list(generes)))

class Procediments():
    class rec_simple(Procediments)
        + calcular avg_item,num_vots,avg_global
        - avg_item:valoració mitja que li han donat els usuaris a l’ítem ( descartem 0 )
            avr=0
            lencounter=0
            for peli,i in enumerate(llistapelis):
                if peli.rating!=0.0:
                    lencounter+=1
                    avr+=peli.rating
            avg_item=avr/lencounter

        - num_vots: nº d’usuaris que han puntuat aquest ítem
        - avg_global: valoració mitja de tots els ítems considerats.





    class rec_colaborativa(Procediments)
        + calcular_similitud


    class rec_contigut(Procediments)


'''
