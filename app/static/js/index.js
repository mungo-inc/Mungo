// document.getElementsByClassName("btn-recettes").addEventListener("click", ajouterRecetteAuMenu);
const buttons = document.querySelectorAll(".btn-recettes");
const defilement  = document.getElementById("customRange1");
const defilement_out = document.getElementById("montant-budget");
defilement_out.innerHTML = defilement.value;
defilement.oninput = function(){defilement_out.innerHTML = this.value;}

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


