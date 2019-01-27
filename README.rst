types Q, U, D, f

.. line-block::

    mul Q -> Q -> Q # 1
    mul Q -> U -> Q
    mul U -> Q -> Q
    mul Q -> f -> Q # 2
    mul f -> Q -> Q # 2
    mul U -> U -> U # 3
    mul U -> f -> Q # 3
    mul f -> Q -> Q
    mul D -> D -> D

^^ ditto div

.. line-block::

    pow Q -> f -> Q
    pow U -> f -> U
    pow D -> f -> D



units:

.. line-block::
    u * u -> u
    u / u -> u
    u ** f -> u
