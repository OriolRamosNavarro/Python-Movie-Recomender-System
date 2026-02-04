import csv, os, time, logging
import numpy as np
from dataclasses import dataclass, field
from Procediments.procediments import Procediments
from user import User


class Rec_simple(Procediments):
    """
    Subclasse de Procediments que calcula els ítems millor valorats.

    Atributes
    ---------
    _min_vots : int
        Valor mínim de vots per considerar un ítem
    _diccionari_score : dict
        Diccionari que guarda les valoracions dels ítems
    _avg_global : float
        Float que guarda la mitjana de tots els ítems
    _k_items : list
        Llista amb els k items més ben valorats

    Methods
    -------
    __init__(min_vots, usuari, ci, r)
        Inicialitza un nou objecte amb els paràmetres rebuts
    __main__()
        Mètode principal que s'encarrega de fer totes les operacions necesaris per calcular els ítems més ben valorats.
    _calcula_score()
        Mètode que calcula les puntuacions del ítems
    _set_llista_ratings()
        Mètode que genera un diccionari '_ratings' on es gaurden les valoracions rebudes pels ítems i els vots obtinguts.
    _calcula_avg_global()
        Mètode que s'encarrega de calcular la mitjana de puntuacions de tots els ítems
    _descarta_minims()
        Mètode que elimina aquells ítems amb menys valoracions que _min_vots
    _select_k_items(usuari)
        Mètode que selecciona els k_items millor valorats
    """
    _min_vots: int
    _diccionari_score = {}
    _avg_global: float
    
    def __init__(self) -> None:
        """
        Inicialitza una nova instància de la classe Rec_simple.

        Aquest mètode utilitza el constructor de la superclasse per inicialitzar els atributs generals.
        
        Parameters
        ----------
        None

        Return
        ------
        None
        """
        super().__init__()
        self._min_vots = int()
        self._avg_global = float
 
    def __main__(self, min_vots: int) -> None:
        """
        Mètode principal que s'encarrega de crida els altres mètodes de la classe per tal de calcular els k ítems amb millor valoració.

        Parameters
        ----------
        min_vots : int
            Número de vots mínims per contabilitzar un ítem.
            
        Return
        ------
        None

        """
        self._min_vots = min_vots
        ## Descartem els ítems amb pocs vots.
        self._descarta_minims()

        ## Calculem el avg_global i els avg_item de cada ítem
        self._calcula_avg_global()  

        ## Calculem els scores de cada ítem
        self._calcula_score()

        ## Seleccionem als k ítems amb millor puntuació que l'usuari no ha vist
        self._k_items = self._select_k_items()

    def _calcula_score(self) -> None:
        """
        Calcula el score dels diferents ítems

        Parameters
        ----------
        None
        
        Return

        ------
        None

        Notes
        -----
        El mètode guarda els següents valors:
            _diccionari_score : dict
                Diccionari que guarda com a keys els items i com a valors el score d'aquest.
        
        Example
        --------
        >>> _diccionari_score()
        {'itemID1': score1, 'itemID2': score2}
        """
        diccionari_score = dict()
        try:
            ## El count ens serveix per guardar les dades en el logging.
            count = 0
            ## Per cada item calculem el seu score i el guardem a '_diccionari_score'
            for i in self._ratings:
                score1 = (int(self._ratings[str(i)][1])/(int(self._ratings[str(i)][1] + int(self._min_vots)))) * float(self._ratings[str(i)][0])
                score2 = (int(self._min_vots)/(int(self._ratings[str(i)][1] + int(self._min_vots)))) * float(self._avg_global)                
                score = round((score1 + score2),5) 
                diccionari_score[str(i)] = score    
                count += 1
        except: 
             logging.error(f"Hi ha hagut un error al calcular el score del registre amb ID: {i}")
        logging.info(f"S'han creat correctament {count} de {len(self._ratings)}, {(count)/(len(self._ratings))*100}%, scores del Rec_Simple.")
        self._diccionari_score = diccionari_score

    def _set_llista_ratings(self) -> None:
        """
        Crea un '_diccionari_ratings' amb el format {'itemID': (suma_ratings, num_vots)}

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètode guarda els següents valors:
            _ratings : dict
                Diccionari que guarda com a key el itemID i com a valors la suma total dels ratings obtinguts, i el total de vots rebut.
        
        Example
        --------
        >>> _set_llista_ratings()
        {'itemID1': (total_ratings1, total_vots1), 'itemID2': (total_ratings2, total_vots2)}
        """
        diccionari_ratings = {}

        ## Guardem en un diccionari per cada item la suma dels ratings i el nº de vots total.
        for user_id, item in self._llista_ratings.items():
            for item_id, rating in item.items():
                if item_id in diccionari_ratings:
                    suma_ratings, num_item = diccionari_ratings[item_id]
                    diccionari_ratings[item_id] = (float(suma_ratings) + float(rating), num_item + 1)
                else:
                    diccionari_ratings[item_id] = (float(rating), 1)
        ## Guardem a '_ratings' el diccionari creat.
        self._ratings = diccionari_ratings    
        
    def _calcula_avg_global(self) -> None:
        """
        Mètode que calcula el avg de cada item i  el avg de tots els ítems de '_ratings'.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètode guarda els següents valors:
            _ratings : list
                Llista que guarda com a key el itemID i com a values: (avg_item, num_vots)
            _avg_global : float
                Flotant que guarda la mitjana de tots els items.

        Example
        --------
        >>> _calcula_avg_global()
        {'itemID': (avg_item1, num_vots1), 'itemID2': (avg_item2, num_vots2)}
        """
        try:
            avg = 0.0
            for i in self._ratings:
                ## Agafem la suma de ratings del item i el dividim entre els vots obtinguts, per calcular el avg_item.
                avg_item = float(self._ratings[str(i)][0])/(self._ratings[str(i)][1])
                ## Guardem el avg_item calculat en el item.
                self._ratings[str(i)] = (round(avg_item,5),self._ratings[str(i)][1])
                ## Sumem a 'avg' la mitja calcula d'aquest item.
                avg += self._ratings[str(i)][0]
            ## Guardem el avg_global de tots els items.
            self._avg_global = round((avg/len(self._ratings)),5)
        except:
             logging.error(f"Hi ha hagut un error al calcular el avg_item del registre amb ID: {i}")

    def _descarta_minims(self) -> None:
        """
        Descarta aquells item amb menys valoracions que el límit estipulat per _min_vots.
        
        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètode guarda els següents valors:
            _ratings : dict
                Diccionari que guarda com a key el itemID i com a valors la suma total dels ratings obtinguts, i el total de vots rebut.
                Eliminant aquells items amb menys de x vots determinat per _min_vots.
        
        Example
        --------
        _min_vots = 3
        _ratings = {'itemID1': (suma_ratings1, 4), 'itemID2': (suma_ratings2, 2), 'itemID3': (suma_ratings3, 3)}
        >>> _descarta_minims()
        {'itemID1': (suma_ratings1, 4), 'itemID3': (suma_ratings3, 3)}    
        """
        ## Cridem al mètode '_set_llista_ratings' 
        self._set_llista_ratings()
        ## Guardem els itemID que no superen el límit estipulat per _min_vots
        keys_a_eliminar = list()
        for i in self._ratings:
            if self._ratings[str(i)][1] < self._min_vots:
                keys_a_eliminar.append(i)        
        ## Eliminem els itemID que no superen el límit del diccionari
        for i in keys_a_eliminar:
            del self._ratings[str(i)]

    def _select_k_items(self) -> list:
        """
        Selecciona els k items amb millor valoració que no ha evaluat el usuari especificat.

        Parameters
        ----------
        usuari : int
            L'usuari específic pel que retornem la llista.

        Return
        ------
        list
            Llista dels k items millor valorats que no ha vist l'usuari especificat.

        Example
        --------
        _llista_ratings = {'13': {'1': 4.0, '3': 3.0, '4': 2.0, '5': 4.0}, '14': {'1': 2.0, '2': 4.0}}
        _ratings_usuari = {'1': 2.0, '2': 4.0}
        >>> _select_k_items(14)
        [('5', score), ('3', score), ('2', score)]
        """
        ## Comprobem que el usuari existeixi.
        if str(User.get_user()) in self._llista_ratings.keys():
            ## Guardem les valoracions del usuari especificat.
            items_usuari = self._llista_ratings[str(User.get_user())]
            ## Creem un nou diccionari amb tots els items NO valorats per l'usuari.
            dict_no_valorades = dict()
            for i in self._diccionari_score:
                if i not in items_usuari:
                    dict_no_valorades[i] = self._diccionari_score[i]

            ## Retornem els k amb millor valoració
            return self._set_k_items(dict_no_valorades,5)
        else:
            logging.error(f"L'usuari {User.get_user()} no es troba dintre d'aquest dataset.")
            return None
    