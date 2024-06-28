const ajouterButtons = document.querySelectorAll(".btn-recettes");
const retirerPanierButtons = document.getElementById("collapseOne");
const defilement  = document.getElementById("customRange1");
const defilement_out = document.getElementById("montant-budget");
const nombre_recette_panier = document.getElementById("notification-cart");
document.addEventListener("DOMContentLoaded", function() {
    chargerListeEpicerie();
    majNombreEpicerie();
});

if (defilement != null && defilement_out != null) {
    defilement_out.innerHTML = defilement.value;
    defilement.oninput = function(){defilement_out.innerHTML = this.value;}
}

/**
 *
 */
ajouterButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        let strongs = document.querySelectorAll('.accordion-body strong');
        if (strongs.length === 1 && strongs[0].textContent === 'Aucun item') {
            ajouterElementPanier.call(this, strongs, 0);
            ajouterCloseButton();
        } else {
            let div = document.getElementById('collapseOne');
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
    });
});

retirerPanierButtons.addEventListener("click", function(event) {
    const target = event.target;
    let listeEpicerie = JSON.parse(localStorage.getItem('listeEpicerie'));
    let parentElem = target.closest('.accordion-body');
    let nomRecette = parentElem.querySelector('strong').textContent;
    if (estCloseButtonRecette(target)) {
        retirerRecettes(parentElem, listeEpicerie, nomRecette);
    } else if (estCloseButtonAliment(target)) {
        let li = target.closest('li');
        retirerAliment(parentElem, listeEpicerie, nomRecette, li);
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
    parentElem.remove();
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    if (listeEpicerie.length === 0) {
        afficherAucunItem(document.getElementById('collapseOne'));
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
    afficherSucces();
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    setTimeout(function(){
        enleverSucces();
    }, 5000);
}

function ajouterCloseButton() {
    let buttons = document.getElementsByClassName('btn-close');
    buttons[0].hidden = false;
}

function afficherSucces(){
    alerte_id = document.getElementById('notif-succes');
    alerte_id.hidden = false;
    alerte_id.classList.add("alert-animation");
    alerte_id.classList.remove("alert-animation-enlever");
}

function enleverSucces(){
    alerte_id = document.getElementById('notif-succes');
    alerte_id.classList.add("alert-animation-enlever");
    alerte_id.classList.remove("alert-animation");
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
    let div = document.getElementById('collapseOne');
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
