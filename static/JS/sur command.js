const bar = document.getElementById('bar');
const navbar = document.getElementById('mobile');
const Close = document.getElementById('Close');

bar.addEventListener('click', function () {
    navbar.classList.add('active'); // Change nav to navbar
    
    if (mobile) {
        mobile.addEventListener("click", () => {
            
        })
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

const choix = document.getElementById('choix').addEventListener('change', function() {
    var selectedOption = this.value;
    // Exemple d'action basée sur l'option sélectionnée
    switch(selectedOption) {
        case 'option1':
            alert('Vous avez choisi l\'input');
            break;
        case 'option2':
            alert('Vous avez choisi l\'option 2');
            break;
        case 'option3':
            alert('Vous avez choisi l\'option 3');
            break;
        case 'option4':
            alert('Vous avez choisi l\'option 4');
            break;
        default:
            alert('Option invalide');
    }
        });


