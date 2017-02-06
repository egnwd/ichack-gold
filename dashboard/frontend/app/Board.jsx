import React from 'react';
import Stage from './Stage.jsx';
import Letter from './Letter.jsx';
import Tech from './Tech.jsx';
import ActionCable from 'actioncable';

export default class Board extends React.Component {

    constructor(props) {
        super(props);
        this.stages = [];
        this.letters = [];
        this.current = 0;
    }

    componentWillMount() {
        this.props.stages.forEach((s) => { this.stages[s] = <Stage key={s} id={s} done={false} /> });
        for (var i = 0; i < 6; i++) {
            this.letters[i] = <Letter letter="" key={i}/>;
        }
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
                var obj = data.message;
                var id = parseInt(obj["id"]);
                var letter = obj["letter"];
                var idx = parseInt(obj["idx"]);
                el.done(id, letter, idx);
            }
        });
    }

    done(id, letter, idx) {
        if (letter != null) {
            this.letters[idx] = <Letter letter={letter} key={idx}/>
        }
        this.stages[id] = <Stage key={id} id={id} done={true}/>;
        this.current = id;
        this.forceUpdate();
    }

    render() {
        var stages = this.stages;
        return (
            <div>
                <ul className="container">
                    {stages}
                </ul>
                <Tech idx={this.current}/>
                <div className="container">
                    <ul className="letters">
                        {this.letters}
                    </ul>
                </div>
            </div>
        );
    }
}
