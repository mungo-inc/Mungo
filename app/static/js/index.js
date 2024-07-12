const ajouterButtons = document.querySelectorAll(".btn-recettes");
const retirerPanierButtons = document.getElementById("collapseOne");
const viderPanierButton = document.getElementsByClassName("btn-vider")[0];
const defilement  = document.getElementById("customRange1");
const defilementOut = document.getElementById("montant-budget");
const nombreRecettePanier = document.getElementById("notification-cart");
const afficherEcranConnexionBtn = document.querySelector(".login-btn");
const connecterEnregistrerLien = document.querySelectorAll(".form-box .lien-creation-compte a");
const afficherEcranEnregistrer = document.querySelector(".formulaire-popup");
const sauvegarderButton = document.getElementById("save-list-btn");

const fermerConnexionBtn = document.getElementById("fermer-connexion");
let compteur = 0;
let restants = []; // {idAliment, qteRestante, aDejaEteEnlever}


connecterEnregistrerLien.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        afficherEcranEnregistrer.classList[link.id === "lien-inscription" ? 'add' : 'remove']("afficher-enregistrer");
        if (link.id === "lien-inscription") {
            document.getElementById("courriel-r").focus();
        } else {
            document.getElementById("courriel").focus();
        }
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
        setTimeout(function() {
                document.getElementById("courriel").focus();
            }, 250);
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
            montrerTotalPanier();
            montrerButton('btn-close');
            montrerButton('btn-vider');
            montrerButton('save-list-btn');
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
        updaterRestants.call(this, restants);
        updaterPrixPage(restants);
        let message = "La recette a été ajouté au panier."
        ajouterNombrePanier(message);
    });
});

function updaterRestants(restants) {
    let idRecette = this.getAttribute('data-id-recette');
    document.querySelectorAll('p.r' + idRecette).forEach (elem => {
        let idAliment = parseInt(elem.getAttribute('data-id-aliment'));
        let qteAliment = parseFloat(elem.getAttribute('data-quantite-aliment'));
        let qteRecette = parseFloat(elem.getAttribute('data-quantite-recette'));
        let qteRestante = qteAliment - qteRecette;
        let alimentExiste = restants.some(aliment => aliment.idAliment === idAliment);
        console.log(alimentExiste);
        console.log(restants);
        if (!alimentExiste && qteRestante >= 0) {
            restants.push({idAliment, qteRestante});
        } else if (!alimentExiste && elem.getAttribute("data-type-aliment") != 'p') {
            while (qteRestante < 0) {
                qteAliment += qteAliment;
                qteRestante = qteAliment - qteRecette;
            }
            restants.push({idAliment, qteRestante});
        } else if (!alimentExiste) {
            restants.push({idAliment, qteRestante: 0});
        } else if (elem.getAttribute("data-type-aliment") != 'p') {
            modifierQteRestante(restants, idAliment, qteRestante - qteRecette, qteAliment);
        }
    });
}

function modifierQteRestante(restants, idAliment, nouvelleQte, qteAliment) {
    let aliment = restants.find(aliment => aliment.idAliment === idAliment);
    if (aliment) {
        aliment.qteRestante = nouvelleQte;
        while (aliment.qteRestante < 0) {
            aliment.qteRestante += qteAliment;
        }
    }
}

function updaterPrixPage(restants) {
    let div = document.querySelector('div.liste-recettes.conteneur-recettes');
    restants.forEach(restant =>  {
        for (let childDiv of div.children) {
            let idRecette = childDiv.id;
            childDiv.querySelectorAll('p.r' + idRecette).forEach(p => {
                if (parseInt(p.getAttribute('data-id-aliment')) === restant.idAliment) {
                    if (parseInt(p.getAttribute('data-quantite-recette')) < restant.qteRestante) {
                        let prix = parseFloat(childDiv.querySelector('p .prix-recette').textContent);
                        childDiv.querySelector('p .prix-recette').textContent = prix - parseFloat(p.getAttribute('data-prix-aliment'));
                    }
                }
            });
        }
    });
}

function montrerTotalPanier() {
    let total = document.getElementById('total-panier');
    total.hidden = false;
}

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
        retirerRecettes(parents[0], listeEpicerie, listeEpicerie[0].nomRecette);
    }
});

if (sauvegarderButton) {
sauvegarderButton.addEventListener("click", function() {
    let accordionBodies = document.querySelectorAll('.accordion-body');
    let listeASauvegarder = [];
    accordionBodies.forEach(body => {
        let idRecette = body.querySelector('strong').getAttribute('data-id-recette')
        let nomRecette = body.querySelector('strong').textContent;
        let lis = body.querySelectorAll('li');
        aliments = [];
        lis.forEach(li => {
            aliments.push({
                id: li.getAttribute('data-id-aliment'), 
                nom: li.textContent.trim() 
            });
        });
        listeASauvegarder.push({
            id: idRecette, 
            nom: nomRecette, 
            aliments: aliments
        });
    });
    fetch('/sauvegarder-liste', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(listeASauvegarder)
    })
    .then(response => response.json())
    .then(response => {
        let child = afficherSucces(response.message);
        setTimeout(function() {
            enleverSucces(child);
            setTimeout(function() {
                suppressionMessageAlerte(child);
            }, 1500);
        }, 5000);
    })
});
}

function estCloseButtonRecette(target) {
    return target.classList.contains('btn-close-recette');
}

function estCloseButtonAliment(target) {
   return target.classList.contains('btn-close-aliment');
}

function retirerRecettes(parentElem, listeEpicerie, nomRecette) {
    let recette = listeEpicerie.find(r => r.nomRecette === nomRecette);
    let index = listeEpicerie.indexOf(recette);
    if (index > -1) {
        listeEpicerie.splice(index, 1);
    }
    parentElem.remove();
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    if (listeEpicerie.length === 0) {
        afficherAucunItem(document.getElementById('accordion-content'));
    }
}

function retirerAliment(parentElem, listeEpicerie, nomRecette, li) {
    let nomAliment = li.textContent;
    let recette = listeEpicerie.find(r => r.nomRecette === nomRecette);
    index = listeEpicerie.indexOf(recette);
    let aliment = listeEpicerie[index].items.find(a => a.nom === nomAliment);
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
    strongs[index].textContent = this.getAttribute('data-nom-recette');
    let idRecette = document.createAttribute('data-id-recette');
    idRecette.value = this.getAttribute('data-id-recette');
    strongs[index].setAttributeNode(idRecette);
    idRecette = this.getAttribute('data-id-recette');
    let aliments = document.querySelectorAll('.r' + idRecette);
    let ul = document.querySelectorAll('.accordion-body ul');
    listerAliment(ul, aliments, index);
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    setTimeout(function() {
        enleverSucces();
    }, 5000);
}

function montrerButton(className) {
    let button = document.getElementsByClassName(className);
    if (button[0] != null) {
        button[0].hidden = false;
    }
}

function ajouterNombrePanier(message) {
    let child = afficherSucces(message);
    incrementerNumeroRecette();
    setTimeout(function() {
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
        let idAliment = document.createAttribute('data-id-aliment');
        idAliment.value = aliments[i].getAttribute('data-id-aliment');
        li.setAttributeNode(idAliment);
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
        let nomRecette = accordions[i].querySelector('strong').textContent;
        let idRecette = accordions[i]
            .querySelector('strong')
            .getAttribute('data-id-recette');
        let items = extraireItems(accordions[i]);
        listeEpicerie.push(
            { idRecette: idRecette, nomRecette: nomRecette, items: items }
        );
    }
    return listeEpicerie;
}

function extraireItems(accordion) {
    let ul = accordion.querySelector('ul');
    const items = [];
    let lis = ul.querySelectorAll('li');
    for (let j = 0; j < lis.length; j++) {
        items.push({ id: lis[j].getAttribute('data-id-aliment'), nom: lis[j].textContent });
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
    let div = document.getElementById('accordion-content');
    div.innerHTML = '';
    if (listeEpicerie.length === 0) {
        afficherAucunItem(div);
    } else {
        for (let i = 0; i < listeEpicerie.length; i++) {
            ajouterRecetteAuDiv(div, listeEpicerie[i], i);
        }
        montrerTotalPanier();
        calculerTotalPanier();
    }
}

function calculerTotalPanier() {
    restants = []; // { idAliment, qteRestante }
    
}

function updatePrixResultat() {

}

function afficherAucunItem(div) {
    div.innerHTML = `
        <div class="accordion-body">
            <button type="button" class="btn-close btn-close-recette" aria-label="Close" hidden></button>
            <strong>Aucun item</strong>
            <ul></ul>
        </div>`;
    let button = document.getElementsByClassName('btn-vider');
    let saveButton = document.getElementById('save-list-btn');
    if (saveButton != null) {
        saveButton.hidden = true;
    }
    let total = document.getElementById('total-panier');
    total.hidden = true;
    button[0].hidden = true;
}

function ajouterRecetteAuDiv(div, entree, index) {
    div.innerHTML += `
        <div class="accordion-body">
            <button type="button" class="btn-close btn-close-recette" aria-label="Close"></button>
            <strong data-id-recette="${entree.idRecette}">${entree.nomRecette}</strong>
            <ul></ul>
        </div>`;
    
    const ul = div.querySelectorAll('.accordion-body ul')[index];
    for (let j = 0; j < entree.items.length; j++) {
        let li = document.createElement('li');
        let button = creerCloseButton();
        li.append(button);
        let idAliment = document.createAttribute('data-id-aliment');
        idAliment.value = entree.items[j].id;
        li.setAttributeNode(idAliment);
        li.innerHTML += entree.items[j].nom;
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
