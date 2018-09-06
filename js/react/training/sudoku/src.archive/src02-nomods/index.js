import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import _ from 'lodash';

function Circle(props) {
  return (
    <button className="circle" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Square extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
      class: "square"
    };
  }

  render() {
    return (
      <button
        className={this.state.class +
          " left" + this.props.col +
          " top" + this.props.row}
        onClick={() => this.setState({
          value: this.state.value < 9 ? this.state.value + 1 : 1
        })}
      >
        {this.state.value}
      </button>
    );
    /* to display coordinates use these instead of {this.state.value}
        {this.props.row},{this.props.col}
    */
  }
}

class Board extends React.Component {
  renderSquare(r, c) {
    return <Square row={r} col={c} />;
  }

  render() {
    const s = 9;
    return (
      <div>
        {_.times(s, r =>
          <div className="board-row">
            {_.times(s, c =>
              this.renderSquare(r,c)
            )}
          </div>
        )}
      </div>
    );
  }
}

class Game extends React.Component {
  renderCircle(i) {
    return <Circle value={i} />;
  }

  render() {
    const s = 9;
    return (
      <div className="game">
        <div className="game-board">
          <Board />
        </div>
        <div className="game-nums">
          {_.times(s, i =>
            this.renderCircle(i+1)
          )}
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);
