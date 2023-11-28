# Test de scène (PBRT 4, MTI882, Mitsuba 3)

Ce référentiel Git contient la scène de test pour les moteurs de rendu suivants :
- MTI882 (C++ ou Rust)
- PBRT 4 (C++)
- Mitsuba 3 (Python) _(* recommandé pour la comparaison)_

Veuillez vous référer à la documentation pour la définition des matériaux : 
- [PBRT File Format v4 - Materials](https://pbrt.org/fileformat-v4#materials)
- [Mitsuba v3 - BSDFs](https://mitsuba.readthedocs.io/en/latest/src/generated/plugins_bsdfs.html)

Les images pour le diffus se trouve dans le dossier `images`.

## MTI882

Pour éditer le matériau, ouvrez `test00001.json` et éditez le premier matériau (ligne 19) nommé "case".

Rendu MTI882: 

![Diffuse from MTI882](images/mti882_diffuse.png)

## PBRT-v4

Code: https://github.com/mmp/pbrt-v4
```bash
git clone --recursive https://github.com/mmp/pbrt-v4.git
```

Pour éditer le matériau, ouvrez `test00001.pbrt` et éditez le premier matériau (ligne 26) nommé "case".

**Problèmes connus**
- Décalage potentiel des textures

Rendu PBRT-v4:

![Diffuse from MTI882](images/pbrt_diffuse.png)

Comparaison avec MTI882:

![Diffuse from MTI882](images/pbrt_diff.png)


### Mitsuba 3 

Installation et génération. Vous devez avoir Python installer sur votre systeme. 
```bash
pip install --user mitsuba
python mitsuba3.py
```

Pour éditer le matériau, ouvrez `test00001.xml` et éditez le premier matériau (ligne 27) nommé "case".

Rendu Mitsuba 3:

![Diffuse from MTI882](images/mitsuba3_diffuse.png)

Comparaison avec MTI882:

![Diffuse from MTI882](images/mitsuba3_diff.png)
