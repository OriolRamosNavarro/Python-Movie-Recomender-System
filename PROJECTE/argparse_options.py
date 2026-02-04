import argparse

def valid_dataset(opcio: str) -> str:
    """
    Comproba si l'opció rebuda és vàlida.

    Parameters
    ----------
    opcio : str
        L'opció de dataset a validar.
    
    Return
    ------
    str
        L'opció del dataset vàlida en minúscules
    
    Raises
    ------
    argparse.ArgumentTypeError
        Si l'opció rebuda no és vàlida es llença una excepció indicant els valors vàlids.
    
    Examples
    --------
    >>> valid_dataset('BOOKS')
    'books'
    
    >>> valid_dataset('Movies')
    'movies'
    
    >>> valid_dataset('music')
    argparse.ArgumentTypeError: Dataset NO vàlid: music. Els datasets acceptats són: ('books' or 'movies').
    """
    if opcio.lower() not in ['books', 'movies']:
        raise argparse.ArgumentTypeError(f"Dataset NO vàlid: {opcio.lower()}. Els datasets acceptats són: ('books' or 'movies').")
    return opcio.lower()

def valid_metode(opcio: str) -> str:
    """
    Valida si l'opció proporcionada és un sistema de recomanació vàlid.

    Parameters
    ----------
    opcio : str
        L'opció del sistema de recomanació a validar.

    Returns
    -------
    str
        L'opció del sistema de recomanació validada en minúscules.

    Raises
    ------
    argparse.ArgumentTypeError
        Si l'opció no és vàlida, es llença una excepció indicant els valors vàlids.

    Examples
    --------
    >>> valid_metode('REC_SIMPLE')
    'rec_simple'
    
    >>> valid_metode('Rec_Colaboratiu')
    'rec_colaboratiu'
    
    >>> valid_metode('rec_contingut')
    'rec_contingut'
    
    >>> valid_metode('rec_aleatori')
    argparse.ArgumentTypeError: Mètode NO vàlid: rec_aleatori. Els mètodes acceptats són: ('rec_simple', 'rec_colaboratiu', 'rec_contingut')
    """
    if opcio.lower() not in ['rec_simple', 'rec_colaboratiu', 'rec_contingut']:
        raise argparse.ArgumentTypeError(f"Mètode NO vàlid: {opcio.lower()}. Els mètodes acceptats són: ('rec_simple', 'rec_colaboratiu', 'rec_contingut')")
    return opcio.lower()

def set_arguments() -> argparse.Namespace:
    """
    Defineix i comprova els arguments de la línia de comandes rebudes.

    Parameters
    ----------
    None
    
    Returns
    -------
    argparse.Namespace
        Un objecte Namespace que conté els arguments de la línia de comandes.

    Examples
    --------
    >>> args = set_arguments()
    >>> print(args.dataset)
    'books'
    >>> print(args.metode)
    'rec_simple'
    """
    ## Iniciem els arguments de argparse
    arguments = argparse.ArgumentParser()

    ## Afegim dos arguments, dataset i metode, comprobem individualment si els rebuts estan dintre de la llista de paràmetres vàlids.
    arguments.add_argument('dataset', type = valid_dataset,  help="El dataset a utilitzar.")
    arguments.add_argument('metode', type = valid_metode, help='El metode de recomanació a aplicar al dataset.')

    ## Retornem els arguments un cop validats.
    args = arguments.parse_args()
    return args

def get_arguments(args: argparse.Namespace) -> tuple:
    """
    Extreu i retorna els arguments de dataset i metode des de l'objecte Namespace.

    Parameters
    ----------
    args : argparse.Namespace
        L'objecte Namespace que conté els arguments analitzats.

    Returns
    -------
    tuple
        Una tupla que conté el dataset i el metode.

    Examples
    --------
    >>> args = set_arguments()
    >>> dataset, metode = get_arguments(args)
    >>> print(dataset)
    'books'
    >>> print(metode)
    'rec_simple'
    """
    dataset = args.dataset
    metode = args.metode
    return dataset, metode
