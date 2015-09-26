var pecPinAlert='دارنده كارت تجارت الكترونيك پارسيان در  صورتي كه رمز شما چهار رقمي مي باشد 00 به انتهاي آن اضافه نماييد. اين امر به جهت افزايش امنيت انجام شده است.'
function OnPaymentClick()
{
	document.getElementById('btnCancel').disabled=true; 
	document.getElementById('btnPayment').disabled=true; 
	cellError.innerText = 'سيستم در حال پردازش درخواست شما ميباشد ، لطفا كمي صبر كنيد...';
}
function OnMaxLengthJump(source, target)
{
	if (source.value.length == source.maxLength)
		target.focus();
}
function AddOpt(ownr, val, txt)
{
	var o = new Option(txt, val);   
	var s = document.getElementById(ownr);   
	s.options[s.options.length] = o;
}/*keypad fa-ir*/
(function($) { 

$.keypad.qwertzAlphabetic = ['ضصثقفغغعهخحجچ', 'شسيبلاتنمكگ', 'ظطزرذدئوژپ'];
	$.keypad.qwertzLayout = 
		['!"§$%&/()=?`' + $.keypad.BACK + $.keypad.HALF_SPACE + '$£€/',
		'<>°^@{[]}\\~´;:' + $.keypad.HALF_SPACE + '789*',
		$.keypad.qwertzAlphabetic[0] + '+*' +
		$.keypad.HALF_SPACE + '456-',
		$.keypad.HALF_SPACE + $.keypad.qwertzAlphabetic[1] +
		'#\'' + $.keypad.SPACE + '123+',
		'|' + $.keypad.qwertzAlphabetic[2] + 'µ,.-_' +
		$.keypad.SPACE + $.keypad.HALF_SPACE +'.0,=', 
		$.keypad.SHIFT + $.keypad.SPACE + $.keypad.SPACE_BAR +
		$.keypad.SPACE + $.keypad.SPACE + $.keypad.SPACE + $.keypad.CLEAR +
		$.keypad.SPACE + $.keypad.SPACE + $.keypad.HALF_SPACE + $.keypad.CLOSE];
	$.keypad.regionalOptions['fa-IR'] = {
		buttonText: '...', buttonStatus: 'نمايش كيبرد',
		closeText: 'بستن', closeStatus: 'بستن كيبرد',
		clearText: 'پاك كردن', clearStatus: 'پاك كردن تمامي متن',
		backText: 'تصحيح', backStatus: 'تصحيح كلمه قبل',
		shiftText: 'Shift', shiftStatus: 'جهت حروف بزرگ و كوچك',
		spacebarText: '&nbsp;', spacebarStatus: '',
		enterText: 'ورود', enterStatus: '',
		tabText: '?', tabStatus: '',
		alphabeticLayout: $.keypad.qwertzAlphabetic,
		fullLayout: $.keypad.qwertzLayout,
		isAlphabetic: $.keypad.isAlphabetic,
		isNumeric: $.keypad.isNumeric,
		toUpper: $.keypad.toUpper,
		isRTL: false};
	$.keypad.setDefaults($.keypad.regionalOptions['fa-IR']);

})(jQuery);
/*Page Script*/
if (top.frames.length != 0) 
{
	top.location = window.location;
};
function valid(ctrl) {
    !/^[0-9]*$/.test(ctrl.value) ? ctrl.value = ctrl.value.replace(/[^0-9]/g, '') : null;
}

function SetAlert(text)
{
        $("#cellAlert").text(text).effect("pulsate", { times:3 }, 400);
}

function ClearAlert()
{
    $( "#cellAlert:visible" ).text('').removeAttr( "style" ).fadeOut();
}
    $(document).ready(function() { 
    $("#cellAlert").hide();
   
    document.getElementById('txtPin').title =			"<div class='titleStyle'>جهت افزايش امنيت از كيبورد مجازي استفاده نماييد.</div>";
    document.getElementById('txtCvv2').title = 		"<div class='titleStyle'>جهت افزايش امنيت از كيبورد مجازي استفاده نماييد.</div>";
    document.getElementById('ImageStringTextBox').title=	"<div class='titleStyle'>بزرگ يا كوچك بودن حروف انگليسي اهميت ندارد.</div>";
    document.getElementById('imgCaptcha').title=	"<div class='titleStyle'>در صورت خوانا نبودن متن تصوير بر روي تصوير جديد كليك نماييد. براي راحتي شما، در حروف تصوير حرف لاتين O وجود ندارد.</div>";
    document.getElementById('imgbtnRefreshCaptcha').title= 	"<div class='titleStyle'>جهت تغيير تصوير كليك نماييد.</div>";
    /*
    $("#ImageStringTextBox").tooltip({ 
        tip: '#ImageStringTextBoxToolTip',  
        offset: [10, 2], 
        position: "center right",
        effect: 'slide' ,
        delay: 1000,
        predelay : 2000
    }).dynamic( { 
        bottom: { 
            direction: 'down', 
            bounce: true 
        } 
    }); 
    $("#imgCaptcha").tooltip({ 
        tip: '#imgCaptchaToolTip',  
        offset: [10, 2], 
        position: "center right",
        effect: 'slide'  ,
        delay: 1000,
        predelay : 2000
    }).dynamic( { 
        bottom: { 
            direction: 'down', 
            bounce: true 
        } 
    }); 
    $("#imgbtnRefreshCaptcha").tooltip({ 
        tip: '#imgbtnRefreshCaptchaToolTip',  
        offset: [10, 2], 
        position: "center left",
        effect: 'slide'  ,
        delay: 1000,
        predelay : 2000
    }).dynamic( { 
        bottom: { 
            direction: 'down', 
            bounce: true 
        } 
    });  
     */
});
$(function () {
    KeyPadInit($('#txtPin'));
    KeyPadInit($('#txtCvv2'));
    $('#txtCard1').focus();
$('#imgbtnRefreshCaptcha').click(function(){var dt = new Date();
    $('#imgCaptcha')[0].src='JpegImage.aspx?GenerateNew=True&amp;'+'dt=' + dt.getMilliseconds();});
});
function KeyPadInit(txt)
{
    var x = txt.keypad({keypadOnly: false, showAnim:"fadeIn", duration: "fast", randomiseNumeric: true, showOn: 'button', buttonImageOnly: true,buttonImage: 'resource/keypad.png'});
    /*
$(x).tooltip({ 
    tip: '#KeyPadToolTip',  
    offset: [10, 2], 
    position: "bottom left",
    effect: 'slide'  ,
    delay: 1000,
    predelay : 1000
}).dynamic( { 
    bottom: { 
        direction: 'down', 
        bounce: true 
    } 
}); */
}
function PecCardValidation(source, arguments)
   {
    var cardPart1 = $("#txtCard1").val();
    var cardPart2 = $("#txtCard2").val();
    var cardPart3 = $("#txtCard3").val();
    var cardPart4 = $("#txtCard4").val();
    var pin = $("#txtPin").val();
    var Cvv2 = $("#txtCvv2").val();
    var Month = $("#txtMonth").val();
    var Year = $("#txtYear").val();
    var ImageString = $("#ImageStringTextBox").val();
    ClearAlert();
    if(cardPart1.length != 4 || cardPart2.length != 4 || cardPart3.length != 4 || cardPart4.length != 4 ||
        pin.length == 0 || Cvv2.length == 0 || Month.length == 0 || Year.length == 0 || ImageString.length == 0)
    {
            SetAlert('تمامي اطلاعات اجباري مي باشد.');
            arguments.IsValid = false;
    }
    else if(!/^[0-9]*$/.test(cardPart1) ||
            !/^[0-9]*$/.test(cardPart2) ||
            !/^[0-9]*$/.test(cardPart3) ||
            !/^[0-9]*$/.test(cardPart4))
    {
            SetAlert('فرمت كارت صحيح نمي  باشد');
            arguments.IsValid = false;
    }
    else if(!/^0[1-9]|1[0-2]$/.test(Month))
    {
            SetAlert('ماه را صحيح وارد نماييد.');
            arguments.IsValid = false;
    }
    else if(!/^[0-9][0-9]$/.test(Year))
    {
            SetAlert('سال را صحيح وارد نماييد.');
            arguments.IsValid = false;
    }
    else if(!/^[0-9]*$/.test(pin))
    {
            SetAlert('رمز اينترنتي عددي مي باشد');
            arguments.IsValid = false;
    } 
    else if(cardPart1 == '6221' && cardPart2 != '0610' && /^06/.test(cardPart2) && pin.length < 6)
    {
            SetAlert(pecPinAlert);
            arguments.IsValid = false;
        } 
        else if(pin.length < 5){
            SetAlert('رمز اينترنتي بايد حداقل 5 رقم باشد.');
            arguments.IsValid = false;
        }
        else
        {
            arguments.IsValid = true;
        }
   }
function AlertPecPin()
{
    var cardPart1 = $("#txtCard1").val();
    var cardPart2 = $("#txtCard2").val();
    var pin = $("#txtPin").val();
    ClearAlert();
    if(cardPart1 == '6221' && cardPart2 != '0610' && cardPart2.length == 4 && /^06/.test(cardPart2) && pin.length < 6)
    {
        SetAlert(pecPinAlert);
    }
}
