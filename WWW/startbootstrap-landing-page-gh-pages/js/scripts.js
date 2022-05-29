

var el = x => document.getElementById(x);

function showPicker() {
    el("file-input").click();
    el("result-label").className = "alert alert-danger top-buffer no-display";
  }

function showPicked(input) {
    el("upload-label").innerHTML = input.files[0].name;
    el("upload-label").className = "badge badge-pill badge-info"
    el("upload-button").innerHTML = "Upload another photo!"
    el("image-picked").className = "rounded mx-auto d-block fit-inside"

    // Read the file from user upload
    var reader = new FileReader();
    reader.onload = function(e) {
        el("image-picked").src = e.target.result
    }
    reader.readAsDataURL(input.files[0]);
  }

  function analyse() {
    var uploadFiles = el("file-input").files;
    if (uploadFiles.length !== 1) {
      alert("Please select a file to analyse");
      el("result-label").className = "alert alert-danger top-buffer";
    } else {
  
      el("upload-button").className = "btn btn-light no-display";
      el("analyse-button").className = "btn btn-light no-display";
      el("result-announcement").className = "alert alert-warning";
      el("result-spinner").className = "spinner-border text-light";

      var xhr = new XMLHttpRequest();
      xhr.open("POST", `https://puparazziservice-k7kqwtqxdq-uc.a.run.app/predict`,
        true);
      xhr.onerror = function() {
        alert(`Sorry, someting went wrong. Try again. ${xhr.responseText}`);
        el("result-label").className = "alert alert-danger top-buffer";
        el("reset-button").className = "btn btn-light";
        el("result-announcement").className = "alert alert-warning no-display";
        el("result-spinner").className = "spinner-border text-light no-display";
      };
      xhr.onload = function(e) {
        if (this.readyState === 4) {
          var response = JSON.parse(e.target.responseText);

          let probs = response.map(a => a.prob);
          probs = formatProb(probs)
          let breed = response.map(a => a.class)

          // Insert main prediction
          el("result-label").innerHTML = `I am <b>${probs[0]}%</b> sure this is a <b><a href="https://www.google.com/search?q=dog+${breed[0].replaceAll('_','+')}" target="_blank">${breed[0].replaceAll("_"," ")}</a></b>`;
          el("result-label").className = "alert alert-success top-buffer"

          // Insert other results
          el("OR-container").className = ""
          
          for (let i = 1; i < response.length; i++) {
            el(`OR${i}-title`).innerHTML = `Option ${i}: <a href="https://www.google.com/search?q=dog+${breed[i].replaceAll('_','+')}" target="_blank">${breed[i].replaceAll("_"," ")}</a>`
            el(`OR${i}-prob`).innerHTML = `I am ${probs[i]}% sure`
            el(`OR${i}-img`).src = `assets/img/dogs/${breed[i]}.jpg`
          }
        }
        el("reset-button").className = "btn btn-light";
        el("result-announcement").className = "alert alert-warning no-display";
        el("result-spinner").className = "spinner-border text-light no-display";
      };
    
      var fileData = new FormData();
      fileData.append("file", uploadFiles[0]);
      xhr.send(fileData);
    }
  }

  function formatBreed(array) {
    var output = [];
    for (let index = 0; index < array.length; index++) {
      output.push(array[index].replaceAll("_"," "));
    }
    return output
  }

  function formatProb(array) {
    var output = [];
    for (let index = 0; index < array.length; index++) {
      output.push((array[index]*100).toFixed(1));
    }
    return output
  }