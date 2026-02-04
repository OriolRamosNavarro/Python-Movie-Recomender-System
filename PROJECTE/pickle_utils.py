import pickle, logging, os
from Setup_Datasets.content_items import Content_Items
from Setup_Datasets.ratings import Ratings

from Procediments.rec_colaboratiu import Rec_colaborativa

def pickle_write(pickle_file: str, data) -> None:
    """
    Funció que escriu les dades rebudes en un fitxer pickle.

    Parameters
    ----------
    pickle_file : str
        Nom del fitxer on hem de guardar les dades.    
    
    data: np.array o dict
        Les dades a desar. Pot ser tant un matriu de NumPy com un diccionari.
    
    Returns
    -------
    None

    Examples
    --------
    >>> pickle_write('matriu_data.pkl', np.array([1,4,2]))

    >>> pickle_write('diccionari_data.pkl', {'1': '3', '2': '5'})
    """
    try:
        ## Guardem les dades rebudes en el fitxer pickle indicat.
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)
        logging.info(f"Dades desades a {pickle_file}")
    except:
        logging.error(f"Error al inicialitzar el pickle {pickle_file}")

def pickle_read(pickle_file: str):
    """
    Funció que llegeix les dades d'un fitxer pickle i retorna les dades d'aquest

    Parameters
    ----------
    pickle_file : str
        Nom del fitxer del qual hem de agafar les dades.

    Returns
    -------
    data
        Les dades del fitxer indicat, poden ser tant un diccionari com una matriu de NumPy.

    Examples
    --------
    >>> pickle_read('diccionari_data.pkl')
    {'1': '3', '2': '5'}

    >>> pickle_read('matriu_data.pkl')
    np.array([1,4,2])
    """
    try:
        ## Llegim les dades del fitxer pickle i retornem les dades rebudes.
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
        logging.info(f"Dades carregades des de {pickle_file}")
        return data
    except:
        logging.error(f"Error al carregar el pickle {pickle_file}")        

def create_content_items(pickle_file: str, csv_file: str) -> None:
    """
    Crea un diccionari de Content_Items a partir d'un fitxer CSV i desa les dades en un fitxer pickle.

    Parameters
    ----------
    pickle_file : str
        Nom del fitxer pickle on guardarem les dades.
    csv_file : str
        Nom del fitxer d'on extreurem les dades.
    
    Returns
    -------
    Content_Items : object
        L'objecte Content_Items creat.
    """
    ## Cridem a 'llegeix_fitxer' de Contetn_Items() per generar el diccionari d'items.
    ci = Content_Items()
    dict_data = ci.llegeix_fitxer(csv_file)
    ## Enviem el diccionari generat a 'pickle_write' perquè el guardi en aquest.
    pickle_write(pickle_file, dict_data)
    
def load_content_items(pickle_file: str) -> None:
    """
    Carrega un diccionari de Content_Items a partir d'un fitxer pickle.

    Parameters
    ----------
    pickle_file : str
        Nom del fitxer pickle on tenim guardades les dades.

    Returns
    -------
    Content_Items : object
        L'objecte Content_Items carregat a partir del fitxer pickle.    
    """
    ## Guardem les dades rebudes des de 'pickle_read'.
    data = pickle_read(pickle_file)
    ## Cridem a 'load_pickle()' de Content_Items() perquè guardi les dades rebudes.
    ci = Content_Items()
    ci.load_pickle(data)

def create_ratings(pickle_file: str, csv_file: str) -> None:
    """
    Crea un diccionari de Ratings a partir d'un fitxer CSV i desa les dades en un fitxer pickle.

    Parameters
    ----------
    pickle_file : str
        Nom del fitxer pickle on guardarem les dades.
    csv_file : str
        Nom del fitxer d'on extreurem les dades.
    
    Returns
    -------
    Ratings : object
        L'objecte Ratings creat.
    """
    ## Cridem a 'llegeix_fitxer' de Ratings() per genera el diccionari de ratings.
    r = Ratings()
    dict_data = r.llegeix_fitxer(csv_file)
    ## Enviem el diccionari generat a 'pickle_write' perquè el guardi en aquest.
    pickle_write(pickle_file, dict_data)
    
def load_ratings(pickle_file: str) -> None:
    """
    Carrega un diccionari de Content_Items a partir d'un fitxer pickle.

    Parameters
    ----------
    pickle_file : str
        Nom del fitxer pickle on tenim guardades les dades.

    Returns
    -------
    Ratings : object
        L'objecte Ratings carregat a partir del fitxer pickle.    
    """
    ## Guardem les dades rebudes des de 'pickle_read'.
    data = pickle_read(pickle_file)
    ## Cridem a 'load_pickle()' de Ratings() perquè guardi les dades rebudes.
    r = Ratings()
    r.load_pickle(data)
    
def create_matriu_valoracions(pickle_file: str) -> Rec_colaborativa:
    """
    Crea un matriu de valoracions, de NumPy, de tots els usuaris a partir de les dades proporcionades i la guarda en un fitxer pickle.
    
    Parameters
    ----------
    ci : object
        Objecte de Content_Items().
    r : object
        Objecte de Ratings().
    pickle_file : str
        Fitxer pickle on hem de guardar les dades.

    Returns
    -------
    Rec_colaborativa : object
        L'objecte de Rec_colaborativa creat.
    """
    ## Cridem a 'crea_ratings_usuaris' perquè ens generia la matriu NumPy.
    rc = Rec_colaborativa()
    matriu_valoracions = rc.crea_ratings_usuaris()
    ## Enviem aquesta matriu generada a 'pickle_write' perquè la guardi en el fitxer.
    pickle_write(pickle_file, matriu_valoracions)
    return rc

def load_matriu_valoracions(pickle_file: str) -> Rec_colaborativa:
    """
    Carregem una matriu de valoracions de NumPy guardada en el fitxer pickle.
    
    Parameters
    ----------
    ci : object
        Objecte de Content_Items().
    r : object
        Objecte de Ratings().
    pickle_file : str
        Fitxer pickle on hem de guardar les dades.

    Returns
    -------
    Rec_colaborativa : object
        L'objecte de Rec_colaborativa creat.
    """
    ## Guardem la matriu que ens torna 'pickle_read' des del fitxer pickle.
    data = pickle_read(pickle_file)
    ## Guardem la matriu a l'objecte Rec_colaborativa()
    rc = Rec_colaborativa()
    rc.set_pickle_bool(True)
    rc.load_pickle(data)
    return rc
