'use strict';


const EMPTY = ' ';
const DISK1 = 'BLACK';
const DISK2 = 'WHITE';

const DISPLAY = {
    'BLACK': '<i class="fas fa-circle"></i>',
    'WHITE': '<i class="far fa-circle"></i>'
};

const PREFIX = 'reversi-';

const BOARD_SIZE = {HEIGHT: 8, WIDTH: 8};

function gen_id() {
    return '_' + Math.random().toString(36).substr(2);
}

class Reversi {
    constructor(element_target) {
        // generate game id
        this.id = gen_id();

        this.element_target = element_target;

        this.init_game();

    }

    generate_elements() {
        this.element_target.className = PREFIX + 'game';
        this.element_target.id = PREFIX + 'game' + this.id;

        this.table_board = document.createElement("TABLE");
        this.table_board.className = PREFIX + 'board-table';

        this.btn_newgame = document.createElement("BUTTON");
        this.btn_newgame.innerText = 'New Game';
        this.btn_newgame.setAttribute('type', 'button');
        let init_game = this.init_game.bind(this);
        this.btn_newgame.onclick = function () {
            init_game();
        };

        this.div_log = document.createElement("DIV");
        this.div_log.className = PREFIX + 'log';

        let div_board = document.createElement("DIV");
        div_board.className = PREFIX + 'board';
        div_board.appendChild(this.table_board);

        let div_control = document.createElement("DIV");
        div_control.appendChild(this.btn_newgame);


        this.element_target.innerHTML = '';

        this.element_target.appendChild(div_board);
        this.element_target.appendChild(this.div_log);
        this.element_target.appendChild(div_control);
    }

    init_game() {
        this.data = [];
        this.hilighted = [];

        let row;
        for (row = 0; row < BOARD_SIZE.HEIGHT; row++) {
            this.data[row] = new Array(BOARD_SIZE.WIDTH).fill(EMPTY);
        }

        this.data[3][3] = DISK1;
        this.data[3][4] = DISK2;
        this.data[4][4] = DISK1;
        this.data[4][3] = DISK2;

        this.generate_elements();

        this.turn = DISK1;
        this.disk1_count = 0;
        this.disk2_count = 0;

        this.hilighted = this.find_available(this.turn);

        this.render_table();
        this.log('<strong>Game Initialized</strong>');
        this.log('Now is ' + DISPLAY[this.turn] + this.turn + "'s turn.");
    }

    place_disk(row, col) {
        console.log('Clicked at', row, col);
        if (this.data[row][col] !== EMPTY) {
            this.log('Cannot place at here: Block already occupied.');
        }
        else {
            let flipped = this.get_flipped(this.turn, row, col);
            console.log(flipped);
            if (flipped.length === 0) {
                this.log('Cannot place at here: No disk will be flipped.');
                return;
            }
            if (this.turn === DISK1) {
                this.data[row][col] = DISK1;
            }
            else {
                this.data[row][col] = DISK2;
            }
            for (let disk of flipped) {
                this.data[disk[0]][disk[1]] = this.turn;
            }
            this.count_disk();

            if (this.check_result() === EMPTY && this.disk1_count + this.disk2_count < BOARD_SIZE.HEIGHT * BOARD_SIZE.WIDTH) {
                this.switch_turn();
                let available = this.find_available(this.turn);
                if (available.length === 0) {
                    this.log('No spot available for ' + DISPLAY[this.turn] + this.turn + ' to move in this round. Skipped.');
                    this.switch_turn();
                    available = this.find_available(this.turn);
                }
                this.hilighted = available;
            }
            this.render_table();
        }
    }

    switch_turn() {
        if (this.turn === DISK1) {
            this.turn = DISK2;
        }
        else {
            this.turn = DISK1;
        }


        // Display Message
        this.log('Now is ' + DISPLAY[this.turn] + this.turn + "'s turn.");
    }

    get_flipped(turn, row, col) {
        let flipped = [];
        for (let drow of [-1, 0, 1]) {
            for (let dcol of [-1, 0, 1]) {
                if (!(drow === 0 && dcol === 0)) {
                    flipped = flipped.concat(this.get_line(turn, row, col, drow, dcol))
                }
            }
        }
        return flipped;
    }

    get_line(terminal_disk_type, row, col, drow, dcol) {
        let blocks = [];
        let flipped = [];
        while ((row + drow >= 0 && row + drow < BOARD_SIZE.HEIGHT) && (col + dcol >= 0 && col + dcol < BOARD_SIZE.WIDTH)) {
            row += drow;
            col += dcol;
            if (this.data[row][col] === EMPTY) {
                break;
            }
            else if (this.data[row][col] === terminal_disk_type) {
                flipped = blocks;
                break;
            }
            else {
                blocks.push([row, col]);
            }
        }
        return flipped;
    }

    count_disk() {
        let disk1_count = 0;
        let disk2_count = 0;
        for (let row of this.data) {
            for (let val of row) {
                if (val === DISK1) {
                    disk1_count++;
                }
                else if (val === DISK2) {
                    disk2_count++;
                }
            }
        }
        this.disk1_count = disk1_count;
        this.disk2_count = disk2_count;

        // Display Message
        this.log('Now there are ' + DISPLAY[DISK1] + DISK1 + 'x' + disk1_count.toString() + ', ' + DISPLAY[DISK2] + DISK2 + 'x' + disk2_count.toString());
    }

    check_result() {
        let winner = EMPTY;
        if (this.disk1_count === 0) {
            winner = DISK2;
        }
        else if (this.disk2_count === 0) {
            winner = DISK1;
        }
        else if (this.disk1_count + this.disk2_count === BOARD_SIZE.HEIGHT * BOARD_SIZE.WIDTH) {
            if (this.disk1_count > this.disk2_count) {
                winner = DISK1;
            }
            else if (this.disk1_count < this.disk2_count) {
                winner = DISK2;
            }

            // Display winner message
            if (winner === EMPTY) {
                this.log('<b>IT IS A TIE!</b>');
            }
            else {
                this.log('<b>' + DISPLAY[winner] + winner + ' WIN THE GAME!' + '</b>');
            }
        }
        return winner;
    }

    find_available(turn) {
        let available = [];
        let row;
        for (row = 0; row < BOARD_SIZE.HEIGHT; row++) {
            let col;
            for (col = 0; col < BOARD_SIZE.WIDTH; col++) {
                if (this.data[row][col] === EMPTY) {
                    if (this.get_flipped(turn, row, col).length > 0) {
                        available.push([row, col]);
                    }
                }
            }
        }
        return available;
    }

    render_table() {
        this.table_board.innerHTML = '';

        let row;
        let place_disk = this.place_disk.bind(this);
        for (row = 0; row < BOARD_SIZE.HEIGHT; row++) {
            let tr = this.table_board.insertRow();
            let col;
            for (col = 0; col < BOARD_SIZE.WIDTH; col++) {
                let td = tr.insertCell();

                if (this.data[row][col] === DISK1) {
                    td.innerHTML = DISPLAY[DISK1];
                }
                else if (this.data[row][col] === DISK2) {
                    td.innerHTML = DISPLAY[DISK2];
                }
                else {
                    td.innerHTML = '<i></i>';
                }

                td.setAttribute('row', row.toString());
                td.setAttribute('col', col.toString());
                td.id = PREFIX + 'board-block' + '-' + row.toString() + '-' + col.toString() + this.id;
                td.className = PREFIX + 'board-block';

                let block;
                for (block of this.hilighted) {
                    if (block[0] === row && block[1] === col) {
                        td.classList.add('hilighted-block');
                    }
                }

                td.onclick = function (event) {
                    console.log('Click event from', event.target);
                    let block = event.target;
                    if (block.tagName === 'I') {
                        block = block.parentNode;
                    }
                    place_disk(parseInt(block.getAttribute('row')), parseInt(block.getAttribute('col')));
                }
            }
        }
    }

    log(text) {
        this.div_log.innerHTML = this.div_log.innerHTML + text + '<br>';
        this.div_log.scrollTop = this.div_log.scrollHeight;
    }
}


for (let element of document.getElementsByClassName('reversi-game')) {
    let reversi = new Reversi(element);
    window['Reversi' + reversi.id] = reversi;
}


