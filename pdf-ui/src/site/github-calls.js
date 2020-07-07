
function gCheckSession(sessionId){
    //checks if session is valid?
    // return true/false
    if(sessionId==419789456)
        return true;
    else
        return false;
}

function gRenewSession(sessionid){
  
  if(!isValidSession())
    return;

  // if valid, then create new token ID(sessionid) and return
  if(sessionid==419789456)
      return 419789456;
  // if not valid, then return 0
      return 0;
}

function gListAllSite(sessionid){
  
  if(!isValidSession())
    return;

  return ['pod10', 'pod15', 'pod17', 'pod18'];
}

function gAddNewSite(sessionid, sitename){

  if(!isValidSession())
    return;

  //add new site with name sitename

}

function gGetPDF(sessionid, sitename){

  if(!isValidSession())
    return;

  var pdf = '{"_comment_head1":"User should Configure all profiles. Add new, if reqd.", \
  "_comment_head2":"User should Configure the roles", \
  "_comment_head3":"All infos should be filled by the user", \
  "_comment_head4":"The servers data will be automatically generated", \
  "_comment_info1":"All Infos", \
  "management_info": { \
    "owner":"Dummy Name", \
    "area_name": "Dummy Area Name", \
    "area_center_name": "Dummy Center Name", \
    "room_id": "Dummy Room ID 5", \
    "city": "Dummy City Name", \
    "resource_pool_name": "Dummy resource Pool name" \
  }, \
  "jumphost_info": { \
    "ip":"", \
    "name":"" \
  }, \
  "rack_info": [ \
    { \
      "rack_id":"Dummy Rack ID", \
      "rack_details": { \
        "rack_name":"Dummy Rack Name", \
        "rack_description":"Dummy Rack Description" \
      } \
    }   \
  ] \
  }';
  
  return pdf;
}

function gDeletePDF(sessionid, sitename){

  if(!isValidSession())
    return;

  // delete pdf with sitename
  console.log('Deleted '+sitename);
}

function gSavePDF(sessionid, sitename, pdf){

  if(!isValidSession())
    return false;


    // save pdf with sitename(note github server should check if PDF is valid before pushing to github)
    console.log(pdf);
    return true;

    // Return bool
        // True --> success
        // False --> fail
}