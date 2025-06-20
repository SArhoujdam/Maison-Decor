const bar = document.getElementById('bar');
const navbar = document.getElementById('mobile');
const Close = document.getElementById('Close');

bar.addEventListener('click', function() {
    navbar.classList.add('active'); 
    if (mobile) {
        mobile.addEventListener("click", () => {
        })
    }
});
function afficherImageGrande() {
    var modal = document.getElementById("modal");
    var img = document.getElementById("image-cliquee");
    var imgGrande = document.getElementById("img-grande");
    modal.style.display = "block";
    imgGrande.src = img.src;
}

//page categoriesafficherPagePromotions

//////////////////////////////////

function fermerModal() {
    document.getElementById("modal").style.display = "none";
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

const passwordInput = document.getElementById('password');
const eyeIcon = document.getElementById('icon2');

eyeIcon.addEventListener('click', () => {
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    eyeIcon.classList.remove('fa-eye');
    eyeIcon.classList.add('fa-eye-slash');
  } else {
    passwordInput.type = 'password';
    eyeIcon.classList.remove('fa-eye-slash');
    eyeIcon.classList.add('fa-eye');
  }
});  
function verifierForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var password = document.getElementById("password1").value;
    var password = document.getElementById("start").value;
    if (username == "" || password == "") {
      document.getElementById("erreur").style.display = "block";
    } else {
      window.location.href = "confirm-account.html";
    }
  }
  //button shopge paiment 
//apres clique button 
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        produit: params.get('produit'),
        prix: params.get('prix'),
        image: params.get('image')
    };
}

// Affiche les détails du produit sur la page
document.addEventListener("DOMContentLoaded", () => {
    const { produit, prix, image } = getQueryParams();
    document.getElementById("product-name").innerText = produit;
    document.getElementById("product-price").innerText = `Prix : $${prix}`;
    document.getElementById("product-image").src = image;
});

// Simule le paiement
function effectuerPaiement() {
    const cardNumber = document.getElementById("card-number").value;
    const cardExpiry = document.getElementById("card-expiry").value;
    const cardCvc = document.getElementById("card-cvc").value;

    if (cardNumber && cardExpiry && cardCvc) {
        alert("Paiement réussi ! Merci pour votre achat.");
        window.location.href = "confirmation.html";
    } else {
        alert("Veuillez remplir tous les champs.");
    }
}
///////////////////////paiment/////////
