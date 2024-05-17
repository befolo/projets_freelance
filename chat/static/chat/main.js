$(document).ready(function(){
    var display = $("#display");
    setInterval(function(){
        $.ajax({
            type: 'GET',
            url: "/chat/messages/{{groupe_id}}",  // Utilisation de l'URL avec l'ID du groupe de chat
            success: function(response){
                console.log(response);
                var isAtBottom = display.scrollTop() + display.innerHeight() >= display[0].scrollHeight;
                $("#display").empty();
                for (var key in response.messages) {
                    var message = response.messages[key];
                    var rawDate = new Date(response.messages[key].date);
                    var formattedDate = rawDate.toLocaleString('fr-FR', {day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute:'2-digit'});
                    var temp = "<div class='darker div_file'><b>" + message.auteur + " --  " + message.role + "</b><p>" + message.contenu + "</p><span>" + formattedDate + "</span>";
                    if (message.file_url) {
                        if (message.is_image) {
                            temp += "<br><img src='" + message.file_url + "' alt='Prévisualisation' width='200'>";
                        } else {
                            temp += "<br><a href='" + message.file_url + "' target='_blank'>Télécharger le fichier</a>";
                        }
                    }

                    if (message.lien_supprimer) {
                        temp += "<br><a href='{% url 'msg_spp'"+ message.id +"%}' target='_blank'>Télécharger le fichier</a>";
                    }

                    temp += "</div>";
                    $("#display").append(temp);
                }
                // Scroll to the bottom of the chat window if the user is already at the bottom
                if (isAtBottom) {
                    $("#display").scrollTop($("#display")[0].scrollHeight);
                }
            },
            error: function(response){
                console.log('Une erreur s\'est produite');
            }
        });
    }, 500);
});
