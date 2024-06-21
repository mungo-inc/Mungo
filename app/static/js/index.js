// document.getElementsByClassName("btn-recettes").addEventListener("click", ajouterRecetteAuMenu);
const buttons = document.querySelectorAll(".btn-recettes");
const defilement  = document.getElementById("customRange1");
const defilement_out = document.getElementById("montant-budget");

if (defilement != null && defilement_out != null) {
    defilement_out.innerHTML = defilement.value;
    defilement.oninput = function(){defilement_out.innerHTML = this.value;}
}

/**
 *
 */
buttons.forEach(function(button) {
    button.addEventListener("click", function() {
        console.log("Salut")
        let ul = document.getElementById('liste-epicerie');
        let li = document.createElement('li');
        let recette = this.getAttribute('data');
        li.innerText = recette;
        ul.append(li)
    });
});
