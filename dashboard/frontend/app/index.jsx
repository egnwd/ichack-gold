import React from 'react';
import {render} from 'react-dom';

import Board from './Board.jsx';

var N = 10;
var stages = Array.apply(null, {length: N}).map(Number.call, Number);

class App extends React.Component {
    render() {
        var board = <Board stages={stages}/>;
        console.log(board);
        return board;
  }
}

render(<App/>, document.getElementById('app'));

