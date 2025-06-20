// JavaScript لإدارة قائمة الجوال
document.getElementById("mobile").addEventListener("click", function() {
    const navbar = document.getElementById("navbar");
    navbar.classList.toggle("active");
});

document.getElementById("Close").addEventListener("click", function() {
    const navbar = document.getElementById("navbar");
    navbar.classList.remove("active");
});

let currentSlide = 0;
const slides = document.querySelectorAll("#img-slider .slideactive"); 

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.display = i === index ? "block" : "none"; 
    });
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length; 
    showSlide(currentSlide);
}

setInterval(nextSlide, 3000); 


showSlide(currentSlide);

const cartButtons = document.querySelectorAll(".cart");
let cartCount = 0;

cartButtons.forEach(button => {
    button.addEventListener("click", function(event) {
        event.preventDefault();
        cartCount++;
        updateCartCount();
    });
});

function updateCartCount() {
    const cartIcon = document.querySelector(".head-Cart"); // يختار أيقونة السلة في العنوان
    cartIcon.setAttribute("data-count", cartCount); 
}

function afficherImageGrande(image) {
    var modal = document.getElementById("modal");
    var imgGrande = document.getElementById("img-grande");

    modal.style.display = "block";
    imgGrande.src = image.src; 
}

function fermerModal() {
    document.getElementById("modal").style.display = "none";
}
////////////////////////////////////////////////////

///////////////////////////////////////////////////////

function supprimerProduit(produitId) {
    fetch(`/Home/supprimer_produit_home/${produitId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector("[name=csrfmiddlewaretoken]").value
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire("Succès!", data.message, "success");
            location.reload(); 
        } else {
            Swal.fire("Erreur!", data.error, "error");
        }
    })
    .catch(error => Swal.fire("Erreur!", "Une erreur est survenue.", "error"));
}

function modifierProduit(produitId) {
    var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;


    Swal.fire({
        title: 'Modifier le produit',
        html:
            `<input id="swal-input1" class="swal2-input" placeholder="Nom">` +
            `<input id="swal-input2" class="swal2-input" placeholder="Description">` +
            `<input id="swal-input3" class="swal2-input" placeholder="Prix">`,
        focusConfirm: false,
        preConfirm: () => {
            return [
                document.getElementById('swal-input1').value,
                document.getElementById('swal-input2').value,
                document.getElementById('swal-input3').value
            ];
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const nom = result.value[0];
            const description = result.value[1];
            const prix = result.value[2];

            if (!nom || !description || !prix) {
                Swal.fire("Erreur!", "Tous les champs doivent être remplis.", "error");
                return;
            }

            const url = `modifier_produit_home/${produitId}/`;
            console.log("URL de modification:  ", url);

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: new URLSearchParams({
                    'nom': nom,
                    'description': description,
                    'prix': prix
                })
            })
            .then(response => {
                if (!response.ok) {
                    return Promise.reject('Réponse du serveur invalide');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    Swal.fire("Succès!", data.message, "success");
                    location.reload();
                } else {
                    Swal.fire("Erreur!", data.error || "Une erreur est survenue.", "error");
                }
            })
            .catch(error => Swal.fire("Erreur!", error, "error"));
        }
    });
}



function fermerModalHome() {
    document.getElementById('popupHome').style.display = 'none';
}
