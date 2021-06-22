function lookup(method, endpoint, callback, data){
  let jsondata;
  if(data){
    jsondata = JSON.stringify(data)
  }
    const xhr = new XMLHttpRequest()
    const url = `http://localhost:8000/api/${endpoint}`
    xhr.responseType = "json"
    xhr.open(method, url)
  
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

export function loadTweets(callback) {
  lookup("GET", "/tweets/", callback)
  }