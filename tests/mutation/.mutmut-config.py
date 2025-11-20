"""
Configuration pour les tests de mutation avec mutmut.

Ce fichier définit les paramètres pour exécuter les tests de mutation
sur le projet contract-test-generation.
"""


def pre_mutation(context):
    """
    Hook exécuté avant chaque mutation.
    Permet de filtrer certaines mutations si nécessaire.
    """
    # Ignorer les mutations dans les docstrings
    if context.current_source_line.strip().startswith('"""'):
        context.skip = True

    # Ignorer les mutations dans les commentaires
    if context.current_source_line.strip().startswith('#'):
        context.skip = True


def post_mutation(context):
    """
    Hook exécuté après chaque mutation.
    Permet de faire des vérifications post-mutation.
    """
    pass
