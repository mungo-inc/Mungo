const ajouterButtons = document.querySelectorAll(".btn-recettes");
const retirerPanierButtons = document.getElementById("collapseOne");
const viderPanierButton = document.getElementsByClassName("btn-vider")[0];
const defilement  = document.getElementById("customRange1");
const defilementOut = document.getElementById("montant-budget");
const nombreRecettePanier = document.getElementById("notification-cart");
const afficherEcranConnexionBtn = document.querySelector(".login-btn");
const connecterEnregistrerLien = document.querySelectorAll(".form-box .lien-creation-compte a");
const afficherEcranEnregistrer = document.querySelector(".formulaire-popup");

const fermerConnexionBtn = document.getElementById("fermer-connexion");
let compteur = 0;


connecterEnregistrerLien.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        afficherEcranEnregistrer.classList[link.id === "lien-inscription" ? 'add' : 'remove']("afficher-enregistrer");
    });
});


document.addEventListener("DOMContentLoaded", function() {
    chargerListeEpicerie();
    majNombreEpicerie();
});

if (defilement != null && defilementOut != null) {
    defilementOut.innerHTML = defilement.value;
    defilement.oninput = function(){defilementOut.innerHTML = this.value;}
}

if (afficherEcranConnexionBtn) {
    afficherEcranConnexionBtn.addEventListener("click", () => {
        document.body.classList.toggle("afficher-popup");
    });
} else {
    console.error("Element with class 'login-btn' not found.");
}

fermerConnexionBtn.addEventListener("click", () => {
    document.body.classList.toggle("afficher-popup");
});


/**
 *
 */
ajouterButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        let strongs = document.querySelectorAll('.accordion-body strong');
        if (strongs.length === 1 && strongs[0].textContent === 'Aucun item') {
            ajouterElementPanier.call(this, strongs, 0);
            montrerButton('btn-close');
            montrerButton('btn-vider');
        } else {
            let div = document.getElementById('accordion-content');
            div.innerHTML += `
                <div class="accordion-body">
                    <button type="button" class="btn-close btn-close-recette" aria-label="Close"></button>
                    <strong></strong>
                        <ul>
                        </ul>
                </div>`
            let strongs = document.querySelectorAll('.accordion-body strong');
            ajouterElementPanier.call(this, strongs, strongs.length - 1);
        }
        let message = "La recette a été ajouté au panier."
        ajouterNombrePanier(message);
    });
});


retirerPanierButtons.addEventListener("click", function(event) {
    const target = event.target;
    let listeEpicerie = JSON.parse(localStorage.getItem('listeEpicerie'));
    let parentElem = target.closest('.accordion-body');
    if (parentElem) {
        let nomRecette = parentElem.querySelector('strong').textContent;
        if (estCloseButtonRecette(target)) {
            retirerRecettes(parentElem, listeEpicerie, nomRecette);
        } else if (estCloseButtonAliment(target)) {
            let li = target.closest('li');
            retirerAliment(parentElem, listeEpicerie, nomRecette, li);
        }
    }
});

viderPanierButton.addEventListener("click", function() {
    let listeEpicerie = JSON.parse(localStorage.getItem('listeEpicerie'));
    while (listeEpicerie.length) {
        let parents = document.getElementsByClassName('accordion-body');
        retirerRecettes(parents[0], listeEpicerie, listeEpicerie[0].recette);
    }
});

function estCloseButtonRecette(target) {
    return target.classList.contains('btn-close-recette');
}

function estCloseButtonAliment(target) {
   return target.classList.contains('btn-close-aliment');
}

function retirerRecettes(parentElem, listeEpicerie, nomRecette) {
    let recette = listeEpicerie.find(r => r.recette === nomRecette);
    index = listeEpicerie.indexOf(recette);
    if (index > -1) {
        listeEpicerie.splice(index, 1);
    }
    console.log(parentElem);
    parentElem.remove();
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    if (listeEpicerie.length === 0) {
        afficherAucunItem(document.getElementById('accordion-content'));
    }
}

function retirerAliment(parentElem, listeEpicerie, nomRecette, li) {
    let nomAliment = li.textContent;
    let recette = listeEpicerie.find(r => r.recette === nomRecette);
    index = listeEpicerie.indexOf(recette);
    let aliment= listeEpicerie[index].items.find(a => a === nomAliment);
    let indexAliment = listeEpicerie[index].items.indexOf(aliment);
    if (index > -1) {
        listeEpicerie[index].items.splice(indexAliment, 1);
    }
    li.remove();
    sauvegarderListeEpicerie();
    if (listeEpicerie[index].items.length === 0) {
        retirerRecettes(parentElem, listeEpicerie, nomRecette);
    }
}

function ajouterElementPanier(strongs, index) {
    strongs[index].textContent = this.getAttribute('nom-recette');
    recette_id = this.getAttribute('id-recette');
    let aliments = document.querySelectorAll('.r' + recette_id);
    let ul = document.querySelectorAll('.accordion-body ul');
    listerAliment(ul, aliments, index);
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    setTimeout(function(){
        enleverSucces();
    }, 5000);
}

function montrerButton(className) {
    let button = document.getElementsByClassName(className);
    button[0].hidden = false;
}

function ajouterNombrePanier(message) {
    let child = afficherSucces(message);
    incrementerNumeroRecette();
        setTimeout(function(){
        enleverSucces(child);
        setTimeout(function(){
             suppressionMessageAlerte(child);
            compteur--;
        }, 1500);
    }, 5000);
}

function creationMessageAlerte(messageSucces) {
    const message = document.createElement('p');
    message.textContent = messageSucces;
    message.classList.add("alert-success", "alert");
    let topValue;
    if (++compteur == 1) {
         topValue = 15;
    } else {
         topValue = ((compteur - 1) * 60) + 15;
    }
    message.style.top = topValue + "px";
    let divAlerte = document.getElementById('notif-succes').appendChild(message);
    return divAlerte;
}

function suppressionMessageAlerte(child) {
    document.getElementById('notif-succes').removeChild(child);
}

function afficherSucces(message) {
    let child = creationMessageAlerte(message);
    let alerte_id = document.getElementById('notif-succes');
    alerte_id.hidden = false;
    child.hidden = false;
    child.classList.add("alert-animation");
    child.classList.remove("alert-animation-enlever");
    return child;
}


function enleverSucces(child){
    child.classList.add("alert-animation-enlever");
    child.classList.remove("alert-animation");
}


function listerAliment(ul, aliments, index) {
    for (let i = 0; i < aliments.length; i++) {
        let li = document.createElement('li');
        let button = creerCloseButton();
        li.append(button);
        li.innerHTML += aliments[i].textContent;
        ul[index].append(li);
    }
}

function creerCloseButton() {
    let button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn-close btn-close-aliment';
    return button;
}

function sauvegarderListeEpicerie() {
    let accordions = document.querySelectorAll('.accordion-body');
    let listeEpicerie = extraireListeEpicerie(accordions);
    localStorage.setItem('listeEpicerie', JSON.stringify(listeEpicerie));
}

function incrementerNumeroRecette(){
    let recipeCount = localStorage.getItem('notification-cart') || 0;
    recipeCount = parseInt(recipeCount) + 1;
    localStorage.setItem('notification-cart', recipeCount);
    majNombreEpicerie();
}

function majNombreEpicerie() {
    let listeEpicerie = JSON.parse(localStorage.getItem('listeEpicerie'));
    if (listeEpicerie.length) {
        recipeCount = listeEpicerie.length;
        document.getElementById('notification-cart').hidden = false;
        document.getElementById('notification-cart').innerHTML = recipeCount;
    } else {
        document.getElementById('notification-cart').hidden = true;
    }
}

function extraireListeEpicerie(accordions) {
    let listeEpicerie = [];
    for (let i = 0; i < accordions.length; i++) {
        let recette = accordions[i].querySelector('strong').textContent;
        let items = extraireItems(accordions[i]);
        listeEpicerie.push({ recette: recette, items: items });
    }
    return listeEpicerie;
}

function extraireItems(accordion) {
    let ul = accordion.querySelector('ul');
    const items = [];
    let lis = ul.querySelectorAll('li');
    for (let j = 0; j < lis.length; j++) {
        items.push(lis[j].textContent);
    }
    return items;
}

function chargerListeEpicerie() {
    let listeEpicerie = chargerListeLocale();
    afficherListeEpicerie(listeEpicerie);
}

function chargerListeLocale() {
    let listeEpicerie = localStorage.getItem('listeEpicerie');
    if (listeEpicerie) {
        return JSON.parse(listeEpicerie);
    } else {
        return [];
    }
}

function afficherListeEpicerie(listeEpicerie) {
    // let div = document.getElementById('collapseOne');
    let div = document.getElementById('accordion-content');
    div.innerHTML = '';
    if (listeEpicerie.length === 0) {
        afficherAucunItem(div);
    } else {
        for (let i = 0; i < listeEpicerie.length; i++) {
            ajouterRecetteAuDiv(div, listeEpicerie[i], i);
        }
    }
}

function afficherAucunItem(div) {
    div.innerHTML = `
        <div class="accordion-body">
            <button type="button" class="btn-close btn-close-recette" aria-label="Close" hidden></button>
            <strong>Aucun item</strong>
            <ul></ul>
        </div>`;
    let button = document.getElementsByClassName('btn-vider');
    button[0].hidden = true;
}

function ajouterRecetteAuDiv(div, entree, index) {
    div.innerHTML += `
        <div class="accordion-body">
            <button type="button" class="btn-close btn-close-recette" aria-label="Close"></button>
            <strong>${entree.recette}</strong>
            <ul></ul>
        </div>`;
    
    const ul = div.querySelectorAll('.accordion-body ul')[index];
    for (let j = 0; j < entree.items.length; j++) {
        let li = document.createElement('li');
        let button = creerCloseButton();
        li.append(button);
        li.innerHTML += entree.items[j];
        ul.append(li);
    }
}

function ecrireTexteConteneur(texte, container, vitesse, callback) {
    let index = 0;
    function type() {
        if (index < texte.length) {
            container.textContent += texte.charAt(index);
            index++;
            setTimeout(type, vitesse);
        } else {
            if (callback) callback();        }
    }
    type();
}

const texte1 = "Des recettes personnalisées,";
const texte2 = "des courses optimisées";
const conteneur1 = document.querySelector('.phrase1'); 
const conteneur2 = document.querySelector('.phrase2'); 

if (conteneur1 && conteneur2) {
    ecrireTexteConteneur(texte1, conteneur1, 50, () => {
        ecrireTexteConteneur(texte2, conteneur2, 50);
    });
}
  
majNombreEpicerie();

function allerBasPage() {
    document.getElementById('bottom').scrollIntoView();
}
