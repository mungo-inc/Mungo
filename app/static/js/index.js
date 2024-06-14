// document.getElementsByClassName("btn-recettes").addEventListener("click", ajouterRecetteAuMenu);
const buttons = document.querySelectorAll(".btn-recettes");

/**
 *
 */
buttons.forEach(function(button) {
    button.addEventListener("click", function() {
        let ul = document.getElementById('liste-epicerie');
        let li = document.createElement('li');
        //  aller chercher liste ingredient de la recette cliqué
        let recette = this.parentElement;
        li.innerText = recette.querySelector('h2').innerText
        ul.append(li)
    });
});
