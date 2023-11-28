# Test de scène (PBRT, MTI882)

Ce référentiel Git contient la scène de test pour les moteurs de rendu suivants :
- MTI882
- PBRT

Veuillez vous référer à la documentation de PBRT pour la définition des matériaux : [PBRT File Format v4 - Materials](https://pbrt.org/fileformat-v4#materials)

## MTI882

Veuillez éditer le premier matériau (nommé "case").

Rendu MTI882: 

![Diffuse from MTI882](images/mti882_diffuse.png)

## PBRT-v4

Code: https://github.com/mmp/pbrt-v4
```bash
git clone --recursive https://github.com/mmp/pbrt-v4.git
```

Veuillez éditer le premier matériau (nommé "case").

**Problèmes connus**
- Décalage potentiel des textures

Rendu PBRT:

![Diffuse from MTI882](images/pbrt_diffuse.png)

Comparaison avec MTI882:

![Diffuse from MTI882](images/pbrt_diff.png)


### Mitsuba 3 

TODO
