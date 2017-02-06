import React from 'react';
import {render} from 'react-dom';

import Board from './Board.jsx';

var N = 12;
var stages = Array.apply(null, {length: N}).map(Number.call, Number);

class App extends React.Component {
    render() {
        return <Board stages={stages}/>;
    }
}

render(<App/>, document.getElementById('app'));

