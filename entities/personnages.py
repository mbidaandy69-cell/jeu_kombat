#coding: utf-8


PERSONNAGES= {
    "kenzo": {
        "nom": "kenzo",
        "dossier": "personnages/kenzo",
        "vie": 100,
        "vitesse": 6,
        "force_saut": 18,
        "boite": (70, 178),
        "animations": {
            "repos": ("idle.png", 6),
            "marche": ("walk.png", 8),
            "saut": ("jump.png", 4),
            "touche": ("hurt.png", 4),
            "ko": ("ko.png", 6),
        },
        "coups": [
            
            {"image": "attack1.png", "nb_images": 6, "duree": 24, "actif": (3, 4), "degats": 8, "portee": 100},
            {"image": "attack2.png", "nb_images": 6, "duree": 24, "actif": (3, 4), "degats": 8, "portee": 100},
            {"image": "attack3.png", "nb_images": 7, "duree": 35, "actif": (4, 5), "degats": 14, "portee": 90},
        ]
    },
    
    
    "gorak": {
        "nom": "gorak",
        "dossier": "personnages/gorak",
        "vie": 140,
        "vitesse": 4,
        "force_saut": 15,
        "boite": (96, 198),
        "animations": {
            "repos": ("idle.png", 6),
            "marche": ("walk.png", 8),
            "saut": ("jump.png", 4),
            "touche": ("hurt.png", 4),
            "ko": ("ko.png", 6),
        },
        "coups": [
            
            {"image": "attack1.png", "nb_images": 6, "duree": 30, "actif": (2, 3), "degats": 14, "portee": 75},
            {"image": "attack2.png", "nb_images": 7, "duree": 42, "actif": (4, 5), "degats": 24, "portee": 85},
        ]
    },
    
        "zephyr": {
        "nom": "Zephyr",
        "dossier": "personnages/zephyr",
        "vie": 85,
        "vitesse": 8,
        "force_saut": 22,
        "boite": (60, 165),
        "animations": {
            "repos": ("idle.png", 6),
            "marche": ("walk.png", 8),
            "saut": ("jump.png", 4),
            "touche": ("hurt.png", 4),
            "ko": ("ko.png", 6),
        },
        "coups": [
            
            {"image": "attack1.png", "nb_images": 4, "duree": 16, "actif": (1, 2), "degats": 5, "portee": 50},
            {"image": "attack2.png", "nb_images": 4, "duree": 16, "actif": (1, 2), "degats": 6, "portee": 60},
            {"image": "attack3.png", "nb_images": 5, "duree": 20, "actif": (1, 2), "degats": 9, "portee": 70},
            {"image": "attack4.png", "nb_images": 6, "duree": 30, "actif": (2, 4), "degats": 13, "portee": 75},
        ]
    }
}