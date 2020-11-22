

/*변수 선언*/

var pw1 = document.querySelector('#password');
var userName = document.querySelector('#username');

/*이벤트 핸들러 연결*/

pw1.addEventListener("focusout", checkPw);
userName.addEventListener("focusout", checkName);

/*콜백 함수*/

/* ID */
function checkName() {
    if (userName.value === "") {
        error[0].innerHTML = "아이디를 입력하세요!";
        error[0].style.display = "block";
    }
}

/* 비밀번호 */
function checkPw() {
    if(pw1.value === "") {
        error[1].innerHTML = "필수 정보입니다.";
        error[1].style.display = "block";
    }
}

/*
2월 : 윤년에는 29일까지, 평년에는 28일까지.
1,3,5,7, 8,10,12 -> 31일
2,4,6, 9,11 -> 30일

    var days31 = [1, 3, 5, 7, 8, 10, 12];
    var days30 = [4, 6, 9, 11];

    if(mm.value )

var sel = document.getElementById("sel");
var val = sel.options[sel.selectedIndex].value;

var id = document.querySelector('#id');
var pw1 = document.querySelector('#pswd1');
var pw2 = document.querySelector('#pswd2');
var yourName = document.querySelector('#name');
var yy = document.querySelector('#yy');
var mm = document.querySelector('#mm');
var dd = document.querySelector('#dd');
var email = document.querySelector('#email');
var mobile = document.querySelector('#mobile');
var error = document.querySelectorAll('.error_next_box');

var pattern_num = /[0-9]/;
var pattern_spc = /[~!@#$%^&*()_+|<>?:{}]/;


id.onchange = checkId;
pw1.onchange = checkPw;
pw2.onchange = comparePw;
yourName.onchange = checkName;
yy.onchange = checkYear;


function checkId() {
    if(id.value === "") {
        error[0].style.display = "block";
    } else if(id.value.length < 5 || id.value.length > 20){
        error[0].innerHTML = "5~20자의 영문 소문자, 숫자와 특수기호(_),(-)만 사용 가능합니다.";
        error[0].style.display = "block";
    }
}

function checkPw() {
    if(pw1.value === "") {
        error[1].style.display = "block";
    } else if (pw1.value.length < 8 || pw1.value.length > 16) {
        error[1].innerHTML = "8~16자 영문 대 소문자, 숫자, 특수문자를 사용하세요.";
        error[1].style.display = "block";
    }
}

function comparePw() {
    if(pw2.value === "") {
        error[2].style.display = "block";
    } else if (pw2.value !== pw1.value) {
        error[2].innerHTML = "비밀번호가 일치하지 않습니다.";
        error[2].style.display = "block";
    }
}

function checkName() {
    if( yourName.value.indexOf(" ") >= 0 || pattern_spc.test(yourName.value) || pattern_num.test(yourName.value) ) {
        error[3].innerHTML = "한글과 영문 대 소문자를 사용하세요. (특수기호, 공백 사용 불가)";
        error[3].style.display = "block";
    } else if(yourName.value.length === 0) {
        error[3].style.display = "block";
    } else {
        error[3].style.display = "none";
    }
}

function checkYear() {
    isBirthEntered();
    if(yy.value.length !== 4 || !pattern_num.test(yy.value)) {
        error[4].innerHTML = "태어난 년도 4자리를 정확하게 입력하세요.";
    } else if (parseInt(yy.value) < 1920) {
        error[4].innerHTML = "정말이세요?";
        error[4].style.display = "block";
    }

}

function isBirthEntered() {

}

function checkEmail() {

}

function checkNumber() {

}
*/