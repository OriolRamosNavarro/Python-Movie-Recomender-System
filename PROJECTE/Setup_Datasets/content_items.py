import csv, os, time, logging
from dataclasses import dataclass, field

from Setup_Datasets.dataset import Setup_Dataset

## HEM DE CANVIAR EL NOM DE LA CLASSE, NO POT SER MOVIES, PQ TAMBÉ HI HA LLIBRES XD

class Content_Items(Setup_Dataset):
    """
    Subclasse de Setup_Datset que gestiona els dataset Content_Items.

    Atributes
    ---------
    _dict_dataset : dict
        Diccionari que guarda les dades rebudes en un format {'itemID': ('itemTitle', 'Others')}

    Methods
    -------
    __init__()
        Inicialitza un nou objecte.
    llegeix_fitxer(nom_fitxer)
        Mètode que a partir d'un fitxer proporcionat genera un diccionari.
    """
#    _dict_dataset = {}
     
    def __init__(self) -> None:
        """
        Inicialitza una nova instància de la classe Content_Items.

        Aquest mètode utilitza el constructor de la superclasse per inicialitzar els atributs heredats.

        Parameters
        ----------
        None

        Return
        ------
        None
        """        
        super().__init__()

    def llegeix_fitxer(self, nom_fitxer: str) -> dict:
        """
        Llegeix el fitxer rebut i genera un diccionari '_dict_dataset'.
        
        Parameters
        ----------
        nom_fitxer : str
            Nom del fitxer des del qual es generarà el diccionari.
        
        Return
        ------
        None

        Notes
        -----
        El fitxer CSV ha de tenir el format:

        movieId,title,genres
        1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
        2,Jumanji (1995),Adventure|Children|Fantasy

        Example
        -------
        >>> llegeix_fitxer('fitxer.csv')
        {'1': ('Toy Story (1995)', 'Adventure|Animation|Children|Comedy|Fantasy') ,
         '2': ('Jumanji (1995)','Adventure|Children|Fantasy')}
        """
        with open(nom_fitxer, 'r', encoding='utf8') as csv_file:
            ## Contem el número de files del fitxer.
            count_file = 0
            for _ in csv_file:
                count_file += 1
            csv_file.seek(0)
            
            csvreader = csv.reader(csv_file)
            fields = next(csvreader)

            ## Fem un try, except per controlar si hi ha algun error, registrar-lo i enviar-ho al fitxer 'log.txt'.
            dict_items = dict()
            try:
                count = 0
                for row in csvreader:
                    title_id = row[0]
                    titol = row[1]
                    generes_author = row[2]
                    dict_items[title_id] = (titol, generes_author)
                    count += 1
            except FileNotFoundError:
                logging.error(f"No s'ha trobat el fitxer {nom_fitxer}.")                
            except ValueError:
                logging.error(f"Hi ha hagut un error al carregar el registre de Content_Items amb ID: {self._movie_id}")
        logging.info(f"S'han creat correctament {count} de {count_file-1}, {(count)/(count_file-1)*100}%, registres de Content_Items.")

        ## Amb el __class__ ens estem assegurant de guardar la variable a la clase i no a la instància.
        ## Al fer això ens assegurem que si iniciem una nova instància aquesta no sigui eliminiada.
        self.__class__._dict_items = dict_items
        ## Retornem el diccionari per guardar-lo en un fitxer .pkl per següents execuccions.
        return dict_items

    @classmethod
    def get_dict_dataset(cls) -> dict:
        """
        Retorna el diccionari del dataset.

        Returns
        -------
        _dict_dataset
            El diccionari del dataset emmagatzemat.
        """
#        return self._dict_dataset
        return cls._dict_items

    @classmethod
    def load_pickle(cls, data: dict) -> None:
        """
        Carrega les dades del dataset des d'un objecte serialitzat en bytes.

        Parametres
        ----------
        data : dict
            El diccionari de les dades a guardar.

        Notes
        -----
        Aquesta funció actualitza el diccionari intern '_dict_dataset' amb les dades rebudes.
        No retorna cap valor.
        """
#        self._dict_dataset = data
        cls._dict_items = data

