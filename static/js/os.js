function getOSActual(name, major) {
    fetch(`/os_actual?os=${name}&version=${major}`)
      .then(response => {
        if (response.ok) {
          respuesta = response.text();
          if (respuesta instanceof Promise) {
            respuesta.then(data => {
              const navegadorActualSpan = document.getElementById('os_actual');
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

  function getMalwareDetector() {
    fetch(`/blacklist`)
      .then(response => {
        if (response.ok) {
          respuesta = response.text();
          if (respuesta instanceof Promise) {
            respuesta.then(data => {
              const navegadorActualSpan = document.getElementById('malware_activo');
              navegadorActualSpan.textContent = " ";
              if (data == "OK") {
                navegadorActualSpan.textContent =navegadorActualSpan.textContent + "No se detectó acceso malicioso";
              } else if (data == "NOK") {
                navegadorActualSpan.textContent =navegadorActualSpan.textContent + "Tu teléfono hizo al menos un acceso a dominios con malware o virus";
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
getMalwareDetector();