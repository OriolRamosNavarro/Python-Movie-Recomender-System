import numpy as np, os

class User:
    """
    Representa un usuari del sistema de recomanacions.

    Atributes
    ---------
    _user : int
        L'ID de l'usuari actual.
    _posicio_user : int
        La posició de l'usuari actual a la matriu de valoracions.
    _matriu_user : np.ndarray
        La matriu de valoracions de l'usuari actual.

    Methods
    -------
    set_user(user: int)
        Estableix l'ID de l'usuari actual.
    get_user()
        Retorna l'ID de l'usuari actual.
    set_posicio_user(posicio: int)
        Estableix la posició de l'usuari actual a la matriu de valoracions.
    get_posicio_user()
        Retorna la posició de l'usuari actual a la matriu de valoracions.
    set_matriu_user(matriu: np.ndarray)
        Estableix la matriu de valoracions de l'usuari actual.
    get_matriu_user()
        Retorna la matriu de valoracions de l'usuari actual.
    __str__(self, valor)
        Converteix l'objecte en una cadena de text per a la seva impressió per pantalla.
    """
    _user = None
    _posicio_user = None
    _matriu_user = None

    @classmethod
    def set_user(cls, user: int) -> None:
        """
        Estableix l'ID de l'usuari actual.

        Parameters
        ----------
        user : int
            L'ID de l'usuari.

        Return
        ------
        None
        """
        cls._user = user

    @classmethod
    def get_user(cls) -> int:
        """
        Retorna l'ID de l'usuari actual.

        Parameters
        ----------
        None

        Return
        ------
        int
            Número d'usuari previament establert.
        """
        return cls._user    
    
    @classmethod
    def set_posicio_user(cls, posicio: int) -> None:
        """
        Estableix la posició de l'usuari actual a la matriu de valoracions.

        Parameters
        ----------
        posicio : int
            Posició del usuari a la matriu
        
        Return
        ------
        None
        """
        cls._posicio_user = posicio

    @classmethod
    def get_posicio_user(cls) -> int:
        """
        Retorna la posició de l'usuari actual a la matriu de valoracions.

        Parameters
        ----------
        None

        Return
        ------
        int
            Posició del usuari a la matriu de valoracions.
        """
        return cls._posicio_user

    @classmethod
    def set_matriu_user(cls, matriu: np.ndarray) -> None:
        """
        Estableix la matriu de valoracions de l'usuari actual.

        Parameters
        ----------
        matriu : np.ndarray
        
        Return
        ------
        None
        """
        cls._matriu_user = matriu

    @classmethod
    def get_matriu_user(cls) -> np.ndarray:
        """
        Retorna la matriu de valoracions de l'usuari actual.

        Parameters
        ----------
        None

        Return
        ------
        np.ndarray
            Matriu de valoracions.
        """
        return cls._matriu_user

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
