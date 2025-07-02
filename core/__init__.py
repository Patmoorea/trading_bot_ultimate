# Initialisation optimisée M4 avec gestion d'erreurs
try:
    from .performance import optimize_for_m4
    # Initialisation au chargement du module
    optimize_for_m4()
    # Alias pour compatibilité
    configure_m4_precision = optimize_for_m4
except ImportError as e:
    # Fallback si tensorflow n'est pas disponible
    def optimize_for_m4():
        """Fallback function when tensorflow is not available"""
        pass
    configure_m4_precision = optimize_for_m4
