// document.getElementsByClassName("btn-recettes").addEventListener("click", ajouterRecetteAuMenu);
const buttons = document.querySelectorAll(".btn-recettes");
const defilement  = document.getElementById("customRange1");
const defilement_out = document.getElementById("montant-budget");
const nombre_recette_panier = document.getElementById("notification-cart");
let compteur = 0;
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
        ajouterNombrePanier();
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

function ajouterNombrePanier(){
    let child = afficherSucces();
    incrementerNumeroRecette();
        setTimeout(function(){
        enleverSucces(child);
        setTimeout(function(){
             suppressionMessageAlerte(child);
            compteur--;
        }, 1500);
    }, 5000);

   }

function creationMessageAlerte(){
    const message = document.createElement('p');
    message.textContent = "La recette a été ajouté au panier."
    message.classList.add("alert-success", "alert");
    let topValue;
    if (++compteur == 1) {
         topValue = 15;
    } else {
         topValue = ((compteur - 1) * 60) + 15;
    }
    message.style.top = topValue + "px";
    let div_alerte = document.getElementById('notif-succes').appendChild(message);
    return div_alerte;
}

function suppressionMessageAlerte(child){
    document.getElementById('notif-succes').removeChild(child);
}

function afficherSucces(){
    let child = creationMessageAlerte();
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
        li.innerText = aliments[i].textContent;
        ul[index].append(li);
    }
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
    const recipeCount = localStorage.getItem('notification-cart') || 0;
    if (recipeCount === 0) {
        document.getElementById('notification-cart').hidden = true;
    } else {
        document.getElementById('notification-cart').hidden = false;
        document.getElementById('notification-cart').innerHTML = recipeCount;
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

majNombreEpicerie();
