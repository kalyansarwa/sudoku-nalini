


function pencilOptions() {
    var buttons = document.getElementById('form-pencil');
    if (!buttons) { return; }
    var checks = buttons.getElementsByTagName('input');
    for (var i = 0; i < checks.length; i++) {
        if (checks[i].checked) {
            show = true;
        } else {
            show = false;
        }
    }
    var objs = document.getElementsByClassName("pencil");

    if (show == true) {
        var i;
        for (i = 0; i < objs.length; i++) {
            objs[i].style.display = "block";
        }

    } else {
        var i;
        for (i = 0; i < objs.length; i++) {
            objs[i].style.display = "none";
        }
    }
}



function hintsOptions() {
    var buttons = document.getElementById('form-hints')
    if (!buttons) { return; }
    var checks = buttons.getElementsByTagName('input');
    for (var i = 0; i < checks.length; i++) {
        if (checks[i].checked) {
            show = true;
        } else {
            show = false;
        }
    }
    var objs = document.getElementsByClassName("hints");

    if (show == true) {
        var i;
        for (i = 0; i < objs.length; i++) {
            objs[i].style.display = "block";
        }

    } else {
        var i;
        for (i = 0; i < objs.length; i++) {
            objs[i].style.display = "none";
        }
    }
}

function free() {
    //document.body.classList.remove('wait');
    document.body.style.cursor = 'auto';
}



function doHints() {
    var checks = document.getElementById('form-hints').getElementsByTagName('input');
    for (var i = 0; i < checks.length; i++) {
        checks[i].checked = true;
    }
    var objs = document.getElementsByClassName("hints");
    for (var i = 0; i < objs.length; i++) {
        objs[i].style.display = "block";
    }
}

function busy(btn) {
    //document.body.classList.add('wait');
    document.body.style.cursor = 'wait';
    btn.style.cursor = 'wait';
}



// This whole construct causes the returned solution to paint in slo mo on the screen
const timeout = ms => new Promise(resolve => setTimeout(resolve, ms));

async function paint(j_changed) {

    if (!j_changed.length) {
        return;
    }

    entry = j_changed.shift();
    if (entry.starter == 0) {
        if ( entry.color ){
            console.log('got color '+entry.color);
            var cell = document.getElementById('cell-row' + entry.row + 'col' + entry.col);
            colorCell(cell, entry.color);
        }
        var div = document.getElementById('hints-row' + entry.row + 'col' + entry.col);
        div.innerHTML = entry.possible.join('');
        var inp = document.getElementById('answer-row' + entry.row + 'col' + entry.col);
        if (entry.answer) { await timeout(100); }
        inp.value = entry.answer;
    }
    if (j_changed.length) {
        await timeout(100);
        await paint(j_changed);
    }
    return;
}


function doChanges() {

    console.log('in doChanges');

    var input = document.getElementById('changed');

    if (!input) {
        return;
    }

    var changed = input.value;

    if (changed.length) {
        var j_changed = JSON.parse(changed);

        console.log(j_changed.length);
        doHints();
        paint(j_changed);

    }
}


function printGrid() {

    console.log('in printGrid');

    var printContents = document.getElementById("theGrid").innerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;
    window.print();

    document.body.innerHTML = originalContents;
}


function colorOptions() {
    console.log('in colorOptions');
    var buttons = document.getElementById('form-color');
    if (!buttons) { return; }
    var checks = buttons.getElementsByTagName('input');
    for (var i = 0; i < checks.length; i++) {
        if (checks[i].checked) {
            show = true;
        } else {
            show = false;
        }
    }
    var obj = document.getElementById("form-colors");

    if (show == true) {
        obj.style.display = "block";
    } else {
        obj.style.display = "none";
        activeColor = null;
        var objs = document.getElementsByClassName("color-cell");
        for (var i = 0; i < objs.length; i++) {
            objs[i].style.backgroundColor = 'inherit';
        }

    }
}


function colorsOptions() {

    console.log('in colorsOptions');
    var buttons = document.getElementById('form-colors');
    if (!buttons) { return; }
    var checks = buttons.getElementsByTagName('input');
    for (var i = 0; i < checks.length; i++) {
        if (checks[i].checked) {
            activeColor = checks[i].value;
        }
    }
}


function colorMe(clicked) {

    var theColors = {
        "green": "rgb(204, 255, 204)",
        "blue": "rgb(166, 255, 243)",
        "purple": "rgb(213, 203, 255)",
        "red": "rgb(255, 194, 179)",
        "orange": "rgb(255, 205, 112)",
        "yellow": "rgb(242, 255, 134)"
        }

    var obj = document.getElementById(clicked);

    if (typeof activeColor !== 'undefined' && activeColor
            && obj.style.backgroundColor != theColors[activeColor]) {
        console.log("current color="+obj.style.backgroundColor);
        obj.style.backgroundColor = theColors[activeColor];
    } else {
        console.log("trying to uncolor")
        obj.style.backgroundColor = 'inherit';
    }
}


function colorCell(obj, color) {

    var theColors = {
        "green": "rgb(204, 255, 204)",
        "blue": "rgb(166, 255, 243)",
        "purple": "rgb(213, 203, 255)",
        "red": "rgb(255, 194, 179)",
        "orange": "rgb(255, 205, 112)",
        "yellow": "rgb(242, 255, 134)"
        }

    console.log("current color="+obj.style.backgroundColor);
    if (['green', 'blue', 'purple', 'red', 'orange', 'yellow'].includes(color)) {
        obj.style.backgroundColor = theColors[color];
    } else {
        obj.style.backgroundColor = color;
    }
}


function dontColor(clicked) {

    console.log('hit dontColor');

}


function checkFormatting(grid, cells, rows) {

    console.log('in checkFormatting cells='+cells);
    if (cells == 0) {
        grid += '<tr>';
    } else if (cells > 8) {
        grid += '</tr>'
        cells = 0;
    }
    console.log(grid)
}



function gridify() {

    var objs = document.getElementsByClassName("given");

    for (var i = 0; i < objs.length; i++) {
        var given = objs[i].innerHTML;
        var grid = '<table class="mini-grid">';
        var cells = 0;
        var rows = 0;
        var cellClass = "sudoku-odd";
        var rowClass = "sudoku-odd";

        for (var j = 0; j < given.length; j++) {
            if ('0123456789'.indexOf(given[j]) !== -1) {
                if (cells == 0) {
                    grid += '<tr class="'+rowClass+'" >';
                }
                if (given[j] == '0') {
                    grid += '<td class="'+cellClass+'" >&nbsp;</td>';
                } else {
                    grid += '<td class="'+cellClass+'" >'+given[j]+'</td>';
                }
                cells++;
                if (cells == 3) {
                    cellClass = "sudoku-even";
                } else if (cells == 6) {
                    cellClass = "sudoku-odd";
                } else if (cells > 8) {
                    grid += '</tr>'
                    cells = 0;
                    cellClass = "sudoku-odd";
                    rows += 1;
                    if (rows == 3) {
                        rowClass = "sudoku-even";
                    } else if (rows == 6) {
                         rowClass = "sudoku-odd";
                    }
                }
            }
        }
        grid += '</table>';

        objs[i].innerHTML = grid;
    }
}
