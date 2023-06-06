var current_course_id = -1;
var current_course_type = "course";

function loadChat(course_id, course_name, course_type) {
  current_course_id = course_id;
  current_course_type = course_type;
  var target_url = "";
  if (course_type == "course") {
    target_url = '/chat/courses/'+course_id;
  }
  else {
    target_url = '/chat/groups/'+course_id;
  }
  $.get(target_url, function(response_data, status){
    var finalHtml = "";
    var lastSender = -1;
    for (const message_id in response_data) {
      message = response_data[message_id];
      if (message.sender == currentUserID) {
        finalHtml += `
        <div class="message text-only">
          <div class="response">
            <p class="text">${message.message}</p>
          </div>
        </div>
        `;
      }
      else {
        if (lastSender != message.sender) {
            displayImageUrl = `${staticPhotosFolder}/blank_profile.png`;
            if (message.user_image_url) {
                displayImageUrl = message.user_image_url;
            }
            finalHtml += `
              <div class="message text-only">
                <div class="photo" style="background-image: url(${displayImageUrl});"></div>
                <p class="text">${message.message}</p>
              </div>
            `;
          }
          else {
            finalHtml += `
                <div class="message text-only">
                  <div style="width: 45px; display: block;"></div>
                  <p class="text">${message.message}</p>
                </div>
              `;
          }
        }
      lastSender = message.sender;
    }
    document.getElementById("selected-chat-name").innerHTML = course_name;
    document.getElementById("messages-chat").innerHTML = finalHtml;
  });
}

function sendMessage()
{
  var message = document.getElementById("chatTextBox").value;
  var request = {
      message: message,
      csrfmiddlewaretoken: csrf_token,
    }
  if (current_course_type == "course") {
    request["courseId"] = current_course_id;
  }
  else {
    request["groupId"] = current_course_id;
  }
  $.post('/chat/post-message/',
    request,
    function(data, status){
        document.getElementById("chatTextBox").value = "";
        document.getElementById("messages-chat").innerHTML += `
        <div class="message text-only">
          <div class="response">
            <p class="text">${message}</p>
          </div>
        </div>
        `;
    });
}
