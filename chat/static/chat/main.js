// Récupération des messages en ajax

$(document).ready(function(){
      var display = $("#display");
      setInterval(function(){
          $.ajax({
              type: 'GET',
              url : "/getMessages/{{room}}/",
              success: function(response){
                  console.log(response);
                  var isAtBottom = display.scrollTop() + display.innerHeight() >= display[0].scrollHeight;
                  $("#display").empty();
                  for (var key in response.messages)
                  {
                      var rawDate = new Date(response.messages[key].date);
                      var formattedDate = rawDate.toLocaleString('fr-FR', {day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute:'2-digit'});
                      var temp="<div class='darker'><b>"+response.messages[key].user+"</b><p>"+response.messages[key].value+"</p><span>"+formattedDate+"</span></div>";
                      $("#display").append(temp);
                  }
                  // Scroll to the bottom of the chat window if the user is already at the bottom
                  if (isAtBottom) {
                      $("#display").scrollTop($("#display")[0].scrollHeight);
                  }
              },
              error: function(response){
                  alert('An error occured')
              }
          });
      },500);
 });

// pour soumettre le formulaire en ajax
 $(document).on('submit','#post-form',function(e){
        e.preventDefault();

        $.ajax({
          type:'POST',
          url:'/send',
          data:{
              username:$('#username').val(),
              room_id:$('#room_id').val(),
              message:$('#message').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
          },
        //la  réponse HTTP pour signaler que le message a été envoyé avec succes
          success: function(data){
           // alert(data)
          }
        });
        document.getElementById('message').value = ''
});

$(document).ready(function(){
    var display = $("#display");
    setInterval(function(){
        $.ajax({
            type: 'GET',
            url: "{% url 'liste_messages' groupe_chat_id %}",  // Utilisation de l'URL avec l'ID du groupe de chat
            success: function(response){
                console.log(response);
                var isAtBottom = display.scrollTop() + display.innerHeight() >= display[0].scrollHeight;
                $("#display").empty();
                for (var key in response.messages) {
                    var message = response.messages[key];
                    var formattedDate = new Date(message.date_envoi).toLocaleString('fr-FR', {day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute:'2-digit'});
                    var temp = "<div class='darker'><b>" + message.auteur + "</b><p>" + message.contenu + "</p><span>" + formattedDate + "</span>";
                    if (message.file_url) {
                        if (message.is_image) {
                            temp += "<br><img src='" + message.file_url + "' alt='Prévisualisation' width='200'>";
                        } else {
                            temp += "<br><a href='" + message.file_url + "' target='_blank'>Télécharger le fichier</a>";
                        }
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
                alert('Une erreur s\'est produite');
            }
        });
    }, 500);
});
