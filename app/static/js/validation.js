const ingredientsDiv = document.getElementById("ingredients-conteneur");
const ingredientsQuantiteDiv = document.getElementById("ingredients");
const courriel = document.getElementById("courriel");
const password = document.getElementById("password");
const courrielR = document.getElementById("courriel-r");
const passwordR = document.getElementById("password-r");
const nomRecette = document.getElementById("nom-recette");
const formInscription = document.getElementById("form-inscription");
const formConnexion = document.getElementById("form-connexion");
const formAvis = document.getElementsByClassName("formulaire-avis")[0];
const formRecette = document.getElementById("form-recette");


if (courriel) {
    courriel.addEventListener("change" , () => {
        verifierChamp("courriel", "err-courriel", "Veuillez entrer une adresse courriel valide.");
    });
}

if (password) {
    password.addEventListener("change", () => {
        verifierChamp("password", "err-password", "Le mot de passe ne peut pas être vide.");
    });
}

if (courrielR) {
    courrielR.addEventListener("change" , () => {
        verifierChamp("courriel-r", "err-courriel-r", "Veuillez entrer une adresse courriel valide.");
    });
}

if (passwordR) {
    passwordR.addEventListener("change", () => {
        verifierChamp("password-r", "err-password-r", "Le mot de passe ne peut pas être vide.");
    });
}

if (nomRecette) {
    nomRecette.addEventListener("change", () => {
        verifierChamp("nom-recette", "err-titre", "Le titre ne peut pas être vide.");
    });
}

if (formInscription) {
    formInscription.addEventListener("submit", function(event) {
        if(verifierSpanInscription()) {
            event.preventDefault();
        }
    });
}

if (formConnexion) {
    formConnexion.addEventListener("submit", function(event) {
        if(verifierSpanConnexion()) {
            event.preventDefault();
        }
    });
}

if (formAvis) {
    formAvis.addEventListener("submit", function(event) {
        if(verifierNoteNomAvis()) {
            event.preventDefault();
        }
    });
}

if (formRecette) {

    formRecette.addEventListener("submit", function(event) {
        verifierQuantiteIngredient();
        verifierNombreIngredient();
        verifierChamp("nom-recette", "err-titre", "Le titre ne peut pas être vide.");
        if(confirmationEnvoieRecette()) {
            event.preventDefault();
        }
    });
}

if (ingredientsDiv) {
    ingredientsDiv.addEventListener("change", function(event) {
        verifierNombreIngredient();
    });
}

if (ingredientsQuantiteDiv) {
    ingredientsQuantiteDiv.addEventListener("change", function(event) {
        verifierQuantiteIngredient();
    });
}

function verifierNoteNomAvis() {
    let nom = document.getElementById("nom-avis").innerHTML;
    let avis = document.getElementById("avis-avis").innerHTML;
    let note = document.getElementById("note").value;
    return nom == "" && avis == "" && note == "";
}

function confirmationEnvoieRecette() {
    let titre = document.getElementById("nom-recette").value;
    let span = document.getElementById("err-titre").innerHTML;
    let nbrIngredient = document.getElementsByClassName("liste-ingredients").length;
    let ingredientClass = document.getElementsByClassName("liste-ingredients");
    let ingredientListe = [];
    let ingredientErreur = [];
    for (let i = 0; i < nbrIngredient; i++) {
        let variable = ("err-item-selectionne-" + i);
        ingredientListe.push(ingredientClass[i].value);
        ingredientErreur.push(document.getElementById(variable).innerHTML);
    }
    let ingredientQuantiteListe = [];
    let ingredientQuantiteErreur = [];
    for (let i = 0; i < nbrIngredient; i++) {
        let variable2 = ("err-item-selectionne-" + i);
        let ingredientQuantite = document.getElementById("selected-ingredient-"+i).querySelector("input");
        console.log(ingredientQuantite);
        console.log("Regarde en haut");
        if (ingredientQuantite != null){
            ingredientQuantiteListe.push(ingredientQuantite.value);
        } else {
            ingredientQuantiteListe.push("");
        }
        ingredientQuantiteErreur.push(document.getElementById(variable2).innerHTML);
    }

    return (titre == "" || span != "" || ingredientListe.some(str => str === '') || ingredientErreur.some(str => str != '') || ingredientQuantiteListe.some(valeur => valeur === '' || isNaN(valeur)) || ingredientQuantiteErreur.some(str => str != ''));
}

function verifierChamp(id, erreur, message) {
    let titre = document.getElementById(id).value;
    if (titre == "") {
        ecrireErreur(erreur, message);
    } else {
        let span = document.getElementById(erreur);
        span.textContent = "";
    }
}

function verifierQuantiteIngredient() {
    let nbrIngredient = document.getElementsByClassName("liste-ingredients").length;
        for (let i = 0; i < nbrIngredient; i++) {
            let variable = "selected-ingredient-"+i; 
            let ingredientQuantite = document.getElementById(variable).querySelector("input");
            erreur = "err-selected-ingredient-"+i;
            if (ingredientQuantite == null) {
            } else if (ingredientQuantite.value == "") {
                ecrireErreur(erreur, "Le champ ne peut pas être vite");
            } else if (isNaN(ingredientQuantite.value))  {
                ecrireErreur(erreur, "Le champ doit être un nombre");
            } else {
                document.getElementById(erreur).textContent = "";
        }
    }
}

function verifierNombreIngredient() {
    let nbrIngredient = document.getElementsByClassName("liste-ingredients").length;
    let ingredientClass = document.getElementsByClassName("liste-ingredients");
    for (let i = 0; i < nbrIngredient; i++) {
        if (ingredientClass[i].value == "") {
            ecrireErreur("err-item-selectionne-" + i, "Vous devez sélectionner un ingrédient");
        } else {
            let variable = "err-item-selectionne-" + i;
            document.getElementById(variable).textContent = "";
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
