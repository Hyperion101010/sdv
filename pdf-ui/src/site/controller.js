

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

function syncSiteList(){

  var [sessionId, l] = getSession();
  var sitelist = gListAllSite(sessionId);

  var site = document.getElementById('sitename');
  for (i = site.length - 1; i >= 0; i--) 
    site.remove(i);

  for(sitename of sitelist){
    var newoption = document.createElement('option');
    newoption.value = sitename;
    newoption.appendChild( document.createTextNode(sitename) )
    site.appendChild(newoption);
  }

}

function loadNewDefaultPDF(){

  var defaultPDF = '{ "management_info": { "owner":"New Name", "area_name": "New Area Name", \
    "area_center_name": "New Center Name", \
    "room_id": "New Room ID 5", "city": "New City Name", \
    "resource_pool_name": "New resource Pool name" }, \
  "rack_info": [ \
    { "rack_id":"New Rack ID", \
      "rack_details": { "rack_name":"New Rack Name", \
        "rack_description":"New Rack Description" } }]}';

  defaultPDF = JSON.parse(defaultPDF);

  for(category of document.getElementsByClassName('pdfData'))
      writeToHTML(category ,defaultPDF);
}





/*********************
*** Program Control
**********************/

function addNewPDF(){
    var sitename = prompt('Enter site name');

    var [sessionId, l] = getSession();

    if(sitename === null)
        return;

    gAddNewSite(sessionId, sitename);

    syncSiteList();
    document.getElementById('sitename').value = sitename;
    loadNewDefaultPDF();
}

function reloadPDF(){

    var [sessionId, sitename] = getSession();
    var msg = confirm("Do you want to reload "+sitename+" PDF from github?");
    if(!msg)
      return;

    var [sessionId, sitename] = getSession();
    var pdf = JSON.parse( gGetPDF(sessionId, sitename));

    for(category of document.getElementsByClassName('pdfData'))
        writeToHTML(category ,pdf);

}

function deletePDF(){

  var [sessionId, sitename] = getSession();
  var msg = confirm("Do you really want to delete "+sitename+"?");
  if(!msg)
    return;

  var [sessionId, sitename] = getSession();
  gDeletePDF(sessionId, sitename);

  window.location.href = '/site?session='+sessionId;

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
    alert('Invalid session! Login again')
    login();
    return false;
  }
  return true;
}


function login(){
    window.location.href="/login"; 
}


function loadpage(){

  var urlParams = new URLSearchParams(window.location.search);
  document.getElementById('sessionid').value = urlParams.get('session');

  syncSiteList();
  document.getElementById('sitename').selectedIndex = '0';

  var [sessionId, sitename] = getSession();
  var pdf = JSON.parse( gGetPDF(sessionId, sitename));

  for(category of document.getElementsByClassName('pdfData'))
       writeToHTML(category ,pdf);

  renewSession();
  controllerLoop();
}

function siteChanged(){
  
  var [sessionId, sitename] = getSession();
  var pdf = JSON.parse( gGetPDF(sessionId, sitename));

  for(category of document.getElementsByClassName('pdfData'))
       writeToHTML(category ,pdf);
}