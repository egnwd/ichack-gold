import React from 'react';

class Stage extends React.Component {

    constructor() {
        super();
    }

    done() {
        this.setState({done: true});
    }

    render() {
        var id = this.props.id;
        console.log(this.props.done)
        var done = this.props.done ? " done" : "";
        return (
            <li className={"stage" + done}>
                {id+1}
            </li>
        );
    }

}

export default Stage;
