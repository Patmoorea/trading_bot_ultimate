class Config:
    # Configuration Numba
    USE_NUMBA = True  # Mettez False si Numba n'est pas installé
    
    # Configuration GPU/CPU
    USE_GPU = True
    
    # Paramètres de trading
    MAX_DRAWDOWN = 0.05
    DAILY_STOP_LOSS = 0.02
    
    # Debug
    DEBUG = False
    LOG_LEVEL = 'INFO'
