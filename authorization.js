# THIS IS MY FUNCTION THAT WORKS IN GOOGLE APP SCRIPT. I NEED TO CONVERT IT TO PYTHON, BUT THE PYTHON ONE ISN'T WORKING.

function login() {
  
  var usrname = "MY EMAIL HERE";
  var pwd = "MY PASSWORD HERE";
  
  var URL = "https://api.pocketcasts.com/user/login";
  var origin = "https://play.pocketcasts.com";
  var payload = {email: usrname, password: pwd, scope: "webplayer"};
  
  var options = {
    "headers": {
      "Origin": origin
    },
    "method" : "POST",
    "payload": payload,
  }
  var token = JSON.parse(UrlFetchApp.fetch(URL, options).getContentText()).token;
  
  var tokenRange = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Settings').getRange("C5");
  tokenRange.setValues([[token]]);
  Logger.log(token);
  
  
}
