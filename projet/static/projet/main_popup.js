$(document).ready(function() {
    // Ouvrir la popup
    $('.open-popup').click(function(e) {
        e.preventDefault();
        var popup = $(this).next('.popup');
        popup.data('originalParent', popup.parent());  // Stocker le parent original
        $('body').append(popup);
        popup.show();
        $('body').css('overflow', 'hidden');  /* Désactive le défilement */
    });

    // Fermer la popup
    $('.close-popup').click(function(e) {
        e.preventDefault();
        var popup = $(this).closest('.popup');
        popup.hide();
        popup.data('originalParent').append(popup);  // Remettre la popup à sa place originale
        $('body').css('overflow', 'auto');  /* Réactive le défilement */
    });
});

