----
Pour avoir une page username.github.io/repo, il suffit de
- créer le répo `repo`
- dans ["Settings" -> Pages](https://github.com/m-f-h/OEIS/settings/pages), activer la publication
- C'est tout! 
- Jekyll est automatiquement activé, sauf si on crée un fichier .nojekyll
- Les fichiers .html apparaissent en tant que tels
- Les fichiers .md *doivent* impérativement avoir une en-tête Jekyll (c-à-d. un `----` au début), même si elle est vide;<br/>
  elles apparaissent après avec le même nom mais extension .html
- En particulier, cela s'applique pour index.md / index.html
- aussi bien à la racine que dans les sous-répertoires
- Le thème par défaut affiche un "menu de navigation" dans l'en-tête de la page
- TO DO: add more about jekyll themes
