$(function(){
    var $sectionAuto = $("#ModeAuto");
    var $sectionManu = $("#ModeManu");
    var $SelectionMode = $('select#ProtectionMode');
    var $OpeningTimeCorrectionSection = $('#OpeningTimeCorrectionSection')
    var $OpeningTimeSection = $('#OpeningTimeSection')
    var $OpeningMode = $('#OpeningMode')
    var $FormReset = $('#FormReset')
    var $ClosingMode = $('#ClosingMode')
    var $ClosingTimeSection = $('#ClosingTimeSection')
    var $ClosingTimeCorrectionSection = $('#ClosingTimeCorrectionSection')

    DisplaySections();
    DisplayTimeSections($OpeningMode, $OpeningTimeCorrectionSection, $OpeningTimeSection);
    DisplayTimeSections($ClosingMode, $ClosingTimeCorrectionSection, $ClosingTimeSection);

    $SelectionMode.on('change', function() {
        DisplaySections();
    });

    $OpeningMode.on('change', function() {
        DisplayTimeSections($OpeningMode, $OpeningTimeCorrectionSection, $OpeningTimeSection);
    });

    $ClosingMode.on('change', function() {
        DisplayTimeSections($ClosingMode, $ClosingTimeCorrectionSection, $ClosingTimeSection);
    });

    $FormReset.on('click', function() {
        setTimeout(DisplaySections, 1);
    });

    $('form').on('submit', function(e) {
        var $form = $(this);
        var action = $form.attr('action');

        $.ajax({
            type: "POST",
            url: action,
            data: $form.serialize(),
            success: function(data) {
                $.confirm({
                    title: 'Paramètres enregistrés',
                    content: 'Les paramètres ont bien été enregistrés !',
                    type: 'green',
                    typeAnimated: true,
                    buttons: {
                        ok: {
                            text: "Ok"
                        }
                    },
                    onAction: function() {
                        location.reload();
                    }
                });
            }
        });

        e.preventDefault();
    });

    function DisplaySections() {
        var value = $SelectionMode.val();

        if (value === "Auto") {
            $sectionManu.hide();
            $sectionAuto.show();
            DisplayTimeSections($OpeningMode, $OpeningTimeCorrectionSection, $OpeningTimeSection);
            DisplayTimeSections($ClosingMode, $ClosingTimeCorrectionSection, $ClosingTimeSection);
        } else {
            $sectionManu.show();
            $sectionAuto.hide();
        }
    }

    function DisplayTimeSections($mode, $correctionSection, $timeSection) {
        var value = $mode.val();

        if (value == 1) {
            $correctionSection.show();
            $timeSection.hide();
        } else {
            $correctionSection.hide();
            $timeSection.show();
        }
    }
});