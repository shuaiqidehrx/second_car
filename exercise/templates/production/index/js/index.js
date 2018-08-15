$(function() {
	$('.right').children('li:').mouseover(function() {
		//				$(this).css('background-color','white')
		$(this).children('ul').show();
	}).mouseleave(function() {
		$(this).children('ul').hide();
	}).children('ul').children('li').mouseover(function() {
		$(this).css({
			'background-color': 'rgba(42, 44, 55)',
			'color': 'ghostwhite'
		})
	}).mouseleave(function() {
		$(this).css({
			'background-color': 'ghostwhite',
			'color': 'black'
		})
	})

	$('#main').children('button').mouseover(function() {
		$(this).css('background-color', 'rgba(0, 0, 0, 0.5)');
	}).mouseleave(function() {
		$(this).css('background-color', '');
	})
	$('#colse').click(function() {
		$(this).parent().hide();
	})
	$('#serch').focus(function(){
		$('.serch_list').show();
		$(this).css('background-color','white').parent().css('background-color','white').children('button').css('background-color','white')
	}).blur(function(){
		$('.serch_list').hide();
		$(this).css('background-color','ghostwhite').parent().css('background-color','ghostwhite').children('button').css('background-color','ghostwhite')
	})
})
window.onload = function() {
	var p0 = document.getElementById('p0');
	var p1 = document.getElementById('p1');
	var p2 = document.getElementById('p2');
	var p3 = document.getElementById('p3');
	var c0 = document.getElementById('c0');
	var c1 = document.getElementById('c1');
	var c2 = document.getElementById('c2');
	var c3 = document.getElementById('c3');
	var left_buttom = document.getElementById('but1');
	var right_buttom = document.getElementById('but2');
	var box = document.getElementById('main');
	var arr = [p0, p1, p2, p3];
	var arrc = [c0, c1, c2, c3];
	var speed = 20;
	var leftnum = 0;
	var index = 0;
	var timeM = null;

	function changeimage() {
		clearInterval(timeM)
		timeM = setInterval(function() {
			move(index)
		}, 10);
	}

	function move(i) {
		if (leftnum > 1900) {
			arrc[index].style.backgroundColor = 'white'
			index--;
			if (index == -1) {
				index = 3
			}
			arrc[index].style.backgroundColor = 'red'
			leftnum = 0
			clearInterval(timeM);
			return;
		}
		if (leftnum < -1900) {
			arrc[index].style.backgroundColor = 'white'
			index++;
			if (index == 4) {
				index = 0
			}
			arrc[index].style.backgroundColor = 'red'
			leftnum = 0
			clearInterval(timeM);
			return;
		}
		leftnum += speed;
		arr[(i != 0) ? (i - 1) : (3)].style.left = (leftnum - 1920) + 'px';
		arr[(i != 3) ? (i + 1) : (0)].style.left = (leftnum + 1920) + 'px';
		arr[i].style.left = leftnum + 'px';
	}
	var timeB = setInterval(function() {
		changeimage();
	}, 5000);
	left_buttom.onclick = function() {
		left_buttom.disabled = true;
		clearInterval(timeB)
		speed = 20;
		changeimage();
		left_buttom.disabled = false;
		timeB = setInterval(function() {
			changeimage();
		}, 5000);
	}
	right_buttom.onclick = function() {
		right_buttom.disabled = true;
		clearInterval(timeB)
		speed = -20;
		changeimage();
		right_buttom.disabled = false;
		timeB = setInterval(function() {
			changeimage();
		}, 5000);
	}
		box.onmouseover = function() {
		clearInterval(timeB)
	}
	box.onmouseleave = function() {
		timeB = setInterval(function() {
			changeimage();
		}, 5000);
	}
}