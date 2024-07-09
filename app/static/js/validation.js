document.getElementById("courriel").addEventListener("change" , () => {
    verifierCourriel("courriel", "err-courriel");

});

document.getElementById("password").addEventListener("change", () => {
verifierMotDePasse("password", "err-password");
});

document.getElementById("courriel-r").addEventListener("change" , () => {
verifierCourriel("courriel-r", "err-courriel-r");
});

document.getElementById("password-r").addEventListener("change", () => {
verifierMotDePasse("password-r", "err-password-r");
});

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

function verifierMotDePasse(id, erreur){
    let motDePasse = document.getElementById(id).value;

    if (motDePasse == ""){
        ecrireErreur(erreur, "Le mot de passe ne peut être vide")
    } else {
        let span = document.getElementById(erreur);
        span.textContent = "";
    }
}

function verifierCourriel(id, erreur){
    let courriel = document.getElementById(id).value;
    if(!(estUneAdresseCourriel(courriel))){
        ecrireErreur(erreur,"Veuillez entrer une adresse courriel valide")
    }else {
        let span = document.getElementById(erreur);
        span.textContent = "";
    }
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
