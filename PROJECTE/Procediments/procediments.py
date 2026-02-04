import csv, os, time, logging
import numpy as np
from dataclasses import dataclass, field
from Setup_Datasets.content_items import Content_Items
from Setup_Datasets.ratings import Ratings
from user import User
from abc import ABC, abstractmethod


class Procediments(ABC):
    """
    Classe que gestiona els diferents tipus de procediments de dades.

    Atributes
    ---------
    _llista_ratings : dict[Ratings]
        Un diccionari que conté les valoracions de els usuaris
    _lllista_items : dict[Content_items]
        Un diccionari que conté les dades del dataset
    _k_items : list
        Llista de k ítems amb més puntuació a partir els k_usuaris.

    Methods
    -------
    __init__(ci, r)
        Inicialitza un nou objecte amb el conjunt de dades proporcionats.
    __main__()
        Mètode abstracte que s'encarrega de tota l'execucció dels procediments.
    _set_k_items(diccionari, k, increment)
        Ordena un diccionari i agafa els k amb més puntuació
    get_k_items()
        Mètode que retorna la variable '_k_items'.
    __str__(valor)
        S'encarrega de retornar un valor en format str() per poder ser printat per pantalla.
    """
    _llista_ratings: dict
    _llista_items: dict  
    _k_items: list

    def __init__(self) -> None:
        """
        Inicialitza un nou objecte amb el conjunt de dades proporcionades.
        
        Parameters
        ----------
        None
                
        Return
        ------
        None
        """
        self._llista_ratings = Ratings().get_dict_dataset()
        self._llista_items = Content_Items().get_dict_dataset()
        self._k_items = list()



    @abstractmethod
    def __main__(self) -> None:
        """
        Métode abstracte que ha de ser implementat per les subclases.

        Funció principal del procediment, s'encarrega de fer tots els calculs necesaris del procediment en concret.
        
        Parameters
        ----------
        None

        Return
        ------
        None
        """
        pass    
        
    def _set_k_items(self, diccionari: dict, k: int, increment = int(0)) -> list:
        """
        Retorna els k ítems amb més valoració a partir d'un diccionari proporcionat.

        Parameters
        ----------
        diccionari : dict
            Diccionari que conté els ítems a ordenar amb les seves valoracions.
        k : int+ 
            El nombre d'ítems amb més puntuació a retornar
        increment : int, opcional
            Un valor que s'afegirà a les keys del diccionari en cas de ser necesari.
            Per defecte és 0.
        
        Return
        ------
        list
            Una llista que conté els k ítems amb més valoració.

        Exemple
        -------
        >>> _set_k_items({'10': 4.5, '11': 3.8, '12': 2.1, '14': 6.2, '15': 2.4}, 2)
        [('14', 6.2), ('10', 4.5)] 
        """
        # Ordenem els ítems del diccionari de major a menor, i agafem els k més grans.
        k_items = sorted(diccionari.items(), key=lambda x: x[1], reverse=True)
        k_items = k_items[:k]

        # En cas que rebem un increment, modificarem les claus amb aquest.
        if increment != 0:
            k_items = [(clave + increment, valor) for clave, valor in k_items]
        return k_items

    def get_k_items(self) -> list:
        """
        Retorna la llista de _k_items amb millor puntuació

        Parameters
        ----------
        None

        Return
        ------
        list
            Llista que guarda els k_items amb millor puntuació que es recomnanen al usuari específic.
        """
        return self._k_items

    
    def get_nom_items(self):
        """
        Printa els noms dels items millor recomanats

        Parameters
        ----------
        None

        Return
        ------
        None
        """
        try:
            for i in self._k_items:
                print(self._llista_items[str(i[0])][0], self._llista_items[str(i[0])][1])
            print()
        except:
            logging.error(f"Hi ha hagut un error al intentar accedir al nom dels ítems.")


    def calcular_metriques(self):
        """
        Calcula les mètriques MAE i RMSE del sistema.

        Parameters
        ----------
        None

        Return
        ------
        float, float
            Valors del MAE i RMSE.
        """
        try:
            items_puntuats = [item for item in self._llista_ratings[str(User.get_user())] if self._llista_ratings[str(User.get_user())][item] != 0][:5]
            llista_items_valoracions = [float(self._llista_ratings[str(User.get_user())][item]) for item in items_puntuats]

            items_recomanar = self.get_k_items()

            llista_prediccions_sistema = list()
            for id_item, valoracio in items_recomanar:
                llista_prediccions_sistema.append(valoracio)
                    
            llista_prediccions_sistema = sorted(llista_prediccions_sistema)
            llista_prediccions_sistema = np.array(llista_prediccions_sistema)

            llista_items_valoracions = np.array(llista_items_valoracions)

            mae = np.sum(np.abs(llista_prediccions_sistema - llista_items_valoracions)) / 5
            rmse = np.sqrt(np.sum((llista_items_valoracions - llista_prediccions_sistema) ** 2) / 5)
            return mae, rmse
        except:
            logging.error("S'ha ocasionat un error durant el calcul de mètriques")
            return 0.0, 0.0

    def __str__(self, valor) -> str:
        """
        Converteix l'objecte en una cadena de text per la seva impresió per pantalla.

        Parameters
        ----------
        valor : Any
            El valor a convertir en cadena.

        Returns
        -------
        str
            La representació en cadena del valor proporcionat.
        """
        return str(valor)
