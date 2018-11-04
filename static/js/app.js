$(function(){
    var $sectionAuto = $("#ModeAuto");
    var $sectionManu = $("#ModeManu");
    var $SelectionMode = $('select#inputGroupSelectMode');

    $(document).ready(function() {
        DisplaySections();
    });

    $SelectionMode.on('change', function() {
        DisplaySections();
    });

    function DisplaySections() {
        var value = $SelectionMode.val();

        if (value === "auto")
        {
            $sectionManu.hide();
            $sectionAuto.show();
        }
        else {
            $sectionManu.show();
            $sectionAuto.hide();
        }
    }
});