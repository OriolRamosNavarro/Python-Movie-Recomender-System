import csv, os, time, logging
import numpy as np
from dataclasses import dataclass, field
from Procediments.procediments import Procediments
from user import User

class Rec_colaborativa(Procediments):
    """
    Subclasse de Procediments que calcula una puntuació a partir d'un sistema colaboratiu i recomanda aquells que els usuaris més similars han puntuat correctament.

    Atributes
    ---------
    _matriu_valoracions : np.array
        Matriu que guarda tot el conjunt de valoracions dels diferents usuaris. Es guarda en un pickle.
    _k : int
        Número que ens indica els ítmes més similars a seleccionar.
    _pickle : bool
        Indica si s'ha guardat la _matriu_valoracions en un fitxer pickle.
    _posicons_items : dict
        Diccionari que conté la posició de cada ítem en la matriu de valoracions. La clau és la ID de l'ítem en string i el valor és la seva posició a la matriu.
    _posicions_usuaris : dict
        Diccionari que conté la posició de cada usuari en la matriu de valoracions. La clau és la ID de l'usuari en string i el valor és la seva posició a la matriu.
    _diccionari_similituds : dict
        Diccionari que conté les similituds de tots els usuaris amb el indicat.
        
    Methods
    -------
    __init__() 
        Constructor de la classe.
    __main__(k: int)
        Mètode principal que s'encarrega de fer totes les operacions necesaries cridant als altres mètodes de la classe.
    set_pickle_bool(pickle: bool)
        Actualitza l'indicador de pickle.
    _set_matriu_valoracions(id_posicio_usuaris: dict, id_posicio_items: dict)
        Crea la matriu de valoracions.
    crea_ratings_usuaris()
        Crea els indexs de posicios i en cas de no existir s'encarrega de crida a '_set_matriu_valoracions'. 

    _comparacio_matrius()
        Calcula les similituds entre tots els parells d'usuaris mitjançant la similitud del cosinus.
    
    _calcul_similitud(u: np.ndarray, v: np.ndarray)
        Calcula la similitud del cosinus entre dos vectors.
    
    _calcul_puntuacio()
        Calcula les puntuacions recomanades per a cada ítem no avaluat per l'usuari actual.
        
    _calcul_mitjana(matriu: np.ndarray)
        Calcula la mitjana dels valors no nuls d'una matriu NumPy.
    
    load_pickle(data: np.array)
        Carrega la matriu de valoracions des d'un fitxer pickle.
    """
    _matriu_valoracions = {}
    _k: int
    _pickle = False
    _posicions_items: dict
    _posicions_usuaris: dict
    _diccionari_similituds: dict

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
        self._k = int()
        self._posicions_items = dict()
        self._posicions_usuaris = dict()
        self._diccionari_similituds = dict()

    def __main__(self, k: int) -> None:
        """
        Funció principal del sistema de recomanació col·laboratiu. Executa els passos necessaris per calcular les puntuacions recomanades per a cada usuari.

        Parameters
        ----------
        k : int
            El nombre d'usuaris més similars a utilitzar per a les recomanacions.

        Return
        ------
        None            
        """
        self._k = k
        self.crea_ratings_usuaris()
        self._comparacio_matrius()
        self._calcul_puntuacio()


    def set_pickle_bool(self, pickle: bool) -> None:
        """
        Actualitza l'indicador de pickle que assenyala si la matriu de valoracions s'ha guardat en un fitxer pickle.

        Parameters
        ----------
        pickle : bool
            True si la matriu de valoracions s'ha guardat en un fitxer pickle, False en cas contrari.

        Return
        ------
        None
        """
        self._pickle = pickle


    def _set_matriu_valoracions(self, id_posicio_usuaris: dict, id_posicio_items: dict) -> np.ndarray:
        """
        Crea la matriu de valoracions a partir dels diccionaris de posicions d'usuaris i ítems i les valoracions dels usuaris.

        Parameters
        ----------
        id_posicio_usuaris : dict
            Diccionari que conté la posició de cada usuari en la matriu de valoracions. La clau és la ID de l'usuari en string i el valor és la seva posició a la matriu.
        id_posicio_items : dict
            Diccionari que conté la posició de cada ítem en la matriu de valoracions. La clau és la ID de l'ítem en string i el valor és la seva posició a la matriu.

        Return
        ------
        np.ndarray
            La matriu de valoracions generada.
        """
        matriu_valoracions = np.zeros((int(len(id_posicio_usuaris)),int(len(id_posicio_items))),dtype='float16')
        for user_id, items_ratings in self._llista_ratings.items():
            try:
                posicio_usuari = id_posicio_usuaris.get(str(user_id))
                if posicio_usuari is None:
                    logging.error(f"Hi ha un error amb l'usuari {user_id}, aquest no es troba en el dataset.")
                    continue
                for item_id, rating in items_ratings.items():
                    posicio_item = id_posicio_items.get(str(item_id))
                    if posicio_item is None:
                        logging.error(f"Hi ha un error amb l'item {item_id}, aquest no es troba en el dataset.")
                        continue
                    matriu_valoracions[posicio_usuari][posicio_item] = rating
            except:
                logging.error(f"Hi ha hagut un error al guardar el registre a la matriu amb ID: {item_id}")        
     
        ## Guardem la matriu_valoracions, també la retornem perquè sigui guardada en un fitxer pickle.
        self._matriu_valoracions = matriu_valoracions
        self.set_pickle_bool(True)
        return self._matriu_valoracions    

    def crea_ratings_usuaris(self) -> np.ndarray:
        """
        Crea la matriu de valoracions a partir dels diccionaris de valoracions d'usuaris i ítems.

        Parameters
        ----------
        None

        Return
        ------
        np.ndarray
            La matriu de valoracions generada.
        
        Notes
        -----
        El mètode guarda els següents valors:
            _id_posicio_items : dict
                Diccionari que guarda com a key la posició de la matriu i com a valor el nº d'item.
            _id_posicio_usuaris : dict
                Diccionari que guarda com a key la posició de la matriu i com a valor el nº d'usuari.            
        """
        id_posicio_items = dict()
        count = 0
        for i in self._llista_items:
            id_posicio_items[str(i)] = count
            count += 1

        id_posicio_usuaris = dict()
        count = 0
        for i in self._llista_ratings:
            id_posicio_usuaris[str(i)] = count
            count += 1
        
        if self._pickle == False:
            return self._set_matriu_valoracions(id_posicio_usuaris, id_posicio_items)

        ## Guardem el 'conjunt_items'.
        self._posicions_items = id_posicio_items

        self._posicions_usuaris = id_posicio_usuaris

        try:
            ## Guardem la posicio del usuari a partir de 'conjunt_usuaris'.
            User.set_posicio_user(id_posicio_usuaris[str(User.get_user())])
            ## Guardem la matriu del usuari.
            User.set_matriu_user(self._matriu_valoracions[User.get_posicio_user()])
        except:
            logging.error(f"Hi ha hagut un error al guardar les dades del usuari {User.get_user()}")

    def _comparacio_matrius(self) -> None:
        """
        Compara totes les matrius dels diferents usuaris amb la '_matriu_usuari'.

        Guarda una puntuació de similitud entre els diferents usuaris amb el usuari específic.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètode guarda els següents valors:
            _dict_distancies : dict
                Diccionari que guarda com a key un usuari i com a valor la similitud d'aquest amb el usuari específic.

        Les similituds guardades oscil·len entre 0.0 i 1.0.
                
        Example
        --------
        >>> _compara_matrius()
        {usuari1: [similitud1], usuari2: [similitud2]}
        """
        ## El Count ens serveix per tenir una referencia del usuari que estem calculant
        count = 0; diccionari_similituds = dict()
        for i in self._matriu_valoracions:
            
            if count != User.get_posicio_user():
                similitud = self._calcul_similitud(User.get_matriu_user(), i)
            else:
                similitud = 0.0
            diccionari_similituds[count] = similitud
            count += 1
        self._diccionari_similituds = diccionari_similituds

    def _calcul_similitud(self, u: np.ndarray, v: np.ndarray) -> float:
        """
        Calcula la similitud entre dues matrius a partir de la similitud del cosinus.
        
        Parameters
        ----------
        u : np.array
            Matriu de valoracions del usuari específic.
        v : np.array
            Matriu de valoracions d'un usuari.
        count : int
            Número d'usuari per si es necessari enviar un error al fitxer de logs.

        Return
        ------
        float
            El valor de la similitud entre les matrius.
        
        Notes
        -----
        La similitud entre matrius es calcula mitjançant la fórmula del cosinus entre els dos vectors,
        que es defineix com la suma del producte dels elements dels vectors,
        dividit pel producte de les seves normes Euclidianes.

        Example
        --------
        >>> _similitud(np.array([1, 2, 3]), np.array([3, 4, 5]) , 1)
        0.9827076298239908
        """
        try:
            no_zero = (u != 0.0) & (v != 0.0)

            suma_coincidencies = np.sum(u[no_zero] * v[no_zero])

            norma_u = np.sqrt((u[no_zero]**2).sum())
            norma_v= np.sqrt((v[no_zero]**2).sum())
                
            if norma_u == 0.0 or norma_v == 0.0:
                return 0.0
            else:
                ## Retorna el resultat de la fórmula del cosinus entre els dos vectors
                return round((suma_coincidencies / (norma_u * norma_v)),2)
        except:
            return 0.0

    def _calcul_puntuacio(self):
        """
        Calcula la puntuació dels diferents ítems a partir dels k_usuaris amb millor similitud.

        Parameters
        ----------
        None

        Return
        ------
        None

        Notes
        -----
        El mètode guarada els següents valors:
            _k_items : list
                Llista que conté els k items amb millor puntuació no puntuades per l'usuari específic.
                
        Example
        -------
        >>> _calcul_puntuacio()
        [('item1', 4.8), ('item2', 4.5), ('item3', 4.2)]
        """
        k_usuaris = self._set_k_items(self._diccionari_similituds, self._k)
        mitjana_usuari = self._calcul_mitjana(User.get_matriu_user())
        no_evaluades = np.where(User.get_matriu_user() == 0)
        divisor = sum(similitud for usuario, similitud in k_usuaris)

        diccionari_scores = dict()
        for i in no_evaluades[0]:
            ## i conté la posició del item en la matriu.
            suma_calculs = 0.0
            for j in k_usuaris:
                similitud = j[1]
                calcul = similitud * (self._matriu_valoracions[j[0]][i] - self._calcul_mitjana(self._matriu_valoracions[j[0]]))
                suma_calculs += calcul
            puntuacio = mitjana_usuari + (suma_calculs / divisor)
            diccionari_scores[i] = puntuacio
        
        self._k_items = self._set_k_items(diccionari_scores, 5)
        posicio_id = {str(posicio): id for id, posicio in self._posicions_items.items()}
        k_items = [(posicio_id[str(posicio)], valoracio) for posicio, valoracio in self._k_items]

        ## Guardem la nova llista '_k_items'
        self._k_items = k_items

    def _calcul_mitjana(self, matriu: np.ndarray) -> np.float64:
        """
        Calcula la mitjana de puntuacions guardades en una matriu.

        Parameters
        ----------
        matriu : np.array
            Matriu que representa les valoracions dels ítems per un usuari.
        
        Return
        ------
        np.float64
            Puntuació mitjana d'aquesta matriu sense comptar valors nul·ls, 0.0.
        """
        try:
            no_zero = matriu[matriu != 0]
            return np.mean(no_zero)
        except:
            return 1.0


    def load_pickle(self, data: np.array) -> None:
        """
        Carrega les dades de la matriu des d'un objecte serialitzat en bytes.

        Parametres
        ----------
        data : np
            La matriu de les dades a guardar.

        Return
        ------
        None
            
        Notes
        -----
        Aquesta funció guarda la matriu np rebuda a '_matriu_valoracions'.
        """
        self._matriu_valoracions = data




