import csv, logging, os
from dataclasses import dataclass, field

from Setup_Datasets.dataset import Setup_Dataset

class Ratings(Setup_Dataset):
    """
    Subclasse de Setup_Datset que gestiona els dataset Ratings.

    Atributes
    ---------
    _dict_dataset : dict
        Diccionari que guarda les dades rebudes en un format {'userID': {'itemID': rating}, 'userID': {'itemID': rating}}

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
        Inicialitza una nova instància de la classe Ratings.

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

        userId,movieId,rating
        1,1,4.0
        1,3,3.0
        2,6,5.0

        Example
        -------
        >>> llegeix_fitxer('fitxer.csv')
        {'1': {'1': '4.0', '3': '4.0'}, '2': {'6': '5.0'}}
        """
        with open(nom_fitxer, 'r', encoding='utf8') as csv_file:
            ## Contem el número de files del fitxer.
            count_file = 0
            for _ in csv_file:
                count_file += 1
            csv_file.seek(0)
            
            csvreader = csv.reader(csv_file)
            fields = next(csvreader)

            dict_ratings = dict()
            ## Fem un try, except per controlar si hi ha algun error, registrar-lo i enviar-ho al fitxer 'log.txt'.
            try:
                count = 0
                for row in csvreader:
                    id_user = row[0]
                    title_id = row[1]
                    rating = row[2]
                    
                    if str(id_user) not in dict_ratings:
                        dict_ratings[str(id_user)] = {str(title_id): rating}
                    else:
                        dict_ratings[str(id_user)][str(title_id)] = rating
                    count += 1
            except FileNotFoundError:
                logging.error(f"No s'ha trobat el fitxer {nom_fitxer}.")                
            except ValueError:
                logging.error(f"Hi ha hagut un error al carregar el registre de Ratings amb ID: {self._title_id}")
        logging.info(f"S'han creat correctament {count} de {count_file-1}, {(count)/(count_file-1)*100}%, registres de Ratings.")
        
        self.__class__._dict_ratings = dict_ratings
        return dict_ratings

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
        return cls._dict_ratings

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
        cls._dict_ratings = data
