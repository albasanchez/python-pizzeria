function sendRequest(url, csrf_token, data){
  return new Promise((resolve, reject) => {
    axios({
      method : "POST",
      url: url,
      headers: {'X-CSRFTOKEN': csrf_token, 'Content-Type': 'application/json'},
      data : data,
    }).then(response => {
      resolve(response.data);
    }).catch(err => {
      reject(err);
    });
  });
}
