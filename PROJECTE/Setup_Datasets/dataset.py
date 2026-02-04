import csv, logging, pickle
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.
## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.
## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.
## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.
## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.
## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.
## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.
## Aquesta clase estaria bé que fos una clase que agrupes el generic de 'Ratings' i 'Content_Items'.

class Setup_Dataset(ABC):
    """
    Classe que gestiona els diferents tipus de dades a carregar.

    Atributes
    ---------
    _dict_dataset : dict
        Diccionari que guarda les dades rebudes en un format específic.
    _
        
    Notes
    -----
    El format del diccionari _dict_dataset depèn de la subclasse

    Methods
    -------
    __init__()
        Inicialitza un nou objecte buit.
    llegeix_fitxer(nom_fitxer)
        Mètode abstracte que s'encarrega de llegir un fitxer i guardar les dades en un diccionari.
    load_pickle(data)
        Mètode que guarda un diccionari rebut a '_dict_dataset'.
    __str__(valor)
        S'encarrega de retornar un valor en format str() per poder ser printat per pantalla.        
    """
    _dict_ratings = {}
    _dict_items = {}

    def __init__(self) -> None:
        """
        Inicialitza la nova instància de la classe Setup_Dataset.

        Crea un diccionari buit, '_dict_datset' per emmagatzemar les dades.

        Parameters
        ----------
        None

        Return
        ------
        None   
        """
#        self._dict_dataset = {}
#        self._dict_dataset = dict()
#        self._dict_dataset = {}
        pass

    @abstractmethod
    def llegeix_fitxer(self, nom_fitxer: str) -> None:
        """
        LLegeix el fitxer especificat.

        Aquesta funció és abstracta i ha de ser implementada per subclasses.

        Parameters
        ----------
        nom_fitxer : str
            El nom del fitxer que s'ha de llegir.
        
        Raises
        ------
        NotImplementedError
            Si la subclasse no implementa aquesta funció.        
        """
        pass

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
