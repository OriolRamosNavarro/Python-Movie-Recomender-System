import csv, os, time, logging
import numpy as np
from dataclasses import dataclass, field
from Procediments.procediments import Procediments
from user import User

from sklearn.feature_extraction.text import TfidfVectorizer

class Rec_contingut(Procediments):
    """
    Subclasse de Procediments que recomanda aquells ítems amb millor similitud de contingut en comparació amb els puntuats per l'usuari.

    Atributes
    ---------
    _llista_generes : list
        Llista de gèneres de tots els ítems.
    _tfidf_matrix : np.ndarray
        Matriu TF-IDF de tots els ítems.
    _perfils_usuaris : dict
        Diccionari que conté el perfil de cada usuari.
    _similituds_usuaris : dict
        Diccionari que conté la similitud entre cada parell d'usuaris.
    _scores_usuaris : dict
        Diccionari que conté la puntuació recomanada per a cada ítem per a cada usuari.

    Methods
    -------

    __init__()
        Constructor de la classe.
    __main__()
        Mètode principal que s'encarrega de fer totes les operacions necesaries cridant als altres mètodes de la classe.
    _set_llista_generes()
        Genera la llista de gèneres diferents de tots els ítems.
    _crear_matriu()
        Crea la matriu TF-IDF de tots els ítems.
    _calcular_perfils_usuaris()
        Calcula el perfil de cada usuari.
    _calcular_similituds()
        Calcula la similitud entre cada parell d'usuaris amb el usuari indicat.
    _puntuacio_maxima()
        Retorna la puntuació màxima possible per a un ítem.
    _calcular_puntuacions()
        Calcula la puntuació recomanada per a cada ítem per a cada usuari.
    _set_k_items()
        Omple la llista dels k ítems recomanats per a l'usuari actual.
    """
    _llista_generes: list
    _tfidf_matrix: np.ndarray
    _perfils_usuaris: dict
    _similituds_usuaris: dict
    _scores_usuaris: dict

    def __init__(self) -> None:
        """
        Inicialitza una nova instància de la classe Rec_colaborativa.

        Aquest mètode utilitza el constructor de la superclasse per inicialitzar els atributs generals.

        Parameters
        ----------
        None

        Return
        ------
        None
        """
        super().__init__()
        self._llista_generes = list()  
        self._tfidf_matrix = np.ndarray
        self._perfils_usuaris = dict()
        self._similituds_usuaris = dict()
        self._scores_usuaris = dict 
    
    def __main__(self) -> None:
        """
        Funció principal del sistema de recomanació col·laboratiu. Executa els passos necessaris per calcular les puntuacions recomanades per a cada usuari.

        Parameters
        ----------
        None
        
        Return
        ------
        None            
        """
        self._crear_matriu()
        self._calcular_perfils_usuaris()
        self._calcular_similituds()
        self._calcular_puntuacions()
        self._set_k_items()

    def _set_llista_generes(self) -> None:
        """
        Genera la llista de gèneres diferents d'entre tots els ítems.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètodes guarda els següents valors:
            _llista_generes : list
                Llista de tots els diferents generes d'entre tots els ítems.
        """
        for i in self._llista_items.keys():
            genres = self._llista_items[str(i)][1].replace('|', ' ')
            self._llista_generes.append(genres)
            
    def _crear_matriu(self):
        """
        Crea la matriu TF-IDF de tots els ítems.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètodes guarda els següents valors:
            _tfidf_matrix : np.ndarray
                Matriu TF-IDF
        """
        self._set_llista_generes()
        tfidf = TfidfVectorizer(stop_words = 'english')
        self._tfidf_matrix = tfidf.fit_transform(self._llista_generes).toarray()
    
    def _calcular_perfils_usuaris(self) -> None:
        """
        Calcula el perfil de cada usuari.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètodes guarda els següents valors:
            _perfils_usuaris : dict
                Diccionari que guarda tots els perfils dels diferents usuaris.
        """
        perfils_usuaris = {}
        for user_id, ratings in self._llista_ratings.items():
            vector_usuari = np.zeros(self._tfidf_matrix.shape[1])
            total_puntuacio = 0.0
            for item_id, rating in ratings.items():
                index = list(self._llista_items.keys()).index(item_id)
                vector_usuari += float(rating) * self._tfidf_matrix[index]
                total_puntuacio += float(rating)
            perfils_usuaris[user_id] = (vector_usuari / total_puntuacio)

        self._perfils_usuaris = perfils_usuaris


    def _calcular_similituds(self) -> None:
        """
        Calcula la similitud entre cada parell d'usuaris.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètodes guarda els següents valors:
            _similituds_usuaris : dict
                Diccionari que guarda la similitud de tots els usuaris.
        """
        similituds_usuaris = {}
        for user_id, matriu in self._perfils_usuaris.items():
            matriu_perfil = np.transpose(matriu)
            similitud = np.dot(self._tfidf_matrix, matriu_perfil)
            similituds_usuaris[user_id] = similitud

        self._similituds_usuaris = similituds_usuaris

    def _puntuacio_maxima(self) -> float:
        """
        Retorna la puntuació màxima possible per a un ítem.

        Parameters
        ----------
        None
        
        Return
        ------
        float
            La puntuació màxima possible per a un ítem.
        """
        max_rating = 0.0
        for i in self._llista_ratings:
            for j in self._llista_ratings[str(i)].items():
                if float(j[1]) > max_rating:
                    max_rating = float(j[1])
        return max_rating

    def _calcular_puntuacions(self) -> None:
        """
        Calcula la puntuació recomanada per a cada ítem per a cada usuari.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètodes guarda els següents valors:
            _scores_usuaris : dict
                Diccionari que conté les puntuacions dels usuaris.
        """
        max_rating = self._puntuacio_maxima()
        scores_usuaris = {}
        for user_id, similitud in self._similituds_usuaris.items():
            scores_usuaris[user_id] = similitud * max_rating
        
        self._scores_usuaris = scores_usuaris

    def _set_k_items(self) -> None:
        """
        Genera la llista dels k ítems recomanats per a l'usuari actual.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        Es sobre escriu aquest mètode ja que tot i que fa la mateixa funció no ho fa a partir de les mateixes dades.
        El mètode guarda els següents valors:
            _k_items : list
                Llista dels ítems més similars a partir d'una puntuació.
        """
        user_id = User.get_user()
     
        scores = self._scores_usuaris[str(user_id)]
        index_items = np.argsort(scores)[::-1][:5]

        valors = [list(self._llista_items.keys())[i] for i in index_items]

        self._k_items = []
        for i in valors:
            self._k_items.append((i,''))
