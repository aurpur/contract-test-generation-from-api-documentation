"""
===============================================================================
Reporting Utilities for Experiment Notebooks
===============================================================================

OBJECTIF:
    Fournit des utilitaires de style publication pour les graphiques 
    matplotlib/seaborn dans les notebooks d'expérimentation.

FONCTIONNALITÉS:
    - PublicationStyle: Configuration cohérente pour tous les graphiques
    - apply_publication_style: Applique le style aux figures
    - save_figure: Sauvegarde multi-format (PNG, PDF) pour publication

USAGE DANS LES NOTEBOOKS:
    from experiments.reporting_utils import (
        PublicationStyle, 
        apply_publication_style, 
        save_figure
    )
    
    # Appliquer le style au début du notebook
    apply_publication_style()
    
    # Sauvegarder les figures pour publication
    save_figure(fig, Path("results/figures/my_chart"))

Auteur: Aurel IKAMA HONEY
Date: December 11, 2025
===============================================================================
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
import seaborn as sns


# ==============================================================================
# CONFIGURATION DE STYLE PUBLICATION
# ==============================================================================

@dataclass
class PublicationStyle:
    """
    Configuration pour le style de graphiques de qualité publication.
    
    Attributes:
        seaborn_style: Style seaborn (whitegrid, darkgrid, etc.)
        seaborn_context: Contexte (paper, notebook, talk, poster)
        font_scale: Échelle de police (1.0 = normal, 1.2 = plus grand)
        palette: Palette de couleurs (colorblind recommandé pour accessibilité)
        rc_params: Paramètres matplotlib additionnels
    """
    
    seaborn_style: str = "whitegrid"
    seaborn_context: str = "paper"
    font_scale: float = 1.2
    palette: str = "colorblind"  # Palette accessible aux daltoniens
    rc_params: dict = field(default_factory=dict)


# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================

def apply_publication_style(style: Optional[PublicationStyle] = None) -> None:
    """
    Applique un style cohérent de qualité publication aux graphiques.
    
    Cette fonction doit être appelée au début de chaque notebook pour
    garantir une apparence uniforme de tous les graphiques.
    
    Args:
        style: Configuration PublicationStyle. Utilise les défauts si None.
    
    Example:
        >>> apply_publication_style()
        >>> # Tous les graphiques suivants auront le style publication
    """
    if style is None:
        style = PublicationStyle()
    
    # Appliquer le style et contexte seaborn
    sns.set_style(style.seaborn_style)
    sns.set_context(style.seaborn_context, font_scale=style.font_scale)
    sns.set_palette(style.palette)
    
    # Paramètres matplotlib par défaut pour publication
    default_rc = {
        "figure.figsize": (8, 5),
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "font.family": "sans-serif",
    }
    default_rc.update(style.rc_params)
    plt.rcParams.update(default_rc)


def save_figure(
    fig: plt.Figure,
    path: Path,
    formats: Optional[List[str]] = None,
    dpi: int = 300,
    bbox_inches: str = "tight",
) -> List[Path]:
    """
    Sauvegarde une figure matplotlib dans plusieurs formats.
    
    Utile pour générer à la fois PNG (web/documentation) et PDF (publication).
    
    Args:
        fig: Figure matplotlib à sauvegarder.
        path: Chemin de base (sans extension).
        formats: Liste des formats (ex: ["png", "pdf"]). 
                 Défaut: ["png", "pdf"].
        dpi: Résolution pour formats raster (PNG).
        bbox_inches: Configuration bounding box.
    
    Returns:
        Liste des chemins où les figures ont été sauvegardées.
    
    Example:
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3], [1, 4, 9])
        >>> paths = save_figure(fig, Path("results/figures/my_chart"))
        >>> print(paths)  # [Path("results/figures/my_chart.png"), ...]
    """
    if formats is None:
        formats = ["png", "pdf"]
    
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    saved_paths = []
    for fmt in formats:
        out_path = path.with_suffix(f".{fmt}")
        fig.savefig(out_path, format=fmt, dpi=dpi, bbox_inches=bbox_inches)
        saved_paths.append(out_path)
    
    return saved_paths
