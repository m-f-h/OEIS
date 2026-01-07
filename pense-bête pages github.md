----
Pour avoir une page username.github.io/repo, il suffit de
- créer le répo `repo`
- dans ["Settings" -> Pages](https://github.com/m-f-h/OEIS/settings/pages), activer la publication
- C'est tout! 
- Jekyll est automatiquement activé, sauf si on crée un fichier .nojekyll; dans ce cas tous les fichiers sont publiés "tels quels"<br/>
  (permet de "debloquer" de déploiement si la compilation Jekyll plante (auqeul cas il n'y aurait pas de site visible du tout)
- Les fichiers .html apparaissent en tant que tels
- Les fichiers .md *doivent* impérativement avoir une en-tête Jekyll (c-à-d. un `----` au début), même si elle est vide;<br/>
  elles apparaissent après avec le même nom mais extension .html
- En particulier, cela s'applique pour index.md / index.html
  - aussi bien à la racine que dans les sous-répertoires
- Le thème par défaut affiche
  - un "menu de navigation" dans l'en-tête de la page,
  - le README.md dans le footer de la page
- TO DO: add more about jekyll themes
