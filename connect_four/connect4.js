//Begin By Collecting Names of Players
//Mofify Text as we go

//Draw board
tableCreate();

//Set control variable newgame to true
var newgame = true;

var player_colors = {
  '0': 'player 1',
  '1': 'player 2'
}

var currentPlayer = 0;
var board_height = 6;
var board_width = 7;
var game_history = [];


function getColor(){
  $(document).ready(function(){
    player_colors[0] = prompt("Enter Color of Player 1");
    console.log("Player 1 color: " + player_colors[0]);
    player_colors[1] = prompt("Enter Color of Player 2");
    console.log("Player 2 color: " + player_colors[1]);
  })
}

function startHeader(){
  $(document).ready(function(){
    $('#gameheading').find('h3').text('Setting Up The Game');
    $('#gameheading').find('p').text('Enter The Color Checker for Each Player');
  })
}

function tableCreate(){
  //Define Board (Table) Objects, ID, Class
  var gameBoard = document.createElement('table');
  gameBoard.setAttribute("id", "gameBoard");
  gameBoard.setAttribute("class", "table table-bordered center")
  //insert a bunch of rows, cells
  for (var i = 0; i < 6; i++) {
    var tableRow = gameBoard.insertRow();

    for (var j = 0; j < 7; j++) {
      var tableCell = tableRow.insertCell();
      //Define Checker piece object, class - preloading pieces
      var checkerPiece = document.createElement("SPAN");
      //Adding column identifier here instead of calculating it from get position
      checkerPiece.setAttribute("class", "dot");
      tableCell.appendChild(checkerPiece);
      tableCell.setAttribute('class', "column[" + j + "]");
      tableCell.addEventListener('click', function(){tableClick($(this).attr('class'))})
    }
  }
  for (var k = 0; k < 7; k++) {
    console.log($(".column[" + k + "]").attr("class"));
  }
  var gameLoc = document.getElementById("gameContainer");
  gameLoc.appendChild(gameBoard);
}

function addPiece(col){
  //Update board via click event.
  //Sum non-null column members
  var temp_sum = 0;
  for (var i = 0; i < board_height; i++) {
    if (game_history[i][col] !== null) {
      temp_sum += 1;
    }
  }
  //temp_sum is now the row to addPiece
  console.log('row: ' + (board_height - temp_sum - 1) + ' and col: ' + col);
  add_row = board_height - temp_sum - 1;
  if (add_row >= 0) {
    //Update gaem history for checkWin protocol
    game_history[add_row][col] = currentPlayer;
    drawPiece(add_row, col);
    console.log(game_history);
  }
  else {
    alert("Invalid Move")
  }
}

function drawPiece(row, col, color=player_colors[currentPlayer]){
  //Change the color of the 'added' pieces
  row = parseInt(row);
  col = parseInt(col);
  var change_loc = (7 * row) + col;
  $('td').eq(change_loc).children().css('background-color', color);
}

function parseColInfo(colinfo){
  //May change depending on class lookup procedure.
  //Returns integer number of column
  return colinfo[7];
}

function tableClick(colinfo){
//Process the table click and call addPiece->checkWin
  addPiece(parseColInfo(colinfo));
  if (checkWin()) {
      advanceTurn();
  }
  else {
    //Setting newgame to true will trip win logic in runGame
    newgame = true;
    runGame();
  }
}

function checkWin(){
  //Read board and see if someone has won
  var check_sum = 0;
  var temp_history = [];
  for (var i = 0; i < board_height; i++) {
    for (var j = 0; j < board_width; j++) {
      temp_history.push(game_history[i][j]);
    }
  }
  //Diagonal ReferenceList (assumes 6 row x 7 col table, index starts at 0)
  var diagonals = [
    [0,8,16,24,32,40],
    [7,15,23,31,39],
    [14,22,30,38],
    [1,9,17,25,33,41],
    [2,10,18,26,34],
    [3,11,19,27],
    [6,12,18,24,30,36],
    [13,19,25,31,37],
    [20,26,32,38],
    [5,11,17,23,29,35],
    [4,10,16,22,28],
    [3,9,15,21]
  ];
  //Check horizontals
  var horizontals = [0,1,2,3,4,5,6]
  for (var m = 0; m < board_height; m++) {
    check_sum = 0;
    for (var n = 0; n < horizontals.length; n++) {
      if (temp_history[7* m + horizontals[n]] == currentPlayer) {
        check_sum += 1;
      }
      else {
        check_sum = 0;
      }
      if (check_sum == 4) {
        return false;
      }
    }
  }
  //Check verticals
  var verticals = [0,7,14,21,28,35];
  for (var x = 0; x < board_width; x++) {
    for (var y = 0; y < verticals.length; y++) {
      if (temp_history[verticals[y] + x] == currentPlayer) {
        check_sum += 1;
      }
      else {
        check_sum = 0;
      }
      if (check_sum == 4) {
        return false;
      }
    }
  }
  //Check diagonals
  for (var b = 0; b < diagonals.length; b++) {
    for (var c = 0; c < diagonals[b].length; c++) {
      if (temp_history[diagonals[b][c]] == currentPlayer) {
        check_sum += 1;
        console.log("Diagonal check_sum: " + check_sum);
      }
      else {
        check_sum = 0;
      }
      if (check_sum == 4) {
        return false;
      }
    }
  }


  return true;
}

function advanceTurn(){
  currentPlayer = !currentPlayer ? 1 : 0;
  runGame();
}

function resetGame(){
  //Clear game_history
  clearHistory();
  //Re-Draw Board
  for (var i = 0; i < board_height; i++) {
    for (var j = 0; j < board_width; j++) {
      drawPiece(i,j,"grey")
    }
  }
  //Run game
  runGame();
}

function clearHistory(){
  game_history = [];
  //generate empty game_history
  var temp_element = [];
  for (var i = 0; i < board_width; i++) {
    temp_element.push(null);
  }
  for (var i = 0; i < board_height; i++) {
    game_history.push(temp_element.slice());
  }
}

function loadGame(){
  //initialize a new game
  console.log("the game state is: "+ newgame);

  if (newgame) {
    newgame = false;
    currentPlayer = 0;
    $('button').on("click", function(){
      startHeader();  setTimeout(getColor, 50); setTimeout(resetGame, 100);});
  }
}

function runGame(){
  //Draw Board and act as landing pad for worker functions
  if (!newgame) {
    console.log("The Game's Begun");
    //Notify player of turn
    $('#gameheading').find('h3').text('It is ' + player_colors[currentPlayer] + "'s turn");
    $('#gameheading').find('p').text("Click the column to drop your piece in.");
    console.log("The Current Player is: " + currentPlayer);
  }
  else {
    $('#gameheading').find('h3').text('Congratulations!! ' + player_colors[currentPlayer] + " Has Won!");
    newgame = false;
  }
}


loadGame();
