var weekday = new Array(7);
weekday[0]="Sunday";
weekday[1]="Monday";
weekday[2]="Tuesday";
weekday[3]="Wednesday";
weekday[4]="Thursday";
weekday[5]="Friday";
weekday[6]="Saturday";

var month = new Array(12);
month[0] = "January";
month[1] = "February";
month[2] = "March";
month[3] = "April";
month[4] = "May";
month[5] = "June";
month[6] = "July";
month[7] = "August";
month[8] = "September";
month[9] = "October";
month[10] = "November";
month[11] = "December";

$(document).ready(function(){
  
  if($("#start_day").size() > 0){
    $("#sections li#"+$("#section").val()+" button").addClass("selected");
  
    adjDeskerHeight();
  
    adjAssignHeight();
  
    viewDashboard($("#section").val(), $("#start_day").val(), $("#end_day").val());
  
    $("#sections li button").live("click",function(){
      newSection = $(this).parent().attr("id");
      viewDashboard(newSection, $("#start_day").val(), $("#end_day").val())
    });
  
    $("#prev-week").click(function(){
      changeWeek("prev");
    });
    $("#next-week").click(function(){
      changeWeek("next");
    });
  }
  
});

function changeWeek(dir){
  if(dir == "next"){
    change = 7;
  }else if(dir == "prev"){
    change = -7;
  }else {
    change = 0;
  }
  
  start = $("#start_day").val();
  end = $("#end_day").val();
  
  startDay = new mustrunDate(start);
  endDay = new mustrunDate(end);
  //alert("Start/End: "+startDay.YMD+"/"+endDay.YMD);
  
  tempStart = new Date(startDay.date);
  tempStart.setDate(startDay.date.getDate() + change);
  newStart = new mustrunDate(tempStart);
  //alert("New Start: "+newStart.YMD);
  
  tempEnd = new Date(endDay.date);
  tempEnd.setDate(endDay.date.getDate() + change);
  newEnd = new mustrunDate(tempEnd);
  //alert("New End: "+newEnd.YMD);
  
  viewDashboard($("#section").val(), newStart.YMD, newEnd.YMD);
  
}

function viewDashboard(section, start, end){
  buildCal(section, start, end);
//  buildDeskers(section, start, end);
  $("#sections li#"+$("#section").val()+" button").removeClass("selected");
  $("#sections li#"+section+" button").addClass("selected");
  $("#section").val(section)
  $("#start_day").val(start)
  $("#end_day").val(end)
}

function adjDeskerHeight(){
  var deskersHeight = 0;
  
  $(".deskers").each(function(index) {
    thisDivHeight = 0;
    $(this).children().each(function(index){
      thisDivHeight += $(this).outerHeight();
      thisDivHeight += parseInt($(this).css("margin-bottom"));
      thisDivHeight += parseInt($(this).css("margin-top"));
    });
    
    if(thisDivHeight > deskersHeight){
      deskersHeight = thisDivHeight;
    }
  });
  $(".deskers").height(deskersHeight);
}

function adjAssignHeight(){
  var assignmentsHeight = 0;
  
  $(".assignments").each(function(index) {
    thisDivHeight = 0;
    $(this).children("div").each(function(index){
      thisDivHeight += $(this).outerHeight();
      thisDivHeight += parseInt($(this).css("margin-bottom"));
      thisDivHeight += parseInt($(this).css("margin-top"));
    });
    
    if(thisDivHeight > assignmentsHeight){
      assignmentsHeight = thisDivHeight;
    }
  });
  
  $(".assignments").height(assignmentsHeight);
}

function addDeskerField(dayID){
  formDiv = mkDiv(["desker"]);
  
  deskerField = document.createElement("input");
  $(deskerField).attr("type","text").attr("name","desker-name").addClass("text").width("100%").keyup(function(event){
    if(event.keyCode == '13'){
      addDesker($(this).parent());
    }
  });
  
  actionsDiv = mkDiv(["actions"])
  
  hr = document.createElement("hr");
  
  saveButton = document.createElement("button");
  $(saveButton).html("Save").click(function(){
    addDesker($(this).parent().parent());
  });
  
  cancelButton = document.createElement("button");
  $(cancelButton).html("Cancel").click(function(){
    $(this).parent().parent().remove();
    adjDeskerHeight();
  });
  
  $(actionsDiv).append(saveButton).append(cancelButton);
  
  br = document.createElement("br");
  $(br).addClass("clear");
  
  $(formDiv).append(deskerField).append(hr).append(actionsDiv).append(br);
  
  $("#"+dayID).children(".deskers").append(formDiv);
  adjDeskerHeight();
  $(deskerField).focus();
}

function addDesker(deskerDiv){
  deskerField = $(deskerDiv).children("input[name='desker-name']");
  if($(deskerField).val() == ""){
    $(deskerField).css("border","1px solid red").css("background","#faa");
  }else{
    deskerName = $(deskerField).val();
    
    $.getJSON("/create_desker", {name: deskerName, section: $("#section").val(), date: $(deskerDiv).parent().parent().attr("id")}, function(data){ 
      
      $(data).each(function(index){
        if(this != 'false'){
          $(deskerDiv).children().remove();

          deskerRemoveDiv = mkDiv(["actions"]);
          removeButton = mkButton([],"x");
          $(removeButton).click(function(){
            removeDesker($(this).parent().parent());
          })
          
          $(deskerRemoveDiv).append(removeButton);

          deskerText = document.createTextNode(deskerName);

          $(deskerDiv).attr("id",this.dID).append(deskerRemoveDiv).append(deskerText).append(mkBr(["clear"]));
          
          adjDeskerHeight();
        }else{
          alert("returned false");
        }
      });
    });
  }
  
  adjDeskerHeight();
}
function removeDesker(deskerDiv){
  dID = $(deskerDiv).attr("id");
  $.getJSON("/delete", {key: dID}, function(data){ 
    $(data).each(function(index){
      if(this != 'false'){
        $(deskerDiv).remove();
        adjDeskerHeight();
      }else{
        alert("returned false");
      }
    });
  });
  
  adjDeskerHeight();
}
function buildDeskers(section, start, end){
  $.getJSON("/get_weeks_deskers",{start_day: start, end_day: end, section: section}, function(data){
    $(data).each(function(index){
      deskerDiv = mkDiv(["desker"]);
      
      deskerRemoveDiv = mkDiv(["actions"]);
      removeButton = mkButton([],"x");
      $(removeButton).click(function(){
        removeDesker($(this).parent().parent());
      })
      
      $(deskerRemoveDiv).append(removeButton);

      deskerText = document.createTextNode(this.name);

      $(deskerDiv).attr("id",this.dID).append(deskerRemoveDiv).append(deskerText).append(mkBr(["clear"])).appendTo("#"+this.date+" .deskers");
      
      adjDeskerHeight();
    });
  });
}


function buildCal(section, start, end){
  $("#week").children().remove();
  now = new Date();
  
  calHeader = $("#date-header h2");
  
  startDay = new mustrunDate(start);
  endDay = new mustrunDate(end);
  
  if(startDay.Y == endDay.Y){
    calHeader.html(startDay.shortDate+" &ndash; "+endDay.longDate);
  }else{
    calHeader.html(startDay.longDate+" &ndash; "+endDay.longDate);
  }
  
  for(x = 0; x < 6; x++){
    day = new mustrunDate(start);
    //day = new mustrunDate("2010-05-02");
    tempDay = new Date(day.date)
    tempDay.setDate(day.date.getDate()+x);
    thisDay = new mustrunDate(tempDay);
    
    dayDiv = mkDiv(["span-4","dotw"]);
    $(dayDiv).attr("id",thisDay.YMD);
    if(thisDay.date.getFullYear() == now.getFullYear() && thisDay.date.getMonth() == now.getMonth() && thisDay.date.getDate() == now.getDate()){
      $(dayDiv).addClass("today");
    }
    
    dateDiv = mkDiv(["date"]);
    
    dayLabel = mkHeader(3,[],thisDay.day);
    
    dateText = document.createTextNode(thisDay.month+" "+parseInt(thisDay.D,10));
    
    if(x == 5){
        $(dayDiv).addClass("last");
        $(dayLabel).html("Friday/Saturday");
        tomorrow = new mustrunDate(new Date(thisDay.Y, parseInt(thisDay.M,10)-1, parseInt(thisDay.D,10)+1));
        if(thisDay.M != tomorrow.M){
          dateText.nodeValue = thisDay.month+" "+parseInt(thisDay.D,10)+", "+tomorrow.month+" "+parseInt(tomorrow.D,10);
        }else{
          dateText.nodeValue = thisDay.month+" "+parseInt(thisDay.D,10)+", "+parseInt(tomorrow.D,10);
        }
        
    }
    
    $(dateDiv).append(dayLabel).append(dateText);
    
    $(dayDiv).append(dateDiv);
    
    $("#week").append(dayDiv);
    
    deskersDiv = mkDiv(["deskers"]);
    deskersActionsDiv = mkDiv(["actions"]);
    addDeskerButton = mkButton([],"Add");
    $(addDeskerButton).click(function(){
      addDeskerField($(this).parent().parent().parent().parent().attr("id"));
    });
    $(deskersActionsDiv).append(addDeskerButton);
    
    deskersHeader = mkHeader(4,[],"Deskers:");
    $(deskersHeader).append(deskersActionsDiv);
    
    $(deskersDiv).append(deskersHeader).append(mkHr([]));
    
    asgnmntsDiv = mkDiv(["assignments"]);
    
    addAsgnmntDiv = mkDiv(["actions"]);
    
    addButton = document.createElement("button");
    $(addButton).html("Add Assignment").click(function(){
      addAsgnmntField($(this).parent().parent().attr("id"));
    });
    //alert(thisDay.YMD);
    
    $(addAsgnmntDiv).append(addButton);
    
    $(dayDiv).append(deskersDiv).append(addAsgnmntDiv).append(mkHr([])).append(asgnmntsDiv);
        
  }
  
  $(".assignments").sortable({
    connectWith: '.assignments',
    change: function(event, ui) {
      adjAssignHeight();
    },
    receive: function(event, ui) {
      setWeights(event.target);
      adjAssignHeight();
    },
    remove: function(event, ui) {
      setWeights(event.target);
    },
    stop: function(event, ui) {
      setWeights(event.target);
    }
  });
  
  $.getJSON("/get_weeks_deskers",{start_day: start, end_day: end, section: section}, function(data){
    $(data).each(function(index){
      deskerDiv = mkDiv(["desker"]);
      
      deskerRemoveDiv = mkDiv(["actions"]);
      removeButton = mkButton([],"x");
      $(removeButton).click(function(){
        removeDesker($(this).parent().parent());
      })
      
      $(deskerRemoveDiv).append(removeButton);

      deskerText = document.createTextNode(this.name);

      $(deskerDiv).attr("id",this.dID).append(deskerRemoveDiv).append(deskerText).append(mkBr(["clear"])).appendTo("#"+this.date+" .deskers");
      
      adjDeskerHeight();
    });
  });
  
  $.getJSON("/get_weeks_assignments", {start_day: start, end_day: end, section: section}, function(data){ 
    $(data).each(function(index){
      buildAsgnmnt(this);
    });
  });
}

function setWeights(assignmentsDiv){
  //$(assignmentsDiv).effect("highlight");
  $(assignmentsDiv).children(".assignment").each(function(index){
    $.getJSON("/cr_mod_assignment",{aID: $(this).attr("id"), dueDate: $(this).parent().parent().attr("id"), weight: index});
  })
}

function addAsgnmntField(dayID){
  dateString = dayID;
  asgnmntDiv = mkDiv(['assignment']);
  
  asgnmntTitle = document.createElement("input");
  $(asgnmntTitle).attr("type","text").attr("name","title").addClass("text").width("100%").keyup(function(event){
    if(event.keyCode == '13'){
      addAsgnmnt($(this).parent());
    }
  });
  
  hr = mkHr([]);
  
  asgnmntActionsDiv = mkDiv(["actions"]);
  
  editButton = document.createElement("button");
  $(editButton).html("Details");
  cancelButton = document.createElement("button");
  $(cancelButton).html("Cancel").click(function(){
    $(this).parent().parent().remove();
    adjAssignHeight();
  });
  saveButton = document.createElement("button");
  $(saveButton).html("Save").click(function(){
    addAsgnmnt($(this).parent().parent());
  });
  
  $(asgnmntActionsDiv).append(editButton).append(cancelButton).append(saveButton);
  
  $(asgnmntDiv).append(asgnmntTitle).append(hr).append(asgnmntActionsDiv);
  
  $("#"+dateString+" .assignments").append(asgnmntDiv);
  //alert(date);
  $(asgnmntTitle).focus();
  
  adjAssignHeight();
}

function addAsgnmnt(asgnmntDiv){
  asgnmntField = $(asgnmntDiv).children("input[name='title']");
  if($(asgnmntField).val() == ""){
    $(asgnmntField).css("border","1px solid red").css("background","#faa");
  }else{
    asgnmntTitle = $(asgnmntField).val();
    weight = $(asgnmntDiv).parent().children(".assignment").size() - 1;
    
    $.getJSON("/cr_mod_assignment", {title: asgnmntTitle, section: $("#section").val(), dueDate: $(asgnmntDiv).parent().parent().attr("id"), weight: weight}, function(data){ 
      $(data).each(function(index){
        if(this != 'false'){
          $(asgnmntDiv).remove();

          buildAsgnmnt(this);
          
          adjAssignHeight();
        }else{
          alert("returned false");
        }
      });
    });
  }
  
  adjAssignHeight();
}

function removeAsgnmnt(asgnmntDiv){
  $.getJSON("/delete",{key:$(asgnmntDiv).attr("id")}, function(data){
    $(data).each(function(index){
      if(this == false){
        alert("There was an error deleting, Please try again");
      }else{
        assignmentsDiv = $(asgnmntDiv).parent();
        $(asgnmntDiv).remove();
        setWeights(assignmentsDiv);
      }
    })
  })
}

function buildAsgnmnt(asgnmnt){
  asgnmntDiv = mkDiv(['assignment']);

  $(asgnmntDiv).attr("id",asgnmnt.aID);
  $(asgnmntDiv).html(mkHeader(6,["title"],asgnmnt.title));
  
  if(asgnmnt.status != ""){
    $(asgnmntDiv).append("<hr />");
    $(asgnmntDiv).append("Status: "+asgnmnt.status);
  }
  
  actionsDiv = mkDiv(["actions"]);
  editButton = mkButton([],"Edit");
  $(editButton).click(function(){
    editAsgnmnt(asgnmnt.aID);
  });
  deleteButton = mkButton([],"Remove");
  $(deleteButton).click(function(){
    if(confirm("Are you sure? Click OK to remove this assignment")){
      removeAsgnmnt($(this).parent().parent());
      //$(this.parent().parent()).remove();
    }else{
      //alert("doing nothing");
    }
  });
  $(actionsDiv).append(editButton).append(deleteButton);
  
  $(asgnmntDiv).append(mkHr([])).append(actionsDiv);
  
  dueDate = new mustrunDate(asgnmnt.dueDate);
  //alert(asgnmnt.title+" on "+dueDate.YMD);
  if(dueDate.day == "Saturday"){
    displayDate = new Date(dueDate.date);
    displayDate.setDate(displayDate.getDate() - 1);
    displayDate = new mustrunDate(displayDate);
    
    $("#"+displayDate.YMD+" .assignments").append(asgnmntDiv);
  }else{
    $("#"+dueDate.YMD+" .assignments").append(asgnmntDiv); 
  }
}

function addAssignee(assigneeDiv, aID, email){
  $.getJSON("/add_assignee", {aID: aID, email: email}, function(data){
    $(data).each(function(index){
      if(data != "false"){
        assignee = mkDiv(["assignee"]);
        $(assignee).attr("id",email);
        
        actionsDiv = mkDiv(["actions"]);
        removeButton = mkButton([],"Remove");
        
        $(actionsDiv).append(removeButton);
        
        $(assignee).append(actionsDiv).append(document.createTextNode(email));
        
        $(assigneeDiv).append(assignee);
        
        $(assignee).effect("highlight", {}, 3000);
      }else{
        $("#"+email).effect("highlight", {}, 3000);
      }
    })
  });
}

function saveAsgnmnt(){
  asgnmntForm = $("#asgnmnt-form");
  
  aID = $(asgnmntForm).children("input[name='aID']").val();
  
  title = $(asgnmntForm).children().find("input[name='title']").val();
  status = $(asgnmntForm).children().find("input[name='status']").val();
  desc = $(asgnmntForm).children().find("textarea[name='description']").val();
  
  if($(asgnmntForm).children().find("input[name='public']").is(":checked")){
    public = "True"
  }else{
    public = "False";
  }
  
  dueDate = $(asgnmntForm).children().find("input[name='dueDate']").val();
  
  $.getJSON("/cr_mod_assignment",{aID: aID, title: title, status: status, descript: desc, public: public, dueDate: dueDate}, function(data){
    $(data).each(function(index){
      if(data != "false"){
        buildCal($("#section").val(),$("#start_day").val(),$("#end_day").val());
        $("#overlay-container").remove();
      }else{
        alert("There was an error, please try again.");
      }
    });
  });
  //alert(aID+", "+title+", "+status+", "+desc+", "+public+", "+dueDate);
}

function editAsgnmnt(aID){
  if(aID){
    $.getJSON("/get_assignment", {aID: aID}, function(data){
      $(data).each(function(index){
        overlayContainer = mkDiv([]);
        $(overlayContainer).attr("id","overlay-container");

        overlayShadowContainer = mkDiv(["ui-overlay"]);
        overlayShadow = mkDiv(["ui-widget-shadow", "ui-corner-all", "mustrun-widget-shadow"]); //height: 252px; left: 50px; 
        $(overlayShadow).width(812);

        overlayContentContainer = mkDiv(["ui-widget", "ui-widget-content", "ui-corner-all", "container", "mustrun-widget-content"]); //height: 230px; left: 50px;
        $(overlayContentContainer).width(790);

        asgnmntForm = mkDiv([]);
        $(asgnmntForm).attr("id","asgnmnt-form");
         
        aIDField = mkInput([],"hidden","aID");
        $(aIDField).val(aID);
        $(asgnmntForm).append(aIDField);

        asgnmntHeader = mkHeader(2,[],this.title);

        actionsDiv = mkDiv(["actions"]);
        saveButton = mkButton([],"Save");
        $(saveButton).click(function(){
          saveAsgnmnt();
        });
        cancelButton = mkButton([],"Cancel");
        $(cancelButton).click(function(){
          $("#overlay-container").remove();
        });
        $(actionsDiv).append(saveButton).append(cancelButton);
        
        actionsDiv2 = mkDiv(["actions"]);
        saveButton2 = mkButton([],"Save");
        $(saveButton2).click(function(){
          saveAsgnmnt();
        });
        cancelButton2 = mkButton([],"Cancel");
        $(cancelButton2).click(function(){
          $("#overlay-container").remove();
        });
        $(actionsDiv2).append(saveButton2).append(cancelButton2);
        
        $(actionsDiv).prependTo(asgnmntHeader);

        leftDiv = mkDiv(["span-10"]);
        rightDiv = mkDiv(["span-10", "last"]);

        infoFieldset = mkFieldset([],"Information");
        optionsFieldset = mkFieldset([],"Options");

        authorsFieldset = mkFieldset([],"Author(s)");
        dueDateFieldset = mkFieldset([],"Due Date ");

        // ----- Information Fieldset ----- //
        titleLabel = mkLabel([],"Assignment Title","title");
        titleField = mkInput(["title","span-9"],"text","title");
        $(titleField).val(this.title);
        $(infoFieldset).append(titleLabel).append(titleField).append(mkBr([]));

        statusLabel = mkLabel([],"Status","status");
        statusField = mkInput(["text","span-9"],"text","status");
        if(this.status != ""){
          $(statusField).val(this.status);
        }
        $(infoFieldset).append(statusLabel).append(statusField).append(mkBr([]));

        descLabel = mkLabel([],"Description","description");
        descTextArea = document.createElement("textarea");
        $(descTextArea).addClass("span-9").attr("name","description");
        if(this.descript != ""){
          $(descTextArea).append(document.createTextNode(this.descript))
        }
        $(infoFieldset).append(descLabel).append(descTextArea).append(mkBr([]));
        // ----- End Information Fieldset ----- //

        // ----- Options Fieldset ----- //
        gDocLabel = mkLabel([],"Google Docs","gDoc");
        gDocCheckbox = mkInput([],"checkbox","gDoc");
        $(gDocCheckbox).attr("disabled","disabled");
        gDocText = document.createTextNode("Create a Google Doc for this assignment");

        derivAsgnmntLabel = mkLabel([],"Derivative Assignments","derivAsgnmnts");
        photoCheckbox = mkInput([],"checkbox","derivAsgnmnts");
        $(photoCheckbox).attr("disabled","disabled");
        photoText = document.createTextNode("Create a Photo Assignment from this assignment");
        designCheckbox = mkInput([],"checkbox","derivAsgnmnts");
        $(designCheckbox).attr("disabled","disabled");
        designText = document.createTextNode("Create a Design Assignment from this assignment");
        
        publicLabel = mkLabel([],"Public/Private","public");
        publicCheckbox = mkInput([],"checkbox","public");
        $(publicCheckbox).val("true");
        if(this.public == true){
          $(publicCheckbox).attr("checked","checked")
        }
        publicText = document.createTextNode("Make assignment public");

        $(optionsFieldset).append(gDocLabel).append(mkBr([])).append(gDocCheckbox).append(gDocText).append(mkBr([])).append(mkBr([]));
        
        $(optionsFieldset).append(derivAsgnmntLabel).append(mkBr([])).append(photoCheckbox).append(photoText).append(mkBr([]));
        $(optionsFieldset).append(designCheckbox).append(designText).append(mkBr([])).append(mkBr([]));
        
        $(optionsFieldset).append(publicLabel).append(mkBr([])).append(publicCheckbox).append(publicText).append(mkBr([]));
        // ----- End Options Fieldset ----- //

        // ----- Authors Fieldset ----- //
        authorsDiv = mkDiv(["assignees"]);
        authorsText = document.createTextNode("Enter the email address of the author to assign and then click Add.");
        authorsField = mkInput(["text"],"text","author");
        $(authorsField).keyup(function(event){
          if(event.keyCode == '13'){
            if($(this).val() == ""){
              $(this).css("border","1px solid red").css("background","#faa");
            }else{
              addAssignee(authorsDiv,aID,$(this).val());
              $(this).val();
              $(this).css("background","none").css("border","1px solid black");
            }
          }
        });
        authorsButton = mkButton(["mustrun"],"Add");
        $(authorsButton).click(function(){
          if($(authorsField).val() == ""){
            $(authorsField).css("border","1px solid red").css("background","#faa");
          }else{
            addAssignee(authorsDiv,aID,$(authorsField).val());
            $(authorsField).val();
            $(authorsField).css("background","none").css("border","1px solid black");
          }
        })

        $(authorsFieldset).append(authorsDiv).append(authorsText).append(authorsField).append(authorsButton);
        // ----- End Authors Fieldset ----- //

        // ----- Due Date Fieldset ----- //
        dueDateCalendar = document.createElement("div");
        $(dueDateCalendar).attr("id","datepicker");
        
        $(dueDateCalendar).datepicker({
          showOtherMonths: true,
          selectOtherMonths: true,
          changeMonth: true,
          changeYear: true,
          dateFormat: 'yy-mm-dd',
          altField: '[name="dueDate"]',
          defaultDate: this.dueDate,
        });
        
        $(dueDateFieldset).append(dueDateCalendar);

        dueDateLegend = $(dueDateFieldset).children("legend");
        dueDateField = mkInput([],"text","dueDate");
        $(dueDateField).val(this.dueDate).attr("id","dueDate").attr("disabled","disabled").appendTo(dueDateLegend);
        // ----- End Due Date Fieldset ----- //

        $(leftDiv).append(infoFieldset).append(optionsFieldset);
        $(rightDiv).append(authorsFieldset).append(dueDateFieldset);

        $(asgnmntForm).append(asgnmntHeader).append(mkHr([])).append(leftDiv).append(rightDiv).append(mkHr([])).append(actionsDiv2).append(mkBr(["clear"]));

        $(overlayContentContainer).append(asgnmntForm);
        $(overlayShadowContainer).append(overlayShadow);

        // Complete Build of Overlay Container and Append to <body> element
        $(overlayContainer).append(overlayShadowContainer).append(overlayContentContainer).appendTo("body");

        // ----- Adjust size and position of box ----- //
        containerWidth = $(overlayShadow).width();
        bodyWidth = $("body").width();
        formHeight = $(asgnmntForm).height();

        leftPos = (bodyWidth/2)-(containerWidth/2);
        $(overlayShadow).css("left",leftPos+"px");
        $(overlayContentContainer).css("left",leftPos+"px");

        $(overlayContentContainer).height(formHeight);
        $(overlayShadow).height(formHeight+22);
      });
    });
  }else{
    overlayContainer = mkDiv([]);
    $(overlayContainer).attr("id","overlay-container");
  
    overlayShadowContainer = mkDiv(["ui-overlay"]);
    overlayShadow = mkDiv(["ui-widget-shadow", "ui-corner-all", "mustrun-widget-shadow"]); //height: 252px; left: 50px; 
    $(overlayShadow).width(812);
  
    overlayContentContainer = mkDiv(["ui-widget", "ui-widget-content", "ui-corner-all", "container", "mustrun-widget-content"]); //height: 230px; left: 50px;
    $(overlayContentContainer).width(790);
  
    asgnmntForm = mkDiv([]);
    $(asgnmntForm).attr("id","asgnmnt-form"); 
  
    asgnmntHeader = mkHeader(2,[],"New Assignment");
  
    actionsDiv = mkDiv(["actions"]);
    saveButton = mkButton([],"Save");
    cancelButton = mkButton([],"Cancel");
    $(cancelButton).click(function(){
      $("#overlay-container").remove();
    });
    $(actionsDiv).append(saveButton).append(cancelButton);
    actionsDiv2 = $(actionsDiv).clone([true]);
    $(actionsDiv).prependTo(asgnmntHeader);
  
    leftDiv = mkDiv(["span-10"]);
    rightDiv = mkDiv(["span-10", "last"]);
  
    infoFieldset = mkFieldset([],"Information");
    optionsFieldset = mkFieldset([],"Options");
  
    authorsFieldset = mkFieldset([],"Author(s)");
    dueDateFieldset = mkFieldset([],"Due Date ");
  
    // ----- Information Fieldset ----- //
    titleLabel = mkLabel([],"Assignment Title","title");
    titleField = mkInput(["title","span-9"],"text","title");
    $(infoFieldset).append(titleLabel).append(titleField).append(mkBr([]));
  
    statusLabel = mkLabel([],"Status","status");
    statusField = mkInput(["text","span-9"],"text","status");
    $(infoFieldset).append(statusLabel).append(statusField).append(mkBr([]));
  
    descLabel = mkLabel([],"Description","description");
    descTextArea = document.createElement("textarea");
    $(descTextArea).addClass("span-9").attr("name","description");
    $(infoFieldset).append(descLabel).append(descTextArea).append(mkBr([]));
    // ----- End Information Fieldset ----- //
  
    // ----- Options Fieldset ----- //
    gDocLabel = mkLabel([],"Google Docs","gDoc");
    gDocCheckbox = mkInput([],"checkbox","gDoc");
    $(gDocCheckbox).attr("disabled","disabled");
    gDocText = document.createTextNode("Create a Google Doc for this assignment");

    derivAsgnmntLabel = mkLabel([],"Derivative Assignments","derivAsgnmnts");
    photoCheckbox = mkInput([],"checkbox","derivAsgnmnts");
    $(photoCheckbox).attr("disabled","disabled");
    photoText = document.createTextNode("Create a Photo Assignment from this assignment");
    designCheckbox = mkInput([],"checkbox","derivAsgnmnts");
    $(designCheckbox).attr("disabled","disabled");
    designText = document.createTextNode("Create a Design Assignment from this assignment");
    
    publicLabel = mkLabel([],"Public/Private","public");
    publicCheckbox = mkInput([],"checkbox","public");
    $(publicCheckbox).val("true");
    publicText = document.createTextNode("Make assignment public");

    $(optionsFieldset).append(gDocLabel).append(mkBr([])).append(gDocCheckbox).append(gDocText).append(mkBr([])).append(mkBr([]));
    
    $(optionsFieldset).append(derivAsgnmntLabel).append(mkBr([])).append(photoCheckbox).append(photoText).append(mkBr([]));
    $(optionsFieldset).append(designCheckbox).append(designText).append(mkBr([])).append(mkBr([]));
    
    $(optionsFieldset).append(publicLabel).append(mkBr([])).append(publicCheckbox).append(publicText).append(mkBr([]));
    // ----- End Options Fieldset ----- //
  
    // ----- Authors Fieldset ----- //
    authorsText = document.createTextNode("Enter the email address of the author to assign and then click Add.");
    authorsField = mkInput(["text"],"text","author");
    authorsButton = mkButton(["mustrun"],"Add");
  
    $(authorsFieldset).append(authorsText).append(authorsField).append(authorsButton);
    // ----- End Authors Fieldset ----- //
  
    // ----- Due Date Fieldset ----- //
    dueDateLegend = $(dueDateFieldset).children("legend");
    dueDateField = mkInput([],"text","dueDate");
    $(dueDateField).attr("id","dueDate").attr("disabled","disabled").appendTo(dueDateLegend);
  
    dueDateCalendar = document.createElement("div");
    $(dueDateCalendar).attr("id","datepicker");
  
    $(dueDateFieldset).append(dueDateCalendar);
  
    $(dueDateCalendar).datepicker({
      showOtherMonths: true,
      selectOtherMonths: true,
      changeMonth: true,
      changeYear: true,
      dateFormat: 'yy-mm-dd',
      altField: '[name="dueDate"]',
    });
    // ----- End Due Date Fieldset ----- //
  
  
    $(leftDiv).append(infoFieldset).append(optionsFieldset);
    $(rightDiv).append(authorsFieldset).append(dueDateFieldset);
  
    $(asgnmntForm).append(asgnmntHeader).append(mkHr([])).append(leftDiv).append(rightDiv).append(mkHr([])).append(actionsDiv2).append(mkBr(["clear"]));
  
    $(overlayContentContainer).append(asgnmntForm);
    $(overlayShadowContainer).append(overlayShadow);
  
    // Complete Build of Overlay Container and Append to <body> element
    $(overlayContainer).append(overlayShadowContainer).append(overlayContentContainer).appendTo("body");
  
    // ----- Adjust size and position of box ----- //
    containerWidth = $(overlayShadow).width();
    bodyWidth = $("body").width();
    formHeight = $(asgnmntForm).height();
  
    leftPos = (bodyWidth/2)-(containerWidth/2);
    $(overlayShadow).css("left",leftPos+"px");
    $(overlayContentContainer).css("left",leftPos+"px");
  
    $(overlayContentContainer).height(formHeight);
    $(overlayShadow).height(formHeight+22);
  
  }
}

function mkDiv(classes){
  theDiv = document.createElement("div");
  for(i = 0; i < classes.length; i++){
    $(theDiv).addClass(classes[i]);
  }
  return theDiv;
}
function mkHeader(level,classes,text){
  header = document.createElement("h"+level);
  for(j = 0; j < classes.length; j++){
    $(header).addClass(classes[j]);
  }
  text = document.createTextNode(text);
  $(header).append(text);
  return header;
}
function mkButton(classes,text){
  button = document.createElement("button");
  for(k = 0; k < classes.length; k++){
    $(button).addClass(classes[k]);
  }
  text = document.createTextNode(text);
  $(button).append(text);
  return button;
}
function mkFieldset(classes,legendText){
  fieldset = document.createElement("fieldset");
  for(l = 0; l < classes.length; l++){
    $(fieldset).addClass(classes[l]);
  }
  legend = document.createElement("legend");
  legendText = document.createTextNode(legendText);
  $(legend).append(legendText);
  $(fieldset).append(legend);
  return fieldset;
}
function mkLabel(classes, text, forField){
  label = document.createElement("label");
  for(m = 0; m < classes.length; m++){
    $(label).addClass(classes[m]);
  }
  text = document.createTextNode(text);
  $(label).append(text).attr("for",forField);
  return label;
}
function mkInput(classes, type, name){
  input = document.createElement("input");
  for(n = 0; n < classes.length; n++){
    $(input).addClass(classes[n]);
  }
  $(input).attr("type",type).attr("name",name);
  
  return input;
}
function mkHr(classes){
  hr = document.createElement("hr");
  for(y = 0; y < classes.length; y++){
    $(hr).addClass(classes[y]);
  }
  return hr;
}
function mkBr(classes){
  br = document.createElement("br");
  for(z = 0; z < classes.length; z++){
    $(br).addClass(classes[z]);
  }
  return br;
}

function mustrunDate(theDate){
  if(typeof theDate == "string"){
    temp = theDate.split("-");
    theDate = new Date(temp[0],temp[1]-1,temp[2]);
  }
  this.date = theDate;
  this.Y = this.date.getFullYear();
  this.M = ((this.date.getMonth() < 9) ? "0"+(this.date.getMonth()+1) : (this.date.getMonth()+1));
  this.D = ((this.date.getDate() < 10) ? "0"+this.date.getDate() : this.date.getDate());
  this.day = weekday[this.date.getDay()];
  this.month = month[this.date.getMonth()];
  this.YMD = this.Y+"-"+this.M+"-"+this.D;
  this.shortDate = this.month+" "+parseInt(this.D,10);
  this.longDate = this.month+" "+parseInt(this.D,10)+", "+this.Y;
}