/*
Make sure the versions are consistent across calendars.
The script belongs to each individual calendar to reduce the number of things that need to be shared.
Making the script a library requires another access to be distributed to users.
The repository is https://bitbucket.org/dcollins4096/fsu_seminar_calendar

changeset:   --
tag:         tip
user:        dcollins4096
date:        Fri Jun 01 09:42:05 2018 -0400
summary:     First good draft.
*/
//
//
// Notes:
//.  The Duration key exists but isn't on the sheet.
var valueSelector = function(line, head_line,meta_data){
  var general_defaults={};
  general_defaults['Series']='Please select series';
  general_defaults['Date']=new Date();
  general_defaults['Time']='';
  general_defaults['Location'] = '';
  general_defaults['Speaker']='';
  general_defaults['Affiliation']='';
  general_defaults['Title']='';
  general_defaults['Abstract']='';
  general_defaults['Publish']='';
  general_defaults['Host']='';
  general_defaults['Travel']='';
  general_defaults['Accomodation']='';
  general_defaults['Duration'] = 1;
  general_defaults['CalendarEventID']=null;
  general_defaults['Test']='';
  var get = function(key){
    var meta_value = meta_data[key];
    var output = general_defaults[key];
    var default_this_series = meta_data[key];
    if ( meta_value != undefined ){
      output = meta_value;
    }
    var this_index = head_line.indexOf(key);
    if ( this_index != -1 ){
      //most values are strings, so if the length is non-zero use the value.
      //For the dates, the length will be undefined if it exists.
      if ( line[this_index].length > 0 ){
        output = line[this_index];
      }
      if ( (key=='Date' || key == 'Time') && line[this_index].length == undefined ){
        output = line[this_index];
      }
    }
    return output
  }//return the extractor funciton get(key)
  return get
}

var event = function(this_line,head_line,metaData,sheetPackage){
  //The main event object.
  //Stores all the information (at the end) subject to defaults (both in metaData and general sane defaults);
  //has some getter methods that sanatize the data.
  //

  this.Errors = [];
  this.calendar_event_id = null;
  var getValue = valueSelector(this_line, head_line,metaData);
  this.checkDate = function(dateToCheck){
    //Error checking for dates.  Should get fleshed out more.
    if ( dateToCheck.getTime == undefined ){
      var thisStatus = sheetPackage.getBoxByID( sheetPackage.currentLine, 'Status');
      thisStatus.setValue('Poorly Formatted Date');SpreadsheetApp.flush();
      this.Errors.push('Date');
    }
    return dateToCheck;
  }

  this.Series            = getValue("Series"); //this_line[ head_line.indexOf('Series')];
  this.Date              = this.checkDate(getValue("Date"));
  this.Time              = getValue("Time");
  this.Duration          = getValue("Duration");
  this.Speaker           = getValue('Speaker');
  this.Affiliation       = getValue('Affiliation');
  this.Title             = getValue('Title');
  this.Location          = getValue('Location');
  this.Abstract          = getValue('Abstract');
  this.Publish           = getValue('Publish');
  this.Publish           = this.Publish.toLowerCase();
  this.Host              = getValue('Host');
  this.Travel            = getValue('Travel');
  this.Accomodation      = getValue('Accomodation');
  this.CalendarEventID   = getValue('CalendarEventID');
  this.TestBoxIndex      =  head_line.indexOf('Alert');
  this.CalendarID        = getValue('calendar id');

  //var thisStatus = sheetPackage.getBoxByID( sheetPackage.currentLine, 'Status');
  //var thisName = sheetPackage.getBoxByID( sheetPackage.currentLine, 'Speaker').getValue();

  //thisStatus.setValue(this_line[6]);

  this.getCalendarURL = function(){
    //This presently does not work.
    //https://stackoverflow.com/questions/10553846/get-link-url-to-an-calendar-event-in-google-apps-script?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    var eventURL = "";
    if( this.CalendarEventID != null ){
      var mycal = 'fsuphysicsrooms@m'
      var splitEventId = this.CalendarEventID.split('@');
      var eventURL = "https://www.google.com/calendar/event?eid=" +
      Utilities.base64Encode(splitEventId[0] + " " + mycal).toString().replace('=','');

      //var splitEventId = this.CalendarEventID.split('@');
      //eventURL = "https://www.google.com/calendar/event?eid=" + Utilities.base64Encode(splitEventId[0] + " " + this.CalendarId);
    }
    return eventURL;


  }


  this.getLocation = function(){
    return this.Location.trim();
  }
  this.getTalkTitle = function(){
    var output = this.Title.trim()
    output = '"' + output + '"';
    return output;
  }

  this.getDescription = function(){
    var output = String(this.Abstract);
    output = output.trim();
    return output;
  }
  this.getAffiliation = function(){

    var output = "";
    if ( this.Affiliation != '' ){
      output = " ("+ this.Affiliation + ")";
    }
    return output;

  }
  this.getTitle = function(){
    var fullTitle = this.getSeriesName() + ": " + this.getSpeakerName() + this.getAffiliation();
    if ( this.Title.trim().length > 0 ){
      fullTitle += ", "+ this.getTalkTitle();
    }
    return fullTitle
  }
  this.getStartTime = function(){
    //Assemble the date and time.  Correct for AM/PM.
    var eventDate = this.Date;
    if ( this.Time.split == undefined ){
      var HoursMinutes = [this.Time.getHours(), this.Time.getMinutes()];
      var tree;
    }else{
      var HoursMinutes = this.Time.split(":");
    }
    if ( HoursMinutes[0] < 7 ){
      HoursMinutes[0] += 12;
    }
    eventDate.setHours(HoursMinutes[0]);
    eventDate.setMinutes(HoursMinutes[1]);
    return eventDate;
  }
  this.getEndTime = function(){
    var endTime = new Date(this.getStartTime().getTime() + this.Duration*3600*1000);
    return endTime;
  }
  this.getSeriesName = function(){
    //This might need more work.
    var seriesMap = {}
    seriesMap["AST"] = "Astrophysics Seminar";
    seriesMap["NUC"] =  "Nuclear Physics Seminar";
    seriesMap["COL"] = "Physics Colloquium";
    seriesMap["COND"] = "Condensed Matter Seminar";
    seriesMap["HEP"] = "High Energy Physics Seminar";
    seriesMap["GRAD"] = "Graduate Student Seminar";
    var output = this.Series;
    if ( seriesMap[this.Series] != undefined ){
      output = seriesMap[this.Series];
    }
    return output;
  }
  this.getSpeakerName = function(){
    //Swap the first and last if there's a comma.
    var output = this.Speaker;
    var ind = this.Speaker.indexOf(',');
    if ( ind > -1 ){
     var thisSplit = this.Speaker.split(',');
     output = thisSplit[1].trim() + ' ' + thisSplit[0].trim();
    }
    return output;
  }
  this.updateCalendarEvent = function(thisCalendarEvent, newEvent){
    //time
    //title
    //location
    //description
    var update={time:false,location:newEvent,description:newEvent,title:false}

    if ( newEvent != true){
      if ( thisCalendarEvent.getLocation() != this.getLocation() ){ update.location=true;}
      if ( Math.abs(thisCalendarEvent.getStartTime() - this.getStartTime()) > 60*1000 ){ update.time=true;}
      if ( Math.abs(thisCalendarEvent.getEndTime() - this.getEndTime()) > 60*1000 ){ update.time=true;}
      if ( thisCalendarEvent.getTitle() != this.getTitle() ){ update.title=true;}


    }
    if ( update.location ) {thisCalendarEvent.setLocation( this.getLocation() );}
    if ( update.description ) {thisCalendarEvent.setDescription( this.getDescription() );}
    if ( update.time ){ thisCalendarEvent.setTime(this.getStartTime(), this.getEndTime()); }
    if ( update.title ) { thisCalendarEvent.setTitle( this.getTitle() ); }

  }



};
var boxFetcher = function(sheet,headLineNumber,headLine, alertBoxID){
  var getBoxByID = function(line,id){
    var thisID = headLine.indexOf(id);
    if ( thisID < 0 ){
      var testBox = sheet.getRange(alertBoxID);
      testBox.setValue('Error: Unable to locate column "'+id+ '". Save and contact Collins.');
      SpreadsheetApp.flush();
      testBox.setBackground('red');
    }
    var thisBox = sheet.getRange(line+headLineNumber+1,thisID + 1);
    return thisBox
  }
  return getBoxByID;
};
var findHeadLine = function(sheet, testBox){
  //Find the headder information:
  //headLine, headLineNumber, metaData
  var lastRow = sheet.getLastRow();
  var lastColumn = sheet.getLastColumn();
  var headLineNumber = -1;
  var metaData={};

  for ( var i=1;i<lastRow;i++){
    var thisRow = sheet.getRange(i,1,1,lastColumn).getValues()[0];
    var ok = true;
    var checkForThese = ['Status','Publish','Speaker','CalendarEventID'];
    for ( var j=0; j < checkForThese.length; j++){
      if ( thisRow.indexOf(checkForThese[j]) < 0){
        ok = false;
      }
    }
    if ( ok == true){
      headLineNumber = i;
      break;
    }else{
      var name = thisRow[0]
      metaData[name]=thisRow[1];
    }
  }

  //also sanitize the head row.
  var headLine = thisRow;
  for ( var i=0;i<thisRow.length;i++){
    headLine[i] = thisRow[i].trim();
  }
  metaData['headLine'] = headLine;


  return {headLineNumber:headLineNumber, headLine:headLine, metaData:metaData}
};

function CalendarPusher() {
  //Read the spreaadsheet.
  //For each line after the headder row,
  //create/update/delete calendar items.

  //spreadsheet variables
  var sheet = SpreadsheetApp.getActiveSheet();
  var alertBoxID = 'B5';
  var testBox = sheet.getRange(alertBoxID);
  testBox.setValue('Parse header'); testBox.setBackground(null); SpreadsheetApp.flush();

  var lastRow = sheet.getLastRow();
  var lastColumn = sheet.getLastColumn();

  //Find the structure.
  var headStock = findHeadLine(sheet, testBox);
  var headLine = headStock.headLine;
  var headLineNumber = headStock.headLineNumber;
  var metaData = headStock.metaData;

  var calendar = CalendarApp.getCalendarById(metaData['calendar id']);

  var getBoxByID = new boxFetcher(sheet,headLineNumber,headLine, alertBoxID);
  var sheetPackage = {sheet:sheet, getBoxByID:getBoxByID, alertBox:testBox};  //things for debugging.
  if ( 1 == 1 ){
  testBox.setValue('Start Loop'); SpreadsheetApp.flush();

  var eventRange =   sheet.getRange(headLineNumber+1,1,lastRow,lastColumn);
  eventRange.setBackground(null); SpreadsheetApp.flush();
  var events = eventRange.getValues();
  for (var i=0;i< lastRow - headLineNumber; i++){
    var thisThing = events[i];
    sheetPackage.currentLine = i;
    var thisEvent = new event(thisThing,headLine, metaData,sheetPackage);
    var thisTestBox = getBoxByID(i,'Status');
    //testBox.setValue('Working, clown '+i + " " + thisEvent.Speaker); SpreadsheetApp.flush();
    //Utilities.sleep(1000);
    //continue;

    //Check for errors.  Not well fleshed out.
    var somethingBroke=false;
    for ( var nError = 0; nError < thisEvent.Errors.length; nError++){
      var brokenBox = getBoxByID(i,thisEvent.Errors[nError]);
      brokenBox.setBackground('red');
      somethingBroke=true;
    }

    if ( thisEvent.Publish== 'stop' || somethingBroke){
    testBox.setValue('Something broke.'); 
    testBox.setBackground('red');
      break;
    }

    //Publish, or delete.
    var thisCalendarIdBox = getBoxByID(i,'CalendarEventID');
    thisTestBox.setValue('Unchanged');

    if ( thisEvent.Publish == 'yes'){
      thisTestBox.setBackground('yellow')
      var makeNewCalendarEvent = true; //this is for debugging only.
      if ( makeNewCalendarEvent == true ){
        if ( thisEvent.CalendarEventID == null ){
          thisTestBox.setValue( 'Creating new event'); SpreadsheetApp.flush();

          var thisCalendarEvent = calendar.createEvent(thisEvent.getTitle(), thisEvent.getStartTime(), thisEvent.getEndTime());
          thisEvent.updateCalendarEvent( thisCalendarEvent,newEvent=true);
          thisEvent.CalendarEventID = thisCalendarEvent.getId();

          thisTestBox.setValue( 'Published');
          //thisTestBox.setBackground(null);

        }else{
          var thisCalendarEvent = calendar.getEventById(thisEvent.CalendarEventID);
          if ( thisCalendarEvent == null ){
            testBox.setValue("Error: Calendar Event Not Found. "+thisEvent.CalendarEventID);
          }else{
            thisTestBox.setValue( 'Fetching existing event.'); SpreadsheetApp.flush();
            var newID = thisCalendarEvent.getId();
            thisTestBox.setValue('t12 Existing ID ' + thisEvent.CalendarEventID );
            if ( newID != thisEvent.CalendarEventID ){
              testBox.setValue('Error: event ID mismatch');
            }
            thisTestBox.setValue( 'Even exists: updating values');
            thisEvent.updateCalendarEvent( thisCalendarEvent,newEvent=false);
            thisTestBox.setValue('Updated');
          }

        }
        thisCalendarIdBox.setValue(thisEvent.CalendarEventID);
      }//makeNewCalendarEvent
      //The url should be done, but doesn't work right now.
      //thisTestBox.setValue( thisEvent.getCalendarURL() );

    }//end publish yes
    if ( thisEvent.Publish == 'wut' ){  //A PLACE FOR DEBUGGING.
      if ( thisEvent.CalendarEventID == null ){
        thisTestBox.setValue('No id, cant query'); SpreadsheetApp.flush();
        
      }else{
        //here we get the URL for the event.
        // code from https://stackoverflow.com/questions/10553846/get-link-url-to-an-calendar-event-in-google-apps-script/47481173
        var thisCalendarEvent = calendar.getEventById(thisEvent.CalendarEventID);
        var newID = thisCalendarEvent.getId();
        var mycal = metaData['calendar id'];
        var splitEventId = thisCalendarEvent.getId().split('@');
        var eventUrl = "https://www.google.com/calendar/event?eid=" + 
        Utilities.base64Encode(splitEventId[0] + " " + mycal).toString().replace('=','');
        //thisTestBox.setValue(eventUrl); SpreadsheetApp.flush();
        thisTestBox.setValue(thisEvent.getStartTime()); SpreadsheetApp.flush();
      }
      
    }// end publish wut
    
    if ( thisEvent.Publish == 'delete'){
      thisTestBox.setValue( 'Deleting event'); SpreadsheetApp.flush();
      if ( thisEvent.CalendarEventID != null ){
        var thisCalendarEvent = calendar.getEventById(thisEvent.CalendarEventID);
        thisCalendarEvent.deleteEvent();
        thisEvent.CalendarEventID = null;
        thisCalendarIdBox.setValue('');
        var thisPublishBox = getBoxByID(i,'Publish');
        thisPublishBox.setValue("");
      }
      thisTestBox.setValue('Deleted from Calendar.');
      //thisTestBox.setBackground(null);
    }//delete
  thisTestBox.setBackground(null);
  }

  }// main work conditional (0==1)
  if ( ! somethingBroke ){
  testBox.setValue('Finished.'); testBox.setBackground(null);
  }
}

function onOpen(){
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var menuEntries=[];
  menuEntries.push({name:'UpdateCalendar',functionName:'CalendarPusher'});
  sheet.addMenu("Push Calendar Items",menuEntries);
}
