/**
 * Created by Habibd on 28/09/2017.
 */
var nodesBySource = {
    HabibDee: ["RedCloakedGirl", "OneTife", "hameedatt_", "_odujokod", "Adebayodeji14",
    "Mokeam", "iamOpetunde", "iiv_lyn", "Max_Spane", "oshomah", "StephenAfamO", "_Lolu",
    "TonyElumeluFDN"],
    mtz5prif: ["Folabz_", "oshomah", "Max_Spane", "olusergio", "iiv_lyn", "Oluso_LA", "iamOpetunde",
    "Mokeam", "_odujokod", "_Lolu", "StephenAfamO", "Sureife", "Adebayodeji14", "TonyElumeluFDN"],
    olusergio:["Folabz_", "Oluso_LA", "iamOpetunde", "Mokeam", "_odujokod", "_Lolu", "StephenAfamO",
    "Sureife", "Adebayodeji14", "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "RedCloakedGirl", "oshomah"],
    Sureife: ["Folabz_", "Oluso_LA", "iamOpetunde", "Mokeam", "_odujokod", "_Lolu", "StephenAfamO",
"Max_Spane", "olusergio", "Adebayodeji14", "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "RedCloakedGirl",
        "oshomah", "iiv_lyn"],
    Oluso_LA:  ["Folabz_", "_Lolu", "StephenAfamO", "Max_Spane", "olusergio", "Adebayodeji14",
         "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "RedCloakedGirl",
        "oshomah", "iiv_lyn"],
    RedCloakedGirl:  ["Oluso_LA", "_Lolu", "StephenAfamO", "Max_Spane", "olusergio", "Adebayodeji14",
         "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "HabibDee",
        "oshomah", "iiv_lyn", "iamOpetunde", "Mokeam", "_odujokod", "Sureife"],
    Folabz_: ["Oluso_LA", "_Lolu", "StephenAfamO", "Max_Spane", "olusergio", "Adebayodeji14",
         "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife",
        "oshomah", "iiv_lyn", "iamOpetunde", "Mokeam", "_odujokod", "Sureife"]
}
function changecat(value){
    if (value.length == 0){
        document.getElementById("drp_ego").innerHTML = "<option></option>";
    }
    else {
            var catOptions = "";
            for ( categoryId in nodesBySource[value]) {
                catOptions += "<option>" + nodesBySource[value][categoryId] + "</option>";
            }
            document.getElementById("drp_ego").innerHTML = catOptions;
    }
//    var HabibDee = ["RedCloakedGirl", "OneTife", "hameedatt_", "_odujokod", "Adebayodeji14",
//    "Mokeam", "iamOpetunde", "iiv_lyn", "Max_Spane", "oshomah", "StephenAfamO", "_Lolu",
//    "TonyElumeluFDN"];
//    var mt = ["Folabz_", "oshomah", "Max_Spane", "olusergio", "iiv_lyn", "Oluso_LA", "iamOpetunde",
//    "Mokeam", "_odujokod", "_Lolu", "StephenAfamO", "Sureife", "Adebayodeji14", "TonyElumeluFDN"];
//    var serg = ["Folabz_", "Oluso_LA", "iamOpetunde", "Mokeam", "_odujokod", "_Lolu", "StephenAfamO",
//    "Sureife", "Adebayodeji14", "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "RedCloakedGirl", "oshomah"];
//    var sureife = ["Folabz_", "Oluso_LA", "iamOpetunde", "Mokeam", "_odujokod", "_Lolu", "StephenAfamO",
//"Max_Spane", "olusergio", "Adebayodeji14", "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "RedCloakedGirl",
//        "oshomah", "iiv_lyn"];
//     var sola = ["Folabz_", "Oluso_LA", "_Lolu", "StephenAfamO", "Max_Spane", "olusergio", "Adebayodeji14",
//         "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "RedCloakedGirl",
//        "oshomah", "iiv_lyn"];
//    var rcg = ["Oluso_LA", "_Lolu", "StephenAfamO", "Max_Spane", "olusergio", "Adebayodeji14",
//         "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife", "HabibDee",
//        "oshomah", "iiv_lyn", "iamOpetunde", "Mokeam", "_odujokod", "Sureife"];
//    var fola = ["Oluso_LA", "_Lolu", "StephenAfamO", "Max_Spane", "olusergio", "Adebayodeji14",
//         "TonyElumeluFDN", "mtz5prif", "hameedatt_", "OneTife",
//        "oshomah", "iiv_lyn", "iamOpetunde", "Mokeam", "_odujokod", "Sureife"];

//var select = document.getElementById('drpego').options.length;
//for (var i = 0; i < select; ) {
//        document.getElementById('drpego').options.remove(i);
//    }
//if (document.getElementById("drpuser").value == "HabibDee") {
//    for (var i = 0; i < HabibDee.length; i++) {
//        var newSelect = document.createElement('option');
//        selectHTML = "<option value='" + HabibDee[i] + "'>" + HabibDee[i] + "</option>";
//        newSelect.innerHTML = selectHTML;
//        document.getElementById('drpego').add(newSelect);
//    }
//}
//    else if(document.getElementById("drpuser").value == "mtz5prif"){
//        for (var i = 0; i < mt.length; i++) {
//        var newSelect = document.createElement('option');
//        selectHTML = "<option value='" + mt[i] + "'>" + mt[i] + "</option>";
//        newSelect.innerHTML = selectHTML;
//        document.getElementById('drpego').add(newSelect);
//}
//}
//    else if(document.getElementById("drpuser").value == "olusergio"){
//        for (var i = 0; i < serg.length; i++) {
//        var newSelect = document.createElement('option');
//        selectHTML = "<option value='" + serg[i] + "'>" + serg[i] + "</option>";
//        newSelect.innerHTML = selectHTML;
//        document.getElementById('drpego').add(newSelect);
//}
//}
//    else if(document.getElementById("drpuser").value == "Sureife"){
//        for (var i = 0; i < sureife.length; i++) {
//        var newSelect = document.createElement('option');
//        selectHTML = "<option value='" + sureife[i] + "'>" + sureife[i] + "</option>";
//        newSelect.innerHTML = selectHTML;
//        document.getElementById('drpego').add(newSelect);
//}
//}
//     else if(document.getElementById("drpuser").value == "Oluso_LA"){
//        for (var i = 0; i < sola.length; i++) {
//        var newSelect = document.createElement('option');
//        selectHTML = "<option value='" + sola[i] + "'>" + sola[i] + "</option>";
//        newSelect.innerHTML = selectHTML;
//        document.getElementById('drpego').add(newSelect);
//}
//}
//    else if(document.getElementById("drpuser").value == "RedCloakedGirl"){
//        for (var i = 0; i < rcg.length; i++) {
//        var newSelect = document.createElement('option');
//        selectHTML = "<option value='" + rcg[i] + "'>" + rcg[i] + "</option>";
//        newSelect.innerHTML = selectHTML;
//        document.getElementById('drpego').add(newSelect);
//}
//}
//    else if(document.getElementById("drpuser").value == "Folabz_"){
//        for (var i = 0; i < fola.length; i++) {
//        var newSelect = document.createElement('option');
//        selectHTML = "<option value='" + fola[i] + "'>" + fola[i] + "</option>";
//        newSelect.innerHTML = selectHTML;
//        document.getElementById('drpego').add(newSelect);
//}
//}

}

//$('#datatable-responsive').on('view_friends', function(ev){
//    $('#myModal').modal('show')
//})