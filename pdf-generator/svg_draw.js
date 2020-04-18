let batch_size = window.location.pathname.split("batch_")[1].split(".")[0]
const XHR = new XMLHttpRequest();
XHR.open("GET", "/api/grid_data/" + batch_size);
XHR.addEventListener("load", (e) => {
    var j = JSON.parse(e.target.responseText);
    gridData = j.gridData;
    cellData = j.cellData;
    screens = gridData.map((o) => o.screenData);
    for (let i = 0; i < screens.length; i++) {
        screen_maker(batch_size, i + 1, screens[i], cellData);
    }
});
XHR.send();
function ain(y, x) {
    return String.fromCharCode(65 + y) + (x + 1)
}

function gridObj(cells, all_cells) {
    var o = {}
    for (let y = 0; y < 8; y++) {
        for (let x = 0; x < 12; x++) {
            o[ain(y, x)] = 0;
        }
    }
    all_cells.forEach(k => o[k] = 1);
    cells.forEach(k => o[k] = 2);
    return o
}

function drawGrid(cells, all_cells, screenName, comp) {
    var draw = SVG().addTo(comp).size('100%', '100%');
    var baseX = 40
    var baseY = 160;
    var dim = 60;
    var bigRect = draw.rect(720, 480).attr({ fill: '#eeeeee', x: baseX, y: baseY });
    var l = cells.length;
    var numRect = draw.rect(720, 60).attr({ x: baseX, y: 0, fill: '#ffffff' });
    //var text = draw.text("Hello").attr({x : baseX, y : 20});
    var bigFont = { family: 'Verdana', size: 40, leading: '1.5em' }
    var mediumFont = { family: 'Verdana', size: 28, leading: '1.5em' }
    var smallFont = { family: 'Verdana', size: 18, leading: '1.5em' }
    // Sample number
    draw.text(screenName).attr({ x: 6 * baseX, y: 10 }).font(mediumFont);
    // All marked cells
    draw.text(cells.join(", ")).attr({ x: 3.5 * baseX, y: 40 }).font(bigFont);
    var g = gridObj(cells, all_cells);
    // Numbering horizontally
    for (let x = 0; x < 12; x++) {
        draw.text("" + (x + 1)).attr({ x: baseX + x * dim + dim * 0.4, y: 120 }).font(smallFont);
    }
    // Numbering vertically
    for (let y = 0; y < 8; y++) {
        draw.text(String.fromCharCode(65 + y)).attr({ x: 10, y: baseY + y * dim + dim * 0.15 }).font(smallFont);
    }
    for (let y = 0; y < 8; y++) {
        for (let x = 0; x < 12; x++) {
            var a = ain(y, x)
            if (g[a] == 2) {
                draw.rect(dim * 0.7, dim * 0.7).attr({ fill: '#906', x: baseX + x * dim + dim * 0.15, y: baseY + y * dim + dim * 0.15 })
            }
            else {
                if (g[a] == 1) {
                    draw.circle(dim * 0.7, dim * 0.7).attr({ fill: '#bbbbbb', cx: baseX + x * dim + dim * 0.5, cy: baseY + y * dim + dim * 0.5 })
                } else {
                    draw.circle(dim * 0.7).attr({ fill: '#dcdcdc', cx: baseX + x * dim + dim * 0.5, cy: baseY + y * dim + dim * 0.5 })
                }
            }
        }
    }
    return draw;
}

function screen_maker(batch_size, num, cells, all_cells) {
    var g = document.createElement("div");
    var el_id = "batch_" + batch_size + num
    g.setAttribute("id", el_id);
    g.setAttribute("style", "height: 660px;")
    var body = document.getElementsByTagName("BODY")[0];
    body.appendChild(g);
    var svg1 = drawGrid(cells, all_cells, "Sample " + num, "#" + el_id).svg();
}