var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

let width = canvas.width;
let height = canvas.height;
let posx = 0;
let posy = 0;
let rotation = 0;

let speed = 0;
let turn = 0;

let backgroundImage = new Image();
//backgroundImage.src = "/assets/IMG_0016.jpg";
backgroundImage.src = "/assets/tile.jpg";

socket.on('set-speed', function (data) {
	speed = data["speed"];
	turn = data["turn"];
});

function clear() {
	ctx.rect(-1, -1, width + 2, height + 2);
	ctx.fillStyle = "white";
	ctx.fill();
	// ctx.closePath();
}

function drawRover() {
	ctx.save();
	ctx.translate(width / 2, height / 2);
	ctx.rotate(rotation * Math.PI / 180);

	ctx.beginPath();
	ctx.fillStyle = "rgb(0,0,0)";
	ctx.rect(-20, -40, 40, 80);
	ctx.fill();
	ctx.stroke();

	ctx.beginPath();
	ctx.fillStyle = "rgb(100,100,255)";
	ctx.rect(10, -40, 10, 20);
	ctx.rect(-20, -40, 10, 20);
	ctx.fill();
	ctx.stroke();

	ctx.restore();
}

function drawBackground() {
	//ctx.drawImage(backgroundImage, 0, 0, width, height); // Draw image at (0,0) with canvas dimensions
	ctx.drawImage(backgroundImage, 2048 + posx, 2048 + posy, 2048, 2048, 0, 0, width, height);
}

function redraw() {
	drawBackground()
	drawRover();
}

function sanitizeCoord(coord) {
	if(coord <= -2048) {
		coord += 2048;
	} else if(coord >= 2048) {
		coord -= 2048;
	}
	
	return coord;
}

function roversim() {
	rotation += turn;
	if (rotation > 180) rotation -= 360;
	else if (rotation < -180) rotation += 360;
	posy += speed * Math.cos((Math.PI / 180) * rotation * -1);
	posy = sanitizeCoord(posy);
	posx += speed * Math.sin((Math.PI / 180) * rotation * -1);
	posx = sanitizeCoord(posx);
	redraw();
	setTimeout(roversim, 10);
}

roversim();
