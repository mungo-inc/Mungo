const ajouterRecetteButtons = document.querySelectorAll(".btn-recettes");
const ajouterAlimentsButtons = document.querySelectorAll(".btn-aliments");
const envoyerAvis = document.querySelectorAll(".btn-avis");
const retirerRecetteButtons= document.getElementById("div-section-recette");
const retirerAlimentButtons = document.getElementById("div-section-aliment");
const viderPanierButton = document.getElementsByClassName("btn-vider")[0];
const defilement  = document.getElementById("customRange1");
const defilementOut = document.getElementById("montant-budget");
const nombreRecettePanier = document.getElementById("notification-cart");
const afficherEcranConnexionBtn = document.querySelector(".login-btn");
const connecterEnregistrerLien = document.querySelectorAll(".form-box .lien-creation-compte a");
const afficherEcranEnregistrer = document.querySelector(".formulaire-popup");
const sauvegarderButton = document.getElementById("save-list-btn");
const fermerConnexionBtn = document.getElementById("fermer-connexion");
const allRanges = document.querySelectorAll(".range-wrap");
const boutonAjouterIngredient = document.getElementById("ajouter-ingredient");
const boutonEnleverIngredient = document.getElementById("enlever-ingredient");
const ingredientsContainer = document.getElementById("ingredients-conteneur");
const supprimerListeButtons = document.querySelectorAll(".delete-list-btn");
const modifierListeButtons = document.querySelectorAll(".modifier-list-btn");
const sauvegarderModificationsListeButtons = document.querySelectorAll(".save-modif-list-btn");
const produit_vedette = document.getElementById("vedette");

let compteur = 0;
let compteurListeIngredient = 1;
let restants = []; // {idAliment, qteRestante}
let taggedAliments = []; // {idAliment, idRecette, qteRecette};
const barreRecherche = document.getElementById("recherche");
const ordreRecette = document.getElementById("ordre-recette");

if (ordreRecette) {
    ordreRecette.addEventListener("change", function() {
        let valeur = ordreRecette.value;
        console.log(ordreRecette.value);
        if (valeur == "alphabetique") {
            changerOrdre(valeur);
        } else if (valeur == "alphabetique-reverse") {
            changerOrdre(valeur);
        } else if (valeur == "prix") {
            changerOrdre(valeur);
        } else if (valeur == "prix-reverse") {
            changerOrdre(valeur);
        }
    });
}

function changerOrdre(ordre){
    let recettes = document.querySelectorAll(".recettes-js");
    let recettesListe = Array.prototype.slice.call(recettes);
    if (ordre == "alphabetique") {
            recettesListe.sort(function(a, b) {
                let recetteA = a.innerText;
                let recetteB = b.innerText;
                if (recetteA > recetteB) return 1;
                if (recetteA < recetteB) return -1;
                return 0;
            });
    } else if (ordre == "alphabetique-reverse") {
        recettesListe.sort(function(a, b) {
            let recetteA = a.innerText;
            let recetteB = b.innerText;
            if (recetteA > recetteB) return -1;
            if (recetteA < recetteB) return 1;
            return 0;
    });

    } else if (ordre == "prix") {
        recettesListe.sort(function(a, b) {
            let recetteA = parseFloat(a.querySelector('span').textContent);
            let recetteB = parseFloat(b.querySelector('span').textContent);
            if (recetteA > recetteB) return 1;
            if (recetteA < recetteB) return -1;
            return 0;
    });
    } else if (ordre == "prix-reverse") {
        recettesListe.sort(function(a, b) {
            let recetteA = parseFloat(a.querySelector('span').textContent);
            let recetteB = parseFloat(b.querySelector('span').textContent);
            if (recetteA > recetteB) return -1;
            if (recetteA < recetteB) return 1;
            return 0;
        });
    }
    let recetteDiv = document.querySelector("#changer-ordre");
    recetteDiv.innerHTML = "";
    recettesListe.forEach(div => {
        recetteDiv.appendChild(div);
    });
    console.log(recettesListe);
}

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



if (boutonAjouterIngredient) {
    boutonAjouterIngredient.addEventListener("click", function() {
        $.ajax({
            url: "/get_ingredients",
            method: "GET",
            success: function(data) {
                var selectHtml = '<label class="form-check-label" for="'+compteurListeIngredient+'">Choisir un ingrédient : </label>';
                selectHtml += '<select name="ingredients" class="liste-ingredients" id='+ compteurListeIngredient+ '>';
                selectHtml += '<option value="">Choisissez un ingrédient</option>';
                data.forEach(function(ingredient) {
                    selectHtml += '<option id="'+ingredient[0]+'" data-mesure="'+ingredient[2]+'" value="' + ingredient[0] + '">' + ingredient[1] + '</option>';
                });
                selectHtml += '</select>';
                selectHtml += '<span id=err-item-selectionne-'+compteurListeIngredient+'></span>';
                selectHtml += '<div id="selected-ingredient-'+ compteurListeIngredient+'"></div>';
                let div  = document.createElement("div");
                div.innerHTML = selectHtml;
                div.setAttribute("id", "option-"+compteurListeIngredient);
                compteurListeIngredient++;
                document.getElementById("ingredients").appendChild(div);
            },
            error: function(error) {
                console.log("Error:", error);
            }
        });
    });
}

if (boutonEnleverIngredient) {
    boutonEnleverIngredient.addEventListener("click", function() {
        if (compteurListeIngredient >= 1) {
            document.getElementById("option-" + --compteurListeIngredient).remove();
        }
    });
}

if (ingredientsContainer) {
    ingredientsContainer.addEventListener("change", function(e) {
        if (e.target.classList.contains("liste-ingredients")) {
            e.preventDefault();
            let mesure = e.target.options[e.target.selectedIndex];
            console.log(mesure);
            let labelText;
            if (mesure.getAttribute('data-mesure') == "u") {
                labelText = "Entrez le nombre d'unité pour la recette:";
            } else if (mesure.getAttribute('data-mesure') == "g" || mesure.getAttribute('data-mesure') == "p") {
                labelText = "Entrez le nombre de grammes pour la recette:";
            } else if (mesure.getAttribute('data-mesure') == "l") {
                labelText = "Entrez le nombre de millilitres pour la recette:";
            }
            let divRange = document.createElement("div");
            if (mesure.value != "") {
                let label = document.createElement("label");
                label.setAttribute('for', mesure.id + "-quantite");
                label.textContent = labelText;
                let input = document.createElement("input");
                input.classList.add("form-control");
                input.setAttribute("id", mesure.id + "-quantite");
                input.setAttribute("type", "text");
                input.setAttribute("name", mesure.id+"-quantite");
                divRange.appendChild(label);
                divRange.appendChild(input);
                let span = document.createElement("span");
                span.setAttribute("id", "err-selected-ingredient-" + e.target.id);
                divRange.appendChild(span);
            }
            let div = document.getElementById("selected-ingredient-" + e.target.id);
            div.innerHTML = divRange.innerHTML;
        }
    });
}
document.addEventListener("DOMContentLoaded", function() {
    // let restantsLocal = JSON.parse(localStorage.getItem('restants'));
    // let taggedAlimentsLocal = JSON.parse(localStorage.getItem('taggedAliments'));
    // if (restantsLocal) {
    //     restants = restantsLocal;
    // }
    // if (taggedAlimentsLocal) {
    //     taggedAliments = taggedAlimentsLocal;
    // } 
    chargerListeEpicerie();
    majNombreEpicerie();
    //updaterPrixPage(restants);
});

document.getElementById('toggle-menu').addEventListener('change', function() {
    document.querySelector('.col-2').classList.toggle('nav', this.checked);
});

allRanges.forEach(wrap => {
    const range = wrap.querySelector(".range");
    const bubble = wrap.querySelector(".bubble");

    range.addEventListener("input", () => {
        setBubble(range, bubble);
    });
    setBubble(range, bubble);
});

function setBubble(range, bubble) {
    const val = range.value;
    const min = range.min ? range.min : 0;
    const max = range.max ? range.max : 100;
    const newVal = Number(((val - min) * 100) / (max - min));
    bubble.innerHTML = val;
    bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
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
ajouterRecetteButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        let strongs = document.querySelectorAll('.accordion-body .strong-recette');
        if (strongs.length === 1 && strongs[0].textContent === 'Aucun item') {
            ajouterRecetteAuPanier.call(this, strongs, 0);
            montrerTotalPanier();
            montrerButton('btn-close');
            montrerButton('btn-vider');
            montrerButton('save-list-btn');
        } else {
            let div = document.getElementById('div-section-recette');
            div.innerHTML += `
                <div class="div-recette-panier">
                    <button type="button" class="btn-close btn-close-recette" aria-label="Close"></button>
                    <strong class="strong-recette"></strong>
                    <ul>
                    </ul>
                </div>`;
            let strongs = document.querySelectorAll('.accordion-body .strong-recette');
            ajouterRecetteAuPanier.call(this, strongs, strongs.length - 1);
        }
        updaterRestants.call(this, restants, taggedAliments);
        updaterPrixPage(restants, taggedAliments);
        let message = "La recette a été ajouté au panier."
        //localStorage.setItem('restants', JSON.stringify(restants));
        //localStorage.setItem('taggedAliments', JSON.stringify(taggedAliments));
        console.log(localStorage);
        ajouterNombrePanier(message);
    });
});

ajouterAlimentsButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        let strongs = document.querySelectorAll('.accordion-body .strong-aliment');
        if (strongs.length === 1 && strongs[0].textContent === 'Aucun item') {
            ajouterAlimentAuPanier.call(this, strongs, 0);
            montrerTotalPanier();
            montrerButton('btn-vider');
            document.querySelectorAll('#div-section-aliment .btn-close')[0].hidden = false;
            montrerButton('save-list-btn');
        } else {
            let div = document.getElementById('div-section-aliment');
            div.innerHTML += `
                <div class="div-aliment-panier">
                    <button type="button" class="btn-close btn-close-recette" aria-label="Close"></button>
                    <strong class="strong-aliment"></strong>
                </div>`;
            let strongs = document.querySelectorAll('.accordion-body .strong-aliment');
            ajouterAlimentAuPanier.call(this, strongs, strongs.length - 1);
        }
        updaterRestants.call(this, restants, taggedAliments);
        updaterPrixPage(restants, taggedAliments);
        let message = "L'aliment a été ajouté au panier."
        ajouterNombrePanier(message);
    })
});

function updaterRestants(restants) {
    let idRecette = parseInt(this.getAttribute('data-id-recette'));
    document.querySelectorAll('p.r' + idRecette).forEach (elem => {
        let qteRestante;
        let idAliment = parseInt(elem.getAttribute('data-id-aliment'));
        let qteAliment = parseFloat(elem.getAttribute('data-quantite-aliment'));
        let qteRecette = parseFloat(elem.getAttribute('data-quantite-recette'));
        let alimentExiste = restants.some(aliment => aliment.idAliment === idAliment);
        if (alimentExiste) {
            let aliment = restants.find(aliment => aliment.idAliment === idAliment);
            qteRestante = aliment.qteRestante;
        } else {
            qteRestante = qteAliment - qteRecette;
        }
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
            if (idAliment === 132) {
                //console.log("idAliment:", idAliment, "qteRestante:", qteRestante, "qteRecette:", qteRecette);
            }
            let nouvelleQte = qteRestante - qteRecette;
            modifierQteRestante(restants, idAliment, nouvelleQte, qteAliment, idRecette);
            // let restantsCopy = [...restants];
            // console.log("restants: ", restantsCopy);
        }
    });
}

function modifierQteRestante(restants, 
    idAliment, 
    nouvelleQte, 
    qteAliment,  
    idRecette) {
    let aliment = restants.find(aliment => aliment.idAliment === idAliment);
    let alimentTagged = taggedAliments.find(aliment => aliment.idAliment === idAliment);
    alimentExisteDansTagged = taggedAliments.some(elem =>  
        elem.idAliment === idAliment && elem.idRecette === idRecette 
    );
    if (aliment) {
        if (idAliment === 132) {
            //console.log(alimentExisteDansTagged, nouvelleQte);
        }
        // if (alimentExisteDansTagged && nouvelleQte < 0) {
        if (alimentExisteDansTagged && nouvelleQte < alimentTagged.qteRecette) {
            console.log(idAliment, nouvelleQte, aliment.qteRestante);
            //console.log(taggedAliments.length);
            let taggedAlimentsCpy = taggedAliments.filter(elem => 
                elem.idAliment !== idAliment || elem.qteRecette <= nouvelleQte 
            );
            let idsRecette = taggedAliments.filter(x => !taggedAlimentsCpy.includes(x));
            //console.log(taggedAliments.length);
            taggedAliments = taggedAlimentsCpy;
            console.log("cpy", taggedAlimentsCpy);
            console.log("tagged1", taggedAliments);
            augmenterPrixPage(idAliment, idsRecette);
        }
        aliment.qteRestante = nouvelleQte;
        while (aliment.qteRestante < 0) {
            aliment.qteRestante += qteAliment;
        }
        // Pour chaque aliment de chaque recette dans la page, allez verifier
        // si la qteRestante > qteRecette. Ajuster le prix si ce n'est pas le 
        // cas.
    }
    //console.log("tagged: ", taggedAliments);
    //console.log("restants: ", restants);
}

function updaterPrixPage(restants) {
    let div = document.querySelector('div.liste-recettes.conteneur-recettes');
    restants.forEach(restant =>  {
        for (let childDiv of div.children) {
            let idRecette = childDiv.id;
            childDiv.querySelectorAll('p.r' + idRecette).forEach(p => {
                let idAliment = parseInt(p.getAttribute('data-id-aliment'));
                let idRecette = parseInt(childDiv.id);
                let qteRecette = parseInt(p.getAttribute('data-quantite-recette'));
                if (idAliment === restant.idAliment) {
                    let alimentExiste = taggedAliments.some(aliment => 
                        aliment.idAliment === idAliment && aliment.idRecette === idRecette
                    );
                    if (idAliment === 42) {
                        //console.log(qteRecette)
                        //console.log(restant.qteRestante)
                        //console.log(!alimentExiste)
                        // console.log("=============")
                    }
                    if (qteRecette < restant.qteRestante && !alimentExiste) {
                        let prix = parseFloat(childDiv.querySelector('p .prix-recette').textContent);
			            prix -= parseFloat(p.getAttribute('data-prix-aliment'));
                        childDiv.querySelector('p .prix-recette').textContent = prix.toFixed(2); 
                        taggedAliments.push({idAliment, idRecette, qteRecette});
                    } 
                }
            });
        }
    });
}

function augmenterPrixPage(idAliment, idsRecette) {
    let div = document.querySelector('div.liste-recettes.conteneur-recettes');
    let prix = 0;
    idsRecette.forEach(i => {
        for (let childDiv of div.children) {
            if (parseInt(childDiv.id) === i.idRecette) {
                prix = parseFloat(childDiv.querySelector('p .prix-recette').textContent)
                childDiv.querySelectorAll('p.r' + i.idRecette).forEach(p => {
                    if (parseInt(p.getAttribute('data-id-aliment')) === idAliment) {
                        prix += parseFloat(p.getAttribute('data-prix-aliment'));
                        childDiv.querySelector('p .prix-recette').textContent = prix.toFixed(2);
                    }
                });
            }
        }
    });
}

function montrerTotalPanier() {
    console.log("ICI")
    let total = document.getElementById('total-panier');
    total.hidden = false;
}


retirerRecetteButtons.addEventListener("click", function(event) {
    const target = event.target;
    let listeEpicerieRecettes = JSON.parse(localStorage.getItem('listeEpicerieRecettes'));
    let parentElem = target.closest('.div-recette-panier');
    if (parentElem) {
        let nomRecette = parentElem.querySelector('.strong-recette').textContent;
        if (estCloseButtonRecette(target)) {
            retirerRecettes(parentElem, listeEpicerieRecettes, nomRecette);
        } else if (estCloseButtonAliment(target)) {
            let li = target.closest('li');
            retirerAliment(parentElem, listeEpicerieRecettes, nomRecette, li);
        }
    }
    //localStorage.setItem('restants', JSON.stringify(restants));
    //localStorage.setItem('taggedAliments', JSON.stringify(taggedAliments));
});

retirerAlimentButtons.addEventListener("click", function(event) {
    const target = event.target;
    let listeEpicerieAliments = JSON.parse(localStorage.getItem('listeEpicerieAliments'));
    let parentElem = target.closest('.div-aliment-panier');
    if (parentElem) {
        let nomAliment = parentElem.querySelector('.strong-aliment').textContent;
        retirerAlimentIndividuel(parentElem, listeEpicerieAliments, nomAliment);
    }
});

viderPanierButton.addEventListener("click", function() {
    let listeEpicerieRecettes = JSON.parse(localStorage.getItem('listeEpicerieRecettes'));
    let listeEpicerieAliments = JSON.parse(localStorage.getItem('listeEpicerieAliments'));
    while (listeEpicerieRecettes.length) {
        let parents = document.getElementsByClassName('div-recette-panier');
        retirerRecettes(
            parents[0], 
            listeEpicerieRecettes, 
            listeEpicerieRecettes[0].nomRecette
        );
    }
    while (listeEpicerieAliments.length) {
        let parents = document.getElementsByClassName('div-aliment-panier');
        retirerAlimentIndividuel(parents[0], listeEpicerieAliments, listeEpicerieAliments[0].nomAliment);
    }                              
});                                
                                   
if (sauvegarderButton) {
    sauvegarderButton.addEventListener("click", function() {
        let divs = document.querySelectorAll('.div-recette-panier');
        let listeASauvegarder = [];
        divs.forEach(body => {
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

supprimerListeButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        let div = this.parentElement.parentElement;
        let idClient = parseInt(div.getAttribute("data-id-client"));
        let idPanier = parseInt(div.getAttribute("data-id-panier"));
        fetch('/supprimer-liste', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({idClient: idClient, idPanier: idPanier})
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
        div.remove();
        if (document.querySelectorAll(".panier-contenur").length === 0) {
            let message = "Vous n'avez aucun panier sauvegardé";
            document.getElementById('titre-liste-epicerie-sauvegardee').textContent = message;
        }
    });
});


modifierListeButtons.forEach(function(button) {
    button.addEventListener("click", function() {
        const liste = this.closest('.panier-conteneur');
        
        const nomListe = liste.querySelector('#panier-nom');
        
        const input = document.createElement('input');
        input.type = 'text';
        input.value = nomListe.textContent;
        input.className = 'input-nom-liste';
        
        liste.replaceChild(input, nomListe);

        let sauverModifButton = liste.querySelector('.save-modif-list-btn');
        sauverModifButton.hidden = false;
        liste.querySelector('.delete-list-btn').hidden = true;
        liste.querySelector('.modifier-list-btn').hidden = true;
        
        const validerModif = () => {
            let nouveauNom = input.value;
            
            let listeElemNouveauNom = document.createElement('h3');
            listeElemNouveauNom.id = 'panier-nom';
            listeElemNouveauNom.textContent = nouveauNom;
            
            liste.replaceChild(listeElemNouveauNom, input);

            sauverModifButton.hidden = true;
            liste.querySelector('.delete-list-btn').hidden = false;
            liste.querySelector('.modifier-list-btn').hidden = false;
            
            let idPanier = liste.getAttribute('data-id-panier');
            let idClient = liste.getAttribute('data-id-client');
            
            fetch('/sauvegarder-modif-liste', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idPanier: idPanier,
                    idClient: idClient,
                    nouveauNom: nouveauNom 
                }),
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
            .catch((error) => {
                console.error('Error:', error);
            });
        };
        
        sauverModifButton.addEventListener('click', validerModif);
        
        input.focus();
    });
});


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
    lis = Array.from(parentElem.querySelectorAll('li'));
    lis.forEach(li => {
        let idAliment = parseInt(li.getAttribute('data-id-aliment'));
        console.log(li);
        ajusterPrixApresSuppression(restants, idAliment, li);
    });
    parentElem.remove();
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    if (listeEpicerie.length === 0) {
        afficherAucuneRecette();
    } else {
        calculerTotalPanier();
    }
    //localStorage.setItem('restants', JSON.stringify(restants));
    //localStorage.setItem('taggedAliments', JSON.stringify(taggedAliments));
}

function retirerAlimentIndividuel(parentElem, listeEpicerie, nomAliment) {
    let recette = listeEpicerie.find(r => r.nomAliment === nomAliment);
    let index = listeEpicerie.indexOf(recette);
    if (index > -1) {
        listeEpicerie.splice(index, 1);
    }
    parentElem.remove();
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    if (listeEpicerie.length === 0) {
        afficherAucunAliment();
    }

}

function afficherAucuneRecette() {
    let div = document.getElementById('div-section-recette');
    div.innerHTML = `
            <div class="div-recette-panier">
                <button type="button" class="btn-close btn-close-recette" aria-label="Close" hidden></button>
                <strong class="strong-recette">Aucun item</strong>
                <ul>
                </ul>
            </div>`;
    

    let button = document.getElementsByClassName('btn-vider');
    if (localStorage.getItem('listeEpicerieAliments') === "[]") {
        button[0].hidden = true;
        let total = document.getElementById('total-panier');
        total.hidden = true;
        let saveButton = document.getElementById('save-list-btn');
        if (saveButton != null) {
            saveButton.hidden = true;
        }
    }
}

function afficherAucunAliment() {
    let div = document.getElementById('div-section-aliment');
    div.innerHTML = `
            <div class="div-aliment-panier">
                <button type="button" class="btn-close btn-close-recette" aria-label="Close" hidden></button>
                <strong class="strong-aliment">Aucun item</strong>
            </div>`;
    let button = document.getElementsByClassName('btn-vider');
    let listeEpicerieRecettes = JSON.parse(localStorage.getItem('listeEpicerieRecettes'));
    if (!listeEpicerieRecettes || listeEpicerieRecettes.length === 0) {
        button[0].hidden = true;
        let saveButton = document.getElementById('save-list-btn');
        if (saveButton != null) {
            saveButton.hidden = true;
        }
        let total = document.getElementById('total-panier');
        total.hidden = true;
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
    let idAliment = li.getAttribute("data-id-aliment")
    li.remove();
    sauvegarderListeEpicerie();
    if (listeEpicerie[index].items.length === 0) {
        retirerRecettes(parentElem, listeEpicerie, nomRecette);
    }
    // let restants = []; // {idAliment, qteRestante}
    ajusterPrixApresSuppression(restants, idAliment, li);
    calculerTotalPanier();
}

function ajusterPrixApresSuppression(restants, idAliment, li) {
    let restant = restants.find(id => id.idAliment == idAliment);
    // console.log(idAliment);
    // console.log(restants);
    // console.log(restant.qteRestante);
    if (restant) {
        let qteRecette = parseFloat(li.getAttribute("data-quantite-recette"));
        let qteAliment = parseFloat(li.getAttribute("data-quantite-aliment"));
        if (restant.qteRestante - qteAliment + qteRecette >= 0) {
            restant.qteRestante = restant.qteRestante - qteAliment + qteRecette;
        } else {
            restant.qteRestante = 0;
        }
        console.log(restant.qteRestante);
        let idsRecettes = taggedAliments.filter(elem => elem.idAliment == idAliment);
        console.log("idsRecettes", idsRecettes);
        taggedAliments = taggedAliments.filter(elem => elem.idAliment != idAliment);
        augmenterPrixPage(parseInt(idAliment), idsRecettes);
    }
}

function ajouterRecetteAuPanier(strongs, index) {
    strongs[index].textContent = this.getAttribute('data-nom-recette');
    let idRecette = document.createAttribute('data-id-recette');
    idRecette.value = this.getAttribute('data-id-recette');
    strongs[index].setAttributeNode(idRecette);
    idRecette = this.getAttribute('data-id-recette');
    let aliments = document.querySelectorAll('.r' + idRecette);
    let ul = document.querySelectorAll('.accordion-body ul')[index]; // Ensure the correct ul element is selected

    // Create a new list of ingredients excluding already tagged ones
    let filteredAliments = Array.from(aliments).filter(aliment => {
        let idAliment = aliment.getAttribute('data-id-aliment');
        return !taggedAliments.some(item =>
            item.idAliment == idAliment && item.idRecette == idRecette
        );
    });

    // Clear the existing list
    ul.innerHTML = '';

    listerAliment(ul, filteredAliments, index)
    sauvegarderListeEpicerie();
    majNombreEpicerie();
    setTimeout(function() {
        enleverSucces();
    }, 5000);

    calculerTotalPanier();
}

function ajouterAlimentAuPanier(strongs, index) {
    strongs[index].textContent = this.getAttribute('data-nom-recette'); //nom-aliment
    let idAliment = document.createAttribute('data-id-aliment');
    idAliment.value = this.getAttribute('data-id-recette'); //id-aliment
    strongs[index].setAttributeNode(idAliment);
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


function enleverSucces(child) {
    child.classList.add("alert-animation-enlever");
    child.classList.remove("alert-animation");
}


function listerAliment(ul, aliments, index) {
    console.log("salut")
    for (let i = 0; i < aliments.length; i++) {
        let li = document.createElement('li');
        let button = creerCloseButton();
        li.append(button);
        li.innerHTML += aliments[i].textContent;
        let idAliment = document.createAttribute('data-id-aliment');
        idAliment.value = aliments[i].getAttribute('data-id-aliment');
        let qteAliment = document.createAttribute('data-quantite-aliment');
        qteAliment.value = aliments[i].getAttribute('data-quantite-aliment');
        let qteRecette = document.createAttribute("data-quantite-recette");
        qteRecette.value = aliments[i].getAttribute('data-quantite-recette');
        let prixAliment = document.createAttribute("data-prix-aliment");
        prixAliment.value = aliments[i].getAttribute('data-prix-aliment');
        let typeAliment = document.createAttribute("data-type-aliment");
        typeAliment.value = aliments[i].getAttribute('data-type-aliment');
        li.setAttributeNode(idAliment);
        li.setAttributeNode(qteAliment);
        li.setAttributeNode(qteRecette);
        li.setAttributeNode(prixAliment);
        li.setAttributeNode(typeAliment);
        ul.append(li);
    }
    console.log("bte")
}

function creerCloseButton() {
    let button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn-close btn-close-aliment';
    return button;
}

function sauvegarderListeEpicerie() {
    // let sectionRecettes = document.querySelectorAll('.div-section-recette');
    // let sectionAliment = document.querySelectorAll('.div-section-aliment');
    // let listeEpicerie = extraireListeEpicerie(accordions);
    let listeEpicerieRecettes = extraireListeRecettes();
    let listeEpicerieAliments = extraireListeAliments();
    localStorage.setItem('listeEpicerieRecettes', JSON.stringify(listeEpicerieRecettes));
    localStorage.setItem('listeEpicerieAliments', JSON.stringify(listeEpicerieAliments));
}

function extraireListeRecettes() {
    let listeEpicerieRecettes = [];
    let div = document.getElementById('div-section-recette');
    for (divChild of div.children) {
        let nomRecette = divChild.querySelector('.strong-recette').textContent;
        let idRecette = divChild 
            .querySelector('.strong-recette')
            .getAttribute('data-id-recette');
        let aliments = extraireAlimentFaisaitPatrieDuneRecette(divChild);
        if (nomRecette != "Aucun item") {
            listeEpicerieRecettes.push(
                { idRecette: idRecette, nomRecette: nomRecette, items: aliments}
            );
        }
    }
    return listeEpicerieRecettes;
}

function extraireListeAliments() {
    let listeEpicerieAliments = [];
    let div = document.getElementById('div-section-aliment');
    for (divChild of div.children) {
        let nomAliment = divChild.querySelector('.strong-aliment').textContent;
        if (nomAliment != "Aucun item") {
            listeEpicerieAliments.push(
                {nomAliment: nomAliment}
            );
        }
    }
    return listeEpicerieAliments;
}

function incrementerNumeroRecette(){
    let recipeCount = localStorage.getItem('notification-cart') || 0;
    recipeCount = parseInt(recipeCount) + 1;
    localStorage.setItem('notification-cart', recipeCount);
    majNombreEpicerie();
}

function majNombreEpicerie() {
    let listeEpicerieRecettes = JSON.parse(localStorage.getItem('listeEpicerieRecettes'));
    let listeEpicerieAliments = JSON.parse(localStorage.getItem('listeEpicerieAliments'));
    if (listeEpicerieRecettes && listeEpicerieAliments) {
        let nbItems = listeEpicerieRecettes.length + listeEpicerieAliments.length;
        if (nbItems) {
            document.getElementById('notification-cart').hidden = false;
            document.getElementById('notification-cart').innerHTML = nbItems;
        } else {
            document.getElementById('notification-cart').hidden = true;
        }
    }
}

function extraireListeEpicerie(accordions) {
    for (let i = 0; i < accordions.length; i++) {
        let nomRecette = accordions[i].querySelector('strong').textContent;
        let idRecette = accordions[i]
        .querySelector('strong')
        .getAttribute('data-id-recette');
        let items = extraireItems(accordions[i]);
        listeEpicerieRecette.push(
            { idRecette: idRecette, nomRecette: nomRecette, items: items }
        );
    }
    return listeEpicerie;
}

function extraireAlimentFaisaitPatrieDuneRecette(div) {
    let ul = div.querySelector('ul');
    let aliments = [];
    let lis = ul.querySelectorAll('li');
    for (let j = 0; j < lis.length; j++) {
        aliments.push({ 
            id: lis[j].getAttribute('data-id-aliment'), 
            nom: lis[j].textContent,
            qte: lis[j].getAttribute('data-quantite-aliment'),
            qteRecette: lis[j].getAttribute('data-quantite-recette'),
            typeAliment: lis[j].getAttribute('data-type-aliment'),
            prixAliment: lis[j].getAttribute('data-prix-aliment')
        });
    }
    return aliments;
}

function chargerListeEpicerie() {
    let listeEpicerieRecettes = chargerListeLocale('listeEpicerieRecettes');
    let listeEpicerieAliments = chargerListeLocale('listeEpicerieAliments');
    afficherListeEpicerieRecettes(listeEpicerieRecettes);
    afficherListeEpicerieAliments(listeEpicerieAliments);
    if (listeEpicerieRecettes.length || listeEpicerieAliments.length) {
        document.getElementsByClassName('btn-vider')[0].hidden = false;
    }
}

function chargerListeLocale(nomListe) {
    let listeEpicerie = localStorage.getItem(nomListe)
    if (listeEpicerie) {
        return JSON.parse(listeEpicerie);
    } else {
        return [];
    }
}

function afficherListeEpicerieRecettes(listeEpicerie) {
    let div = document.getElementById('div-section-recette');
    div.innerHTML = '';
    // Faire la distinction entre la sous-liste recettes et aliments
    if (listeEpicerie.length === 0) {
        afficherAucuneRecette();
    } else {
        for (let i = 0; i < listeEpicerie.length; i++) {
            ajouterRecetteAuDiv(div, listeEpicerie[i], i);
        }
        calculerTotalPanier();
    }
}


function afficherListeEpicerieAliments(listeEpicerie) {
    let div = document.getElementById('div-section-aliment');
    div.innerHTML = '';
    if (listeEpicerie.length === 0) {
        afficherAucunAliment();
    } else {
        for (let i = 0; i < listeEpicerie.length; i++) {
            ajouterAlimentAuDiv(div, listeEpicerie[i]);
        }
        calculerTotalPanier();
    }
}

function calculerTotalPanier() {
    let recetteElements = document.querySelectorAll('strong[data-id-recette]');
    console.log(recetteElements);
    let recetteIds = [];

    recetteElements.forEach(element => {
        let recetteId = element.getAttribute('data-id-recette');
        recetteIds.push(recetteId);
    });

    console.log("id:", recetteIds);
    let alimentElements = document.querySelectorAll('ul li[data-type-aliment]');
    let prix=0;

    alimentElements.forEach(element => {
        let typeAliment = element.getAttribute('data-type-aliment');
        let quantiteAliment = parseFloat(element.getAttribute('data-quantite-aliment'));    
        let quantiteRecette = parseFloat(element.getAttribute('data-quantite-recette'));
        let prixAliment = parseFloat(element.getAttribute('data-prix-aliment'));
        if (typeAliment == 'u') {
            prix += (quantiteRecette/quantiteAliment) * prixAliment;
        } else if (typeAliment == 'p'){
            prix += (prixAliment/quantiteAliment) * quantiteRecette;
        } else {
            console.log(Math.ceil(quantiteRecette/quantiteAliment));
            prix += Math.ceil(quantiteRecette/quantiteAliment)*prixAliment;
        }
        console.log(`Type d'aliment: ${typeAliment}, Quantité recette: ${quantiteRecette}, Prix: ${prixAliment}, quantite aliment:  ${quantiteAliment}`);
        console.log(`prix total: ${prix}`);
    });
    document.getElementById('total-panier-valeur').textContent = prix.toFixed(2);
    montrerTotalPanier();
}

function ajouterRecetteAuDiv(div, entree, index) {
    div.innerHTML += `
        <div class="div-recette-panier">
            <button type="button" class="btn-close btn-close-recette" aria-label="Close"></button>
            <strong class="strong-recette" data-id-recette="${entree.idRecette}">${entree.nomRecette}</strong>
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
        let qteAliment = document.createAttribute('data-quantite-aliment');
        qteAliment.value = entree.items[j].qte;
        li.setAttributeNode(qteAliment);
        let qteRecette = document.createAttribute('data-quantite-recette');
        qteRecette.value = entree.items[j].qteRecette;
        li.setAttributeNode(qteRecette);
        let typeAliment = document.createAttribute('data-type-aliment');
        typeAliment.value = entree.items[j].typeAliment;
        li.setAttributeNode(typeAliment);
        let prixAliment = document.createAttribute('data-prix-aliment');
        prixAliment.value = entree.items[j].prixAliment;
        li.setAttributeNode(prixAliment);
        li.innerHTML += entree.items[j].nom;
        ul.append(li);
    }
}

function ajouterAlimentAuDiv(div, entree) {
    div.innerHTML +=`
        <div class="div-aliment-panier">
        <button type="button" class="btn-close btn-close-recette" aria-label="Close"></button>
        <strong class="strong-aliment" data-id-aliment="${entree.idAliment}">${entree.nomAliment}</strong>
        </div>`;
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

// avis etoiles
const etoiles = document.querySelectorAll(".avis .stars i");
const note = document.getElementById("note");

etoiles.forEach((etoile, index1) => {
    etoile.addEventListener("click", () => {
        console.log(index1);
        note.value = index1 + 1;
        etoiles.forEach((etoile, index2) => {
            index1 >= index2 ? etoile.classList.add("active") : etoile.classList.remove("active");
        });
    });
});

if (barreRecherche) {
    barreRecherche.addEventListener("input", e => {
        let valeur = e.target.value;
        let divRecette = document.querySelectorAll(".recettes-js");

        for (i = 0; i < divRecette.length; i++){
            let uneRecette = divRecette[i].innerHTML.toUpperCase();
            if (!(uneRecette.includes(valeur.toUpperCase()))){
                divRecette[i].setAttribute("hidden", "true"); 
            } else {
                divRecette[i].removeAttribute("hidden"); 
            }
        }
    });
}


// avis id_recette
const affichageAvisElements = document.querySelectorAll(".affichage-avis");

affichageAvisElements.forEach(affichageAvis => {
    const rating = affichageAvis.getAttribute("data-note");
    const stars = affichageAvis.querySelectorAll(".stars i");
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add("active");
        }
    });
});
