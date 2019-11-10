currentPage=0;


const url = "http://shubham-zvbj.localhost.run/";

// Unit101
$(document).ready(function() {
  
  if (new URL(window.location.href).searchParams.get("id") !== null) {
    console.log("sa");
    $("#search-component").val(
      new URL(window.location.href).searchParams.get("id")
    );

    setTimeout(function() {
      getJSON();
    }, 300);
  }

});

function getJSON() {
  $.get(url + "getUnitData?unitid=" + $("#search-component").val(), function(
    data
  ) {
    if (data.message == "ok") {
      $("#lifecyle-blocks").html("");
      console.log(data);
      animateSTART(0, data.result);
    } else {
      alert("Invalid Component Number");
    }
  });
}

function animateSTART(i, data) {
  if (i == 8) return;
  q = data.defective == true ? "Bad" : "Good";
  var d = new Date(data.stages[i].timestamp * 1000);

  $("#part-info").html(
    '<div class="col-md-6 grid-margin stretch-card"><div class="card"><div class=" card-body pb-0"><h2 class="card-title "><b>Processed Date: ' +
      addZ(d.getMonth() + 1) +
      "/" +
      addZ(d.getDate()) +
      "/" +
      addZ(d.getFullYear()) +
      "</b></br></br><b>Part Type:</b> " +
      data.partType.toUpperCase() +
      "</br></br><b>Quality Check:</b> " +
      q +
      "</h2></div></div></div></div>"
  );

  $("#lifecyle-blocks").append(
    '<div class="col-md-3 grid-margin stretch-card"><div class="card"><div class="card-body"><p id="timestamp' +
      i +
      '"' +
      'class="card-title text-md-center text-xl-left"></p><div class="d-flex flex-wrap justify-content-between justify-content-md-center justify-content-xl-between align-items-center"><h3 style="font-size: 1.4rem"class="mb-0 mb-md-2 mb-xl-0 order-md-1 order-xl-0" id="process' +
      i +
      '"' +
      '></h3><i class=" icon-md text-muted mb-0 mb-md-3 mb-xl-0"></i></div><p class="mb-0 mt-2 text-success" id="position' +
      i +
      '"' +
      "></p></div></div></div>"
  );

  $("#timestamp" + i).html(
    "Time: " +
      addZ(d.getHours()) +
      ":" +
      addZ(d.getMinutes()) +
      ":" +
      addZ(d.getSeconds())
  );
  $("#process" + i).html(data.stages[i].stageName.toUpperCase());
  $("#position" + i).html(
    !(typeof data.stages[i].index == "number")
      ? "<b>Position: </b>" +
          data.stages[i].index.toUpperCase() +
          "</br> <b> Level: </b>" +
          data.stages[i].position.toUpperCase()
      : "Position: N/A </br> Level: N/A"
  );
  animateSTART(++i, data);
}

function addZ(n) {
  return n < 10 ? "0" + n : "" + n;
}

function getTableData(index) {

  $.get(url + "getBulkData?bulkid=" + index, function(data) {
    if (data.message == "ok") {
      console.log(data);
      setTableData(data);
    } else {
      alert("Invalid Index");
    }
  });
}

function setTableData(data) {
  $('#table-body').html("");
  console.log(data.result[0].full_index.split("__")[1]);
  console.log(data.result[0].full_index.split("__")[0]);

  for (let i = 0; i < data.result.length; i++) {

    let cleaningColumns = data.result[i].full_index.split("__")[0].split(",");
    let coatingColumns = data.result[i].full_index.split("__")[1].split(",");
    let quality = data.result[i].defective == false ? "Good" : "Bad";
    let label= quality=="Good"? "success" : "danger";

    let block =
      "<tr><td>" +
      data.result[i].unitid +
      "</td><td>" +
      data.result[i].batch_num +
      "</td><td>" +
      data.result[i].timestamp +
      '</td><td><label class="badge badge-'+label+'">' +
      quality +
      "</label></td>" +
      "<td>" +
      cleaningColumns[0].replace("Batch ", "") +
      "</td>" +
      "<td>" +
      cleaningColumns[1].replace("Stack ", "") +
      "</td>" +
      "<td>" +
      cleaningColumns[2].replace("Bucket ", "") +
      "</td>" +
      "<td>" +
      cleaningColumns[3].replace("Row ", "") +
      "</td>" +
      "<td>" +
      cleaningColumns[4].replace("Column ", "") +
      "</td>" +
      "<td>" +
      coatingColumns[0].replace("Batch ", "") +
      "</td>" +
      "<td>" +
      coatingColumns[1].replace("Rotator ", "") +
      "</td>" +
      "<td>" +
      coatingColumns[2].replace("Cylinder ", "") +
      "</td>" +
      "<td>" +
      coatingColumns[3].replace("Pipe ", "") +
      "</td>" +
      "<td>" +
      coatingColumns[4].replace("Height ", "") +
      "</td>" +
      "<td><button id='"+ data.result[i].unitid +"'class='btn btn-link' onclick='fullAnalysis(this)'>Link</button></td>" +
      "</tr>";

    $("#table-body").append(block);
  }
}

function fullAnalysis(id) {

  window.location.href="../../index.html?id="+id.id
 
}

function nextPageTable()
{
  if(currentPage==199) return;
  else
  getTableData(++currentPage);
}

function previousPageTable()
{
  if(currentPage==0) return;
  else
  getTableData(--currentPage);

}
