# Q8 Post-Mortem

## Le problème

Après la fin du hackaton, je ne comprenais toujours pas pourquoi ma
solution au problème #8 ne fonctionnait pas. J'ai donc passé environ
2h vendredi soir à nettoyer mon code Python pour trouver le bug, sans
succès. Je me suis dit que peut-être le problème était dans une subtilité
de Python. J'ai donc converti ma solution en C++ samedi matin. Celle-ci
me donnait exactement le même résultat que la version Python! Étrange.

## L'investigation

J'ai donc cloné le repo git et compilé la solution officielle, en C#.
Et celli-ci foncitonnait parfaitement! J'ai comparé le code de la solution
C# et il était 100% équivalent à mes solutions!

J'ai donc roulé ma version Python et la solution C# pas-à-pas pour voir
où se trouvait la différence. Or il s'avert que le problème était très
subtil... et qu'il se trouvait dans la solution C# et donc dans l'énoncé
du problème #8.

Le noeud du problème est l'affirmation du problème que les fichiers d'entrés
sont encodés en ASCII et doivent être lus ainsi. Or le programme C# lit les
fichiers d'entrées en mode texte en Unicode! (Plus précisément, UTF-8.)
Heureusement, l'encodage Unicode correspond à 100% à ASCII pour les codes
0-127, donc pour le texte normal. Mais... pour ce qui est des codes au-delà,
et en particulier pour les valeurs 8-bits entre 128-255.

Mais il y avait un autre problème qui rendait la chose encore plus
complexe. En UTF-8, les quand l'encodage d'un caractère commence par
un byte entre 128-255, il lit plusieurs byte, mais certaines séquences
sont illégales. Or le fichier d'entrée contenait plusieurs séquences
illégales. Or, le langage C# traite les séquences illégales différemment
que C++ et Python. Donc, même si on aurait lu le fichier en mode texte
avec l'encodage UTF-8, on ne pouvait pas avoir le même résultat.
Il fallait écrire la solution en C#.

## La validation

J'ai ensuite écrit une fonction Python qui émule le comportement de C#
en lisant le fichier en mode UTF-8, en mettant un mode d'erreur de décodage
spécifique et en reconvertissant les caractères illégaux en post-process.
En ajoutant cette conversion spéciale, ma solution fonctionne. Ouf!

## Post-mortem

Les leçons à retenir pour les futurs hackaton:

- Fournir les fichiers en pur ASCII si possible.
- Écrire un petit programme qui valide qu'un fichier et pur ASCII.
- Dans les cas ou un fichier binaire doit être fournit, le lire en
  binaire, byte par byte.
- Écrire chaque solution dans plusieurss langages pour éviter les
  comportements spécifiques subtils liés aux langages.

Un programme de validation de fichiers ASCII et des unit-tests pour
celui-ci sont fournit: `pure_ascii.py` et `test_pure_ascii.py`.
