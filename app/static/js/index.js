// document.getElementsByClassName("btn-recettes").addEventListener("click", ajouterRecetteAuMenu);
const buttons = document.querySelectorAll(".btn-recettes");
const defilement  = document.getElementById("customRange1");
const defilement_out = document.getElementById("montant-budget");

document.addEventListener("DOMContentLoaded", function() {
    chargerListeEpicerie();
});

if (defilement != null && defilement_out != null) {
    defilement_out.innerHTML = defilement.value;
    defilement.oninput = function(){defilement_out.innerHTML = this.value;}
}

/**
 *
 */
buttons.forEach(function(button) {
    button.addEventListener("click", function() {
        let strongs = document.querySelectorAll('.accordion-body strong');
        if (strongs.length === 1 && strongs[0].textContent === 'Aucun item') {
            index = 0
            ajouterElementPanier.call(this, strongs, index);
        } else {
            let div = document.getElementById('collapseOne');
            div.innerHTML += `
                <div class="accordion-body">
                    <strong></strong>
                        <ul>
                        </ul>
                </div>`
            let strongs = document.querySelectorAll('.accordion-body strong');
            index = strongs.length - 1;
            ajouterElementPanier.call(this, strongs, index);
        }
    });
});

function ajouterElementPanier(strongs, index) {
    strongs[index].textContent = this.getAttribute('nom-recette');
    recette_id = this.getAttribute('id-recette');
    let aliments = document.querySelectorAll('.r' + recette_id);
    let ul = document.querySelectorAll('.accordion-body ul');
    listerAliment(ul, aliments, index);
    sauvegarderListeEpicerie();
}

function listerAliment(ul, aliments, index) {
    for (let i = 0; i < aliments.length; i++) {
        let li = document.createElement('li');
        li.innerText = aliments[i].textContent;
        ul[index].append(li);
    }
}

function sauvegarderListeEpicerie() {
    let accordions = document.querySelectorAll('.accordion-body');
    let listeEpicerie = extraireListeEpicerie(accordions);
    localStorage.setItem('listeEpicerie', JSON.stringify(listeEpicerie));
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
            <strong>Aucun item</strong>
            <ul></ul>
        </div>`;
}

function ajouterRecetteAuDiv(div, entree, index) {
    div.innerHTML += `
        <div class="accordion-body">
            <strong>${entree.recette}</strong>
            <ul></ul>
        </div>`;
    
    const ul = div.querySelectorAll('.accordion-body ul')[index];
    for (let j = 0; j < entree.items.length; j++) {
        const li = document.createElement('li');
        li.innerText = entree.items[j];
        ul.append(li);
    }
}
