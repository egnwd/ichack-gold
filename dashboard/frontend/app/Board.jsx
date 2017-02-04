import React from 'react';
import Stage from './Stage.jsx';
import ActionCable from 'actioncable';

export default class Board extends React.Component {

    constructor(props) {
        super(props);
        this.stages = [];
    }

    componentWillMount() {
        this.props.stages.forEach((s) => { this.stages[s] = <Stage key={s} id={s} done={false} /> });
        this.subscribe();
    }

    subscribe() {
        console.log("Subscribing");
        var el = this;
        var cable = ActionCable.createConsumer('ws://localhost:3000/cable');

        cable.subscriptions.create('StagesChannel', {
            connected: () => {
                console.log("Connected!");
            },

            received: (data) => {
                console.log(data);
                var id = parseInt(data.message);
                el.done(id);
            }
        });
    }

    done(id) {
        this.stages[id] = <Stage key={id} id={id} done={true}/>;
        this.forceUpdate();
    }

    render() {
        var stages = this.stages;
        return (
            <ul className="container">
                {stages}
            </ul>
        );
    }
}

