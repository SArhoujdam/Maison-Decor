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


