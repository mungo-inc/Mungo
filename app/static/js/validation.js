document.getElementById("courriel").addEventListener("change" , () => {
    verifierChamp("courriel", "err-courriel", "Veuillez entrer une adresse courriel valide.");

});

document.getElementById("password").addEventListener("change", () => {
    verifierChamp("password", "err-password", "Le mot de passe ne peut pas être vide.");
});

document.getElementById("courriel-r").addEventListener("change" , () => {
    verifierChamp("courriel-r", "err-courriel-r", "Veuillez entrer une adresse courriel valide.");
});

document.getElementById("password-r").addEventListener("change", () => {
    verifierChamp("password-r", "err-password-r", "Le mot de passe ne peut pas être vide.");
});

document.getElementById("nom-recette").addEventListener("change", () => {
    verifierChamp("nom-recette", "err-titre", "Le titre ne peut pas être vide.");
});

document.getElementsByClassName("liste-ingredients")[0].addEventListener("change", () => {
    verifierNombreIngredient();
});
console.log(document.getElementsByClassName("liste-ingredients")[0]);

document.getElementById("form-inscription").addEventListener("submit", function(event) {
    if(verifierSpanInscription()) {
        event.preventDefault();
    }
});

document.getElementById("form-connexion").addEventListener("submit", function(event) {
    if(verifierSpanConnexion()) {
        event.preventDefault();
    }
});

document.getElementById("form-recette").addEventListener("submit", function(event) {
    if(verifierTitreExiste()) {
        event.preventDefault();
    }
});

function verifierChamp(id, erreur, message) {
    let titre = document.getElementById(id).value;
    if (titre == "") {
        ecrireErreur(erreur, message);
    } else {
        let span = document.getElementById(erreur);
        span.textContent = "";
    }
}

function verifierNombreIngredient() {
    console.log("----------------------")
    let nbrIngredient = document.getElementsByClassName("liste-ingredients").length;
    console.log(nbrIngredient);
    for (let i = 0; i < nbrIngredient; i++) {
        console.log("----------------------")
        if (nbrIngredient[i].value == "") {
            console.log("err-item-selectionne-" + i);
            ecrireErreur("err-item-selectionne-" + i, "Vous devez sélectionner un ingrédient");
        }
    }
}

//Retourne vrai s'il y a un message d'erreur non-vide
function verifierSpanConnexion(){
    let span0 = document.getElementById("err-courriel").innerHTML;
    let courriel = document.getElementById("courriel").value;
    let span1 = document.getElementById("err-password").innerHTML;
    let motDePasse = document.getElementById("password").value;

    return(span0 != "" || span1 != "" || motDePasse == "" || courriel == "")
}

function verifierSpanInscription(){
    let span0 = document.getElementById("err-courriel-r").innerHTML;
    let courriel = document.getElementById("courriel-r").value;
    let span1 = document.getElementById("err-password-r").innerHTML;
    let motDePasse = document.getElementById("password-r").value;

    return(span0 != "" || span1 != "" || motDePasse == "" || courriel == "")
}

//Valide une adresse courriel avec un regex
function estUneAdresseCourriel(valeur) {
    let regex = /^\w+@\w+.\w{2,}$/;
    return regex.test(valeur);
}

function ecrireErreur(id, message) {
    let span = document.getElementById(id);
    span.textContent = message; 
    span.style.color = "red";
}
