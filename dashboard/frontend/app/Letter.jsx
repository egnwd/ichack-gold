import React from 'react';

class Letter extends React.Component {

    constructor() {
        super();
    }

    render() {
        var letter = this.props.letter;
        return (
            <li className={"letter"}>
                {letter}
            </li>
        );
    }
}

export default Letter;
