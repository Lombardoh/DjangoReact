function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function lookup(method, endpoint, callback, data){
  let jsondata;
  if(data){
    jsondata = JSON.stringify(data)
  }
    const xhr = new XMLHttpRequest()
    const url = `http://localhost:8000/api${endpoint}`
    xhr.responseType = "json"
    const csrftoken = getCookie('csrftoken');
    xhr.open(method, url)
    xhr.setRequestHeader("Content-Type", "application/json")
    if(csrftoken){
      xhr.setRequestHeader("X-CSRFToken", csrftoken)
      xhr.setRequestHeader("HTTP_X_REQUEST_WITH", "XMLHttpRequest")
      xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest")
    }
  
    xhr.onload = function () {
      callback(xhr.response, xhr.status)
    }
    xhr.onerror = function (e) {
      callback({
        "message": "the request was an error"
      }, 400)
    }
    xhr.send(jsondata)
}

export function createTweet(newTweet, callback){
  lookup("POST", "/tweets/create/", callback, {content:newTweet})
}

export function loadTweets(callback) {
  lookup("GET", "/tweets/", callback)
  }