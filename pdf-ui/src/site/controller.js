

function getSession(){
  session = document.getElementById('sessionid');
  sitename = document.getElementById('sitename');

  return [ session.value, sitename.value];
}


const isObject = obj => obj && typeof obj === 'object';
function cleanArrayValues(obj){
  if(isObject(obj))
    for (var key of Object.keys(obj)){
        if(Array.isArray(obj[key]))
            obj[key] = null;
        else
            cleanArrayValues(obj[key]);
  }
}





/*********************
*** Program Control
**********************/


function reloadPDF(){

    var [sessionId, sitename] = getSession();
    var msg = confirm("Do you want to reload "+sitename+" PDF from github?");
    if(!msg)
      return;

    var pdf = JSON.parse( gGetPDF(sessionId, sitename));

    for(category of document.getElementsByClassName('pdfData'))
        writeToHTML(category ,pdf);

}

function deletePDF(){

  var [sessionId, sitename] = getSession();
  var msg = confirm("Do you really want to delete "+sitename+"?");
  if(!msg)
    return;

  gDeletePDF(sessionId, sitename);

}

function savePDF(){

  var [sessionId, sitename] = getSession();
  var msg = confirm("Save?");
  if(!msg)
    return;

  //Load current version of PDF from Github except for array values
  var pdf = JSON.parse( gGetPDF(sessionId, sitename));
  cleanArrayValues(pdf);

  // Override PDF with new values from UI
  for(category of document.getElementsByClassName('pdfData'))
      pdf = mergeDeep(pdf, objectifyDiv(category));

  var success = gSavePDF(sessionId, sitename, pdf);
  if(!success){
    alert('Error: Failed to save!');
  }

}


function controllerLoop(){

    var [sessionId, sitename] = getSession();
    
    if(sessionId == '')
        login()

    isValidSession();

    //check for changes and update color of save button
    var pdf = JSON.parse( gGetPDF(sessionId, sitename));
    cleanArrayValues(pdf);
    for(category of document.getElementsByClassName('pdfData'))
        pdf = mergeDeep(pdf, objectifyDiv(category));

    var defaultPDF = JSON.parse( gGetPDF(sessionId, sitename));

    if(!_.isEqual(pdf, defaultPDF))
      document.getElementById('save-changes').classList.add('changed');
    else
      document.getElementById('save-changes').classList.remove('changed');

    setTimeout(controllerLoop, 1500);
}



function renewSession(){

  var [sessionId, sitename] = getSession();
  newsessionID = gRenewSession(sessionId);

  if(newsessionID == 0){
    alert('Session expired! Login again')
    login();
    return;
  }

  session = document.getElementById('sessionid');
  session.value = newsessionID;
  
  setTimeout(renewSession, 4000); 
}


function isValidSession(){

  var [sessionId, sitename] = getSession();
  if(!gCheckSession(sessionId)){
    alert('Session token revoked! Login again')
    login();
    return false;
  }
  return true;
}


function login(){

  username= 'nfvid';
  password='asdas';

  sessionid = gAuthenticate(username, password);


  session = document.getElementById('sessionid');
  session.value = sessionid;

}