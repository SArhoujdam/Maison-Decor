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
function afficherPagelarge_choix() {
    window.location.href = ("{% url 'categories:categories_list' %}"); 
}

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
document.addEventListener('DOMContentLoaded', function () {
    const backgroundColor = localStorage.getItem('backgroundColor') || '#ffffff';
    const textColor = localStorage.getItem('textColor') || '#000000';
    const fontFamily = localStorage.getItem('fontFamily') || 'sans-serif';
    const navbarBgColor = localStorage.getItem('navbarBgColor') || '#ffffff';
    const navbarLinkColor = localStorage.getItem('navbarLinkColor') || '#000000';

    // Appliquer les styles sur le body
    document.body.style.backgroundColor = backgroundColor;
    document.body.style.color = textColor;
    document.body.style.fontFamily = fontFamily;

    // Appliquer les styles sur le navbar
    const navbar = document.querySelector('header, nav, #header');
    const navLinks = document.querySelectorAll('nav a');

    if (navbar) {
        navbar.style.backgroundColor = navbarBgColor;
    }

    navLinks.forEach(link => {
        link.style.color = navbarLinkColor;
    });
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
