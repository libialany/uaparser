function generateCookieValue() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let cookieValue = '';
  for (let i = 0; i < 32; i++) {
    cookieValue += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return cookieValue;
}
function getCookieValue() {
  const name = 'visitor_id';
  const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
  if (cookieValue) {
    return cookieValue;
  } else {
    const newCookieValue = generateCookieValue();
    document.cookie = `${name}=${newCookieValue}; path=/; max-age=31536000`; // Set cookie to expire in 1 year
    return newCookieValue;
  }
}
const visitorId = getCookieValue();
console.log('Visitor ID:', visitorId);

function statusClient() {
  fetch('/status-client', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ visitorId })
  })
    .then(response => {
      if (response.ok) {
        console.log('POST request successful');
      } else {
        console.error('POST request failed');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

setInterval(statusClient, 10000);
statusClient();

function getNavegadorActual(name, major) {
  fetch(`/navegador_actual?navegador=${name}&version=${major}`)
    .then(response => {
      if (response.ok) {
        respuesta = response.text();
        if (respuesta instanceof Promise) {
          respuesta.then(data => {
            const navegadorActualSpan = document.getElementById('navegador_actual');
            navegadorActualSpan.textContent = name + " " + major + " ";
            if (data == "OK") {
              navegadorActualSpan.textContent =navegadorActualSpan.textContent + "Si es actual";
            } else if (data == "NOK") {
              navegadorActualSpan.textContent =navegadorActualSpan.textContent + "No es actual";
            } else {
              navegadorActualSpan.textContent =navegadorActualSpan.textContent + "No se pudo determinar";
            }
          }).catch(error => {
            console.error('Error occurred:', error);
          });
        } else {
          console.log('The variable is not a Promise.');
        }
      } else {
        throw new Error('GET request failed');
      }
    });
}


function getVisitantes() {
    fetch(`/usuariosactivos`)
      .then(response => {
        if (response.ok) {
          respuesta = response.text();
          if (respuesta instanceof Promise) {
            respuesta.then(data => {
              const navegadorActualSpan = document.getElementById('usuarios_activos');
              navegadorActualSpan.textContent = data;
            }).catch(error => {
              console.error('Error occurred:', error);
            });
          } else {
            console.log('The variable is not a Promise.');
          }
        } else {
          throw new Error('GET request failed');
        }
      });
  }
getVisitantes();
setInterval(getVisitantes, 20000);
// getNavegadorActual();
